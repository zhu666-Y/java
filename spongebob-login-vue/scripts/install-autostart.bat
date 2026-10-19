@echo off
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
