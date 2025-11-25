# CRITICAL FINDING - Root Cause Identified

## Hardware Test Results

✅ **NO_SETLIST_UPDATE.PCG** - WORKS
✅ **NW_MODIFIED_ORIGINAL.PCG** - WORKS  
❌ **UNMODIFIED_ROUNDTRIP.PCG** - FAILED ("File Unavailable")

## The Problem

**Changing the SBK1 setlist name breaks the file!**

The only difference between the working and failing files:
- **NO_SETLIST_UPDATE**: SBK1 has "NIGHTWISH LEGACY" (original) ✅
- **UNMODIFIED_ROUNDTRIP**: SBK1 has "MODIFIED SETLIST" (changed) ❌

## Why This Happens

The original file has:
- **SLS1**: "MODIFIED SETLIST"
- **SBK1**: "NIGHTWISH LEGACY"

When we call `_update_all_setlist_chunks()`:
1. Parser reads "MODIFIED SETLIST" from SLS1
2. Writer updates SBK1 to "MODIFIED SETLIST"
3. **File becomes invalid!**

## The Real Issue

There must be **additional data** in the file that:
1. References or validates the SBK1 name
2. We're not updating when we change the name
3. Causes Kronos to reject the file

Possibilities:
- **Checksums/CRCs** - File has checksums we're not recalculating
- **Name index/table** - Another location stores setlist names
- **Cross-references** - Other chunks reference SBK1 data
- **Metadata** - Additional metadata tied to the name

## What We Know

1. ✅ Kronos ACCEPTS files with mismatched SLS1/SBK1 names (original file has this)
2. ❌ Kronos REJECTS files when we CHANGE the SBK1 name
3. ✅ File structure is intact (size unchanged, no corruption)
4. ❌ Something else validates the SBK1 name

## Next Steps

### Option 1: Don't Update SBK1 (Quick Fix)
Only update SLS1, leave SBK1 alone. This would:
- ✅ Allow files to load
- ✅ Display correct names (parser reads SLS1)
- ⚠️ Leave SLS1/SBK1 mismatched
- ⚠️ May cause issues with older firmware

### Option 2: Find What Else Needs Updating (Proper Fix)
Investigate what else references the SBK1 name:
- Search for checksums/CRCs in file
- Look for name tables or indices
- Check if other chunks reference SBK1
- Compare with C# implementation

### Option 3: Use C# Code (Reference)
Study exactly what the C# code does when updating names:
- What fields does it update?
- Does it recalculate checksums?
- Does it update multiple locations?

## Immediate Action

**Disable SBK1 updates in the writer** and test if SLS1-only updates work.

This will tell us if we can work around the issue by only updating the format the parser reads from.
