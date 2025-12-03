@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
py -m flask --app app run --debug
pause
