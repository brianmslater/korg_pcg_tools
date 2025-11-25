# Hardware Test Phase 2 - Diagnostic Files

## Test Results from Phase 1

❌ **WRITER_FIX_TEST.PCG** - Did not load
❌ **DUAL_FORMAT_TEST.PCG** - Did not load

Both files with modified setlist names were rejected by the Kronos.

## New Diagnostic Files on USB Drive

### 1. UNMODIFIED_ROUNDTRIP.PCG
**Purpose:** Test if the write process itself is corrupting files

**What it is:**
- Original file read and written back
- **NO modifications made**
- Should be identical to original

**Test:**
1. Load UNMODIFIED_ROUNDTRIP.PCG on Kronos
2. Check if it loads successfully

**If it FAILS:**
- The write process itself is corrupting data
- Problem is in `writer.write()` method
- Need to investigate how raw_data is being written

**If it LOADS:**
- The write process is OK
- Our modifications are causing the problem
- Need to investigate what we're changing incorrectly

### 2. NW_MODIFIED_ORIGINAL.PCG
**Purpose:** Verify the source file is valid

**What it is:**
- Direct copy of the original test file
- No processing at all

**Test:**
1. Load NW_MODIFIED_ORIGINAL.PCG on Kronos
2. Check if it loads successfully

**If it FAILS:**
- The source file itself is corrupted
- Need a different source file

**If it LOADS:**
- The source file is valid
- Problem is in our processing

## Test Procedure

### Step 1: Test Original Source
```
Load: NW_MODIFIED_ORIGINAL.PCG
Expected: Should load (it's the original file)
```

### Step 2: Test Unmodified Roundtrip
```
Load: UNMODIFIED_ROUNDTRIP.PCG
Expected: Should load (no changes made)
```

### Step 3: Compare Results

| File | Loads? | Conclusion |
|------|--------|------------|
| NW_MODIFIED_ORIGINAL | Yes | Source is valid |
| NW_MODIFIED_ORIGINAL | No | Source is corrupted |
| UNMODIFIED_ROUNDTRIP | Yes | Write process OK, modifications are problem |
| UNMODIFIED_ROUNDTRIP | No | Write process is corrupting data |

## Possible Issues

### If Write Process is Corrupting
Possible causes:
1. Chunk sizes being recalculated incorrectly
2. Checksums/CRCs not being updated
3. File structure being altered
4. Byte order issues

### If Modifications are Problem
Possible causes:
1. Updating wrong offsets in SLS1 or SBK1
2. Not updating all required locations
3. Corrupting adjacent data
4. Breaking internal references

## Next Steps Based on Results

### Scenario A: Both files load successfully
→ Problem is specifically with our setlist name modifications
→ Need to investigate exact bytes we're changing
→ May need to update additional fields (checksums, counts, etc.)

### Scenario B: Original loads, roundtrip fails
→ Write process is corrupting the file
→ Need to investigate `writer.write()` and `_update_raw_data()`
→ May need to avoid modifying raw_data at all

### Scenario C: Neither file loads
→ Source file is corrupted
→ Need to use a different test file
→ Try with a factory preload file

## Files on USB Drive

Current test files:
- ❌ WRITER_FIX_TEST.PCG (modified, failed)
- ❌ DUAL_FORMAT_TEST.PCG (modified, failed)
- ⏳ UNMODIFIED_ROUNDTRIP.PCG (no changes, test this)
- ⏳ NW_MODIFIED_ORIGINAL.PCG (original source, test this)

## What to Document

For each file tested, record:
1. File name
2. Did it load? (Yes/No)
3. If no, what error message?
4. If yes, does it work correctly?

---

**Status:** Awaiting Phase 2 test results
**Critical Question:** Does the write process itself corrupt files, or is it our modifications?
