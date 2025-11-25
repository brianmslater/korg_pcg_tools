# Hardware Test Phase 3 - Critical Diagnostic

## Discovery

The original file ALREADY has mismatched names between SLS1 and SBK1:
- **SLS1 (offset 3744):** "MODIFIED SETLIST"
- **SBK1 (offset 531920):** "NIGHTWISH LEGACY"

This means the Kronos ACCEPTS files with mismatched names! So that's not why our files are being rejected.

## New Test Files on USB Drive

### 1. NO_SETLIST_UPDATE.PCG ⭐ CRITICAL TEST
**What it is:**
- File read and written with NO setlist updates at all
- Raw data written directly without modifications
- Binary IDENTICAL to original file

**Test this FIRST:**
```
Load: NO_SETLIST_UPDATE.PCG
```

**If it LOADS:**
- ✓ Write process is OK
- ✓ Parser is OK
- ❌ Our setlist update methods are corrupting data
- → Problem is in `_update_sls1_names()` or `_update_sbk1_names()`

**If it FAILS:**
- ❌ Something fundamentally wrong
- Could be: parser issue, file format issue, or source file corrupted

### 2. UNMODIFIED_ROUNDTRIP.PCG
**What it is:**
- File read and written WITH setlist updates enabled
- But no explicit name changes made
- However, it DOES change SBK1 from "NIGHTWISH LEGACY" to "MODIFIED SETLIST"

**Differences from original:**
- 16 bytes changed at offset 531920 (SBK1 setlist name)
- Changed from "NIGHTWISH LEGACY" to "MODIFIED SETLIST"

### 3. NW_MODIFIED_ORIGINAL.PCG
**What it is:**
- Direct copy of source file
- No processing at all

## Test Priority

**Test in this order:**

1. **NO_SETLIST_UPDATE.PCG** (most important)
2. **NW_MODIFIED_ORIGINAL.PCG** (verify source is valid)
3. **UNMODIFIED_ROUNDTRIP.PCG** (see if SBK1 change matters)

## Analysis

### Key Finding
The original file has:
- SLS1: "MODIFIED SETLIST"
- SBK1: "NIGHTWISH LEGACY"

The parser reads from SLS1, so it sees "MODIFIED SETLIST".

When we write back:
- Writer updates BOTH SLS1 and SBK1 with "MODIFIED SETLIST"
- This changes SBK1 from "NIGHTWISH LEGACY" to "MODIFIED SETLIST"

### Questions to Answer

1. **Does NO_SETLIST_UPDATE.PCG load?**
   - If YES: Our update methods are the problem
   - If NO: Something else is wrong

2. **Does NW_MODIFIED_ORIGINAL.PCG load?**
   - If YES: Source file is valid
   - If NO: Source file is corrupted

3. **Does UNMODIFIED_ROUNDTRIP.PCG load?**
   - If YES: Changing SBK1 name is OK
   - If NO: Changing SBK1 name breaks something

## Possible Issues with Update Methods

If NO_SETLIST_UPDATE loads but UNMODIFIED_ROUNDTRIP doesn't, the problem could be:

1. **Wrong offset calculation**
   - We're writing to the wrong position
   - Corrupting adjacent data

2. **Chunk size not updated**
   - Chunk headers have size fields
   - We may need to update those

3. **Checksums/CRCs**
   - File may have checksums we're not updating
   - Kronos validates and rejects if wrong

4. **Internal pointers**
   - Other parts of file may reference setlist data
   - We're not updating those references

## Next Steps Based on Results

### Scenario A: NO_SETLIST_UPDATE loads ✓
→ Our update methods are corrupting data
→ Need to investigate `_update_sls1_names()` and `_update_sbk1_names()`
→ Check if we're writing to correct offsets
→ Check if we need to update chunk sizes or checksums

### Scenario B: NO_SETLIST_UPDATE fails ❌
→ Problem is NOT our updates
→ Could be parser corrupting data during read
→ Could be source file is invalid
→ Need different approach

## Files on USB Drive

| File | Status | Purpose |
|------|--------|---------|
| WRITER_FIX_TEST.PCG | ❌ Failed | Modified name test |
| DUAL_FORMAT_TEST.PCG | ❌ Failed | Modified name test |
| NO_SETLIST_UPDATE.PCG | ⏳ Test this | No updates, identical to original |
| UNMODIFIED_ROUNDTRIP.PCG | ⏳ Test | With updates, SBK1 changed |
| NW_MODIFIED_ORIGINAL.PCG | ⏳ Test | Direct copy of source |

---

**Critical Test:** NO_SETLIST_UPDATE.PCG
**This will tell us if our update methods are the problem or not.**
