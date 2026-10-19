@echo off
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
