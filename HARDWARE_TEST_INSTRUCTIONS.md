# Hardware Test Instructions - Writer Fix

## Files Copied to KEYBOARD USB Drive

✓ **WRITER_FIX_TEST.PCG** (11 MB)
✓ **DUAL_FORMAT_TEST.PCG** (11 MB)

Both files are ready for testing on Kronos hardware.

## What Was Changed

Both files have the **first setlist name** modified:
- **WRITER_FIX_TEST.PCG**: First setlist renamed to "WRITER FIX TEST"
- **DUAL_FORMAT_TEST.PCG**: First setlist renamed to "DUAL FORMAT TEST"

All other setlists and slots remain unchanged.

## Test Procedure

### Test 1: WRITER_FIX_TEST.PCG

1. **Load the file on Kronos**
   - Press DISK button
   - Navigate to USB drive
   - Select "WRITER_FIX_TEST.PCG"
   - Press LOAD

2. **Expected Result: File Loads Successfully**
   - ✓ No "Invalid file" error
   - ✓ No "Corrupted data" error
   - ✓ File loads without issues

3. **Verify Setlist Name**
   - Press SET LIST button
   - Check first setlist name
   - **Expected:** "WRITER FIX TEST"
   - **If different:** Note what it shows

4. **Verify Slots Are Intact**
   - Select first setlist
   - Browse through slots
   - **Expected:** All slots accessible and functional
   - Try playing a few patches

5. **Verify Other Setlists**
   - Check second setlist
   - **Expected:** "NIGHTWISH LEGACY 2" (unchanged)
   - Verify it's not corrupted

### Test 2: DUAL_FORMAT_TEST.PCG

Repeat the same procedure with DUAL_FORMAT_TEST.PCG:
- Expected first setlist name: "DUAL FORMAT TEST"
- All other checks same as Test 1

## Success Criteria

### ✓ PASS if:
- File loads without errors
- First setlist shows new name correctly
- All slots are accessible
- Patches play correctly
- Other setlists are unchanged

### ❌ FAIL if:
- File is rejected with error
- Setlist name is wrong or corrupted
- Slots are inaccessible
- Patches don't play
- Other setlists are corrupted

## What to Document

### If Test PASSES ✓
Record:
1. Kronos model and OS version
2. Exact setlist name displayed
3. Any warnings or messages
4. Screenshot if possible

### If Test FAILS ❌
Record:
1. Exact error message
2. When error occurred (load, display, play)
3. What was displayed instead of expected name
4. Any other symptoms

## Technical Background

### The Fix
The writer now updates **BOTH** formats:
- **SLS1** (new format) - What the Kronos displays
- **SBK1** (old format) - Legacy compatibility

Previous versions only updated SBK1, causing the Kronos to detect inconsistency and reject files.

### Why This Should Work
1. Parser reads from SLS1 ✓
2. Writer now updates SLS1 ✓
3. Writer also updates SBK1 ✓
4. Both formats match ✓
5. Kronos validation passes ✓

## Comparison Files

For reference, these files are also on the USB drive:
- `soundcheck_ORIGINAL_TEST.PCG` - Unmodified original
- `soundcheck_NAME_TEST.PCG` - Previous attempt (likely fails)

You can compare behavior between old and new versions.

## Next Steps After Testing

### If Tests PASS
1. Document results in `HARDWARE_TEST_RESULTS.md`
2. Mark writer fix as **CONFIRMED WORKING**
3. Proceed with implementing:
   - Slot name updates
   - Metadata updates (colors, sizes)
   - Patch reference updates

### If Tests FAIL
1. Document exact failure mode
2. Analyze what went wrong
3. May need to:
   - Check Kronos OS version compatibility
   - Investigate additional validation rules
   - Compare with C# implementation more closely

## Questions to Answer

1. Does the file load? (Yes/No)
2. What name is displayed for first setlist?
3. Are slots accessible? (Yes/No)
4. Do patches play correctly? (Yes/No)
5. Are other setlists intact? (Yes/No)
6. Any error messages? (If yes, what exactly?)

## Contact

After testing, update the results in the project documentation so we can proceed with the next phase of development.

---

**Status: Ready for Hardware Testing**
**Date Prepared: November 25, 2025**
**Test Files Location: /Volumes/KEYBOARD/**
