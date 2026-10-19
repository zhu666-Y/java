# -*- coding: utf-8 -*-
r"""
gen_scripts.py — 海绵宝宝登录项目「启动/停止脚本」生成器（GBK 版）

为什么需要它：
  本机每次重置后 node_modules/ 和 target/ 会被清空，但 .bat / .py 这种普通文件会保留。
  可是 .bat 里只要有中文，就必须用 GBK(ANSI-936) 编码保存，否则在 cmd 里会乱码、
  甚至首行的 BOM 字节会让整条命令报错。普通编辑器很容易手滑存成 UTF-8。
  所以：本文件是「唯一正确来源」，所有 .bat 的中文内容都写在这里（UTF-8 的 .py），
  运行本脚本时用 encoding='gbk' 重新写出，保证产出的 .bat 一定是 GBK、无 BOM。

用法（在项目根目录执行）：
  python gen_scripts.py
  或（用 WorkBuddy 托管的 python）：
  C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe gen_scripts.py

约定：
  - 路径一律用 %~dp0 取脚本自身目录，再 .. 向上，整文件夹搬到哪里都能跑（相对路径）。
  - 不依赖 node_modules / target：脚本运行时会自己 npm install / mvnw package。
  - 改任何路径、端口、数据库账号，只改 env.bat 这一段即可。
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "scripts")
os.makedirs(OUT_DIR, exist_ok=True)


def write_bat(name, content):
    """把内容以 GBK（无 BOM）写出，统一用 CRLF 换行。"""
    path = os.path.join(OUT_DIR, name)
    # strip 掉首尾多余空行，再补一个换行
    text = content.strip("\n") + "\n"
    with open(path, "w", encoding="gbk", newline="\r\n") as f:
        f.write(text)
    # 校验：能按 gbk 读回来才算数
    with open(path, "r", encoding="gbk") as f:
        f.read()
    print("  -> 已生成(GBK):", name)


# =====================================================================
# env.bat —— 所有配置的唯一入口（其它脚本都 call 它）
# =====================================================================
ENV_BAT = r"""@echo off
rem ============================================================
rem  环境配置：本机路径只在这里改，其它脚本都引用这里
rem  编码 GBK / ANSI-936：用记事本另存时请选 ANSI，选 UTF-8 会乱码
rem  本文件只定义变量，不做操作，由其它脚本 call
rem ============================================================
chcp 936 >nul

rem ---- 项目目录：全部相对路径，整个文件夹搬到哪都能用 ----
set "SCRIPTS_DIR=%~dp0"
set "FRONTEND_DIR=%~dp0.."
set "BACKEND_DIR=%~dp0..\springBootTest"

rem ---- 外部工具安装位置（换机器只改这三行）----
set "MYSQL_EXE=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
set "JAVA17_HOME=C:\Program Files\Java\jdk-17"
set "NODE_DIR=D:\Program Files\nodejs"

rem ---- 重置安全备份：发布 jar 除项目根目录外，额外存一份到这里 ----
rem      项目文件夹被清空时，靠这份备份也能直接 java -jar 起服务
set "BACKUP_JAR=D:\spongebob-login.jar"

rem ---- 数据库连接 ----
set "DB_USER=root"
set "DB_PASS=123456"
set "DB_NAME=spongebob"

rem ---- 服务端口（改了这里，前端代理也要同步改 vite.config.js）----
set "BACKEND_PORT=8081"
set "FRONTEND_PORT=5173"

rem ---- PATH 里没有 node/npm 时补上 ----
where npm >nul 2>nul
if errorlevel 1 set "PATH=%NODE_DIR%;%PATH%"

rem ---- 优先用 JDK 17 编译运行，没有就退回 PATH 里的 java ----
set "JAVA_EXE=java"
if exist "%JAVA17_HOME%\bin\java.exe" (
    set "JAVA_HOME=%JAVA17_HOME%"
    set "JAVA_EXE=%JAVA17_HOME%\bin\java.exe"
)
exit /b 0
"""

# =====================================================================
# helpers.bat —— 公共小工具（killport / apiup / waitapi）
# =====================================================================
HELPERS_BAT = r"""@echo off
rem ============================================================
rem  公共小工具（由其它脚本 call，不要直接双击）
rem    call helpers.bat killport 8081       结束占用端口的进程
rem    call helpers.bat apiup 8081          服务有响应返回 0，否则返回 1
rem    call helpers.bat waitapi 8081 60     最多等 60 秒，成功返回 0
rem ============================================================
if "%~1"=="" exit /b 1
if /i "%~1"=="killport" goto KILLPORT
if /i "%~1"=="apiup"    goto APIUP
if /i "%~1"=="waitapi"  goto WAITAPI
echo [工具] 未知命令：%~1
exit /b 1

:KILLPORT
rem 同一端口 IPv4/IPv6 会各有一行、PID 相同，用空格分隔的已杀列表去重
setlocal enabledelayedexpansion
set "PORT=%~2"
set "DONE= "
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT% " ^| findstr "LISTENING"') do (
    echo !DONE! | findstr /c:" %%p " >nul
    if errorlevel 1 (
        set "DONE=!DONE!%%p "
        echo [工具] 端口 %PORT% 被进程 %%p 占用，正在结束它 ...
        taskkill /f /pid %%p >nul 2>nul
    )
)
endlocal
exit /b 0

:APIUP
setlocal
set "PORT=%~2"
where curl >nul 2>nul
if errorlevel 1 (
    rem 没有 curl 就退化成"端口是否在监听"
    netstat -ano | findstr ":%PORT% " | findstr "LISTENING" >nul 2>nul
    if errorlevel 1 ( endlocal & exit /b 1 )
    endlocal & exit /b 0
)
for /f %%c in ('curl -s -o nul -w "%%{http_code}" http://127.0.0.1:%PORT%/ 2^>nul') do (
    if not "%%c"=="000" ( endlocal & exit /b 0 )
)
endlocal
exit /b 1

:WAITAPI
setlocal
set "PORT=%~2"
set "TIMES=%~3"
for /l %%i in (1,1,%TIMES%) do (
    call "%~dp0helpers.bat" apiup %PORT%
    if not errorlevel 1 ( endlocal & exit /b 0 )
    ping -n 2 127.0.0.1 >nul
)
endlocal
exit /b 1
"""

# =====================================================================
# init-db.bat —— 幂等数据库初始化（不删数据）
# =====================================================================
INIT_DB_BAT = r"""@echo off
setlocal
call "%~dp0env.bat"

echo.
echo ===== 初始化数据库（MySQL %DB_NAME%）=====

"%MYSQL_EXE%" -u%DB_USER% -p%DB_PASS% -e "SELECT 1;" >nul 2>nul
if errorlevel 1 (
    echo [数据库] 连不上 MySQL，尝试启动 MySQL80 服务 ...
    net start MySQL80 >nul 2>nul
    ping -n 3 127.0.0.1 >nul
    "%MYSQL_EXE%" -u%DB_USER% -p%DB_PASS% -e "SELECT 1;" >nul 2>nul
    if errorlevel 1 (
        echo [数据库] 还是连不上。请手动启动：Win+R 输入 services.msc
        echo          找到 MySQL80 右键启动；或检查 env.bat 里的账号密码。
        exit /b 1
    )
)

echo [数据库] 执行幂等初始化（已有库表和数据不会被覆盖）...
"%MYSQL_EXE%" -u%DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 < "%BACKEND_DIR%\sql\init-db.sql" 2>nul
if errorlevel 1 (
    echo [数据库] 初始化失败，请检查上面的报错信息。
    exit /b 1
)
echo [数据库] 就绪。
exit /b 0
"""

# =====================================================================
# start-backend.bat —— 编译(若缺 jar) + 起后端(8081)
# =====================================================================
START_BACKEND_BAT = r"""@echo off
setlocal
call "%~dp0env.bat"

echo.
echo ===== 启动后端 Spring Boot（端口 %BACKEND_PORT%）=====
cd /d "%BACKEND_DIR%"
if errorlevel 1 (
    echo [后端] 找不到后端目录：%BACKEND_DIR%
    exit /b 1
)

rem target 每次重置都会被清空，缺 jar 就重新编译
if not exist "target\*.jar" (
    echo [后端] 没有构建产物，开始编译（首次需联网下载依赖，可能几分钟）...
    call mvnw.cmd -q package -DskipTests
    if errorlevel 1 (
        echo [后端] 编译失败，请看上面的报错信息。
        exit /b 1
    )
)

set "JAR="
for %%f in ("target\*.jar") do set "JAR=%%~ff"
if "%JAR%"=="" (
    echo [后端] target 下没找到 jar 包。
    exit /b 1
)

rem 端口被占用先清掉，否则 java 启动会失败
call "%~dp0helpers.bat" killport %BACKEND_PORT%

echo [后端] 启动中，jar：%JAR%
start "spongebob-backend" /min /d "%BACKEND_DIR%" "%JAVA_EXE%" -jar "%JAR%" --spring.profiles.active=dev --server.port=%BACKEND_PORT%

call "%~dp0helpers.bat" waitapi %BACKEND_PORT% 90
if errorlevel 1 (
    echo [后端] 90 秒内没有就绪，请查看最小化的 "spongebob-backend" 窗口里的日志。
    exit /b 1
)
echo [后端] 就绪：http://localhost:%BACKEND_PORT%
exit /b 0
"""

# =====================================================================
# start-frontend.bat —— 安装依赖(若缺) + 起前端(5173)
# =====================================================================
START_FRONTEND_BAT = r"""@echo off
setlocal
call "%~dp0env.bat"

echo.
echo ===== 启动前端 Vue + Vite（端口 %FRONTEND_PORT%）=====
cd /d "%FRONTEND_DIR%"

rem node_modules 每次重置都会被删除，缺了就自动装
if not exist "node_modules" (
    echo [前端] 没有 node_modules，开始安装依赖（需联网，约 1-3 分钟）...
    call npm install
    if errorlevel 1 (
        echo [前端] 依赖安装失败。可以换国内镜像后重试：
        echo        npm config set registry https://registry.npmmirror.com
        exit /b 1
    )
)

call "%~dp0helpers.bat" killport %FRONTEND_PORT%

echo [前端] 启动中 ...
start "spongebob-frontend" /min /d "%FRONTEND_DIR%" cmd /c "npm run dev"

call "%~dp0helpers.bat" waitapi %FRONTEND_PORT% 60
if errorlevel 1 (
    echo [前端] 60 秒内没有就绪，请查看最小化的 "spongebob-frontend" 窗口里的日志。
    exit /b 1
)
echo [前端] 就绪：http://localhost:%FRONTEND_PORT%
exit /b 0
"""

# =====================================================================
# stop-backend.bat / stop-frontend.bat
# =====================================================================
STOP_BACKEND_BAT = r"""@echo off
call "%~dp0env.bat"
echo ===== 停止后端（端口 %BACKEND_PORT%）=====
call "%~dp0helpers.bat" killport %BACKEND_PORT%
echo [后端] 已停止。
exit /b 0
"""

STOP_FRONTEND_BAT = r"""@echo off
call "%~dp0env.bat"
echo ===== 停止前端（端口 %FRONTEND_PORT%）=====
call "%~dp0helpers.bat" killport %FRONTEND_PORT%
echo [前端] 已停止。
exit /b 0
"""

# =====================================================================
# start-all.bat / stop-all.bat
# =====================================================================
START_ALL_BAT = r"""@echo off
chcp 936 >nul
title 海绵宝宝登录项目 - 一键启动
call "%~dp0env.bat"

echo ============================================================
echo   海绵宝宝登录项目 一键启动
echo     前端页面 : http://localhost:%FRONTEND_PORT%
echo     后端接口 : http://localhost:%BACKEND_PORT%
echo     数据库   : %DB_NAME%  (账号 %DB_USER%)
echo ============================================================

call "%~dp0init-db.bat"       || goto FAIL
call "%~dp0start-backend.bat" || goto FAIL
call "%~dp0start-frontend.bat" || goto FAIL

echo.
echo ------------------------------------------------------------
echo   全部启动完成
echo   浏览器打开 : http://localhost:%FRONTEND_PORT%
echo   测试账号   : spongebob / 123456
echo   停止项目   : 双击 scripts\stop-all.bat
echo ------------------------------------------------------------
if not "%SPONGE_NO_PAUSE%"=="1" pause
exit /b 0

:FAIL
echo.
echo !!! 启动中断，请看上面的错误提示 !!!
if not "%SPONGE_NO_PAUSE%"=="1" pause
exit /b 1
"""

STOP_ALL_BAT = r"""@echo off
chcp 936 >nul
title 海绵宝宝登录项目 - 停止
call "%~dp0env.bat"

echo ============================================================
echo   停止全部服务
echo ============================================================
call "%~dp0stop-backend.bat"
call "%~dp0stop-frontend.bat"
echo.
echo 完成：端口 %BACKEND_PORT% 和 %FRONTEND_PORT% 已释放。
echo   注意：MySQL 服务保持运行（它是系统服务，不用每次关）。
if not "%SPONGE_NO_PAUSE%"=="1" pause
exit /b 0
"""

# =====================================================================
# build-release.bat —— 前端构建 + 打进后端 + 单 jar 发布
# =====================================================================
BUILD_RELEASE_BAT = r"""@echo off
setlocal
call "%~dp0env.bat"

echo.
echo ===== 打包发布版（前端构建 + 打进后端 + 单 jar）=====
echo 说明：产物是一个 jar，双击运行后访问 http://localhost:%BACKEND_PORT%
echo       就是完整的登录应用，不需要安装 node，也不需要起前端服务。

cd /d "%FRONTEND_DIR%"

rem 1) 前端依赖（重置后会被删，缺了就装）
if not exist "node_modules" (
    echo [发布] 没有 node_modules，先安装前端依赖 ...
    call npm install
    if errorlevel 1 (
        echo [发布] 前端依赖安装失败。
        exit /b 1
    )
)

rem 2) 构建前端产物
echo [发布] 构建前端产物到 dist\ ...
call npm run build
if errorlevel 1 (
    echo [发布] 前端构建失败，请看上面的报错。
    exit /b 1
)

rem 3) 把 dist 拷进后端静态资源目录（同源部署，不需要跨域和代理）
echo [发布] 拷贝 dist 到后端 static\ ...
xcopy /e /y /i "dist" "%BACKEND_DIR%\src\main\resources\static" >nul
if errorlevel 1 (
    echo [发布] 拷贝失败。
    exit /b 1
)

rem 4) 后端打成一个 jar
echo [发布] Maven 打包后端（首次需联网，之后走本地缓存）...
cd /d "%BACKEND_DIR%"
call mvnw.cmd -q clean package -DskipTests
if errorlevel 1 (
    echo [发布] 后端打包失败，请看上面的报错。
    exit /b 1
)

set "JAR="
for %%f in ("target\*.jar") do set "JAR=%%~ff"

rem 额外：把 jar 拷贝到项目根目录（重置后 target/ 会被删，但根目录文件保留）
rem 这样下次开机直接 java -jar spongebob-login.jar 就能起，无需重新编译
copy /y "%JAR%" "%~dp0..\spongebob-login.jar" >nul
echo [发布] 已拷贝发布 jar 到项目根目录：spongebob-login.jar（重置后依然保留）
copy /y "%JAR%" "%BACKUP_JAR%" >nul
echo [发布] 已额外备份发布 jar 到：%BACKUP_JAR%（项目目录被清也能直接 java -jar）
echo.
echo ------------------------------------------------------------
echo   发布完成！
echo   产物：%JAR%
echo   运行：java -jar "%JAR%"
echo   然后浏览器打开 http://localhost:%BACKEND_PORT%
echo   停止：双击 scripts\stop-all.bat
echo ------------------------------------------------------------
if not "%SPONGE_NO_PAUSE%"=="1" pause
exit /b 0
"""


# =====================================================================
# start-jar.bat —— 直接跑项目根目录里「重置后依然保留」的发布 jar（最快）
# =====================================================================
START_JAR_BAT = r"""@echo off
setlocal
call "%~dp0env.bat"

echo.
echo ===== 启动单 jar 发布版（端口 %BACKEND_PORT%，无需 node / 无需编译）=====
echo 说明：spongebob-login.jar 是 build-release.bat 生成并拷贝到项目根目录的，
echo       重置后 target/ 会被删，但根目录的 jar 还在，所以这是最快的启动方式。

rem 先确保数据库存在（重置后库可能没了，幂等建库建表，不删数据）
call "%~dp0init-db.bat" || goto FAIL

set "RELEASE_JAR=%~dp0..\spongebob-login.jar"
if not exist "%RELEASE_JAR%" (
    if exist "%BACKUP_JAR%" (
        set "RELEASE_JAR=%BACKUP_JAR%"
        echo [发布] 项目根目录 jar 缺失，改用备份：%BACKUP_JAR%
    )
)
if not exist "%RELEASE_JAR%" (
    echo [发布] 没找到发布 jar（%RELEASE_JAR%）
    echo        请先双击 scripts\build-release.bat 生成发布 jar。
    exit /b 1
)

call "%~dp0helpers.bat" killport %BACKEND_PORT%

echo [发布] 启动中 ...
start "spongebob-jar" /min "%JAVA_EXE%" -jar "%RELEASE_JAR%" --server.port=%BACKEND_PORT%

call "%~dp0helpers.bat" waitapi %BACKEND_PORT% 90
if errorlevel 1 (
    echo [发布] 90 秒内没有就绪，请查看最小化的 "spongebob-jar" 窗口日志。
    exit /b 1
)
echo.
echo ------------------------------------------------------------
echo   单 jar 启动完成！
echo   浏览器打开 : http://localhost:%BACKEND_PORT%
echo   测试账号   : spongebob / 123456
echo   停止项目   : 双击 scripts\stop-all.bat
echo ------------------------------------------------------------
exit /b 0

:FAIL
echo.
echo !!! 启动中断，请看上面的错误提示 !!!
exit /b 1
"""


# =====================================================================
# install-autostart.bat / uninstall-autostart.bat
# 由用户「以管理员身份」双击一次：把 start-jar.bat 注册成登录时自动启动
# （沙箱里无法跑 schtasks，所以做成脚本交给你在真实 cmd 里执行）
# =====================================================================
INSTALL_AUTOSTART_BAT = r"""@echo off
chcp 936 >nul
title 安装开机自启动（海绵宝宝登录）
call "%~dp0env.bat"
set "TASK_NAME=SpongeBobLoginAutoStart"
set "BAT=%~dp0start-jar.bat"
echo 正在创建计划任务：登录 Windows 时自动启动应用（端口 %BACKEND_PORT%）...
schtasks /create /tn "%TASK_NAME%" /tr "cmd.exe /c %BAT%" /sc onlogon /rl highest /f
if errorlevel 1 (
    echo 创建失败，请确认「以管理员身份」运行本脚本。
    pause
    exit /b 1
)
echo 已安装：下次登录会自动启动 http://localhost:%BACKEND_PORT%
echo 停止自动启动：双击 scripts\uninstall-autostart.bat
pause
"""

UNINSTALL_AUTOSTART_BAT = r"""@echo off
chcp 936 >nul
set "TASK_NAME=SpongeBobLoginAutoStart"
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>nul
echo 已卸载开机自启动任务（%TASK_NAME%）。
pause
"""


def main():
    print("生成脚本目录：", OUT_DIR)
    write_bat("env.bat", ENV_BAT)
    write_bat("helpers.bat", HELPERS_BAT)
    write_bat("init-db.bat", INIT_DB_BAT)
    write_bat("start-backend.bat", START_BACKEND_BAT)
    write_bat("start-frontend.bat", START_FRONTEND_BAT)
    write_bat("stop-backend.bat", STOP_BACKEND_BAT)
    write_bat("stop-frontend.bat", STOP_FRONTEND_BAT)
    write_bat("start-all.bat", START_ALL_BAT)
    write_bat("stop-all.bat", STOP_ALL_BAT)
    write_bat("build-release.bat", BUILD_RELEASE_BAT)
    write_bat("start-jar.bat", START_JAR_BAT)
    write_bat("install-autostart.bat", INSTALL_AUTOSTART_BAT)
    write_bat("uninstall-autostart.bat", UNINSTALL_AUTOSTART_BAT)
    print("全部完成。所有 .bat 均为 GBK(无 BOM)，可直接在 cmd 双击运行。")


if __name__ == "__main__":
    main()
