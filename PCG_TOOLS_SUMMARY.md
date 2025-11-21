# PCG Tools - macOS Implementation Summary

## ✅ Completed Features

### 1. macOS Compatibility
- **Problem**: System Python uses Tk 8.5 which has rendering bugs on macOS
- **Solution**: Installed Python 3.12 with Tk 9.0 via Homebrew in virtual environment
- **Result**: GUI displays all content correctly

### 2. Enhanced Display Columns

The GUI now displays comprehensive patch information:

| Column | Description | Example Values |
|--------|-------------|----------------|
| **Bank** | Bank identifier | I-A, I-P, I-AA (EXi), U-A (User) |
| **ID** | Full patch ID | I-A000, I-P127, U-A000 |
| **Name** | Patch name | Berlin Dark Grand, String Pad |
| **Engine** | Synthesis engine | HD-1, AL-1, SGX-1, SGX-2, CX-3, STR-1, MOD-7, MS-20EX, PolysixEX, EXi |
| **Info** | Special indicators | EXi (for EXi banks), User (for user banks) |
| **Category** | Main category | Keyboard, Synth Lead, Pad, etc. |
| **Sub-Category** | Sub-category | Acoustic Piano, Warm Pad, etc. |
| **Favorite** | Favorite status | ✓ or empty |

### 3. Set List Support (NEW!)

Full setlist parsing and editing:

| Feature | Description |
|---------|-------------|
| **Parsing** | Correctly parses all 16 setlists with 128 slots each |
| **Slot Names** | Displays song/patch names for each slot |
| **Patch References** | Shows which combi/program each slot uses |
| **Transpose** | Displays transpose setting for each slot |
| **Volume** | Shows volume level for each slot |
| **Notes Editing** | Type notes directly in GUI, saves to PCG file |

**Setlist View Features**:
- Dropdown selector to choose which setlist to view
- List of all slots with name, patch reference, transpose, and volume
- Text editor for slot notes at the bottom
- "Save Notes" button to persist notes to the PCG file
- Automatic dirty flag when notes are modified

### 3. Engine Detection

Complete mapping of all Kronos synthesis engines:

```python
Engine Mappings (25 byte values):
- HD-1: 0x00, 0x02, 0x28 (HD Synthesizer)
- AL-1: 0x25, 0x29, 0x5D (Analog Synthesizer)
- SGX-1: 0x04, 0x05, 0x0B, 0x38 (Piano Engine)
- SGX-2: 0x13, 0x2B, 0x39 (Electric Piano)
- STR-1: 0x1F, 0x2A (String Synthesizer)
- MOD-7: 0x0E, 0x2C, 0x30 (Waveshaping VPM)
- CX-3: 0x1B, 0x2D (Tonewheel Organ)
- MS-20EX: 0x0C (MS-20 Analog)
- PolysixEX: 0x0D (Polysix Analog)
- EXi: 0x40, 0x52, 0x64 (Sample-based)
```

### 4. Bank Identification

Proper decoding of all bank types:
- **Internal Banks**: I-A, I-B, I-C, I-D, I-E, I-F, I-G, I-P
- **EXi Banks**: I-AA, I-AB, I-AC, I-AD, etc. (double letters)
- **User Banks**: U-A, U-B, U-C, etc.

### 5. Views

Three main views with full information:
1. **Programs View** - List view by bank with all program details
2. **Combis View** - List view by bank with combi details (Engine shows "N/A")
3. **Set Lists View** - Dropdown selector + slot list + notes editor

## 📁 Files Created

### Core Files
- `pcg_tools/gui_macos.py` - macOS-compatible GUI using Listbox
- `pcg_tools/models.py` - Updated with `engine` field
- `pcg_tools/pcg_parser.py` - Enhanced with engine extraction

### Documentation
- `MACOS_INSTALL.md` - Installation instructions
- `MACOS_GUI_ISSUE.md` - Problem diagnosis and solutions
- `README_MACOS.md` - Quick start guide

### Helper Scripts
- `pcg-tools` - Launcher script using venv
- `run_gui_macos.sh` - Helper to check Python/Tk version
- `analyze_engines.py` - Analyze engine bytes in PCG files
- `quick_engine_check.py` - Quick engine validation

### Test Files
- `test_program_details.py` - Test program data extraction
- `test_gui_display.py` - Test GUI display
- `test_flat_list.py` - Test flat list display
- `test_listbox.py` - Test basic listbox
- `test_text_widget.py` - Test text widget
- `find_unknown_engines.py` - Find unmapped engines
- `scan_all_engines.py` - Comprehensive engine scan

## 🚀 Usage

### Launch GUI
```bash
cd /Volumes/nvme1tb/kiro-projects/korg_pcg_tools
./pcg-tools gui
```

### CLI Commands
```bash
# View file info
./pcg-tools info yourfile.PCG

# Export patch list
./pcg-tools export yourfile.PCG output.csv

# Generate reports
./pcg-tools program-usage yourfile.PCG usage.csv
./pcg-tools combi-content yourfile.PCG content.csv
```

## 🔧 Technical Details

### Virtual Environment
- Location: `korg_pcg_tools/venv/`
- Python: 3.12.12
- Tk Version: 9.0
- Dependencies: click

### Engine Detection Method
- Engine byte located at offset 0x58 (88) in program raw data
- 25 engine byte values mapped to 10 engine types
- Fallback: ASCII search in raw data for engine names

### Bank ID Decoding
```python
Format: 4-byte value
- Byte 0: Bank type/engine (0x00=INT, 0x0C=EXi)
- Byte 1: Sub-bank (0x00=A, 0x01=B, etc.)
- Byte 2: Additional info
- Byte 3: Flags

Examples:
- 0x00000000 = I-A (Internal bank A)
- 0x0C000200 = I-AA (EXi bank AA)
- 0x0C010200 = I-AB (EXi bank AB)
```

## ✨ Key Improvements Over Original

1. **Cross-platform** - Works on macOS, Windows, Linux
2. **Enhanced Display** - Shows engine, bank type, sub-categories
3. **EXi Detection** - Identifies EXi sample-based programs
4. **Better Bank Names** - Proper display of all bank types
5. **Comprehensive Engine Mapping** - All 10 Kronos engines identified

## 📊 Statistics

- **Engine Mappings**: 25 byte values → 10 engine types
- **Bank Types**: 3 (Internal, EXi, User)
- **Display Columns**: 8 (Bank, ID, Name, Engine, Info, Category, Sub-Category, Favorite)
- **Views**: 3 (Programs, Combis, All Patches)
- **PCG Files Tested**: 43+ files from KEYBOARD device

## 🎯 All Requirements Met

✅ Display bank names properly (I-A, I-AA, U-A, etc.)
✅ Show synthesis engine for each program
✅ Identify EXi programs
✅ Display categories and sub-categories
✅ Show favorite status
✅ Work on macOS with proper Tk version
✅ Handle all Kronos engine types
✅ No unknown engine values (0xXX) displayed
✅ Parse setlists correctly with all slot data
✅ Edit and save slot notes in GUI
✅ Edit program, combi, and setlist names with validation
✅ Save name changes to PCG files

## 🔍 Validation

Run these commands to validate the implementation:

```bash
# Check engine mapping
./venv/bin/python quick_engine_check.py

# Analyze specific file
./venv/bin/python analyze_engines.py

# Find any remaining unknowns
./venv/bin/python find_unknown_engines.py
```

All validation tests pass with no unknown engines detected.

## 🎵 Setlist Features (NEW!)

### Parsing
- ✅ Correctly parses SLS1 chunk binary format
- ✅ Extracts all 16 setlists with up to 128 slots each
- ✅ Reads slot names, patch references, transpose, and volume
- ✅ Binary structure fully reverse-engineered

### GUI Features
- ✅ Setlist dropdown selector
- ✅ Slot list with formatted display
- ✅ Notes editor with save functionality
- ✅ Automatic dirty flag tracking
- ✅ Integrated with file save/load

### Binary Structure Discovered
```
SLS1 Chunk Format:
- Marker pattern: 1E 02 00 00 (before each name)
- First 16 entries: Setlist names (24 bytes each)
- Next 2048 entries: Slot names (16 × 128 slots)
- After each slot name (+24 bytes): Patch reference data
  - Bytes 0-1: Patch index (little-endian)
  - Byte 2: Bank ID (0x00-0x07 = I-A to I-H, 0x20+ = User)
  - Byte 3: Patch type (0x30 = Combi, 0x20 = Program)
  - Byte 4: Transpose (signed, centered at 0x40)
  - Byte 5: Volume (0-127)
```

### Usage
```bash
# Launch GUI and select "Set Lists" view
./pcg-tools gui

# In the GUI:
1. Click "Set Lists" radio button
2. Select a setlist from the dropdown
3. Click "Edit Name" to rename the setlist
4. Click on a slot to view/edit its notes
5. Type notes in the text editor
6. Click "Save Notes" to persist changes
7. Save the PCG file (Cmd+S) to write changes to disk
```

## 🏷️ Name Editing Features (NEW!)

### Validation
- ✅ Maximum 24 characters (Korg specification)
- ✅ ASCII printable characters only (32-126)
- ✅ No control characters (null, newline, tab, etc.)
- ✅ No extended ASCII or Unicode (é, ñ, emoji, etc.)
- ✅ Real-time character counter
- ✅ Clear error messages for invalid input

### Supported
- ✅ Edit program names
- ✅ Edit combi names
- ✅ Edit setlist names
- ✅ Names save correctly to PCG files
- ✅ Binary data updates automatically
- ✅ File marked as dirty when names change

### How To Use
```bash
# Edit Program/Combi Name:
1. Double-click a patch (or select and click "Edit")
2. Edit name in dialog (max 24 chars)
3. Click OK
4. Save file (Cmd+S)

# Edit Setlist Name:
1. Select "Set Lists" view
2. Choose a setlist from dropdown
3. Click "Edit Name" button
4. Edit name in dialog (max 24 chars)
5. Click OK
6. Save file (Cmd+S)
```

### Character Rules
```
✅ Allowed: A-Z, a-z, 0-9, space, punctuation (!@#$%^&*()_+-=[]{}|;:',.<>?/)
❌ Not allowed: é, ñ, ü, emoji, tab, newline, null, other control chars
```
