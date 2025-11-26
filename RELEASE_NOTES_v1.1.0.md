# Release Notes - PCG Tools Python v1.1.0

**Release Date**: November 26, 2025  
**Status**: Production Ready  
**Hardware Tested**: ✅ Korg Kronos

---

## 🎉 What's New

### Simple Setlist Editor - The Star Feature!

We're excited to introduce the **Simple Setlist Editor** - a clean, reliable GUI for editing PCG setlists that has been **hardware-tested and confirmed working on Korg Kronos**!

**Why This Matters**: Unlike other tools that can corrupt files, the Simple Setlist Editor uses a proven writer implementation that preserves file integrity. Every feature has been tested on actual hardware.

### Key Features

#### Setlist Editing
- ✅ Edit all 16 setlist names
- ✅ Edit all 128 slots per setlist
- ✅ Change slot names (24 characters max)
- ✅ Select from 16 official Kronos colors
- ✅ Adjust text sizes (XS, S, M, L, XL)
- ✅ Set transpose (-24 to +24 semitones)
- ✅ Adjust volume (0-127)
- ✅ Add notes/descriptions to slots

#### User Experience
- ✅ Recent files list (last 10 files)
- ✅ Window position/size memory
- ✅ Unsaved changes warning
- ✅ Keyboard shortcuts (Ctrl+O, Ctrl+S, etc.)
- ✅ Right-click context menu
- ✅ Slot usage counter
- ✅ Clean, intuitive interface

---

## 🚀 Quick Start

### Installation

```bash
cd korg_pcg_tools
pip install -r requirements.txt
```

### Launch Simple Setlist Editor

```bash
./edit-setlists
```

Or:

```bash
python3 simple_setlist_editor.py
```

### Basic Usage

1. **Open a file**: Click "Browse..." or press Ctrl+O
2. **Select setlist**: Choose from dropdown
3. **Edit setlist name**: Click "Edit Setlist Name"
4. **Edit slots**: Double-click any slot
5. **Save**: Click "Save File" or press Ctrl+S
6. **Test on Kronos**: Copy to USB and load - it works! ✅

---

## 🔧 What's Fixed

### Hardware-Tested Writer
- **Fixed PCG writer** that was breaking files
- **SLS1-only updates** confirmed working on Kronos
- **File integrity preserved** - no corruption
- **All changes persist** across save/load cycles

### Repository Cleanup
- **205 files organized** into archive/ and dev_notes/
- **Clean structure** ready for public release
- **Professional layout** with proper documentation

---

## 📚 Documentation

### New Guides
- **SIMPLE_EDITOR_GUIDE.md** - Complete setlist editor guide
- **FEATURE_COMPARISON.md** - Comparison with C# version
- **PROJECT_STRUCTURE.md** - Repository organization
- **RELEASE_CHECKLIST.md** - Pre-release verification

### Updated Guides
- **README.md** - Reflects current features
- **QUICKSTART.md** - Simple Editor tutorial
- **CHANGELOG.md** - Complete version history

---

## ⚠️ Known Limitations

### Not Yet Implemented
The Python version focuses on **reliability** over feature completeness. Some features from the C# version are not yet available:

- ❌ Program/Combi editing GUI
- ❌ Copy/paste operations
- ❌ Timbre editing
- ❌ Batch operations (sort, compact)
- ❌ Program reference editing

**Recommendation**: Use the C# version for these features, and the Python version for setlist editing.

See [FEATURE_COMPARISON.md](FEATURE_COMPARISON.md) for complete details.

---

## 🎯 Use Cases

### When to Use Python Version
- ✅ Editing setlist names
- ✅ Editing slot properties
- ✅ Command-line automation
- ✅ Report generation
- ✅ Cross-platform needs
- ✅ When you need reliable file writing

### When to Use C# Version
- Program/Combi editing
- Copy/paste operations
- Timbre management
- Batch operations

---

## 💻 Platform Support

### Tested Platforms
- ✅ **macOS** - Fully working
- ✅ **Windows** - Should work (not hardware tested)
- ✅ **Linux** - Should work (not hardware tested)

### Requirements
- Python 3.7 or higher
- tkinter (usually included)
- click (for CLI)

See [INSTALL.md](INSTALL.md) for platform-specific instructions.

---

## 🔬 Hardware Testing

All features have been tested on **Korg Kronos hardware**:

| Feature | Status |
|---------|--------|
| Setlist name editing | ✅ Works perfectly |
| Slot name editing | ✅ Works perfectly |
| Color changes | ✅ Display correctly |
| Text size changes | ✅ Display correctly |
| Transpose settings | ✅ Function correctly |
| Volume settings | ✅ Function correctly |
| File integrity | ✅ No corruption |

**Test files created and verified on actual Kronos hardware.**

---

## 📦 What's Included

### Applications
- `simple_setlist_editor.py` - Setlist editor GUI
- `edit-setlists` - Quick launcher script
- `pcg-tools` - CLI launcher

### Command-Line Tools
- `info` - Display file information
- `list-patches` - List all patches
- `export` - Export to CSV/TXT
- `program-usage` - Usage reports
- `combi-content` - Content reports
- `differences` - Compare files

### Documentation
- Complete user guides
- Installation instructions
- Quick reference cards
- Technical documentation
- Feature comparison

---

## 🐛 Bug Reports

Found a bug? Please report it!

1. Check [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
2. Search existing GitHub issues
3. Create a new issue with:
   - PCG file details (model, OS version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages (if any)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Priority Areas
1. Program/Combi editing GUI
2. Copy/paste operations
3. Batch operations
4. More examples

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

Inspired by the original PCG Tools by Michel Keijzers.

---

## 🙏 Acknowledgments

- **Michel Keijzers** - Original PCG Tools (C# version)
- **Korg** - For creating amazing synthesizers
- **Hardware testers** - For confirming it works!
- **Python community** - For excellent tools

---

## 📞 Support

Need help?

1. Read [SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md)
2. Check [QUICKSTART.md](QUICKSTART.md)
3. Review [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
4. Open a GitHub issue

---

## 🎊 What's Next?

See [CHANGELOG.md](CHANGELOG.md) for the roadmap.

**High priority features:**
- Program/Combi editing GUI
- Copy/paste operations
- Batch operations
- Program reference editing

---

**Enjoy editing your setlists!** 🎹

The Simple Setlist Editor is ready for daily use and has been confirmed working on Korg Kronos hardware. Give it a try and let us know what you think!
