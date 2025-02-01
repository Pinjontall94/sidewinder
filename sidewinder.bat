@echo off

REM Activate the python environment and install dependencies
venv\Scripts\activate.bat
python.exe -m pip install -f requirements.txt
python.exe src\main.py
cd public\
python.exe -m http.server 8080

REM Deactivate environment and exit to CMD
cd ..
venv\Scripts\deactivate.bat
exit /B
