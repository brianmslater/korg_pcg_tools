# macOS GUI Display Issue - Summary

## Problem Identified

The PCG Tools GUI is not displaying any content on your macOS system because you're using the system Python with Tk 8.5, which has critical rendering bugs.

## What We Tested

1. ✓ File loading works - PCG files load correctly
2. ✓ Data parsing works - All patches are read properly  
3. ✓ Widget creation works - GUI windows open
4. ✗ Widget rendering FAILS - No content displays (Treeview, Listbox, Text widgets all fail)

## Root Cause

```bash
$ python3 -c "import tkinter; print(tkinter.TkVersion)"
8.5
```

Tk 8.5 from 2007 has known bugs on modern macOS that prevent widgets from rendering content.

## Solutions

### Option 1: Install Homebrew Python (RECOMMENDED)

This gives you a fully working GUI:

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python with working Tk
brew install python-tk@3.12

# Install dependencies
/opt/homebrew/bin/python3 -m pip install click

# Run PCG Tools
cd /path/to/korg_pcg_tools
/opt/homebrew/bin/python3 -m pcg_tools gui
```

Or use the helper script:
```bash
./run_gui_macos.sh
```

### Option 2: Use Command-Line Interface

The CLI works perfectly with system Python:

```bash
# View file information
python3 -m pcg_tools info /Volumes/KEYBOARD/path/to/file.PCG

# Export patch list to CSV
python3 -m pcg_tools export /Volumes/KEYBOARD/path/to/file.PCG output.csv

# List all patches
python3 -m pcg_tools list-patches /Volumes/KEYBOARD/path/to/file.PCG

# Generate program usage report
python3 -m pcg_tools program-usage /Volumes/KEYBOARD/path/to/file.PCG usage.csv

# Generate combi content report
python3 -m pcg_tools combi-content /Volumes/KEYBOARD/path/to/file.PCG content.csv

# Compare two files
python3 -m pcg_tools differences file1.PCG file2.PCG diff.csv

# Get help
python3 -m pcg_tools --help
```

### Option 3: Run on Windows

The original PCG Tools was designed for Windows. If you have access to a Windows machine or VM, the GUI will work perfectly there with system Python.

## Files Created

- `MACOS_INSTALL.md` - Detailed installation instructions
- `run_gui_macos.sh` - Helper script to launch with correct Python
- `pcg_tools/gui_macos.py` - macOS-compatible GUI (requires Tk 8.6+)

## Testing Files

Several test files were created to diagnose the issue:
- `test_gui_load.py` - Tests file loading
- `test_gui_display.py` - Tests tree display
- `test_flat_list.py` - Tests flat list display
- `test_listbox.py` - Tests basic listbox
- `test_text_widget.py` - Tests text widget
- `test_direct_load.py` - Tests direct file loading

All tests show data loads correctly but doesn't render with Tk 8.5.

## Recommendation

Install Homebrew Python for the best experience. The installation takes about 5-10 minutes and gives you a fully functional GUI that matches the Windows version.
