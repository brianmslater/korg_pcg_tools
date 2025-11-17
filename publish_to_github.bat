@echo off
echo ========================================
echo PCG Tools Python - GitHub Publisher
echo ========================================
echo.
echo This script will help you publish to GitHub
echo.
echo BEFORE RUNNING THIS:
echo 1. Create repository on GitHub.com
echo 2. Name it: pcg-tools-python
echo 3. Note your GitHub username
echo.
echo ========================================
echo.

set /p username="Enter your GitHub username: "

if "%username%"=="" (
    echo Error: Username cannot be empty
    pause
    exit /b 1
)

echo.
echo Setting up remote for: https://github.com/%username%/pcg-tools-python.git
echo.

git remote add origin https://github.com/%username%/pcg-tools-python.git
if errorlevel 1 (
    echo Remote already exists, updating URL...
    git remote set-url origin https://github.com/%username%/pcg-tools-python.git
)

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo AUTHENTICATION REQUIRED
    echo ========================================
    echo.
    echo If you see authentication errors:
    echo 1. Go to GitHub.com - Settings - Developer settings
    echo 2. Create Personal Access Token
    echo 3. Run this command with your token:
    echo.
    echo git remote set-url origin https://YOUR_TOKEN@github.com/%username%/pcg-tools-python.git
    echo.
    echo Then run: git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo Next steps:
echo 1. Go to: https://github.com/%username%/pcg-tools-python
echo 2. Add topics: korg, synthesizer, pcg, python
echo 3. Create a release (v2.1.0)
echo.
echo See PUBLISH_TO_GITHUB.md for details
echo.
pause
