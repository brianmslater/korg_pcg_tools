# Color and Text Size Metadata - FOUND!

## Location

Color and text size metadata is stored in the **STL1 → SBK1** chunk, NOT in the SLD1 chunk.

### File Structure
```
PCG1 header
├── SLD1 chunk (setlist names only)
│   └── SDB1 (slot names for all 16 setlists)
└── STL1 chunk (setlist data with metadata)
    └── SBK1 (slot data including color/size)
        ├── Header (16 bytes)
        ├── Setlist name (24 bytes)
        └── Slot data (128 slots × ~542 bytes each)
            ├── Slot name (24 bytes)
            ├── Metadata bytes
            │   ├── +24: Color (1 byte)
            │   ├── +29: Text size (1 byte)
            │   └── Other metadata...
            └── Slot notes/description (text data)
```

## Metadata Byte Positions

For each slot in the SBK1 chunk:
- **Slot name**: 24 bytes (ASCII, null-padded)
- **Byte +24** (from slot name start): **Color** (1 byte)
- **Byte +29** (from slot name start): **Text Size** (1 byte)

## Confirmed Values

### Test Case: Movie Themes File

**Slot 0 "Ghostbusters":**
- Original: Burgundy, M → Byte +24 = 140 (0x8C), Byte +29 = 0 (0x00)
- Modified: Indigo, XL → Byte +24 = 32 (0x20), Byte +29 = 16 (0x10)

**Slot 1 "Never Ending Story":**
- Original: Olive, M → Need to verify exact values
- Modified: Burgundy, L → Need to verify exact values

## Color Mapping (Preliminary)

Based on the test:
- Burgundy = 140 (0x8C)
- Indigo = 32 (0x20)
- Olive = ? (need more data)
- Navy = ? (need more data)

## Text Size Mapping

Based on the test:
- M (Medium) = 0 (0x00)
- XL (Extra Large) = 16 (0x10)
- L (Large) = ? (need to check slot 1)
- S (Small) = ?
- XS (Extra Small) = ?

## Slot Size

Each slot in SBK1 is approximately **542 bytes**:
- 24 bytes: Slot name
- ~518 bytes: Metadata and notes/description text

## Next Steps

1. ✅ Found the location of color and text size metadata
2. ⏳ Map all color values (need file with all colors)
3. ⏳ Map all text size values (need file with all sizes)
4. ⏳ Update parser to read these values
5. ⏳ Update writer to write these values
6. ⏳ Update models to include color and text_size fields
7. ⏳ Update GUI to display and edit these values

## Implementation Notes

- The SLD1 chunk contains ONLY slot names (for quick loading)
- The STL1/SBK1 chunk contains FULL slot data including metadata
- Parser must read BOTH chunks to get complete slot information
- Writer must update BOTH chunks when modifying slots

## File Comparison Results

Comparing original (8.9MB) vs modified (48MB) files:
- Original file: Setlist names only (no program/combi data)
- Modified file: Full data including programs and combis
- Only 22 bytes different in the compared region
- All differences are in the STL1/SBK1 chunk metadata bytes

This confirms that color/size data is stored in STL1/SBK1, not SLD1.
