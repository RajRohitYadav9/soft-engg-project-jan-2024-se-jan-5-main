#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Check if virtual environment is activated
if [ ! $(python3 -c "import sys; print(sys.version)") ]; then
  echo "Error: Could not activate virtual environment. Please create it manually or fix the activation command."
  exit 1
fi

# Get the current directory (script location)
script_dir=$(pwd)

# Install requirements (assuming requirements.txt is in the same directory)
pip install -r requirements.txt

# Path to your main Python file (replace 'main.py' with the actual filename)
main_script="$script_dir/backend/app.py"

# Check if the main script exists
if [ ! -f "$main_script" ]; then
  echo "Error: Main script '$main_script' not found."
  exit 1
fi

# Run the main Python script
python3 "$main_script"
