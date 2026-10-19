@echo off
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
