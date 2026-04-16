#!/bin/bash

echo "Starting manga converter..."

# Go to the folder where the script is located
cd "$(dirname "$0")" || exit

# Run python script (Mac/Linux usually require 'python3' instead of 'python')
python3 cbz_builder.py

# Pause so the terminal window doesn't immediately close
read -p "Press Enter to exit..."