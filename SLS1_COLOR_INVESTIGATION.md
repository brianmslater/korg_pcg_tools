# SLS1/SLD1 Color Data Investigation

## Problem Statement

When loading a PCG file into the Kronos, setlist slot colors are displayed correctly. However, our parser cannot find where these colors are stored in the SLS1/SLD1 format.

## User Report

File: `soundcheck9_25_25_combined2.PCG`  
Setlist: "SC 10/4" (index 4)

**Colors visible in Kronos:**
- Slot 0: Navy (164/165)
- Slot 1: Indigo (160)
- Slots 2, 3, 4: Gold (152/153)

## Investigation Results

### What We Found

1. **SDB1 Chunk Discovered**
   - Located at offset 0x0000006C
   - Size: 202,245,888 bytes (202MB!)
   - Contains setlist names and slot names
   - Uses same marker format as SLS1 (`1E 02 00 00`)

2. **SLD1 Chunk**
   - Contains full combi data (7810 bytes per slot)
   - NO color data found in combi structures
   - Searched entire slot data - colors not present

3. **SLS1 Chunk**
   - Very small (just 12 bytes between SLS1 and SLD1)
   - Only contains chunk header
   - No color data

### What We Searched

✓ SLD1 combi data (all 7810 bytes per slot)  
✓ SLS1 chunk area  
✓ SDB1 chunk (found setlist names but not colors)  
✓ Bytes around slot names  
✓ CBK1 headers  
✓ Sequential color patterns  
✓ Scattered color values throughout slots  

### Theories

1. **Colors in SDB1 Metadata Section**
   - SDB1 is 202MB - way larger than just names
   - Color data likely in a metadata section we haven't found
   - Need to analyze SDB1 structure more thoroughly

2. **Colors in Separate Chunk**
   - Might be in an undiscovered chunk type
   - Could be in global settings area

3. **Colors Derived from Combi Data**
   - Might be stored in combi category or other field
   - Kronos might derive colors from combi properties

4. **Colors in Kronos Internal Memory**
   - Possibly not stored in PCG file at all
   - Kronos might maintain separate color database

## Next Steps

### Immediate Actions

1. **Analyze SDB1 Structure**
   - Map out the 202MB SDB1 chunk
   - Find where names end and metadata begins
   - Look for color data patterns

2. **Compare Files**
   - Get a PCG file with known colors
   - Modify colors in Kronos
   - Save and compare binary differences

3. **Check Original Implementation**
   - Look for C# source code or documentation
   - Check if original PCG Tools supports SLS1 colors

### Code to Add

```python
def _parse_sdb1_metadata(self, pcg: PcgFile):
    """Parse SDB1 chunk for setlist metadata including colors."""
    sdb1_offset = self.data.find(b'SDB1')
    if sdb1_offset < 0:
        return
    
    # TODO: Determine SDB1 structure
    # - Find where slot names end
    # - Locate metadata section
    # - Parse color data for each slot
    pass
```

## Workaround

For now, users who need color information should:

1. **Use STL1 Format**
   - Export individual setlists from Kronos
   - STL1 format includes color data
   - Our parser fully supports STL1 colors

2. **Manual Color Assignment**
   - Edit colors in the GUI
   - Save as STL1 format
   - Re-import to Kronos

## Technical Details

### File Structure

```
PCG File
├─ KORG header
├─ PCG1 container
├─ PRG1 (Programs)
├─ CMB1 (Combis)
├─ SLS1 (4-byte header)
├─ SLD1 (4-byte header)
├─ SDB1 (202MB!) ← COLOR DATA LIKELY HERE
│   ├─ Setlist names
│   ├─ Slot names  
│   └─ Metadata section? ← NEED TO FIND THIS
└─ STL1 (Single setlist export with colors)
```

### Known Color Values

```python
SLOT_COLORS = {
    0: "Default",
    136: "Brick", 137: "Brick",
    140: "Burgundy",
    144: "Ivy",
    148: "Olive",
    152: "Gold", 153: "Gold",
    156: "Cacao", 157: "Cacao",
    160: "Indigo",
    164: "Navy", 165: "Navy",
    168: "Rose",
    172: "Lavender", 174: "Lavender",
    176: "Azure",
    180: "Denim", 181: "Denim",
    184: "Silver",
    188: "Slate",
    196: "Charcoal",
}
```

## Files Created During Investigation

- `find_sld1_colors.py` - Search SLD1 for colors
- `analyze_sld1_color_pattern.py` - Pattern analysis
- `analyze_sdb1_structure.py` - SDB1 structure analysis
- `compare_stl1_sld1.py` - Format comparison

## Conclusion

The color data for SLS1/SLD1 format exists in the file (confirmed by Kronos displaying it), but we haven't yet discovered where it's stored. The most likely location is in the SDB1 chunk's metadata section, which requires further analysis.

**Status:** 🔍 Investigation Ongoing  
**Priority:** Medium (workaround available via STL1 format)  
**Difficulty:** High (requires binary format reverse engineering)

---

**Date:** November 25, 2025  
**Investigator:** Kiro AI Assistant  
**User Report:** Brian Slater
