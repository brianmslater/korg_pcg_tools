# PCG Writer Findings - Critical Issues

## Problem Summary

The Kronos PCG format stores setlist data in **multiple redundant locations** that must ALL be kept in sync. Our writer only updates some locations, causing file corruption.

## Setlist Name Storage Locations

For "NIGHTWISH LEGACY" (first setlist), the name appears at **4 positions**:

1. **Position 3744 (0x000EA0)** - In SLS1/SLD1 chunk (new format)
2. **Position 7356 (0x001CBC)** - In SLS1/SLD1 chunk (second copy?)
3. **Position 531920 (0x081DD0)** - In SBK1 chunk (old format) ← We update this
4. **Position 601336 (0x092CF8)** - In SBK1 chunk (second setlist?)

**Current Status:** We only update position #3, but the Kronos reads from position #1 or #2.

## Chunk Structure

### SLS1 (New Format - Slot Names)
- Offset: 84
- Contains: Setlist names and slot names
- Structure: Marker + Name + Separator + 128 slots

### SLD1 (New Format - Slot Metadata)  
- Offset: 96
- Contains: Patch references, descriptions
- **Likely contains setlist names too**

### SDB1 (New Format - Display Metadata)
- Offset: 108
- Contains: Colors, text sizes, transpose
- **May also have setlist names**

### STL1/SBK1 (Old Format - Complete Data)
- Offset: 462468 (STL1), 462480 (SBK1)
- Contains: Everything in one place
- Structure: 16 setlists × 69,416 bytes each
- First setlist at: SBK1_data + 69,432

## Why Files Are Corrupted

1. **Incomplete Updates**: We update SBK1 but not SLS1/SLD1/SDB1
2. **Inconsistent Data**: Kronos sees different names in different chunks
3. **Validation Failure**: Kronos detects inconsistency and rejects file

## What Needs to Be Done

### Phase 1: Update ALL Name Locations
Update setlist names in:
- [ ] SLS1 chunk (position ~3744)
- [ ] SLD1 chunk (if it has names)
- [ ] SDB1 chunk (if it has names)  
- [x] SBK1 chunk (position 531920) - DONE

### Phase 2: Update Slot Names
Update slot names in:
- [ ] SLS1 chunk (128 slots per setlist)
- [ ] SBK1 chunk (128 slots per setlist)

### Phase 3: Update Metadata
Update transpose, text_size, colors in:
- [ ] SDB1 chunk (new format)
- [ ] SBK1 chunk (old format)

## Recommended Approach

### Option A: Update Everything (Safest)
```python
def _update_all_chunks(self, raw_data):
    self._update_sls1_names(raw_data)   # New format names
    self._update_sld1_data(raw_data)    # New format metadata
    self._update_sdb1_data(raw_data)    # New format display
    self._update_sbk1_data(raw_data)    # Old format everything
```

### Option B: Only Update What Changed (Efficient)
```python
# Track which setlists/slots are dirty
if setlist.is_dirty:
    update_in_all_chunks(setlist)
```

### Option C: Use C# Code as Reference
Port the exact update logic from the original C# implementation.

## Test Strategy

1. **Minimal Change Test**: Update only setlist name, verify in all 4 locations
2. **Single Slot Test**: Update one slot name, verify in SLS1 and SBK1
3. **Metadata Test**: Update transpose/text_size, verify in SDB1 and SBK1
4. **Full Edit Test**: Change everything, verify file loads on Kronos

## Current Blocker

**We don't know the exact structure of SLS1/SLD1/SDB1 chunks well enough to update them safely.**

Need to:
1. Analyze where setlist names are in SLS1/SLD1/SDB1
2. Understand the relationship between all chunks
3. Implement updates for ALL chunks, not just SBK1

## Temporary Solution

**Disable all writers** until we can update ALL chunks consistently. Files can be read but not edited.

## Long-term Solution

Study the C# code more carefully to understand:
- Exact byte offsets for each field in each chunk
- Which chunks are mandatory vs optional
- How chunks reference each other
- Validation rules the Kronos uses
