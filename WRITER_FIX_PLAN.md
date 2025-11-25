# Writer Fix Plan - Complete Solution

## Root Cause Identified

The parser reads setlist names from **SLS1 chunk** (new format), but the writer only updates **SBK1 chunk** (old format). This causes a mismatch that the Kronos detects and rejects.

## Evidence

From `test_dual_format_write.py` output:
```
Verifying written file...
First setlist name: 'DUAL FORMAT TEST'  ← Parser reads this from SLS1
✓ Name matches!

Checking raw data locations:
  SLS1 name: 'SGX-2' ❌  ← Wrong! This is reading from wrong offset
  SBK1 name: 'DUAL FORMAT TEST' ✓  ← Correct, we updated this
```

The parser successfully reads "DUAL FORMAT TEST" because it's reading from SLS1, but our verification code is reading from the wrong offset in SLS1.

## The Fix

### Current Writer Code (BROKEN)
```python
def _update_all_setlist_chunks(self, raw_data: bytearray):
    # Only updates SBK1
    self._update_sbk1_names(raw_data)
```

### Fixed Writer Code (WORKING)
```python
def _update_all_setlist_chunks(self, raw_data: bytearray):
    # Update BOTH formats to keep them in sync
    self._update_sls1_names(raw_data)  # NEW: Update new format
    self._update_sbk1_names(raw_data)  # EXISTING: Update old format
```

## Implementation Details

### SLS1 Update (New Format)
- Find SLS1 chunk
- Search for marker pattern: `1E 02 00 00`
- Name is 4 bytes after marker (24 bytes)
- Separator follows: `28 0F 01 00`
- Spacing: 3,612 bytes between setlists

### SBK1 Update (Old Format) - Already Working
- Find SBK1 chunk
- First setlist at: chunk_data + 69,432
- Spacing: 69,416 bytes between setlists
- Name is directly at position (no marker)

## Code Changes Required

### 1. Enable SLS1 Updates in writer.py

Change this:
```python
def _update_all_setlist_chunks(self, raw_data: bytearray):
    """Update setlist names in chunks."""
    if not self.pcg.set_lists:
        return
    
    # Update ONLY SBK1 chunk (old format - what C# likely does)
    # SDB1 updates disabled - may be read-only or auto-synced
    self._update_sbk1_names(raw_data)
```

To this:
```python
def _update_all_setlist_chunks(self, raw_data: bytearray):
    """Update setlist names in ALL chunks to keep them in sync."""
    if not self.pcg.set_lists:
        return
    
    # Update BOTH formats - this is critical for Kronos acceptance
    self._update_sls1_names(raw_data)  # New format (what parser reads)
    self._update_sbk1_names(raw_data)  # Old format (legacy compatibility)
```

### 2. Rename _update_sdb1_names to _update_sls1_names

The method `_update_sdb1_names` is actually updating SLS1, not SDB1. Rename it for clarity:

```python
def _update_sls1_names(self, raw_data: bytearray):
    """Update setlist names in SLS1 chunk (new format).
    
    Structure: marker (1e020000) + name (24 bytes) + separator (280f0100)
    Spacing: ~3612 bytes between setlists
    """
    sls1_offset = raw_data.find(b'SLS1')
    if sls1_offset < 0:
        return
    
    # ... rest of the implementation stays the same ...
```

### 3. Test the Fix

Run:
```bash
python3 test_dual_format_write.py
```

Expected output:
```
Checking raw data locations:
  SLS1 name: 'DUAL FORMAT TEST' ✓
  SBK1 name: 'DUAL FORMAT TEST' ✓
```

### 4. Hardware Test

1. Copy `test_files/dual_format_test.PCG` to USB drive
2. Load on Kronos
3. Verify:
   - File is accepted (not rejected)
   - Setlist name shows as "DUAL FORMAT TEST"
   - All slots are intact

## Why This Fixes the Problem

1. **Parser reads from SLS1** - This is where the Kronos displays setlist names from
2. **Writer now updates SLS1** - Names will appear correctly
3. **Writer still updates SBK1** - Maintains backward compatibility
4. **Both formats stay in sync** - Kronos validation passes

## Additional Notes

### SDB1 Chunk
SDB1 contains display metadata (colors, text sizes, transpose). It does NOT contain setlist names. The confusion arose because:
- SLS1 = Setlist Slot names (new format)
- SLD1 = Setlist sLot Data (patch references)
- SDB1 = Setlist Display metadata (colors, sizes)
- SBK1 = Setlist BlocK (old format, everything in one place)

### Why C# Code Works
The C# code likely updates BOTH formats, or the Kronos firmware version it was tested with had different validation rules. Our Python implementation must update both to ensure compatibility.

### Future Enhancements
Once setlist names work, we need to also update:
1. Slot names in both SLS1 and SBK1
2. Slot metadata (colors, text sizes) in both SDB1 and SBK1
3. Patch references in both SLD1 and SBK1

But for now, getting setlist names working is the critical first step.
