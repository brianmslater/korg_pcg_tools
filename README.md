# PCG Tools Python

**Cross-platform Korg PCG file editor** - A complete Python rewrite of the original PCG Tools.

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.7+-blue)]()
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)]()
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🎉 Status: Production Ready

All core features have been implemented, tested, and verified on hardware. The application is **ready for daily use**.

**Latest Updates**:
- ✅ **GM2 Banks Support** - View all 10 GM2 banks (g(1)-g(9), g(d)) with 1,280 programs
- ✅ **Read-Only ROM Banks** - Proper handling of ROM banks with copy support
- ✅ **GUI Consolidation** - Single Qt-based GUI (removed legacy tkinter editors)
- ✅ Complete setlist support - All 16 setlists with 128 slots each
- ✅ Working PCG writer - Confirmed on Korg Kronos 2 hardware
- ✅ Full slot editing - Names, colors, transpose, volume, notes

---

## ✨ Features

### GUI Application (Qt-based)
- ✅ **Modern interface** - Single Qt-based GUI with native look and feel
- ✅ **Hardware tested** - Confirmed working on Korg Kronos 2
- ✅ **GM2 Banks** - View all 10 GM2 banks with 1,280 programs (read-only)
- ✅ **ROM Bank Protection** - Cannot accidentally edit ROM banks
- ✅ **Edit setlist names** - All 16 setlists supported
- ✅ **Edit slot properties** - Names, colors, text sizes, transpose, volume, notes
- ✅ **Patch name lookup** - Shows actual program/combi names for each slot
- ✅ **Edit patches** - Modify program and combi properties
- ✅ **Copy and paste** - Patches and setlist slots (including from ROM banks)
- ✅ **Batch operations** - Sort, compact, and organize
- ✅ **Keyboard shortcuts** - Full keyboard navigation

**Note:** Legacy tkinter-based editors have been removed. Use the Qt GUI for all editing.

### Core Functionality
- ✅ **Open and save** PCG files from all Korg synthesizers
- ✅ **Edit** patch names, categories, and favorites
- ✅ **Copy and paste** patches within and between files
- ✅ **Move, sort, and organize** your patches
- ✅ **Generate reports** on program usage and combi content
- ✅ **Export** to CSV and TXT formats
- ✅ **Command-line interface** for automation and batch processing

### User Interface
- ✅ **Qt GUI** - Single, full-featured graphical interface (PySide6)
- ✅ **Command-line tools** - Full API access via CLI
- ✅ **Cross-platform** - Works on Windows, macOS, and Linux
- ⚠️ **Legacy editors removed** - Old tkinter-based simple editor no longer included

---

## 🚀 Quick Start

### GUI Application
```bash
cd korg_pcg_tools
python3 -m pcg_tools.gui_qt
```

**Features:**
- View GM2 banks (g(1)-g(9), g(d)) with 1,280 programs
- Edit setlists and slots
- View actual patch names for each slot
- Edit programs and combis
- Copy/paste operations (including from ROM banks)
- Batch operations
- Hardware-tested and working!

### Command-Line Interface
```bash
# Show file information
python -m pcg_tools info yourfile.PCG

# Export patch list
python -m pcg_tools export yourfile.PCG output.csv

# Generate program usage report
python -m pcg_tools program-usage yourfile.PCG usage.csv

# See all commands
python -m pcg_tools --help
```

---

## 📋 Requirements

- **Python 3.7 or higher**
- **PySide6** (for GUI) - `pip install PySide6`
- **click** (for CLI) - `pip install click`

Or install all at once:
```bash
pip install -r requirements.txt
```

---

## 🎹 Supported Synthesizers

- Korg Kronos / Kronos X
- Korg Oasys
- Korg Triton (all variants)
- Korg Karma
- Korg M3 / M50
- Korg Krome
- Korg Trinity

---

## 📖 Documentation

### Getting Started
- **[SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md)** - Simple Setlist Editor guide (start here!)
- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[INSTALL.md](INSTALL.md)** - Installation instructions for all platforms
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference card

### User Guides
- **[USAGE.md](USAGE.md)** - Detailed usage instructions
- **[GM2_BANKS_REFERENCE.md](GM2_BANKS_REFERENCE.md)** - GM2 banks quick reference
- **[KNOWN_ISSUES.md](KNOWN_ISSUES.md)** - Known limitations and workarounds

### Technical Documentation
- **[GM_BANKS_IMPLEMENTATION.md](GM_BANKS_IMPLEMENTATION.md)** - GM2 banks technical details
- **[docs/TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md)** - PCG file format details
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Repository organization
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Developer guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## ⌨️ Keyboard Shortcuts (Qt GUI)

| Shortcut | Action |
|----------|--------|
| **Ctrl+O** | Open PCG file |
| **Ctrl+S** | Save file |
| **Ctrl+Shift+S** | Save As |
| **Ctrl+N** | New window |
| **Ctrl+W** | Close window |
| **Ctrl+Q** | Quit all windows |
| **Ctrl+C** | Copy selected item |
| **Ctrl+V** | Paste item |
| **Ctrl+X** | Cut item |
| **Double-click** | Edit item |
| **Right-click** | Context menu |

---

## 🖱️ Context Menu (Qt GUI)

Right-click on items to access:
- Edit
- Copy
- Paste
- Cut
- Clear
- Move Up/Down
- Sort
- Compact

---

## 🔧 CLI Commands

### Available Commands
```bash
info            # Display file information
list-patches    # List all patches
export          # Export patch list
program-usage   # Generate program usage report
combi-content   # Generate combi content report
differences     # Compare two PCG files
gui             # Launch GUI
```

### Examples
```bash
# Compare two files
python -m pcg_tools differences file1.pcg file2.pcg diff.csv

# Generate detailed combi content
python -m pcg_tools combi-content file.pcg content.csv --style long

# Export to text format
python -m pcg_tools export file.pcg output.txt --format txt
```

---

## 🎯 Common Tasks

### Edit Setlists and Slots
1. Launch Qt GUI: `python3 -m pcg_tools.gui_qt`
2. Open your PCG file (Ctrl+O)
3. Go to Setlists tab
4. Select a setlist from dropdown
5. Double-click any slot to edit
6. Edit name, color, text size, transpose, volume, or notes
7. Save the file (Ctrl+S)

### Edit Programs and Combis
1. Launch Qt GUI
2. Go to Programs or Combis tab
3. Select a bank from the list
4. Double-click a program/combi to edit
5. Modify name, category, or other properties
6. Save the file

### View GM2 Banks
1. Launch Qt GUI
2. Go to Programs tab
3. Scroll down in bank list to g(1) through g(9) and g(d)
4. Click any GM2 bank to view programs
5. Copy programs to user banks if desired (Edit/Paste disabled for ROM banks)

### Generate Reports
```bash
# Program usage report
python -m pcg_tools program-usage yourfile.PCG usage.csv

# Combi content report
python -m pcg_tools combi-content yourfile.PCG content.csv

# Export patch list
python -m pcg_tools export yourfile.PCG patches.csv
```

---

## 🌟 Advantages Over Original

| Feature | Original C# | Python Port |
|---------|-------------|-------------|
| **Platform** | Windows only | Cross-platform |
| **Framework** | .NET Framework | Pure Python |
| **Setlist Editing** | Complex | Simple & reliable |
| **Hardware Tested** | Unknown | ✅ Confirmed working |
| **CLI** | Limited | Full API access |
| **Library** | No | Yes |
| **Open Source** | No | Yes (MIT) |

---

## 🧪 Hardware Testing

PCG Tools has been extensively tested on **Korg Kronos 2 hardware**:

✅ **Setlist name editing** - Works perfectly
✅ **Slot name editing** - Works perfectly  
✅ **Color changes** - Display correctly on hardware
✅ **Text size changes** - Display correctly on hardware
✅ **Transpose settings** - Function correctly
✅ **Volume settings** - Function correctly
✅ **Program/Combi editing** - Works correctly
✅ **File integrity** - Files load without errors
✅ **GM2 Banks** - Display correctly (read-only)

**Test files created and verified on actual Korg Kronos 2 hardware.**

**Note:** Testing performed on Kronos 2. Should work on original Kronos and Kronos X, but not yet verified.

---

## 📁 Project Structure

```
korg_pcg_tools/
├── README.md                    # This file
├── INSTALL.md                   # Installation guide
├── USAGE.md                     # Usage guide
├── GM2_BANKS_REFERENCE.md       # GM2 banks reference
│
├── pcg_tools/                   # Main package
│   ├── models.py                # Data structures
│   ├── pcg_parser.py            # PCG file parser
│   ├── reader.py                # PCG file reader
│   ├── writer.py                # PCG file writer (hardware-tested)
│   ├── gui_qt.py                # Qt-based GUI
│   ├── gm2_data.py              # GM2 bank definitions
│   ├── cli.py                   # Command-line interface
│   ├── bit_utils.py             # Binary utilities
│   └── ...
│
├── docs/                        # Additional documentation
├── examples/                    # Usage examples
└── test_files/                  # Test PCG files
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.

---

## ⚠️ IMPORTANT: Safe Workflow for Kronos

**The Kronos uses an internal SSD. Always test edited files on USB before copying to internal storage!**

### Recommended Workflow:
1. **Export** PCG from Kronos internal SSD to USB drive
2. **Copy** USB file to your computer
3. **Edit** the copy with PCG Tools
4. **Save** edited file to USB drive
5. **Test** load on Kronos from USB drive
6. **Only if successful**, copy to internal SSD
7. **Keep** USB backup!

### Why This Matters:
- Internal SSD corruption requires factory initialization
- Cannot easily recover from internal storage corruption
- Testing on USB first prevents potential boot issues
- Always keep backups on external storage

---

## 🐛 Troubleshooting

### Qt GUI Won't Launch
```bash
# Check Python installation
python3 --version

# Check PySide6
python3 -c "import PySide6; print('PySide6 OK')"
```

If PySide6 is missing:
```bash
pip install PySide6
```

### File Won't Open
- Verify file is a valid PCG format
- Check file isn't corrupted
- Try with a different file
- Check file permissions

### File Won't Load on Kronos 2
- Verify file was saved successfully
- Check file size matches original
- Test on USB drive first before copying to internal SSD
- If issues persist, please report with your PCG file

### GM2 Banks Not Showing
- GM2 banks are automatically added when opening any PCG file
- Scroll down in the Programs bank list to see g(1) through g(9) and g(d)
- Look for [ROM] indicator next to bank names

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for more details.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Enhancement
- Complete GM2 program names (currently 92 of 1,280 named)
- Undo/redo functionality
- Timbre editing in GUI
- Additional export formats
- More automation examples
- Hardware testing on original Kronos and Kronos X

### Development
```bash
git clone https://github.com/brianmslater/korg_pcg_tools.git
cd korg_pcg_tools
pip install -r requirements.txt
python3 -m pcg_tools.gui_qt
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

Inspired by the original PCG Tools by Michel Keijzers.

---

## 🙏 Acknowledgments

- **Michel Keijzers** - Original PCG Tools
- **Korg** - For creating amazing synthesizers
- **Python Community** - For excellent tools

---

## 📞 Support

For help:
1. Check [USAGE.md](USAGE.md) for GUI and CLI usage
2. See [GM2_BANKS_REFERENCE.md](GM2_BANKS_REFERENCE.md) for GM2 banks info
3. Review [INSTALL.md](INSTALL.md) for installation issues
4. Check [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for limitations
5. See [QUICKSTART.md](QUICKSTART.md) for quick start guide
6. Open an issue on GitHub for bugs or questions

---

## 🎊 Status

**Version:** 1.4.0 "GM2 Banks"  
**Date:** December 2, 2025  
**Status:** ✅ Production Ready - Feature Parity Achieved!  
**Hardware Tested:** ✅ Korg Kronos 2  
**GUI:** Qt-based (PySide6) - Legacy tkinter editors removed  
**New:** ✅ GM2 Banks Support (10 banks, 1,280 programs)  

---

**Made with ❤️ and Python**

*Cross-platform Korg PCG file editing for everyone!*
