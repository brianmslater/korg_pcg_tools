# SLS1/SLD1 Format Parsing - Complete

## Summary

Successfully implemented parsing for the SLS1/SLD1 setlist format used internally by Kronos for storing all 16 setlists.

## Format Details

### SLS1 Chunk (Setlist Names and Slot Names)

The SLS1 chunk contains setlist names and slot names in a compact format:

**Structure:**
- Marker: `0x1E 0x02 0x00 0x00`
- Setlist name (24 bytes, null-terminated)
- Separator: `0x28 0x0F 0x01 0x00`
- Slot 0 name (24 bytes, no marker)
- Slots 1-127: Each with marker `0x1E 0x02 0x00 0x00` + name (24 bytes)

**Key Points:**
- Contains all 16 setlists
- Only stores names, no color/text size metadata
- Compact format with markers and separators

### SLD1 Chunk (Slot Data)

The SLD1 chunk contains the actual slot data as full combis:

**Structure:**
- Each setlist starts with `CBK1` marker
- 128 slots per setlist, each 7810 bytes (0x1E82)
- 24-byte gap between setlists
- Each slot is a complete combi structure
- Combi name at offset +24 from slot start

**Key Points:**
- Slots ARE combis (7810 bytes each)
- No separate color/text size metadata
- Spacing: 128 slots × 7810 bytes + 24 byte gap = 999,704 bytes per setlist

## Implementation

### Parser Methods

1. **`parse_sls1_chunk()`**
   - Entry point for SLS1 parsing
   - Tries NEW format first, falls back to OLD format
   - Calls `_parse_sld1_slot_data()` to get combi names

2. **`_parse_new_setlist_format()`**
   - Parses SLS1 chunk for setlist/slot names
   - Handles marker and separator patterns
   - Creates SetListSlot objects with names

3. **`_parse_sld1_slot_data()`**
   - Finds all CBK1 markers (one per setlist)
   - Parses 128 slots per setlist
   - Extracts combi names from slot data
   - Updates existing slots or creates new ones

### Data Model

**SetListSlot fields for SLS1 format:**
- `name`: Combi name from SLD1
- `description`: Custom label from SLS1 (if different)
- `patch_type`: Always "Combi"
- `patch_index`: Slot index (0-127)
- `color`: 0 (not available in SLS1 format)
- `text_size`: 0 (not available in SLS1 format)

## Comparison: STL1 vs SLS1

| Feature | STL1/SBK1 | SLS1/SLD1 |
|---------|-----------|-----------|
| Setlists | 1 (export) | 16 (internal) |
| Color metadata | ✓ Yes | ✗ No |
| Text size | ✓ Yes | ✗ No |
| Patch references | ✓ Yes | ✗ No |
| Slot data | Metadata only | Full combis |
| Size per slot | ~542 bytes | 7810 bytes |

## Testing

Created comprehensive tests:
- `test_sls1_parsing.py` - Tests SLS1/SLD1 parsing
- `test_both_setlist_formats.py` - Tests both STL1 and SLS1 formats
- `analyze_sls1_format.py` - Analysis tool for SLS1 structure
- `compare_stl1_sld1.py` - Compares both formats

## Files Modified

- `pcg_tools/pcg_parser.py`:
  - Updated `_parse_new_setlist_format()` to set patch_type="Combi"
  - Rewrote `_parse_sld1_slot_data()` to handle CBK1 markers correctly
  - Fixed setlist offset calculation (24-byte gap between setlists)

## Known Limitations

1. **Color and Text Size**: Not available in SLS1/SLD1 format
   - These are set to 0 (default) for all slots
   - May be stored in combi metadata but not currently extracted

2. **Patch References**: Not available in SLS1/SLD1 format
   - Slots ARE the combis, not references to them
   - patch_index is set to slot_index for consistency

3. **Custom Labels**: SLS1 may have custom labels different from combi names
   - Stored in `description` field if different from combi name
   - Not fully tested yet

## Next Steps

1. **Color/Text Size Extraction**: Investigate if these are stored in combi metadata
2. **Writing Support**: Implement writing SLS1/SLD1 format
3. **GUI Integration**: Update GUI to handle both formats
4. **Testing**: Test with more PCG files to verify robustness

## Success Criteria

✓ Parse all 16 setlists from SLS1 chunk
✓ Extract slot names from SLD1 chunk
✓ Handle CBK1 markers correctly
✓ Calculate correct offsets with 24-byte gaps
✓ Create proper SetListSlot objects
✓ Maintain compatibility with STL1 parsing

## Date

November 25, 2025
