#!/bin/bash
set -e

# Activate the virtual environment
SCRIPT_DIR="$(dirname "$0")"
VENV_DIR="$SCRIPT_DIR/taskcat-env"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing TaskCat if not already installed..."
pip install taskcat --upgrade

echo "Running TaskCat tests..."
cd "$SCRIPT_DIR"
taskcat test run

# Deactivate the virtual environment
deactivate

echo "Tests completed. Check the TaskCat report for results."
