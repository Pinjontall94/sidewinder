#!/bin/sh

# Ensure this file is run in the sidewinder root folder
if [ "$(basename "$PWD")" != "sidewinder" ]; then
    echo "Re-run this script in the sidewinder folder!"
    exit 1
fi

# Create virtual environment and install dependencies if not present
if [ ! -d "./venv/" ]; then
    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -r requirements.txt
else
    . venv/bin/activate
fi

# Run the main python script to create the site
python3 src/main.py

# Enter the generated site folder and run the built-in webserver on port 8080
cd public && python3 -m http.server 8080
