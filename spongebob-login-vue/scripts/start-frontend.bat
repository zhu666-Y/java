@echo off
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
