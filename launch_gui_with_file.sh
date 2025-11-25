#!/bin/bash
# Launch GUI with a test file pre-loaded

cd "$(dirname "$0")"

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Clear debug log
rm -f /tmp/pcg_debug.log

# Create a simple test script that opens a file
SCRIPT_DIR="$(pwd)"
cat > /tmp/launch_pcg_gui.py << EOF
import sys
import tkinter as tk
from pathlib import Path

# Add to path
sys.path.insert(0, '$SCRIPT_DIR')

from pcg_tools.gui_macos import PcgToolsGUI

# Create app
root = tk.Tk()
app = PcgToolsGUI(root)

# Auto-open a file
test_file = '/Volumes/KEYBOARD/soundcheck9_25_25.PCG'
if Path(test_file).exists():
    app.open_file(test_file)
    print(f"Loaded: {test_file}")
else:
    print("Test file not found, showing empty GUI")

root.mainloop()
EOF

python3 /tmp/launch_pcg_gui.py
