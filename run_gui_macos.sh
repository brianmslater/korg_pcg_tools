#!/bin/bash
# Helper script to run PCG Tools GUI on macOS with proper Python

echo "PCG Tools - macOS Launcher"
echo "=========================="
echo ""

# Check for Homebrew Python
if [ -f "/opt/homebrew/bin/python3" ]; then
    echo "✓ Found Homebrew Python"
    PYTHON="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    echo "✓ Found Homebrew Python (Intel Mac)"
    PYTHON="/usr/local/bin/python3"
else
    echo "✗ Homebrew Python not found"
    echo ""
    echo "Your system Python has Tk 8.5 which doesn't work properly on macOS."
    echo "Please install Homebrew Python:"
    echo ""
    echo "  brew install python-tk@3.12"
    echo ""
    echo "Or see MACOS_INSTALL.md for detailed instructions."
    echo ""
    exit 1
fi

# Check Tk version
TK_VERSION=$($PYTHON -c "import tkinter; print(tkinter.TkVersion)" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "✗ Tkinter not available"
    exit 1
fi

echo "  Tk version: $TK_VERSION"

if (( $(echo "$TK_VERSION < 8.6" | bc -l) )); then
    echo "✗ Tk version too old (need 8.6+)"
    echo "  Please install: brew install python-tk@3.12"
    exit 1
fi

echo "✓ Tk version OK"
echo ""

# Check for click
$PYTHON -c "import click" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing click..."
    $PYTHON -m pip install click
fi

echo "Launching PCG Tools GUI..."
echo ""

cd "$(dirname "$0")"
$PYTHON -m pcg_tools gui
