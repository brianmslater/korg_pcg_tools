# Setlist Data Structure Notes

## Two Chunk System

The Kronos stores setlist data in TWO chunks:

### 1. SLS1 Chunk (Setlist Structure)
**Location:** Early in file (around 0x00000054)
**Contains:**
- Setlist names (16 setlists)
- Basic slot structure (128 slots per setlist)
- Slot names (if custom names are set)

**Structure:**
```
[Marker: 1E 02 00 00]
[Setlist Name: 24 bytes]
[Separator: 28 0F 01 00]
[Slot 0 Name: 24 bytes] (no marker)
[Marker: 1E 02 00 00]
[Slot 1 Name: 24 bytes]
...
[Marker: 1E 02 00 00]
[Slot 127 Name: 24 bytes]
```

**Current Status:** ✅ FULLY PARSED

### 2. SLD1 Chunk (Setlist Data)
**Location:** Later in file (around 0x00A22000+)
**Contains:**
- Actual slot names (the real names used)
- Patch references (which combi/program)
- Transpose settings
- Volume settings
- Color settings
- Other slot parameters

**Example Data Found:**
- "SLEEPING SUN RIT" at 0x00A2218A
- Followed by binary data: `64 00 00 32 09 00 64 3A`
  - Likely contains: volume, transpose, patch bank, patch index, etc.

**Current Status:** ⚠️ NOT YET PARSED

## Why Two Chunks?

The SLS1 chunk provides a quick index/structure, while SLD1 contains the full data. This is similar to how databases work with indexes and data files.

## Implementation Priority

1. ✅ **Phase 1 (COMPLETE):** Parse SLS1 for basic structure
   - Read setlist names
   - Read slot structure
   - Display in GUI

2. ⚠️ **Phase 2 (TODO):** Parse SLD1 for full data
   - Read actual slot names
   - Read patch references
   - Read transpose/volume
   - Read colors
   - Display complete information in GUI

3. 🔄 **Phase 3 (TODO):** Write SLD1 data
   - Update slot names in SLD1
   - Update patch references
   - Update settings
   - Save changes

## Workaround

For now, users can:
- View and edit setlist names (SLS1)
- View basic slot structure (SLS1)
- Set colors (stored in model, needs SLD1 write support)

The full slot data (patch names, references) requires SLD1 parsing.

## Next Steps

To implement full setlist support:
1. Analyze SLD1 binary format
2. Determine slot data structure
3. Parse slot entries
4. Map to SetListSlot model
5. Update GUI to show complete data
6. Implement SLD1 writing

This is a significant undertaking but would provide complete setlist functionality.
