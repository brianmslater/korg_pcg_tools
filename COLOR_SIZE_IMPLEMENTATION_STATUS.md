# Color and Text Size Implementation Status

## Completed ✅

### 1. Data Models
- Added `color: int` field to `SetListSlot`
- Added `text_size: int` field to `SetListSlot`
- Added `color_name` property for human-readable color names
- Added `text_size_name` property for human-readable size names
- Created `SlotTextSize` enum (partial)
- Created `SLOT_COLORS` and `SLOT_COLOR_VALUES` mappings (partial)

### 2. Parser (Reader)
- Implemented `parse_stl1_chunk()` method in `PcgBinaryParser`
- Reads complete setlist data from STL1/SBK1 chunk
- Extracts color from byte +24 of slot name
- Extracts text_size from byte +29 of slot name
- Successfully tested with real PCG files
- Correctly reads "Movie and TV Themes" setlist with metadata

### 3. Testing
- Created `test_color_size_reading.py` - tests reading from PCG files
- Created `test_direct_stl1_read.py` - direct binary reading test
- Verified color and text_size values are correctly read

## Confirmed Values

From test files:
- **Indigo** = 32 (0x20) ✓
- **Burgundy** = 140 (0x8C) or 204 (0xCC) - needs clarification
- **M (Medium)** = 0 (0x00) ✓
- **XL (Extra Large)** = 16 (0x10) ✓

## In Progress ⏳

### Writer Implementation
The writer needs to:
1. Update STL1/SBK1 chunk with new color/text_size values
2. Maintain the 542-byte slot structure
3. Preserve notes/description text
4. Handle variable-length slot data

**Status**: Not yet implemented
**Complexity**: High - requires careful binary structure handling
**Priority**: High

### GUI Updates
The GUI needs to:
1. Display color visually in slot list
2. Add color picker/dropdown in slot editor
3. Add text size selector (XS/S/M/L/XL)
4. Show current values when editing slots

**Status**: Not yet implemented
**Priority**: Medium

## TODO - Requires User Action

### Create Test Files
Need PCG files to complete the value mappings:

1. **TEXT_SIZE_TEST.PCG** - One slot for each size (XS, S, M, L, XL)
2. **COLOR_TEST.PCG** - One slot for each available color

See `TODO_CREATE_TEST_FILES.md` for detailed instructions.

## Known Issues

1. **Multiple Setlist Formats**: Files can have both SLD1 and SLS1 chunks with different setlist data. Currently prioritizing STL1/SBK1 as authoritative source.

2. **Slot Size Calculation**: Using fixed 542-byte offset between slots. This works but may need refinement for files with very long notes/descriptions.

3. **Incomplete Mappings**: Only have 2-4 confirmed color values and 2 confirmed text size values. Need test files to complete mappings.

## File Structure Reference

```
PCG File
├── SLD1 (Setlist Data - names only, fast loading)
│   └── SDB1 (Set Data Bank)
│       ├── Setlist name (24 bytes)
│       └── Slot names (128 × 28 bytes with markers)
│
└── STL1 (Setlist Data - complete with metadata)
    └── SBK1 (Set Bank)
        ├── Header (16 bytes)
        ├── Setlist name (24 bytes)
        └── Slots (128 × ~542 bytes)
            ├── Slot name (24 bytes)
            ├── +24: Color (1 byte)
            ├── +29: Text Size (1 byte)
            └── Notes/description (variable length)
```

## Next Steps

1. **Complete Value Mappings** - Create test files and run analysis
2. **Implement Writer** - Update STL1/SBK1 chunk when saving
3. **Update GUI** - Add color/size controls to slot editor
4. **Testing** - Verify round-trip (read → modify → write → read)
5. **Documentation** - Update user docs with color/size features

## Testing Commands

```bash
# Test reading color/size from file
python3 test_color_size_reading.py

# Direct binary test
python3 test_direct_stl1_read.py

# Analyze specific file
python3 decode_sbk1_metadata.py
```

## References

- `COLOR_SIZE_METADATA_FOUND.md` - Initial discovery documentation
- `TODO_CREATE_TEST_FILES.md` - Instructions for creating test files
- `pcg_tools/models.py` - Data model definitions
- `pcg_tools/pcg_parser.py` - Parser implementation
