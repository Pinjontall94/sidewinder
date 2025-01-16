@echo off

REM Activate the python environment and install dependencies
venv\Scripts\activate.bat
python.exe -m pip install -f requirements.txt
python.exe main.py

REM Deactivate environment and exit to CMD
venv\Scripts\deactivate.bat
exit /B
