# TODO: Create Test Files for Color and Text Size Mapping

## Purpose
We need test PCG files to map all color and text size values used by the Kronos.

## What We Know So Far

### Confirmed Values
From comparing test files, we found:
- **Burgundy** = 140 (0x8C)
- **Indigo** = 32 (0x20)
- **M (Medium)** = 0 (0x00)
- **XL (Extra Large)** = 16 (0x10)

### Metadata Location
- **STL1 → SBK1 chunk**
- **Byte +24** from slot name: Color (1 byte)
- **Byte +29** from slot name: Text Size (1 byte)

## Test Files Needed

### 1. Text Size Test File
**Filename**: `test_files/TEXT_SIZE_TEST.PCG`

Create a setlist with 5 slots, each with a different text size:
- Slot 0: XS (Extra Small)
- Slot 1: S (Small)
- Slot 2: M (Medium) - already know this is 0
- Slot 3: L (Large)
- Slot 4: XL (Extra Large) - already know this is 16

Name each slot clearly (e.g., "XS Size Test", "S Size Test", etc.)

### 2. Color Test File
**Filename**: `test_files/COLOR_TEST.PCG`

Create a setlist with slots for each available color on the Kronos.
Based on Kronos documentation, the colors are likely:
- Slot 0: Red
- Slot 1: Orange
- Slot 2: Yellow
- Slot 3: Green
- Slot 4: Cyan
- Slot 5: Blue
- Slot 6: Indigo - already know this is 32
- Slot 7: Violet/Purple
- Slot 8: Burgundy - already know this is 140
- Slot 9: Olive
- Slot 10: Navy
- Slot 11: (any other colors available)

Name each slot with its color (e.g., "Red Color", "Orange Color", etc.)

## How to Create

1. On your Kronos, create a new setlist
2. Add slots with the names above
3. Set the text size for each slot in the text size test file
4. Set the color for each slot in the color test file
5. Save/export the PCG file
6. Copy to `korg_pcg_tools/test_files/`

## Analysis Script

Once you create the files, run:
```bash
python3 decode_sbk1_metadata.py
```

This will extract the byte values for each color and text size, allowing us to create complete mapping tables.

## Next Steps After Mapping

1. Update `pcg_tools/models.py` to add `color` and `text_size` fields to `SetListSlot`
2. Update `pcg_tools/pcg_parser.py` to read these values from STL1/SBK1
3. Update `pcg_tools/writer.py` to write these values to STL1/SBK1
4. Update GUI to display and allow editing of color and text size
5. Create mapping constants for color names and size names

## Reference

See `COLOR_SIZE_METADATA_FOUND.md` for detailed technical information about where this data is stored.
