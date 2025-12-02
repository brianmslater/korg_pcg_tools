# Known Issues and Limitations

## ✅ Fixed Issues

### Program/Combi Editing Corrupts Files (FIXED in v1.2.1)
**Status:** ✅ FIXED - Nov 27, 2025  
**Was:** Critical bug blocking all editing  
**Fixed:** Implemented checksum calculation

**Root Cause:**
PCG files use checksums stored at byte 11 of each chunk header. The Kronos validates these checksums and rejects files with incorrect values.

**Solution:**
- Created `pcg_tools/checksum.py` with proper checksum calculation
- Checksums automatically fixed before writing
- Handles nested chunk structure (SLS1 → STL1 → SBK1)
- Updates both SLS1 and STL1 for setlist changes

**Hardware Tested and Verified:**
- ✅ Setlist name editing works
- ✅ Program name editing works
- ✅ Combi name editing works
- ✅ All changes appear correctly on Kronos hardware
- ✅ Files load without errors

---

## 🚨 Critical Issues

None currently! All editing features are working.

---

## ✅ Previously Fixed Issues

### Program/Combi Editing Crash on macOS (FIXED in v1.2.1)
**Status:** ✅ FIXED  
**Was:** Crash issue in v1.2.0  
**Fixed:** v1.2.1 with native Qt dialog

**Original Problem:**
The edit dialog used Tkinter, which conflicted with PySide6 (Qt) on macOS, causing crashes.

**Solution:**
Replaced Tkinter dialog with native Qt dialog (`qt_edit_dialog.py`). However, editing is now disabled due to file corruption issue above.

---

## v1.1.0 - What Works and What Doesn't

### ✅ What Works (Hardware Tested)

**Setlist Name Editing:**
- ✅ Edit all 16 setlist names
- ✅ Changes save correctly to PCG files
- ✅ Files load on Kronos hardware
- ✅ Names display correctly on hardware
- ✅ Hardware tested and confirmed working

**CLI Tools (All Working):**
- ✅ `info` - Display file information
- ✅ `export` - Export patches to CSV/TXT
- ✅ `list-patches` - List all programs/combis
- ✅ `program-usage` - Show reference counts and where programs are used
- ✅ `combi-content` - Show which programs each combi uses
- ✅ `differences` - Compare two PCG files

**File Support:**
- ✅ Read PCG files from all Korg models
- ✅ Parse programs, combis, setlists
- ✅ Cross-platform (Windows, macOS, Linux)

### ❌ What Doesn't Work Yet

**Slot Notes/Comments:**
- ❌ Slot notes are not displayed in the GUI
- **Why**: Notes are stored in a complex structure within the SLS1 chunk that hasn't been fully parsed yet
- **Details**: Notes appear after the slot name with metadata bytes in between
- **Status**: Parsing implementation needed - the data exists in the file but requires additional parser work
- **Workaround**: View/edit notes on Kronos hardware or use C# PCG Tools

**Slot Property Editing:**
- ✅ Slot colors now display correctly (v1.2.1+)
- ✅ Slot text size parsed correctly (v1.2.1+)
- ❌ Editing of transpose, volume not yet implemented
- **Note**: Color and text size are read-only in current version

**Program/Combi Editing:**
- ❌ No GUI for editing program/combi names
- ❌ No editing of categories, favorites
- ❌ No editing of program parameters
- ❌ No editing of combi timbres
- **Status**: Planned for v1.2.0

**Advanced Features:**
- ❌ Drum kits not parsed
- ❌ Wave sequences not parsed
- ❌ Copy/paste operations
- ❌ Batch operations (sort, compact, remove duplicates)
- ❌ Multiple windows
- **Status**: Planned for future versions

### ⚠️ Important Notes

**SLS1/SLD1 Format Limitations:**

The internal 16-setlist format (SLS1/SLD1) used by Kronos only stores:
- ✅ Setlist names (24 characters)
- ✅ Slot names (combi names, 24 characters)

It does NOT store:
- ❌ Slot colors
- ❌ Text sizes
- ❌ Transpose settings
- ❌ Volume settings
- ❌ Notes/descriptions

These are performance settings stored on the Kronos hardware itself, not in the PCG file.

**STL1 Format (Single Setlist Export):**

The single setlist export format (STL1) DOES include:
- ✅ Colors
- ✅ Text sizes
- ✅ Transpose
- ✅ Volume
- ✅ Patch references

Support for STL1 format editing is planned for a future version.

### 🔧 Technical Details

**Writer Implementation:**
- Updates ONLY the SLS1 chunk (new format)
- Does NOT modify SBK1 chunk (old format)
- Kronos accepts files with mismatched SLS1/SBK1 names
- Changing SBK1 breaks hidden file validation

**What's Parsed:**
- Programs: name, id, bank, engine, favorite
- Combis: name, id, bank, favorite, timbres (basic)
- Timbres: midi_channel, mute, pan, volume, status, program reference
- Setlists: name, slots with names

**What's NOT Parsed:**
- Full program parameters (oscillators, filters, effects, etc.)
- Full combi parameters
- Full timbre parameters (key zones, velocity zones, transpose, detune, etc.)
- Drum kits
- Wave sequences

### 📋 Roadmap

**v1.2.0 (Future):**
- Program/Combi name editing
- Category/favorite editing
- Full parameter parsing

**v1.3.0 (Future):**
- STL1 format support (with slot properties)
- Copy/paste operations
- Batch operations

**v2.0.0 (Future):**
- Full program/combi parameter editing
- Drum kit support
- Wave sequence support

### 💡 Recommendations

**For Setlist Name Editing:**
- ✅ Use Simple Setlist Editor - works perfectly!

**For Slot Property Editing:**
- ⚠️ Edit directly on Kronos hardware (not stored in PCG file)

**For Program/Combi Editing:**
- ⚠️ Use original C# PCG Tools for now
- ✅ Python version coming in v1.2.0

**For Reports and Analysis:**
- ✅ Use CLI tools - all working great!
