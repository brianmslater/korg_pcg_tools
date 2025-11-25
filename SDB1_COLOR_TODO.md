# SDB1 Color Data - TODO

## Current Status

✅ **Completed:**
- SLS1/SLD1 format parsing (setlist names, slot names)
- STL1/SBK1 format parsing (includes colors)
- All 16 setlists displayed in GUI
- Combi names extracted correctly

❌ **Missing:**
- Color data from SDB1 chunk for SLS1 format
- Text size data from SDB1 chunk

## Problem

The SDB1 chunk (202MB) contains setlist metadata including colors, but we haven't reverse-engineered its structure yet. Colors ARE present in the file (confirmed by Kronos displaying them), but we need to find where in the SDB1 chunk they're stored.

## What We Know

### SDB1 Chunk Structure
```
Offset: 0x0000006C
Size: 202,245,888 bytes (202MB)

Contains:
- Setlist names (found at offset +18084 for "SC 10/4")
- Slot names (with 1E 02 00 00 markers)
- Metadata section (LOCATION UNKNOWN)
  └─ Color data (STRUCTURE UNKNOWN)
  └─ Text size data (STRUCTURE UNKNOWN)
```

### Test Case
File: `soundcheck9_25_25_combined2.PCG`  
Setlist: "SC 10/4" (index 4)

**Expected Colors:**
- Slot 0: Navy (164/165)
- Slot 1: Indigo (160)
- Slots 2, 3, 4: Gold (152/153)

**Search Results:**
- ✓ Found 3,929 occurrences of Navy values in SDB1
- ✓ Found 12,509 occurrences of Indigo values in SDB1
- ✓ Found 35,211 occurrences of Gold values in SDB1
- ✗ No clear pattern or structure identified

## Required Information

To complete this feature, we need:

1. **Original PCG Tools Documentation**
   - The Windows PCG Tools manual documents the PCG format
   - Need section on SDB1 chunk structure
   - Need color data storage format

2. **Binary Comparison**
   - Load PCG file in Kronos
   - Change slot colors
   - Save and compare binary differences
   - Identify exact byte locations

3. **Community Knowledge**
   - Korg Forums discussions
   - Other reverse-engineering efforts
   - PCG Tools source code (if available)

## Resources

### Official PCG Tools
- **Application:** Windows PCG Tools by Michel Keijzers
- **Manual:** Extensive documentation of PCG format
- **Link:** [PCG Tools Manual](https://www.korgforums.com/forum/phpBB2/viewtopic.php?t=48474)

### Alternative Sources
- **Korg Creator (Chicken Systems):** Commercial software with documentation
- **KARMA Lab Documentation:** Insights into PCG structure
- **Korg Forums:** Community reverse-engineering efforts

## Workaround

Until SDB1 parsing is implemented, users can:

### Option 1: Use STL1 Format
```python
# STL1 format includes full color support
# Export individual setlists from Kronos
# Our parser fully supports STL1 colors
```

### Option 2: Manual Color Assignment
```python
# Edit colors in GUI
# Save as STL1 format
# Re-import to Kronos
```

## Implementation Plan

### Phase 1: Research (CURRENT)
- [ ] Obtain PCG Tools documentation
- [ ] Study SDB1 chunk structure
- [ ] Identify color data location
- [ ] Document byte offsets and patterns

### Phase 2: Parsing
- [ ] Implement `_parse_sdb1_metadata()` method
- [ ] Extract color data for each slot
- [ ] Extract text size data for each slot
- [ ] Update SetListSlot objects with color/size

### Phase 3: Testing
- [ ] Test with soundcheck file
- [ ] Verify colors match Kronos display
- [ ] Test with multiple PCG files
- [ ] Validate all 16 colors

### Phase 4: Writing
- [ ] Implement SDB1 color writing
- [ ] Allow color editing in GUI
- [ ] Save modified colors back to file

## Code Stub

```python
def _parse_sdb1_chunk(self, pcg: PcgFile):
    """Parse SDB1 chunk for setlist metadata including colors.
    
    SDB1 Structure (NEEDS DOCUMENTATION):
    - Offset 0x00: Chunk ID 'SDB1'
    - Offset 0x04: Chunk size (little-endian)
    - Offset 0x08: Header (structure unknown)
    - Offset ???: Setlist names section
    - Offset ???: Slot names section
    - Offset ???: Metadata section
      - Color data (format unknown)
      - Text size data (format unknown)
    """
    sdb1_offset = self.data.find(b'SDB1')
    if sdb1_offset < 0:
        debug_print("SDB1 chunk not found")
        return
    
    sdb1_size = self.get_int(sdb1_offset + 4, 4)
    debug_print(f"Found SDB1 at offset {sdb1_offset:08X}, size {sdb1_size}")
    
    # TODO: Parse SDB1 structure
    # 1. Find where names section ends
    # 2. Locate metadata section
    # 3. Parse color data for each setlist/slot
    # 4. Update pcg.set_lists with color information
    
    pass
```

## Priority

**Priority:** Medium  
**Difficulty:** High (requires reverse engineering)  
**Impact:** Medium (workaround available)  
**User Request:** Yes (Brian Slater confirmed colors missing)

## Notes

- The fact that Kronos displays colors confirms they're in the file
- SDB1 is 202MB - much larger than just names would require
- Color values are scattered throughout SDB1 (not sequential)
- Need to understand the relationship between:
  - Setlist index (0-15)
  - Slot index (0-127)
  - Color byte location in SDB1

## Contact

If you have information about SDB1 structure or PCG Tools documentation:
- Open an issue on GitHub
- Contact via Korg Forums
- Email: [project maintainer]

---

**Status:** 🔍 Awaiting Documentation  
**Last Updated:** November 25, 2025  
**Reported By:** Brian Slater
