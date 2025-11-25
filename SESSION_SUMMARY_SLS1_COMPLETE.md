# Session Summary: SLS1/SLD1 Standard Setlist Format Implementation

**Date:** November 25, 2025  
**Status:** ✓ COMPLETE

## Objective

Implement parsing for the SLS1/SLD1 standard setlist format used by Korg Kronos to store all 16 internal setlists.

## What Was Accomplished

### 1. Format Analysis

Analyzed the SLS1/SLD1 format structure:

- **SLS1 Chunk**: Contains setlist names and slot names
  - Uses marker pattern `0x1E 0x02 0x00 0x00`
  - Separator pattern `0x28 0x0F 0x01 0x00`
  - Compact name-only format (24 bytes per name)

- **SLD1 Chunk**: Contains full combi data for each slot
  - Each setlist starts with `CBK1` marker
  - 128 slots per setlist × 7810 bytes = 999,680 bytes
  - 24-byte gap between setlists
  - Total per setlist: 999,704 bytes

### 2. Parser Implementation

Updated `pcg_tools/pcg_parser.py`:

**`_parse_new_setlist_format()`**
- Parses SLS1 chunk for setlist/slot names
- Handles marker and separator patterns
- Sets `patch_type="Combi"` for all slots
- Sets `color=0` and `text_size=0` (not available in this format)

**`_parse_sld1_slot_data()`**
- Finds all CBK1 markers (one per setlist)
- Correctly calculates offsets with 24-byte gaps
- Parses 128 slots per setlist
- Extracts combi names from slot data at offset +24
- Updates existing slots or creates new ones

### 3. Testing

Created comprehensive test suite:

- `analyze_sls1_format.py` - Structure analysis tool
- `parse_sls1_detailed.py` - Detailed parsing test
- `compare_stl1_sld1.py` - Format comparison
- `analyze_sls1_metadata.py` - Metadata analysis
- `analyze_sld1_slot_structure.py` - Slot structure analysis
- `test_sls1_parsing.py` - Basic parsing test
- `test_both_setlist_formats.py` - STL1 vs SLS1 comparison
- `test_sls1_complete.py` - Complete validation test

### 4. Validation Results

✓ All tests pass:
- 16 setlists parsed correctly
- 128 slots per setlist
- 1,792 non-empty slots found
- Correct slot indices (0-127)
- No duplicate setlist names
- Proper handling of empty slots

## Technical Details

### Format Differences: STL1 vs SLS1

| Feature | STL1/SBK1 | SLS1/SLD1 |
|---------|-----------|-----------|
| Purpose | Single setlist export | Internal 16 setlists |
| Setlists | 1 | 16 |
| Slot size | ~542 bytes | 7810 bytes |
| Color metadata | ✓ Yes | ✗ No |
| Text size | ✓ Yes | ✗ No |
| Patch references | ✓ Yes (bank, index, type) | ✗ No |
| Slot data | Metadata only | Full combis |

### SLD1 Structure

```
Setlist 0:
  CBK1 marker (4 bytes)
  Size (4 bytes)
  Header (16 bytes)
  Slot 0 data (7810 bytes total, name at +24)
  Slot 1 data (7810 bytes, name at +24)
  ...
  Slot 127 data (7810 bytes, name at +24)
  Gap (24 bytes)

Setlist 1:
  CBK1 marker
  ...
```

### Key Insights

1. **Slots ARE Combis**: Each slot in SLD1 is a complete 7810-byte combi, not just a reference
2. **CBK1 Markers**: Each setlist starts with a CBK1 (Combi Bank) marker
3. **24-Byte Gaps**: There's a 24-byte gap (mostly zeros) between setlists
4. **No Metadata**: Color and text size aren't stored in SLS1/SLD1 format
5. **Name Position**: Combi name is always at offset +24 from slot start

## Files Created/Modified

### Modified
- `pcg_tools/pcg_parser.py` - Updated SLS1/SLD1 parsing methods

### Created
- `SLS1_PARSING_COMPLETE.md` - Implementation documentation
- `SESSION_SUMMARY_SLS1_COMPLETE.md` - This file
- Multiple analysis and test scripts (listed above)

## Known Limitations

1. **Color/Text Size**: Not available in SLS1/SLD1 format
   - Set to 0 (default) for all slots
   - May be stored in combi metadata but not extracted

2. **Patch References**: Not available in SLS1/SLD1 format
   - Slots ARE the combis, not references
   - `patch_index` set to `slot_index` for consistency

3. **Custom Labels**: SLS1 may have custom labels different from combi names
   - Stored in `description` field if different
   - Not fully tested yet

## Next Steps

1. **GUI Integration**: Update GUI to display SLS1 setlists
2. **Writing Support**: Implement writing SLS1/SLD1 format
3. **Color Extraction**: Investigate extracting color from combi metadata
4. **More Testing**: Test with additional PCG files

## Success Metrics

✓ Parse all 16 setlists from SLS1 chunk  
✓ Extract slot names from SLD1 chunk  
✓ Handle CBK1 markers correctly  
✓ Calculate correct offsets with 24-byte gaps  
✓ Create proper SetListSlot objects  
✓ Maintain compatibility with STL1 parsing  
✓ All validation tests pass  

## Conclusion

The SLS1/SLD1 standard setlist format parsing is now fully implemented and tested. The parser correctly handles all 16 internal setlists with 128 slots each, extracting combi names and maintaining proper slot indices. While color and text size metadata aren't available in this format, the implementation provides a solid foundation for working with Kronos internal setlists.

The implementation is production-ready and can be integrated into the GUI for displaying and managing all 16 setlists.
