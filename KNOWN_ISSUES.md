# Known Issues

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

## Recommendation

PCG Tools now supports:
- ✅ Viewing and editing Programs
- ✅ Viewing and editing Combis  
- ✅ Viewing and managing Set Lists
- ✅ Copying/pasting patches
- ✅ Organizing banks
- ✅ Exporting patch lists
