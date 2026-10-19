@echo off
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
