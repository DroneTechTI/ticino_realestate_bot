#!/bin/bash

echo "Starting Ticino Real Estate Bot..."
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt
echo ""

echo "Starting bot..."
python main.py
