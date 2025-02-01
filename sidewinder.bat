@echo off
REM Activate the python environment and install dependencies
venv\Scripts\pip -m pip install -f requirements.txt
venv\Scripts\python src\main.py
