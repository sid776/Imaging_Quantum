@echo off
echo === Quantum Medical Image Scanner ===
echo Starting setup and initialization...

:: Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js is not installed. Please install Node.js (v14 or higher).
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed. Please install Python (v3.8 or higher).
    exit /b 1
)

:: Create uploads directory if it doesn't exist
if not exist uploads\ (
    echo Creating uploads directory...
    mkdir uploads
)

:: Install Node.js dependencies if node_modules doesn't exist
if not exist node_modules\ (
    echo Installing Node.js dependencies...
    call npm install
)

:: Install Python dependencies
echo Installing Python dependencies...
call python -m pip install -r requirements.txt

:: Start the development server
echo Starting the development server...
echo Once started, open your browser and navigate to http://localhost:3000
call npm run dev 