#!/bin/bash

# Quantum Medical Image Scanner Runner Script
echo "=== Quantum Medical Image Scanner ==="
echo "Starting setup and initialization..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js (v14 or higher)."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python (v3.8 or higher)."
    exit 1
fi

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "Creating uploads directory..."
    mkdir -p uploads
fi

# Install Node.js dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start the development server
echo "Starting the development server..."
echo "Once started, open your browser and navigate to http://localhost:3000"
npm run dev 