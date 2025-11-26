# Project Structure

This document describes the organization of the PCG Tools repository.

## Root Directory

```
korg_pcg_tools/
├── README.md                    # Main project documentation
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── INSTALL.md                   # Installation instructions
├── QUICKSTART.md                # Quick start guide
├── USAGE.md                     # Detailed usage guide
├── QUICK_REFERENCE.md           # Command reference
├── KNOWN_ISSUES.md              # Known limitations
├── SIMPLE_EDITOR_GUIDE.md       # Simple setlist editor guide
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
│
├── pcg-tools                    # Main CLI launcher (Unix)
├── edit-setlists                # Setlist editor launcher (Unix)
├── launch_gui.bat               # GUI launcher (Windows)
├── launch_gui_fixed.sh          # GUI launcher (Unix)
├── run_gui_macos.sh             # GUI launcher (macOS)
├── simple_setlist_editor.py     # Standalone setlist editor
│
├── pcg_tools/                   # Main application package
│   ├── __init__.py
│   ├── cli.py                   # Command-line interface
│   ├── models.py                # Data models
│   ├── pcg_parser.py            # PCG file parser
│   ├── writer.py                # PCG file writer
│   ├── gui_qt.py                # Main GUI (Qt)
│   ├── edit_dialog.py           # Edit dialogs
│   ├── bit_utils.py             # Binary utilities
│   └── ...
│
├── docs/                        # Additional documentation
│   ├── TECHNICAL_REFERENCE.md   # Technical details
│   ├── HARDWARE_TESTING_GUIDE.md
│   ├── MACOS_INSTALL.md         # macOS-specific install
│   ├── README_MACOS.md          # macOS quick start
│   ├── SLS1_USAGE_GUIDE.md      # Setlist format guide
│   ├── SLS1_QUICK_REFERENCE.md
│   ├── WRITER_QUICK_REFERENCE.md
│   ├── QUICK_START_WRITER.md
│   └── KRONOS_Op_Guide_E10.pdf  # Official Korg manual
│
├── examples/                    # Usage examples
│   └── basic_usage.py
│
├── test_files/                  # Sample PCG files (gitignored)
├── archive/                     # Development scripts (gitignored)
├── dev_notes/                   # Development notes (gitignored)
├── venv/                        # Virtual environment (gitignored)
└── venv_tk/                     # Tk virtual env (gitignored)
```

## Key Files

### User Documentation
- **README.md** - Start here! Overview and features
- **QUICKSTART.md** - Get started in 5 minutes
- **INSTALL.md** - Detailed installation for all platforms
- **USAGE.md** - Complete feature documentation
- **SIMPLE_EDITOR_GUIDE.md** - How to use the simple setlist editor

### Developer Documentation
- **CONTRIBUTING.md** - How to contribute
- **docs/TECHNICAL_REFERENCE.md** - PCG format details
- **CHANGELOG.md** - Version history

### Launchers
- **pcg-tools** - Main CLI entry point (Unix/macOS)
- **edit-setlists** - Quick setlist editor launcher
- **launch_gui.bat** - Windows GUI launcher
- **run_gui_macos.sh** - macOS GUI launcher
- **simple_setlist_editor.py** - Standalone editor (all platforms)

## Application Package (pcg_tools/)

The main Python package containing:
- **cli.py** - Click-based command-line interface
- **models.py** - PCG data structures (Program, Combi, Setlist, etc.)
- **pcg_parser.py** - Binary PCG file parser
- **writer.py** - PCG file writer (hardware-tested)
- **gui_qt.py** - Qt-based graphical interface
- **edit_dialog.py** - Patch editing dialogs
- **bit_utils.py** - Binary manipulation utilities

## Excluded from Git

The following directories are kept locally but not tracked in git:

- **archive/** - Development and test scripts
- **dev_notes/** - Session notes and progress tracking
- **test_files/** - Test PCG files
- **venv/** - Python virtual environments

See `.gitignore` for complete list.

## Documentation Organization

### Root Level
Essential docs that users need immediately:
- Installation, quick start, usage

### docs/ Folder
Detailed technical documentation:
- Platform-specific guides
- Format specifications
- Hardware testing procedures

### dev_notes/ (Local Only)
Development history and session notes

### archive/ (Local Only)
Analysis scripts and test utilities

## For Contributors

If you're contributing to the project:
1. Read CONTRIBUTING.md
2. Check docs/TECHNICAL_REFERENCE.md for format details
3. Development scripts are in archive/ (local only)
4. Session notes are in dev_notes/ (local only)

## For Users

If you're using PCG Tools:
1. Start with README.md
2. Follow INSTALL.md for your platform
3. Try QUICKSTART.md to get started
4. Reference USAGE.md for detailed features
5. Use SIMPLE_EDITOR_GUIDE.md for setlist editing
