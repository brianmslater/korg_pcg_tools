# Binary Comparison Guide - Finding SDB1 Color Data

## Overview

This guide will help you discover where setlist color data is stored in the SDB1 chunk by comparing two PCG files with a known color change.

## Prerequisites

- Korg Kronos synthesizer
- USB drive or network connection to Kronos
- Original PCG file: `soundcheck9_25_25_combined2.PCG`
- Python 3 installed

## Step-by-Step Process

### Step 1: Prepare the Original File

1. Copy `test_files/soundcheck9_25_25_combined2.PCG` to your Kronos
2. Load the PCG file into the Kronos
3. Navigate to the "SC 10/4" setlist
4. Note the current colors:
   - Slot 0: Navy
   - Slot 1: Indigo
   - Slots 2, 3, 4: Gold

### Step 2: Make a Single Color Change

**Important:** Change ONLY ONE slot color to make analysis easier.

1. Select "SC 10/4" setlist
2. Go to Slot 0 (currently Navy)
3. Change the color to **Brick** (or any other distinct color)
4. **Do NOT change anything else!**

### Step 3: Save the Modified File

1. Save the PCG file with a new name:
   - Suggested name: `soundcheck_color_test.PCG`
2. Copy the new file back to your computer
3. Place it in the `test_files/` directory

### Step 4: Run the Comparison Tool

```bash
cd korg_pcg_tools
python3 compare_pcg_files.py \
  test_files/soundcheck9_25_25_combined2.PCG \
  test_files/soundcheck_color_test.PCG
```

### Step 5: Analyze the Results

The tool will show you:

1. **Total differences** - How many bytes changed
2. **Differences by chunk** - Which chunks were affected
3. **Detailed view** - Exact byte locations and values
4. **Potential color changes** - Bytes matching known color values

Look for:
- Changes in the **SDB1 chunk**
- Byte value changing from **164/165** (Navy) to **136/137** (Brick)
- The offset from the SDB1 chunk start

### Step 6: Calculate the Pattern

Once you find the color byte:

1. Note the offset from SDB1 start
2. Calculate for SC 10/4 (setlist index 4), Slot 0:
   ```
   offset = base_offset + (setlist_index * X) + (slot_index * Y)
   ```

3. Solve for X and Y by testing more slots

### Step 7: Verify with More Tests

To confirm the pattern, repeat with different changes:

**Test 2:** Change Slot 1 color (Indigo → Gold)
**Test 3:** Change Slot 2 color (Gold → Navy)
**Test 4:** Change a slot in a different setlist

Each test will help confirm the offset calculation.

## Expected Output

The comparison tool will show something like:

```
Found 15 byte differences

Differences by chunk:
  SDB1: 12 differences
  SLD1: 0 differences
  STL1: 3 differences
  Other: 0 differences

Group 1: 1 bytes changed
  Location: 0x00012345 to 0x00012345
  Chunk: SDB1 (offset +12345)
  
  Byte changes:
    0x00012345: 0xA4 (164) → 0x88 (136)
                 Navy      → Brick
```

## Troubleshooting

### Problem: Too many differences

**Solution:** Make sure you ONLY changed one color. Reload the original file and try again.

### Problem: No color value changes found

**Solution:** The color might be stored in a different format (e.g., as an index). Look for any single-byte changes in the SDB1 chunk.

### Problem: Files are different sizes

**Solution:** This shouldn't happen with just a color change. Make sure you're comparing the right files.

## Advanced Testing

### Test Multiple Slots at Once

Once you have a hypothesis about the offset pattern:

1. Change colors for Slots 0, 1, 2 in SC 10/4
2. Note the exact changes made
3. Run comparison
4. Verify that byte offsets match your calculated pattern

### Test Different Setlists

1. Change a color in "NIGHTWISH LEGACY" (setlist 0)
2. Compare with original
3. Verify the setlist_index multiplier

## Recording Your Findings

Create a file `SDB1_COLOR_FINDINGS.md` with:

```markdown
# SDB1 Color Data Structure

## Discovery Date
[Date]

## Test File
soundcheck9_25_25_combined2.PCG

## Findings

### Color Byte Location
- Chunk: SDB1
- Base offset: 0x[OFFSET]
- Pattern: base + (setlist_idx * [X]) + (slot_idx * [Y])

### Test Results
| Setlist | Slot | Expected Offset | Actual Offset | Match? |
|---------|------|----------------|---------------|--------|
| 4       | 0    | 0x[CALC]       | 0x[FOUND]     | ✓/✗    |
| 4       | 1    | 0x[CALC]       | 0x[FOUND]     | ✓/✗    |

### Confirmed Pattern
```python
def get_color_offset(setlist_index, slot_index):
    base = 0x[BASE]
    return base + (setlist_index * [X]) + (slot_index * [Y])
```
```

## Next Steps

Once you've discovered the pattern:

1. Document it in `SDB1_COLOR_FINDINGS.md`
2. Implement `_parse_sdb1_colors()` in `pcg_parser.py`
3. Test with multiple PCG files
4. Update the GUI to display colors for SLS1 format

## Questions?

If you discover the pattern, please:
- Document it thoroughly
- Share findings with the community
- Open a pull request with the implementation

---

**Tool:** `compare_pcg_files.py`  
**Created:** November 25, 2025  
**Purpose:** Reverse-engineer SDB1 color data structure
