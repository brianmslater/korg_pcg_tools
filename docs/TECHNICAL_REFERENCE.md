# PCG Tools Python - Technical Reference

## PCG File Format

### Overview
PCG (Program/Combi/Global) files use a chunk-based binary format. Each chunk has a 4-byte ID and contains specific data.

### Main Structure
```
PCG1 (Main container)
├── PRG1 (Programs container)
│   ├── PBK1 (Program Bank - standard banks I-A through I-G)
│   └── MBK1 (Model Bank - EXi banks I-AA through I-EE)
├── CMB1 (Combis container)
│   └── CBK1 (Combi Bank - banks I-A through I-G)
└── SLS1 (Set Lists - optional)
```

## Bank Structure

### Program Banks (PBK1)
```
Offset  Size  Description
------  ----  -----------
0       4     Chunk ID: 'PBK1'
4       4     Chunk size (little-endian)
8       4     Gap/padding
12      4     Number of programs (128)
16      4     Program size (4960 bytes for Kronos)
20      4     Bank ID (0x00000000 for I-A, 0x00010000 for I-B, etc.)
24      N     Program data (128 × 4960 bytes)
```

### EXi Program Banks (MBK1)
```
Offset  Size  Description
------  ----  -----------
0       4     Chunk ID: 'MBK1'
4       4     Chunk size (little-endian)
8       12    Header padding
20      4     Bank ID (0x0C000200 for I-AA, 0x0C010200 for I-AB, etc.)
24      N     Program data (128 × 4960 bytes)
```

### Combi Banks (CBK1)
```
Offset  Size  Description
------  ----  -----------
0       4     Chunk ID: 'CBK1'
4       4     Chunk size (little-endian)
8       24    Header (includes bank info)
32      N     Combi data (128 × 7810 bytes)
```

### Bank ID Encoding

**Standard Banks (I-A through I-G):**
- I-A: 0x00000000
- I-B: 0x00010000
- I-C: 0x00020000
- I-D: 0x00030000
- I-E: 0x00040000
- I-F: 0x00050000
- I-G: 0x00060000

**EXi Banks (I-AA through I-EE):**
- Format: 0x0CXXYYZZ
  - 0x0C: EXi engine indicator
  - XX: Bank letter (00=A, 01=B, etc.)
  - YY: Sub-bank (00=A, 01=B, etc.)
  - ZZ: Usually 0x00

Examples:
- I-AA: 0x0C000200
- I-AB: 0x0C010200
- I-AC: 0x0C020200
- I-AD: 0x0C030200
- I-AE: 0x0C040200

## Patch Structure

### Program (4960 bytes)
```
Offset  Size  Description
------  ----  -----------
0       24    Program name (ASCII, null-terminated)
24      2     Category (main, sub)
26      1     Favorite flag (0=no, 1=yes)
27      4933  Program data (oscillators, filters, effects, etc.)
```

### Combi (7810 bytes)
```
Offset  Size  Description
------  ----  -----------
0       24    Combi name (ASCII, null-terminated)
24      2     Category (main, sub)
26      1     Favorite flag (0=no, 1=yes)
27      N     Timbre data (16 timbres)
...     ...   Effects, controllers, etc.
```

### Timbre Structure (within Combi)
Each combi contains 16 timbres. Each timbre references a program:
```
Offset  Size  Description
------  ----  -----------
0       1     Status (0=off, 1=INT, 2=EXi, etc.)
1       1     Bank type
2       2     Bank ID
4       1     Program number (0-127)
...     ...   Volume, pan, transpose, etc.
```

## Format Variations

### Offset Handling
Different Kronos firmware versions use different offsets:

**Older Format (e.g., GLAMV3.PCG):**
- Programs start at chunk offset +24
- Combis start at chunk offset +24

**Newer Format (e.g., generated files):**
- Programs start at chunk offset +32
- Combis start at chunk offset +40

**Solution:** The parser tries multiple offsets automatically.

### Bank ID Location
Bank IDs can be at different offsets:
- Offset +20 (older format)
- Offset +28 (newer format)

The parser checks both locations.

## Set Lists

### Structure
Set lists are stored in the SLS1 chunk (optional):
```
SLS1 Chunk:
├── Header (8 bytes)
├── Number of set lists (4 bytes)
└── For each set list:
    ├── Name (24 bytes)
    ├── Description (variable)
    ├── Color (1 byte)
    ├── Number of slots (4 bytes)
    └── For each slot (128 max):
        ├── Name (24 bytes)
        ├── Patch type (1 byte: 0=Program, 1=Combi)
        ├── Patch bank (2 bytes)
        ├── Patch number (2 bytes)
        ├── Transpose (1 byte, signed -24 to +24)
        ├── Volume (1 byte, 0-127)
        ├── Hold (1 byte, boolean)
        └── Notes (variable length)
```

### Set List Slot Fields
- **Name**: Slot name (e.g., "Song 1 - Intro")
- **Patch Reference**: Points to a Program or Combi
- **Transpose**: -24 to +24 semitones
- **Volume**: 0-127
- **Hold**: Whether to hold previous sound
- **Notes**: Multi-line performance notes

### Current Implementation Status
- ✅ Set lists are parsed and displayed
- ✅ Slot information shown (name, patch, transpose, volume)
- ✅ Notes editor UI exists
- ⚠️ Notes editing works in memory but may not persist to file
- ❌ Creating new set lists not implemented
- ❌ Reordering slots not implemented

## Categories

### Main Categories
Programs and combis have a main category (0-15):
```
0  = Keyboard
1  = Organ
2  = Bass
3  = Guitar/Plucked
4  = Strings/Ensemble
5  = Brass
6  = Reed/Wind
7  = Lead Synth
8  = Pad/Strings Synth
9  = Bell/Mallet
10 = Drum/Percussion
11 = SE/Hit/Stab
12 = Combination
13 = Vocoder
14 = Drums
15 = User
```

### Sub-Categories
Each main category has 8 sub-categories (0-7) for finer classification.

## Supported Models

### Fully Tested
- Korg Kronos / Kronos X

### Framework Support (Untested)
- Korg Oasys
- Korg Triton (all variants)
- Korg Karma
- Korg M3 / M50
- Korg Krome
- Korg Trinity

## Implementation Notes

### Flexible Parsing
The parser handles format variations by:
1. Trying multiple offsets for patch data
2. Checking multiple locations for bank IDs
3. Validating parsed data (checking for valid names)
4. Falling back to alternative parsing methods

### Binary Reading
Uses Python's `struct` module:
```python
import struct

# Read 4-byte little-endian integer
value = struct.unpack('<I', data[offset:offset+4])[0]

# Read null-terminated string
name = data[offset:offset+24].split(b'\x00')[0].decode('ascii', errors='ignore')
```

### Chunk Navigation
```python
offset = 0
while offset < len(data):
    chunk_id = data[offset:offset+4]
    chunk_size = struct.unpack('<I', data[offset+4:offset+8])[0]
    
    # Process chunk
    process_chunk(chunk_id, data[offset:offset+8+chunk_size])
    
    # Move to next chunk
    offset += 8 + chunk_size
```

## Writing PCG Files

### Preservation Strategy
When writing modified files:
1. Keep original binary structure
2. Only modify changed fields (names, categories, favorites)
3. Preserve all other data (parameters, effects, etc.)
4. Maintain chunk alignment

### Modified Fields
Currently editable:
- Patch names (24 characters max)
- Categories (main and sub)
- Favorite flags
- Patch positions (via move/sort)

### Raw Data Preservation
Each patch stores `raw_data` - the original binary data. When writing:
1. Update name, category, favorite in raw_data
2. Write modified raw_data to file
3. All other parameters preserved

## Debugging

### Enable Debug Output
```python
# In pcg_parser.py
DEBUG = True
```

### Examine Files
```python
from pcg_tools.reader import read_pcg_file

pcg = read_pcg_file('yourfile.pcg')
print(f"Model: {pcg.header.model.value}")
print(f"Program banks: {len(pcg.program_banks)}")
print(f"Combi banks: {len(pcg.combi_banks)}")
```

### Check Bank IDs
```python
for bank in pcg.program_banks:
    print(f"Bank {bank.bank_id}: {len(bank.programs)} programs")
```

## Performance Considerations

### File Size
- Minimal PCG (1 program bank, 1 combi bank): ~1.5 MB
- Full PCG (7 program banks, 7 combi banks): ~10 MB
- With EXi banks: Can exceed 20 MB

### Memory Usage
- Entire file loaded into memory
- Each patch stores raw binary data
- Typical memory usage: 2-3x file size

### Parsing Speed
- Typical file: < 1 second
- Large file with EXi: 2-3 seconds

## Error Handling

### Invalid Files
- Check for PCG1 magic number
- Validate chunk IDs
- Check chunk sizes
- Verify patch counts

### Corrupted Data
- Skip invalid patches
- Use default values for missing data
- Log warnings for suspicious data

### Version Compatibility
- Try multiple parsing strategies
- Fall back to older formats
- Warn about unknown chunks

## Future Enhancements

### Planned
1. Full parameter editing (oscillators, filters, effects)
2. Complete set list editing
3. Timbre editing in combis
4. Sample management (for user samples)

### Under Consideration
1. SNG file support (songs)
2. Master file connections
3. Global settings editing
4. Drum track editing

## References

- Original PCG Tools by Michel Keijzers
- Korg Kronos documentation
- Binary analysis of real PCG files
- Community contributions from Korg Forums

---

*Last updated: November 16, 2025*
