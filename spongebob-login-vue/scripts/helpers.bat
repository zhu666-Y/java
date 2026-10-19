@echo off
rem ============================================================
rem  公共小工具（由其它脚本 call，不要直接双击）
rem    call helpers.bat killport 8081       结束占用端口的进程
rem    call helpers.bat apiup 8081          服务有响应返回 0，否则返回 1
rem    call helpers.bat waitapi 8081 60     最多等 60 秒，成功返回 0
rem ============================================================
if "%~1"=="" exit /b 1
if /i "%~1"=="killport" goto KILLPORT
if /i "%~1"=="apiup"    goto APIUP
if /i "%~1"=="waitapi"  goto WAITAPI
echo [工具] 未知命令：%~1
exit /b 1

:KILLPORT
rem 同一端口 IPv4/IPv6 会各有一行、PID 相同，用空格分隔的已杀列表去重
setlocal enabledelayedexpansion
set "PORT=%~2"
set "DONE= "
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT% " ^| findstr "LISTENING"') do (
    echo !DONE! | findstr /c:" %%p " >nul
    if errorlevel 1 (
        set "DONE=!DONE!%%p "
        echo [工具] 端口 %PORT% 被进程 %%p 占用，正在结束它 ...
        taskkill /f /pid %%p >nul 2>nul
    )
)
endlocal
exit /b 0

:APIUP
setlocal
set "PORT=%~2"
where curl >nul 2>nul
if errorlevel 1 (
    rem 没有 curl 就退化成"端口是否在监听"
    netstat -ano | findstr ":%PORT% " | findstr "LISTENING" >nul 2>nul
    if errorlevel 1 ( endlocal & exit /b 1 )
    endlocal & exit /b 0
)
for /f %%c in ('curl -s -o nul -w "%%{http_code}" http://127.0.0.1:%PORT%/ 2^>nul') do (
    if not "%%c"=="000" ( endlocal & exit /b 0 )
)
endlocal
exit /b 1

:WAITAPI
setlocal
set "PORT=%~2"
set "TIMES=%~3"
for /l %%i in (1,1,%TIMES%) do (
    call "%~dp0helpers.bat" apiup %PORT%
    if not errorlevel 1 ( endlocal & exit /b 0 )
    ping -n 2 127.0.0.1 >nul
)
endlocal
exit /b 1
