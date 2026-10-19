@echo off
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
