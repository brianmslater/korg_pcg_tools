# Hardware Testing Guide

This guide will help you test the setlist editing features on your actual Kronos hardware.

## Quick Start

```bash
# Option 1: Use a test file
python test_hardware_ready.py test_files/test_soundcheck9_25_25_combined.PCG

# Option 2: Use your own PCG file
python test_hardware_ready.py "path/to/your/file.PCG"
```

## What to Test

### 1. Text Size Changes
- **What to do**: Change some slots to Small, Medium, and Large text
- **What to verify**: Text displays at the correct size on Kronos screen
- **Expected**: Small = compact, Medium = normal, Large = bigger/bold

### 2. Transpose Values
- **What to do**: Set transpose to +12, -12, +5, -7 on different slots
- **What to verify**: Patches play at the correct pitch when selected
- **Expected**: +12 = one octave up, -12 = one octave down

### 3. Descriptions
- **What to do**: Edit descriptions (up to 512 characters)
- **What to verify**: Descriptions display correctly when viewing slot details
- **Expected**: Full text appears, no truncation or corruption

### 4. Colors
- **What to do**: Change slot colors (Red, Blue, Green, Yellow, etc.)
- **What to verify**: Colors display correctly in setlist view
- **Expected**: Colors match what you set in the editor

### 5. Patch References
- **What to do**: Change bank/patch numbers
- **What to verify**: Correct sound loads when slot is selected
- **Expected**: Slot loads the specified program or combi

## Testing Workflow

1. **Backup your original file** (always!)
   ```bash
   cp original.PCG original_BACKUP.PCG
   ```

2. **Run the test script**
   ```bash
   python test_hardware_ready.py original.PCG
   ```

3. **Make test edits in the GUI**
   - Edit 3-5 slots with different changes
   - Note what you changed (write it down!)

4. **Save the output**
   - File will be saved as `original_HARDWARE_TEST.PCG`

5. **Transfer to Kronos**
   - Copy to USB drive
   - Load on Kronos via DISK mode

6. **Verify on hardware**
   - Check each edited slot
   - Verify all changes appear correctly

7. **Report results**
   - Note what works ✓
   - Note what doesn't work ✗
   - Take photos if helpful

## Test Checklist

Create a simple test log:

```
Slot | Change Made           | Expected Result      | Actual Result | ✓/✗
-----|----------------------|---------------------|---------------|----
1    | Text size = Large    | Large text display  |               |
2    | Transpose = +12      | One octave up       |               |
3    | Color = Red          | Red color shown     |               |
4    | Description edited   | New text appears    |               |
5    | Bank/Patch changed   | New sound loads     |               |
```

## Common Issues to Watch For

### Text Size
- Does "Large" actually appear larger?
- Does "Small" save space on screen?
- Are all three sizes visibly different?

### Transpose
- Does the pitch change match the value?
- Does transpose affect all timbres in a combi?
- Does negative transpose work correctly?

### Colors
- Do all 16 colors display correctly?
- Are colors consistent across slots?
- Do colors persist after power cycle?

### Descriptions
- Do long descriptions (>256 chars) work?
- Are special characters preserved?
- Does text wrap correctly?

## File Formats

The tool supports both setlist formats:

- **STL1/SLD1**: Older format (pre-OS 3.0)
- **SLS1**: Newer format (OS 3.0+)

Your Kronos will use whichever format it finds. Both should work identically.

## If Something Goes Wrong

### File won't load on Kronos
- Check file size (should be similar to original)
- Verify file extension is `.PCG` (uppercase)
- Try loading original backup to confirm Kronos is working

### Changes don't appear
- Double-check you loaded the correct file
- Verify you saved after making edits
- Check if Kronos needs a reboot

### Kronos shows errors
- Note the exact error message
- Try loading a known-good PCG file
- Report the issue with details

## Success Criteria

The test is successful if:
- ✓ File loads without errors
- ✓ Setlists appear in correct locations
- ✓ All edited slots show changes correctly
- ✓ Sounds play as expected
- ✓ No data corruption or crashes

## Next Steps After Testing

### If everything works:
- Start using the tool for real editing!
- Share your success story
- Help improve documentation

### If issues found:
- Document exactly what failed
- Provide test files if possible
- Report issues with details:
  - What you changed
  - What you expected
  - What actually happened
  - Kronos OS version

## Tips for Effective Testing

1. **Start small**: Edit just 2-3 slots first
2. **Test one feature at a time**: Easier to isolate issues
3. **Keep notes**: Write down what you changed
4. **Take photos**: Visual proof of results
5. **Compare**: Load original and modified files side-by-side

## Example Test Session

```bash
# 1. Backup
cp my_setlist.PCG my_setlist_BACKUP.PCG

# 2. Run test
python test_hardware_ready.py my_setlist.PCG

# 3. In GUI, edit:
#    - Slot 1: Text size = Large
#    - Slot 2: Transpose = +12
#    - Slot 3: Color = Red

# 4. Save (creates my_setlist_HARDWARE_TEST.PCG)

# 5. Copy to USB and test on Kronos

# 6. Report back!
```

## Questions?

If you run into issues or have questions:
- Check KNOWN_ISSUES.md
- Review SLS1_USAGE_GUIDE.md
- Check the code comments
- Ask for help with specific details

Happy testing! 🎹
