@echo off
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
