# Feature Comparison: C# vs Python Version

This document compares features between the original C# PCG Tools and the Python port.

## Legend
- ✅ **Implemented** - Feature is fully working
- ⚠️ **Partial** - Feature is partially implemented
- ❌ **Missing** - Feature not yet implemented
- 🚫 **Not Planned** - Feature intentionally not included

---

## Core File Operations

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| Open PCG files | ✅ | ✅ | |
| Save PCG files | ✅ | ✅ | Hardware-tested writer |
| Save As | ✅ | ✅ | |
| Revert to Saved | ✅ | ❌ | |
| Multiple windows | ✅ | ❌ | Single window in Simple Editor |
| Auto-backup | ✅ | ❌ | |
| Master files | ✅ | ❌ | For categories without global chunk |

---

## Supported Models

| Model | C# | Python | Notes |
|-------|----|----|-------|
| Korg Kronos/Kronos X | ✅ | ✅ | All OS versions |
| Korg Oasys | ✅ | ✅ | |
| Korg M3/M50 | ✅ | ✅ | |
| Korg Triton (all) | ✅ | ✅ | |
| Korg Karma | ✅ | ✅ | |
| Korg Krome/Krome EX | ✅ | ✅ | |
| Korg Kross/Kross 2 | ✅ | ✅ | |
| Korg Trinity | ✅ | ✅ | |
| Korg microStation | ✅ | ❌ | |
| Korg microKORG | ✅ | ❌ | .syx files |
| Korg MS2000 | ✅ | ❌ | .syx files |
| Korg M1/M1R | ✅ | ❌ | .syx files |
| Korg 01/W | ✅ | ❌ | .syx files |
| Korg T1/T2/T3 | ✅ | ❌ | .syx files |
| Korg Z1 | ✅ | ❌ | .syx files |
| Korg Wavestation | ✅ | ❌ | .syx files |

---

## Program/Combi Editing

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| View programs | ✅ | ✅ | CLI only |
| View combis | ✅ | ✅ | CLI only |
| Edit program names | ✅ | ❌ | |
| Edit combi names | ✅ | ❌ | |
| Edit categories | ✅ | ❌ | |
| Edit sub-categories | ✅ | ❌ | |
| Mark as favorite | ✅ | ❌ | |
| Copy programs | ✅ | ❌ | |
| Cut programs | ✅ | ❌ | |
| Paste programs | ✅ | ❌ | |
| Move up/down | ✅ | ❌ | |
| Clear patches | ✅ | ❌ | |
| Compact banks | ✅ | ❌ | |
| Sort patches | ✅ | ❌ | |
| Remove duplicates | ✅ | ❌ | |
| Capitalize names | ✅ | ❌ | |

---

## Setlist Editing

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| View setlists | ✅ | ✅ | All 16 setlists |
| Edit setlist names | ✅ | ✅ | **Hardware-tested** |
| Edit slot names | ✅ | ✅ | **Hardware-tested** |
| Edit slot colors | ✅ | ✅ | **Hardware-tested** |
| Edit slot text size | ✅ | ✅ | **Hardware-tested** |
| Edit slot transpose | ✅ | ✅ | **Hardware-tested** |
| Edit slot volume | ✅ | ✅ | **Hardware-tested** |
| Edit slot descriptions/notes | ✅ | ✅ | **Hardware-tested** |
| Assign program to slot | ✅ | ❌ | |
| Auto-fill slots | ✅ | ❌ | |
| Copy slots | ✅ | ❌ | |
| Move slots up/down | ✅ | ❌ | |
| Clear slots | ✅ | ✅ | In Simple Editor |
| Sort slots | ✅ | ❌ | |

---

## Combi Timbre Editing

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| View timbres | ✅ | ❌ | |
| Edit timbre settings | ✅ | ❌ | |
| Move timbres up/down | ✅ | ❌ | |
| Clear timbres | ✅ | ❌ | |
| Sort timbres | ✅ | ❌ | |
| Clear unused timbres | ✅ | ❌ | |

---

## List Generation / Reports

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| Patch list | ✅ | ✅ | CSV/TXT export |
| Program usage list | ✅ | ✅ | Shows combi usage |
| Combi content list | ✅ | ✅ | Shows timbre details |
| Differences list | ✅ | ✅ | Compare two files |
| File content list | ✅ | ❌ | Bank usage summary |
| Drum kit list | ✅ | ❌ | |
| Wave sequence list | ✅ | ❌ | |
| Sample list (SNG) | ✅ | ❌ | |
| ASCII table format | ✅ | ❌ | |
| CSV format | ✅ | ✅ | |
| XML format | ✅ | ❌ | |
| Cubase instrument def | ✅ | ❌ | |

---

## User Interface Features

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| GUI application | ✅ | ✅ | Simple Setlist Editor |
| Command-line interface | ⚠️ | ✅ | Python has full CLI |
| Multiple languages | ✅ | ❌ | 15+ languages in C# |
| Recent files | ❌ | ✅ | In Simple Editor |
| Window position memory | ✅ | ✅ | In Simple Editor |
| Unsaved changes warning | ✅ | ✅ | In Simple Editor |
| Keyboard shortcuts | ✅ | ✅ | In Simple Editor |
| Context menu | ✅ | ✅ | In Simple Editor |
| Status bar | ✅ | ✅ | In Simple Editor |
| Drag and drop | ❌ | ❌ | |

---

## Advanced Features

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| Program reference changer | ✅ | ❌ | Change combi/setlist refs |
| Virtual banks | ✅ | ❌ | Kronos only |
| Show reference counts | ✅ | ❌ | |
| Filter by text | ✅ | ❌ | |
| Filter by favorite | ✅ | ❌ | |
| Filter by category | ✅ | ❌ | |
| CRC values | ✅ | ❌ | For patch comparison |
| Change volumes (batch) | ✅ | ❌ | |

---

## SNG File Support

| Feature | C# | Python | Notes |
|---------|----|----|-------|
| Open SNG files | ✅ | ❌ | Song files |
| View song names | ✅ | ❌ | |
| View samples used | ✅ | ❌ | |

---

## Summary by Category

### ✅ **Python Strengths**
- **Hardware-tested setlist editing** - Confirmed working on Kronos
- **Simple, reliable interface** - Easy to use
- **Full CLI API** - Complete command-line access
- **Cross-platform** - Works on Windows, macOS, Linux
- **Modern Python** - Easy to extend and maintain
- **Recent files** - Quick access to last 10 files
- **Window memory** - Remembers position/size

### ❌ **Python Missing (High Priority)**
- **Program/Combi editing GUI** - No GUI for editing patches
- **Copy/Paste operations** - Can't copy patches between files
- **Timbre editing** - No combi timbre management
- **Batch operations** - No sort, compact, remove duplicates
- **Program reference editing** - Can't change what slots point to

### ❌ **Python Missing (Medium Priority)**
- **Multiple windows** - Only one file at a time in GUI
- **Master files** - For categories without global chunk
- **Auto-backup** - No automatic file backup
- **Revert to saved** - No undo functionality
- **More export formats** - No XML, ASCII table, Cubase

### ❌ **Python Missing (Low Priority)**
- **Multi-language support** - English only
- **SNG file support** - Song files not supported
- **Legacy model support** - No .syx file support
- **Virtual banks** - Kronos feature not implemented

---

## Recommendations

### For Immediate Use
**Use Python version for:**
- Setlist editing (hardware-tested and working!)
- Command-line automation
- Report generation
- Cross-platform needs

**Use C# version for:**
- Program/Combi editing
- Copy/paste operations
- Timbre management
- Batch operations

### Development Priorities
1. **High Priority** - Add program/combi editing to Python GUI
2. **High Priority** - Implement copy/paste operations
3. **Medium Priority** - Add batch operations (sort, compact)
4. **Medium Priority** - Implement program reference editing
5. **Low Priority** - Add more export formats

---

## Version Information

- **C# Version**: 3.1.0 (August 2019)
- **Python Version**: 1.1.0 (November 2025)
- **Comparison Date**: November 26, 2025

---

## Notes

The Python version focuses on **reliability and hardware compatibility** rather than feature completeness. The Simple Setlist Editor is the first tool that has been **confirmed to work on actual Kronos hardware** without breaking files.

The C# version has many more features but some users report file corruption issues. The Python version prioritizes working correctly over having every feature.
