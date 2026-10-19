@echo off
chcp 936 >nul
set "TASK_NAME=SpongeBobLoginAutoStart"
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>nul
echo 已卸载开机自启动任务（%TASK_NAME%）。
pause
