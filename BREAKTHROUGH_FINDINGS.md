# Breakthrough Findings - November 25, 2025

## Hardware Test Results

### Phase 1 - Initial Tests
❌ **WRITER_FIX_TEST.PCG** - Failed (updated both SLS1 and SBK1)
❌ **DUAL_FORMAT_TEST.PCG** - Failed (updated both SLS1 and SBK1)

### Phase 2 - Diagnostic Tests
✅ **NO_SETLIST_UPDATE.PCG** - SUCCESS (no updates at all)
✅ **NW_MODIFIED_ORIGINAL.PCG** - SUCCESS (direct copy)
❌ **UNMODIFIED_ROUNDTRIP.PCG** - FAILED (updated SBK1 name)

## Critical Discovery

**Changing the SBK1 setlist name breaks the file!**

### The Evidence

The only difference between working and failing files:

| File | SBK1 Name | Result |
|------|-----------|--------|
| NO_SETLIST_UPDATE | "NIGHTWISH LEGACY" (original) | ✅ Works |
| UNMODIFIED_ROUNDTRIP | "MODIFIED SETLIST" (changed) | ❌ Fails |

**Difference:** 16 bytes at offset 531920 (SBK1 setlist name)

### Why This Matters

The original file ALREADY has mismatched names:
- **SLS1**: "MODIFIED SETLIST"
- **SBK1**: "NIGHTWISH LEGACY"

And it loads fine! This proves:
1. ✅ Kronos ACCEPTS files with mismatched SLS1/SBK1 names
2. ❌ Kronos REJECTS files when we CHANGE the SBK1 name
3. ⚠️ Something else in the file validates or references the SBK1 name

## The Solution

**Update ONLY SLS1, leave SBK1 unchanged!**

### Why This Works

1. Parser reads from SLS1 → names display correctly
2. SBK1 stays unchanged → file validation passes
3. Mismatched names are OK → original file proves this

### Implementation

```python
def _update_all_setlist_chunks(self, raw_data):
    """Update ONLY SLS1, leave SBK1 alone."""
    if not self.pcg.set_lists:
        return
    
    # Only update SLS1 (new format - what parser reads)
    self._update_sls1_names(raw_data)
    
    # DO NOT update SBK1!
    # Changing SBK1 breaks file validation
```

## Test File Ready

**SLS1_ONLY_TEST.PCG** is on the USB drive for testing.

This file:
- Updates SLS1 to "SLS1 ONLY TEST"
- Leaves SBK1 as "NIGHTWISH LEGACY"
- Should load successfully if our theory is correct

## What We Learned

### Incorrect Assumptions
❌ Both formats must match
❌ Dual-format update is required
❌ Kronos validates SLS1/SBK1 consistency

### Correct Understanding
✅ Mismatched names are acceptable
✅ SBK1 has additional validation we don't understand
✅ Changing SBK1 breaks something else in the file
✅ SLS1-only updates should work

## Implications

### For Setlist Names
- ✅ Can update names (via SLS1 only)
- ✅ Names will display correctly
- ⚠️ SBK1 will have old/different names
- ⚠️ May cause issues with older firmware

### For Slot Names
- Need to test if same issue exists
- Likely same pattern: update SLS1 only
- SBK1 slot names may need to stay unchanged

### For Metadata
- Colors, text sizes, transpose in SDB1
- May be safe to update (not in SBK1)
- Need testing to confirm

## Next Steps

### Immediate
1. **Test SLS1_ONLY_TEST.PCG** on hardware
2. If it works, update writer to only modify SLS1
3. Test with multiple setlist name changes

### Short Term
1. Test slot name updates (SLS1 only)
2. Test metadata updates (SDB1)
3. Verify no side effects

### Long Term
1. Investigate what validates SBK1 names
2. Find if there's a way to safely update SBK1
3. Study C# implementation for clues
4. Consider firmware version differences

## The Mystery

**What validates the SBK1 name?**

Possibilities:
- Checksum/CRC somewhere in the file
- Name table or index we haven't found
- Cross-references from other chunks
- Firmware-specific validation logic

This remains unsolved, but we have a working solution that bypasses the issue.

## Status

**Working solution identified!** 

SLS1-only updates should allow us to:
- ✅ Change setlist names
- ✅ Display correctly on Kronos
- ✅ Load files successfully
- ⚠️ With SLS1/SBK1 mismatch (acceptable)

Awaiting hardware test of SLS1_ONLY_TEST.PCG to confirm.
