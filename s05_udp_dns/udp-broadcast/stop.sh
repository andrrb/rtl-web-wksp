# @echo off
# set DIR=C:\Users\Lenovo\OneDrive\Desktop\Seminar 5\udp-broadcast
# cd /d %DIR%

echo Stopping docker-compose services...
docker-compose down

# echo Closing chat windows...
# taskkill /FI "WINDOWTITLE eq Server*" /F >nul 2>&1
# taskkill /FI "WINDOWTITLE eq Alice*" /F >nul 2>&1
# taskkill /FI "WINDOWTITLE eq Bob*" /F >nul 2>&1
# taskkill /FI "WINDOWTITLE eq Charlie*" /F >nul 2>&1
