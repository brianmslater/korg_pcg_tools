@echo off
REM PCG Tools GUI Launcher for Windows
echo.
echo ================================================
echo   PCG Tools - Korg PCG File Editor
echo ================================================
echo.
echo Starting GUI...
echo.

python -m pcg_tools gui

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start PCG Tools
    echo Make sure you're in the correct directory
    echo.
    pause
)
