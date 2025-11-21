# Known Issues

## Set List Parsing

**Status**: ✅ FIXED

Set list parsing is now fully functional!

**What Works**:
- ✅ Set list names parse correctly
- ✅ Slot names parse correctly
- ✅ Patch references (bank, index) parse correctly
- ✅ Transpose and volume settings parse correctly
- ✅ All 16 setlists with 128 slots each are supported

**Binary Structure Discovered**:
```
SLS1 Chunk Structure:
- First 16 marker entries (1E 02 00 00 + 24-byte name): Setlist names
- Next 2048 entries (16 × 128): Slot names for each setlist
- After each slot name (+24 bytes): 8-byte patch reference data
  - Bytes 0-1: Patch index (little-endian)
  - Byte 2: Bank ID
  - Byte 3: Patch type (0x30=Combi, 0x20=Program)
  - Bytes 4-5: Transpose/Volume
```

**Features**:
- View all setlists and their slots
- See patch references for each slot
- Edit slot notes (GUI feature)
- Export setlist data

## Recommendation

PCG Tools now supports:
- ✅ Viewing and editing Programs
- ✅ Viewing and editing Combis  
- ✅ Viewing and managing Set Lists
- ✅ Copying/pasting patches
- ✅ Organizing banks
- ✅ Exporting patch lists
