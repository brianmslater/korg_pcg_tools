#!/bin/bash
# Fixed GUI launcher with proper initialization

cd "$(dirname "$0")"

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Clear debug log
rm -f /tmp/pcg_debug.log

# Launch GUI with proper environment
export PYTHONUNBUFFERED=1
python3 -m pcg_tools.cli gui
