#!/bin/sh
. venv/bin/activate
python3 -m pip install -f requirements.txt
python3 src/main.py
cd public && python -m http.server 8080
