@echo off
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
