# GitHub Push Helper Script
Write-Host "=== GitHub Push Helper for Quantum Medical Image Scanner ===" -ForegroundColor Green
Write-Host "This script will guide you through the process of pushing your project to GitHub." -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "Error: Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads and try again." -ForegroundColor Yellow
    Write-Host "After installing Git, you may need to restart your terminal." -ForegroundColor Yellow
    exit
}

# Instructions for pushing to GitHub
Write-Host "To push your project to https://github.com/sid776/Imaging_Quantum, follow these steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Initialize a Git repository (if not already done):" -ForegroundColor White
Write-Host "   git init" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Add all files to the repository:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Commit the changes:" -ForegroundColor White
Write-Host "   git commit -m 'Initial commit of Quantum Medical Image Scanner'" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Add the remote repository:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/sid776/Imaging_Quantum.git" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Push to GitHub:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: If your default branch is 'master' instead of 'main', use:" -ForegroundColor White
Write-Host "   git push -u origin master" -ForegroundColor Yellow
Write-Host ""
Write-Host "If you're prompted for credentials:" -ForegroundColor Cyan
Write-Host "- Username: Your GitHub username" -ForegroundColor White
Write-Host "- Password: Use a personal access token (not your GitHub password)" -ForegroundColor White
Write-Host "  To create a token, visit: https://github.com/settings/tokens" -ForegroundColor Yellow
Write-Host ""
Write-Host "Would you like to attempt these commands automatically? (Y/N)" -ForegroundColor Green
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    try {
        Write-Host "Initializing Git repository..." -ForegroundColor Cyan
        git init
        
        Write-Host "Adding all files..." -ForegroundColor Cyan
        git add .
        
        Write-Host "Committing changes..." -ForegroundColor Cyan
        git commit -m "Initial commit of Quantum Medical Image Scanner"
        
        Write-Host "Adding remote repository..." -ForegroundColor Cyan
        git remote add origin https://github.com/sid776/Imaging_Quantum.git
        
        Write-Host "Would you like to push to 'main' or 'master' branch? (main/master)" -ForegroundColor Green
        $branch = Read-Host
        
        if ($branch -ne "main" -and $branch -ne "master") {
            $branch = "main"
        }
        
        Write-Host "Pushing to $branch branch..." -ForegroundColor Cyan
        git push -u origin $branch
        
        Write-Host "Process completed!" -ForegroundColor Green
    }
    catch {
        Write-Host "An error occurred: $_" -ForegroundColor Red
        Write-Host "Please try the commands manually as outlined above." -ForegroundColor Yellow
    }
}
else {
    Write-Host "You've chosen to run the commands manually. Please follow the steps outlined above." -ForegroundColor Yellow
} 