@echo off
echo Setting up Quantum Medical Image Scanner...

:: Create directories if they don't exist
if not exist uploads mkdir uploads
if not exist app\api mkdir app\api
if not exist app\components mkdir app\components
if not exist app\public mkdir app\public
if not exist app\styles mkdir app\styles
if not exist pages\api mkdir pages\api

:: Install Node.js dependencies
echo Installing Node.js dependencies...
call npm install

:: Install Python dependencies
echo Installing Python dependencies...
call pip install -r requirements.txt

echo.
echo Setup complete!
echo Run 'npm run dev' to start the development server. 