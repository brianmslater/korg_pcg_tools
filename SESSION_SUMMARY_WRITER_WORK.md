# Session Summary: PCG Writer Implementation Attempt

## Goal
Implement setlist editing with proper file writing that the Kronos will accept.

## What We Accomplished

### 1. Code Alignment with C# Patterns ✅
- Fixed parser to not pass properties (`transpose`, `volume`, `text_size`) as init args
- Properties are now set after object creation using setters
- Follows C# pattern where properties update underlying `raw_data`

### 2. Identified File Structure ✅
Discovered that setlist names are stored in **4 locations**:
- Position 1 (3744): SDB1 chunk - new format with markers
- Position 2 (7356): SDB1 chunk - second setlist  
- Position 3 (531920): SBK1 chunk - old format, first setlist
- Position 4 (601336): SBK1 chunk - old format, second setlist

### 3. Implemented Multi-Chunk Writer ✅
Created `_update_all_setlist_chunks()` that updates:
- SDB1 names (new format with marker `1e020000` and separator `280f0100`)
- SBK1 names (old format, 69,416 byte spacing)

### 4. Hardware Testing ✅
- Confirmed original files load on Kronos
- Confirmed unmodified read/write works (file identical)
- Confirmed modified files are rejected ("file unavailable")

## The Problem

**Files are still rejected by Kronos even when updating all name locations.**

### What We Tried
1. ❌ Update only SBK1 → Rejected
2. ❌ Update only SDB1 → Rejected  
3. ❌ Update both SDB1 and SBK1 → Still rejected
4. ✅ No modifications → Accepted

### Possible Causes

1. **Missing Chunk Updates**
   - We update SDB1 and SBK1, but not SLS1 or SLD1
   - All 5 chunks (SLS1, SLD1, SDB1, STL1, SBK1) may need updates

2. **Slot Data Mismatch**
   - Changing setlist name might require updating slot data too
   - Slots reference their parent setlist - these refs might be validated

3. **Checksums/Validation**
   - Kronos might validate chunk integrity
   - Cross-chunk references might be checked
   - No obvious checksum fields found in headers

4. **Incomplete Understanding**
   - PCG format has undocumented validation rules
   - C# code took years to develop - handles edge cases we don't know

## Technical Details

### SDB1 Structure (New Format)
```
Marker: 1e 02 00 00 (4 bytes)
Name: 24 bytes (null-padded)
Separator: 28 0f 01 00 (4 bytes)
Slots follow...
```

### SBK1 Structure (Old Format)
```
First setlist: SBK1_data + 69,432 bytes
Spacing: 69,416 bytes between setlists
Name: 24 bytes (null-padded, no markers)
```

### What Changes When We Edit
```
Original file: 48,036,542 bytes
Modified file: 48,036,542 bytes (same size ✓)

Changed bytes: ~40 (just the name in 2 locations)
Chunk headers: Unchanged ✓
File structure: Intact ✓

Yet Kronos rejects it ❌
```

## Code Changes Made

### writer.py
```python
def _update_all_setlist_chunks(self, raw_data):
    """Update names in ALL chunks"""
    self._update_sdb1_names(raw_data)  # New format
    self._update_sbk1_names(raw_data)  # Old format

def _update_sdb1_names(self, raw_data):
    """Find markers, update names between marker and separator"""
    
def _update_sbk1_names(self, raw_data):
    """Update at fixed offsets: 69432 + (N * 69416)"""
```

### parser.py
```python
# Fixed to set properties after creation
slot = SetListSlot(...)
slot._transpose = value  # Not passed in __init__
slot._volume = value
slot._text_size = value
```

## What's Still Missing

### Critical Unknowns
1. **SLS1 Chunk Updates** - We don't update this at all
2. **SLD1 Chunk Updates** - We don't update this at all
3. **Slot Name Synchronization** - Do slot names need updating too?
4. **Cross-References** - Are there pointers between chunks?
5. **Validation Rules** - What exactly does Kronos check?

### Next Steps Required
1. Analyze SLS1 chunk structure and update it
2. Analyze SLD1 chunk structure and update it
3. Test updating ONLY setlist name (no slots)
4. Test with C# tools - do THEY work?
5. Binary diff between C# output and our output

## Recommendations

### Short Term: Disable Writer
```python
# In writer.py _update_raw_data()
# Comment out all chunk updates until we understand validation
```

**Reason:** Better to have read-only tools than tools that corrupt files.

### Medium Term: Incremental Testing
1. Start with simplest possible edit (1 byte change)
2. Test on hardware after each change
3. Build up understanding of what's allowed

### Long Term: Study C# Implementation
1. Get C# source code
2. Find the actual write/save methods
3. Port the exact logic, not just the structure

## Current Status

**Tools can:**
- ✅ Read PCG files perfectly
- ✅ Parse all setlist data
- ✅ Display in GUI
- ✅ Save unmodified files

**Tools cannot:**
- ❌ Edit setlist names (files rejected)
- ❌ Edit slot names
- ❌ Edit transpose/text_size
- ❌ Any modifications at all

## Conclusion

The PCG format is more complex than initially understood. The Kronos performs validation that rejects our modified files even when we update multiple chunk locations. This requires either:

1. **Deep reverse engineering** of Kronos validation
2. **Access to C# source** to see exact write implementation  
3. **Incremental testing** with hardware to find what's allowed

The foundation is solid (reading works perfectly), but writing requires significantly more research and testing.

---

**Time invested:** ~4 hours
**Lines of code:** ~200 (writer methods)
**Hardware tests:** 10+ attempts
**Result:** Files still rejected, cause unknown

**Recommendation:** Pause writer development until we can study working implementation or do systematic reverse engineering with hardware feedback loop.
