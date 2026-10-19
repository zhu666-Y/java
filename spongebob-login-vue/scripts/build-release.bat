@echo off
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
