#!/bin/bash

# Create directories if they don't exist
mkdir -p uploads
mkdir -p app/api
mkdir -p app/components
mkdir -p app/public
mkdir -p app/styles
mkdir -p pages/api

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

echo "Setup complete!"
echo "Run 'npm run dev' to start the development server." 