#!/bin/bash

# Change to the project directory
cd "$(dirname "$0")"

# Ensure virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "Creating virtual environment..."
    python -m venv ../.venv
fi

# Activate virtual environment
source "../.venv/Scripts/activate"

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Install spaCy model if not already installed
if ! python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "Installing spaCy model..."
    python -m spacy download en_core_web_sm
fi

# Set Python path
export PYTHONPATH=$PYTHONPATH:src

# Run the web interface
echo "Starting web interface..."
python src/web_interface.py
