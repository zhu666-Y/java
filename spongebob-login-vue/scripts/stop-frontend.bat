@echo off
call "%~dp0env.bat"
echo ===== Í£Ö¹Ç°¶Ë£¨¶Ë¿Ú %FRONTEND_PORT%£©=====
call "%~dp0helpers.bat" killport %FRONTEND_PORT%
echo [Ç°¶Ë] ÒÑÍ£Ö¹¡£
exit /b 0
