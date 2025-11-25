#!/bin/bash
# Quick start script for hardware testing

echo "🎯 Starting PCG Hardware Testing Tool"
echo ""
echo "This will launch the GUI with your PCG file loaded."
echo "Make your edits, then save for hardware testing."
echo ""

cd "$(dirname "$0")"

# Find a test file or use provided argument
if [ -n "$1" ]; then
    FILE="$1"
elif [ -f "test_files/test_soundcheck9_25_25_combined.PCG" ]; then
    FILE="test_files/test_soundcheck9_25_25_combined.PCG"
else
    echo "❌ No PCG file found"
    echo "Usage: ./START_TESTING.sh <path/to/file.PCG>"
    exit 1
fi

echo "📂 Loading: $FILE"
echo ""

# Launch the GUI directly
python3 launch_gui_test_sls1.py

echo ""
echo "✅ Testing session complete!"
