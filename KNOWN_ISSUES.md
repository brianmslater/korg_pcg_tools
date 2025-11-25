# Known Issues

## PCG Writer - FIXED! ✅

**Status**: ✅ WORKING ON HARDWARE (November 25, 2025)

The PCG writer now successfully saves modified files that load on Kronos hardware!

**The Fix**:
- Update ONLY SLS1 chunk (new format)
- Leave SBK1 chunk (old format) unchanged
- Kronos accepts mismatched SLS1/SBK1 names

**What Works**:
- ✅ Setlist name editing
- ✅ Files load on Kronos hardware
- ✅ Names display correctly
- ✅ All slots remain functional

**Technical Details**:
Changing the SBK1 chunk breaks hidden file validation (checksum/CRC/references). The solution is to only update SLS1, which is what the parser reads. The Kronos accepts files with mismatched names between formats.

See `SOLUTION_CONFIRMED.md` and `WRITER_WORKING.md` for complete details.

## Set List Support

**Status**: ✅ FULLY FUNCTIONAL

Set list parsing and editing are now completely working!

**What Works**:
- ✅ Set list names parse and can be edited/saved
- ✅ Slot names parse and can be edited/saved
- ✅ All 16 setlists with 128 slots each are supported
- ✅ All changes persist across file save/load cycles
- ✅ Tested with multiple PCG file formats

**Binary Structure (NEW Format)**:
```
SLS1 Chunk Structure (Kronos format):
- Marker: 0x1E 0x02 0x00 0x00
- Setlist name (24 bytes, null-terminated)
- Separator: 0x28 0x0F 0x01 0x00
- First slot name (24 bytes, no marker)
- Remaining 127 slots, each with:
  * Marker: 0x1E 0x02 0x00 0x00
  * Slot name (24 bytes, null-terminated)

Total: 16 setlists × 128 slots = 2048 slots
Spacing: 28 bytes per slot (marker + name)
```

**Features**:
- View all setlists and their slots
- Edit setlist names (24 characters max)
- Edit slot names (24 characters max)
- All changes save to PCG files
- Works with both sparse and full setlists

## Set List Colors (SLS1/SLD1 Format)

**Status**: ⚠️ PARTIALLY SUPPORTED

**What Works**:
- ✅ STL1 format: Full color and text size support
- ✅ All 16 official Kronos colors mapped
- ✅ Color display in GUI with visual indicators

**What's Missing**:
- ❌ SLS1/SLD1 format: Color data not yet parsed
- ❌ SDB1 chunk structure not fully reverse-engineered

**Details**:
The SLS1/SLD1 format (internal 16 setlists) stores color data in the SDB1 chunk, but the structure hasn't been fully documented. Colors ARE present in the file (confirmed by Kronos displaying them), but we need the original PCG Tools documentation to understand the SDB1 format.

**Workaround**:
- Use STL1 format (single setlist export) for full color support
- Export individual setlists from Kronos to get colors
- See `SDB1_COLOR_TODO.md` for technical details

**References**:
- `SLS1_COLOR_INVESTIGATION.md` - Investigation notes
- `SDB1_COLOR_TODO.md` - Implementation plan

## Recommendation

PCG Tools now supports:
- ✅ Viewing and editing Programs
- ✅ Viewing and editing Combis  
- ✅ Viewing and managing Set Lists (all 16 setlists)
- ✅ Set list colors (STL1 format only)
- ⚠️ Set list colors (SLS1 format - needs SDB1 documentation)
- ✅ Copying/pasting patches
- ✅ Organizing banks
- ✅ Exporting patch lists
