# Deep Analysis Findings - PCG Writer Issue

## Critical Discovery

**ALL setlist names appear in EXACTLY 2 locations in the file**, not 4 as previously thought.

## Pattern Analysis

### Location 1: SLS1 Chunk (New Format)
- Each setlist name appears with the marker pattern `1E 02 00 00`
- Followed by 24-byte setlist name
- Followed by separator `28 0F 01 00`
- Followed by 128 slot names (24 bytes each)

**Spacing between setlists in SLS1:**
- Setlist 0 → 1: 3,612 bytes (0xE1C)
- Setlist 1 → 2: 3,612 bytes (0xE1C)
- Setlist 2 → 3: 3,612 bytes (0xE1C)
- **CONSISTENT: 3,612 bytes per setlist**

### Location 2: SBK1 Chunk (Old Format)
- Each setlist name appears at fixed intervals
- Spacing: 69,416 bytes (0x10F08) per setlist
- After a 69,432 byte header

**Offsets in SBK1 (chunk-relative):**
- Setlist 0: 601,187 (0x92C63)
- Setlist 1: 670,603 (0xA3B8B) - difference: 69,416
- Setlist 2: 740,019 (0xB4AB3) - difference: 69,416
- **CONSISTENT: 69,416 bytes per setlist**

## Structure Details

### SLS1 Format (3,612 bytes per setlist)
```
Offset  Size  Description
------  ----  -----------
-28     28    Previous setlist padding/marker
-4      4     Marker: 1E 02 00 00
0       24    Setlist name (null-padded)
24      4     Separator: 28 0F 01 00
28      3072  128 slot names × 24 bytes each
3100    512   Metadata/padding
```

### SBK1 Format (69,416 bytes per setlist)
```
Offset  Size   Description
------  -----  -----------
0       24     Setlist name (null-padded)
24      69392  Setlist data (slots, metadata, etc.)
```

## The Problem

**Our writer only updates SBK1, not SLS1!**

When we write a setlist name:
1. ✅ We update SBK1 (old format) correctly
2. ❌ We DON'T update SLS1 (new format)
3. ❌ Kronos reads from SLS1 first (new format takes precedence)
4. ❌ File is rejected due to inconsistency

## The Solution

We need to update BOTH locations:

### 1. Update SLS1 (New Format)
```python
def _update_sls1_setlist_name(self, raw_data, setlist_index, new_name):
    """Update setlist name in SLS1 chunk."""
    # Find SLS1 chunk
    sls1_offset = self._find_chunk(raw_data, b'SLS1')
    if not sls1_offset:
        return raw_data
    
    # Calculate position in SLS1
    # First setlist starts at chunk_data + some offset
    # Each setlist is 3,612 bytes apart
    setlist_offset = BASE_OFFSET + (setlist_index * 3612)
    
    # Find marker (1E 02 00 00)
    # Name is 4 bytes after marker
    name_offset = sls1_offset + 8 + setlist_offset + 4
    
    # Write 24-byte name
    name_bytes = new_name.encode('ascii').ljust(24, b'\x00')
    raw_data = raw_data[:name_offset] + name_bytes + raw_data[name_offset+24:]
    
    return raw_data
```

### 2. Update SBK1 (Old Format) - Already Working
```python
def _update_sbk1_setlist_name(self, raw_data, setlist_index, new_name):
    """Update setlist name in SBK1 chunk - ALREADY IMPLEMENTED."""
    # This part already works!
    pass
```

## Next Steps

1. **Implement SLS1 writer** - Update setlist names in new format
2. **Implement SLS1 slot writer** - Update slot names in new format  
3. **Test with hardware** - Verify Kronos accepts the files
4. **Implement metadata updates** - Colors, text size, transpose in SDB1

## File Offsets Reference

### Test File: nw_modified.PCG

**SLS1 Setlist Names (file offsets):**
- Setlist 0: 3,744 (0x000EA0)
- Setlist 1: 7,356 (0x001CBC)
- Setlist 2: 10,968 (0x002AD8)
- Setlist 3: 14,580 (0x0038F4)
- Setlist 4: 18,192 (0x004710)
- Setlist 5: 21,804 (0x00552C)
- Setlist 6: 25,416 (0x006348)
- Setlist 7: 29,028 (0x007164)
- Setlist 8: 32,640 (0x007F80)
- Setlist 9: 36,252 (0x008D9C)
- Setlist 10: 39,864 (0x009BB8)
- Setlist 11: 43,476 (0x00A9D4)
- Setlist 12: 47,088 (0x00B7F0)
- Setlist 13: 50,700 (0x00C60C)
- Setlist 14: 54,312 (0x00D428)
- Setlist 15: 57,924 (0x00E244)

**SBK1 Setlist Names (file offsets):**
- Setlist 0: 601,336 (0x092CF8)
- Setlist 1: 670,752 (0x0A3C20)
- Setlist 2: 740,168 (0x0B4B48)
- Setlist 3: 809,584 (0x0C5A70)
- Setlist 4: 879,000 (0x0D6998)
- Setlist 5: 948,416 (0x0E78C0)
- Setlist 6: 1,017,832 (0x0F87E8)
- Setlist 7: 1,087,248 (0x109710)
- Setlist 8: 1,156,664 (0x11A638)
- Setlist 9: 1,226,080 (0x12B560)
- Setlist 10: 1,295,496 (0x13C488)
- Setlist 11: 1,364,912 (0x14D3B0)
- Setlist 12: 1,434,328 (0x15E2D8)
- Setlist 13: 1,503,744 (0x16F200)
- Setlist 14: 1,573,160 (0x180128)

## Chunk Information

**Chunks found in nw_modified.PCG:**
- "et L" (likely "Set L" = SLS1/SLD1/SDB1 combined): offset=141, size=7,631,721
- "ist " (likely "list" = STL1): offset=7,681,773, size=3,420,209
- "@@@@" (unknown): offset=11,103,444, size=4,210,752

**Note:** The chunk IDs appear corrupted in the analysis. Need to investigate proper chunk parsing.

## Key Insight

The Kronos uses a **dual-format system**:
- **SLS1/SLD1/SDB1** = New format (smaller, more efficient)
- **STL1/SBK1** = Old format (larger, legacy compatibility)

Both formats must be kept in sync. The Kronos likely:
1. Tries to read from new format first (SLS1)
2. Falls back to old format (SBK1) if new format is missing
3. Validates consistency between both formats
4. Rejects file if they don't match

This explains why our files are rejected - we only update the old format!
