# Known Issues and Limitations

## Current Status: ✅ All Major Features Working

As of v1.4.x (December 2025), all major editing features are working and hardware-tested on Korg Kronos.

---

## ✅ Fixed Issues (Historical)

### Program/Combi Editing Corrupts Files (FIXED in v1.2.1)
**Status:** ✅ FIXED - Nov 27, 2025

**Root Cause:** PCG files use checksums stored at byte 11 of each chunk header. The Kronos validates these checksums and rejects files with incorrect values.

**Solution:** Created `pcg_tools/checksum.py` with proper checksum calculation. Checksums automatically fixed before writing.

### Program/Combi Editing Crash on macOS (FIXED in v1.2.1)
**Status:** ✅ FIXED

**Root Cause:** The edit dialog used Tkinter, which conflicted with PySide6 (Qt) on macOS.

**Solution:** Replaced Tkinter dialog with native Qt dialog (`qt_edit_dialog.py`).

---

## ⚠️ Known Limitations

### Legacy Synthesizer Support
The following models are NOT supported in the Python version:
- Korg microStation
- Korg microKORG / microKORG XL (.syx files)
- Korg MS2000 (.syx files)
- Korg M1/M1R (.syx files)
- Korg 01/W (.syx files)
- Korg T1/T2/T3 (.syx files)
- Korg Z1 (.syx files)
- Korg Wavestation (.syx files)

**Reason:** These models use SysEx (.syx) file format which requires different parsing logic. The C# version supports these, but they are low priority for the Python port.

### Multi-Language Support
The Python version only supports English. The C# version has 15+ language translations.

**Reason:** Low priority - focus was on feature parity first.

### Drum Pattern Parsing
Drum pattern parsing is not implemented for Kronos.

**Reason:** The C# source code throws `NotImplementedException` for Kronos drum patterns (DPI1 chunks). This feature was never completed in the original C# version.

### Kronos OS 1.5/1.6 Extended Bank Support
Files created with Kronos OS 1.5/1.6 that use extended user banks (U-AA to U-GG) in setlist slots or combi timbres may not correctly resolve patch references.

**Technical Details:** OS 1.5/1.6 uses separate STL2/CBK2/PBK2 chunks to store extended bank references. The Python version only reads from the default offsets.

**Impact:** 
- Setlist slots referencing programs in U-AA to U-GG banks may show wrong patch
- Combi timbres referencing programs in U-AA to U-GG banks may show wrong patch

**Workaround:** Most users are on OS 2.x or 3.x where this isn't an issue. If you have OS 1.5/1.6 files, use the original C# PCG Tools.

**Reason:** OS 1.5/1.6 is a legacy version. Most Kronos users have upgraded to OS 2.x or 3.x.

---

## 🔧 Technical Notes

### PCG File Structure
- Programs: name, id, bank, engine type, favorite, category, sub-category
- Combis: name, id, bank, favorite, category, sub-category, 16 timbres
- Timbres: All 16+ parameters including volume, transpose, key zones, velocity zones
- Setlists: 16 setlists × 128 slots each with full property support
- Drum kits: Parsed and displayed
- Wave sequences: Parsed and displayed

### Checksum Handling
- Checksums automatically calculated and updated on save
- Handles nested chunk structure (SLS1 → STL1 → SBK1)
- INI2/INI3 checksums supported for Kronos OS 1.5+

### Hardware Testing
All editing features have been tested on actual Korg Kronos 2 hardware:
- ✅ Program name editing
- ✅ Combi name editing
- ✅ Setlist name editing
- ✅ Slot property editing (name, color, text size, transpose, volume, description)
- ✅ Timbre parameter editing
- ✅ Copy/paste operations
- ✅ Batch operations (sort, compact, remove duplicates)

---

## 💡 Recommendations

### For All Editing Tasks
✅ Use the Python version - it's fully functional and hardware-tested!

### For Legacy Synthesizers (.syx files)
⚠️ Use the original C# PCG Tools for microKORG, MS2000, M1, etc.

### For Non-English Users
⚠️ The Python version is English-only. Use C# version if you need other languages.

---

## Version History

- **v1.4.x** - Feature parity achieved, all major features working
- **v1.3.0** - SNG file support, advanced features
- **v1.2.x** - Program/combi editing, copy/paste, batch operations
- **v1.1.0** - Setlist editing, CLI tools
- **v1.0.0** - Initial release, read-only support
