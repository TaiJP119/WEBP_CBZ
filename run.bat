@echo off
echo Starting manga converter...

REM go to the folder where the script is located (important)
cd /d "%~dp0"

REM run python script
python cbz_builder.py

pause