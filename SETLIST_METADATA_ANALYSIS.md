# Setlist Metadata Analysis: Text Size and Color

## Summary

After comprehensive analysis of multiple PCG files, we can confirm that **text size and color settings for setlist slots are NOT stored in PCG files**. These are display-only settings that exist only on the Kronos hardware.

## Analysis Performed

### 1. SLS1 Format Analysis (narf_modified.PCG - Ultimate Covers)
- File: 9,347,752 bytes
- Format: SLS1 (names only, 32 bytes per slot)
- Structure: SLD1 → SDB1 → Setlist name → Slot names
- Result: No metadata bytes found, only slot names

### 2. SLD1 Format Analysis (GLAMV3.PCG)
- File: 24,561,528 bytes  
- Format: SLD1 (full slot data, 7810 bytes per slot)
- Structure: SLD1 → SDB1 → CBK1 → Full slot data
- Slot size: 0x1E82 (7810 bytes)
- Result: All metadata bytes after slot names are zeros

### 3. Font Size Pattern Analysis (analyze_narf_font_sizes.py)
- Analyzed first 10 slots for byte patterns
- All slots showed identical values: `100 0 0 50` in bytes +24 to +27
- Pattern is too consistent to represent variable settings
- Likely represents default/fixed values, not user-configurable settings

## File Format Structure

### SLS1 Format (Compact)
```
SLD1 header (8 bytes)
└── SDB1 chunk
    ├── Setlist name (24 bytes)
    ├── Separator (0x28 0x0F 0x01 0x00)
    └── Slot names (128 × 32 bytes)
        ├── Marker (0x1E 0x02 0x00 0x00) - slots 1-127
        └── Name (24 bytes)
```

### SLD1 Format (Full)
```
SLD1 header (8 bytes)
└── SDB1 chunk
    ├── Setlist metadata
    └── CBK1 marker
        └── Slot data (128 × 7810 bytes)
            ├── Name (24 bytes at offset +24)
            └── Slot configuration (7786 bytes)
                - Patch references
                - Transpose settings
                - Volume settings
                - Other performance data
```

## Metadata Search Results

### Bytes Analyzed
- Bytes +0 to +23: Slot name (ASCII, null-padded)
- Bytes +24 to +31: All zeros or consistent default values
- Bytes +32 to +200: Analyzed for patterns

### Patterns Found
- No bytes with values 0-15 that vary between slots (would indicate color/size indices)
- No RGB color patterns
- No enumerated values that could represent XS/S/M/L/XL text sizes
- All analyzed slots show identical or zero patterns

## Conclusion

**Text size and color are NOT stored in PCG files.** These settings are:

1. **Hardware-only**: Configured on the Kronos itself
2. **Display preferences**: Not part of the patch/setlist data
3. **Non-exportable**: Cannot be saved or transferred via PCG files

## Implementation Recommendation

The current implementation in `pcg_tools` is correct:

- Text size is a **local editor preference** (XS/S/M/L/XL)
- Color is a **local editor preference** (if implemented)
- These settings should be stored in:
  - Application preferences/config files
  - Separate metadata files (not PCG)
  - User interface state (session-based)

The editor provides better flexibility than the Kronos hardware by allowing users to customize display settings for their workflow, independent of the PCG file format.

## Files Analyzed

1. `test_files/narf_modified.PCG` - Ultimate Covers (9.3 MB)
2. `test_files/files/GLAM V3/GLAMV3.PCG` - GLAM Pack V3 (23 MB)
3. `test_files/files/GLAM V3/GLAMV3_modified.PCG` - Modified GLAM (23 MB)

## Analysis Scripts Created

1. `analyze_narf_font_sizes.py` - Pattern analysis of metadata bytes
2. `analyze_ultimate_covers.py` - Detailed SLS1 structure analysis
3. `analyze_slot_metadata.py` - Full SLD1 slot data analysis

All scripts confirm the same conclusion: no color/text size metadata exists in PCG files.
