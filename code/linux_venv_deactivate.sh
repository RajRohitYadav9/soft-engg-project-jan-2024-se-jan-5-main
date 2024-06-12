#!/bin/bash

# Function to stop the running Python script (replace 'main.py' with the actual filename)
#stop_script() {
  # Find the process ID (PID) of the running script
 # script_pid=$(ps aux | grep app.py | awk '{print $2}')

  # Check if PID exists (script might not be running)
  #if [ ! -z "$script_pid" ]; then
    # Kill the process using the PID
   # kill -SIGINT "$script_pid"
    #echo "Stopped running script (PID: $script_pid)"
  #else
   # echo "Script 'main.py' not found or not running."
  #fi
#}

# Stop the script
#stop_script

# Deactivate the virtual environment
source .venv/bin/deactivate
echo "Deactivated virtual environment."
