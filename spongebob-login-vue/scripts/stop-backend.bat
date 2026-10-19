@echo off
call "%~dp0env.bat"
echo ===== Í£Ö¹ºó¶Ë£¨¶Ë¿Ú %BACKEND_PORT%£©=====
call "%~dp0helpers.bat" killport %BACKEND_PORT%
echo [ºó¶Ë] ÒÑÍ£Ö¹¡£
exit /b 0
