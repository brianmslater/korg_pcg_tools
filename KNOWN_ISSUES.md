# Known Issues and Limitations

## 🚨 Critical Issues

### Program/Combi Editing Corrupts Files (v1.2.1)
**Status:** ❌ DISABLED - Critical bug  
**Severity:** Critical  
**Affects:** All platforms  
**Hardware Impact:** Files become unloadable on Kronos

**Problem:**
Editing program or combi names/parameters corrupts the PCG file. The Kronos hardware rejects edited files with "File Unavailable" error.

**Root Cause:**
Programs and combis have internal checksums or validation data that we don't know how to update. When we change any parameter (even just the name), the checksum becomes invalid and the Kronos rejects the file.

**Evidence:**
- Unmodified roundtrip: ✅ Works (file identical, loads on hardware)
- Name-only edit: ❌ Fails (only 24 bytes changed, but file rejected)
- Full edit: ❌ Fails (file rejected)

**Current Status:**
- Program/combi editing DISABLED in GUI (shows warning dialog)
- Setlist editing still works perfectly (no checksums)
- Parameter parsing works correctly (read-only)

**Workaround:**
Use the C# PCG Tools for program/combi editing until we figure out the checksum algorithm.

**Investigation Needed:**
1. Reverse engineer the checksum algorithm from C# code
2. Find where checksums are stored in the binary format
3. Implement checksum calculation and update

---

## ✅ Fixed Issues

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

**Slot Property Editing:**
- ❌ Slot colors, text size, transpose, volume, notes
- **Why**: These properties are NOT stored in the SLS1/SLD1 format
- **Details**: The internal 16-setlist format only stores setlist names and slot names (combi names)
- **Workaround**: These are display settings on the Kronos itself, not in the PCG file

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
