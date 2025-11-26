# PCG Tools - macOS Quick Start

## ✓ Installation Complete!

You now have PCG Tools running with Python 3.12 and Tk 9.0, which fixes all the display issues.

## Running PCG Tools

### GUI (Graphical Interface)

```bash
cd /Volumes/nvme1tb/kiro-projects/korg_pcg_tools
./pcg-tools gui
```

Or directly:
```bash
./venv/bin/python -m pcg_tools gui
```

### CLI (Command Line)

```bash
# View file info
./pcg-tools info /Volumes/KEYBOARD/path/to/file.PCG

# Export patch list
./pcg-tools export /Volumes/KEYBOARD/path/to/file.PCG output.csv

# List all patches
./pcg-tools list-patches /Volumes/KEYBOARD/path/to/file.PCG

# Generate reports
./pcg-tools program-usage /Volumes/KEYBOARD/path/to/file.PCG usage.csv
./pcg-tools combi-content /Volumes/KEYBOARD/path/to/file.PCG content.csv

# Compare files
./pcg-tools differences file1.PCG file2.PCG diff.csv

# Help
./pcg-tools --help
```

## What Was Fixed

- **Problem**: System Python uses Tk 8.5 (from 2007) which has rendering bugs on modern macOS
- **Solution**: Installed Python 3.12 with Tk 9.0 via Homebrew in a virtual environment
- **Result**: GUI now displays all patches correctly

## Files in Your PCG Tools Directory

- `pcg-tools` - Launcher script (use this to run the tool)
- `venv/` - Virtual environment with working Python/Tk
- `pcg_tools/` - Main application code
- `test_files/` - Sample PCG files
- Test files created during troubleshooting (can be deleted):
  - `test_*.py` files
  - `MACOS_*.md` files

## Using the GUI

1. Launch: `./pcg-tools gui`
2. File > Open PCG to load a file from /Volumes/KEYBOARD
3. View Programs or Combis tabs
4. Double-click a patch to edit
5. Use Copy/Paste to move patches between files
6. File > Save to save changes

## Keyboard Shortcuts

- **Cmd+O** - Open file
- **Cmd+S** - Save file
- **Cmd+C** - Copy patches
- **Cmd+V** - Paste patches
- **Delete** - Clear patches
- **Return** - Edit selected patch

## Support

All features from the Windows version now work on macOS:
- ✓ Open/Save PCG files
- ✓ Edit patch names, categories, favorites
- ✓ Copy/paste patches
- ✓ Multiple windows
- ✓ Export to CSV/TXT
- ✓ Generate reports
- ✓ Drag and drop (within same window)

Enjoy editing your Korg patches!
