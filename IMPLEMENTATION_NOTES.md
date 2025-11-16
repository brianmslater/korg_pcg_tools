# PCG Tools Python - Implementation Notes

## Overview

This is a Python rewrite of the original PCG Tools (C#/WPF) for cross-platform compatibility, particularly to support macOS alongside Windows.

## Architecture

### Core Modules

1. **models.py** - Data structures
   - `PcgFile`: Main container for PCG file data
   - `Program`, `Combi`, `SetListSlot`: Patch types
   - `Bank`: Container for patches
   - `PcgHeader`: File header information
   - `WorkstationModel`: Enum of supported Korg models

2. **reader.py** - PCG file parsing
   - `PcgReader`: Reads and parses PCG binary files
   - Handles different Korg models (Kronos, Oasys, Triton, M3, M50, etc.)
   - Chunk-based parsing (PCG1, PRG1, CMB1, etc.)

3. **writer.py** - PCG file writing
   - `PcgWriter`: Writes PCG files back to disk
   - Currently preserves raw binary data for unmodified sections

4. **cli.py** - Command-line interface
   - Built with Click framework
   - Commands: info, list-patches, export, gui
   - Export formats: CSV, TXT

5. **gui.py** - Graphical interface
   - Built with tkinter (cross-platform)
   - File open/save/save-as
   - Program and Combi browsers
   - Patch list export

## Current Implementation Status

### ✓ Implemented

- Basic PCG file structure parsing
- File header reading (model detection, version)
- Command-line interface framework
- GUI framework with file browser
- Export to CSV and text formats
- Cross-platform compatibility (Windows, macOS, Linux)

### ⚠ Partially Implemented

- Binary chunk parsing (structure in place, needs model-specific details)
- Program/Combi data extraction (framework ready, needs binary format details)
- Category and favorite flag reading

### ✗ Not Yet Implemented

The following features from the original PCG Tools need implementation:

1. **Full Binary Parsing**
   - Complete program parameter extraction
   - Complete combi parameter extraction
   - Timbre data within combis
   - Set list slot data
   - Drum kit data
   - Wave sequence data
   - Global settings

2. **Editing Features**
   - Patch name editing
   - Category/sub-category editing
   - Favorite flag toggling
   - Timbre editing in combis
   - Parameter value editing

3. **Copy/Paste Operations**
   - Copy programs between files
   - Copy combis with referenced programs
   - Copy set list slots
   - Cut/paste functionality
   - Clipboard management

4. **Advanced Features**
   - Move patches up/down
   - Sort patches
   - Compact patches (remove empty slots)
   - Clear patches
   - Master file connections
   - SNG file support

5. **List Generation**
   - Program usage lists
   - Combi content lists (short/long)
   - Differences lists
   - File content lists
   - XML export with XSL

## Binary Format Notes

The PCG file format is chunk-based:

```
Header (16 bytes):
  0-3:   Magic "KORG"
  4:     Product ID (0x68=Kronos, 0x6A=Oasys, etc.)
  5:     File Type (0x01=PCG, 0x02=SNG)
  6:     Major Version
  7:     Minor Version
  8-15:  Flags and reserved

Chunks:
  PCG1: Main PCG data container
    DIV1: Division info
    PRG1: Program data
    CMB1: Combi data
    SLS1: Set list data
    GLB1: Global data
    DKT1: Drum kit data
    WSQ1: Wave sequence data
```

Each chunk has:
- 4 bytes: Chunk ID
- 4 bytes: Size (little-endian)
- N bytes: Data
- Padding to 4-byte boundary

## Model-Specific Differences

Different Korg models have different:
- Bank structures (I-A through I-F, U-A through U-GG, etc.)
- Program sizes (Kronos: 4960 bytes, Oasys: 6174 bytes)
- Combi sizes (Kronos: 7810 bytes, Oasys: 11288 bytes)
- Number of timbres per combi (typically 16)
- Category systems
- Feature support (favorites, set lists, etc.)

## Development Roadmap

### Phase 1: Core Reading (Current)
- ✓ Basic file structure
- ✓ Header parsing
- ✓ Chunk identification
- ⚠ Program/Combi extraction (needs work)

### Phase 2: Full Parsing
- Parse all program parameters
- Parse all combi parameters
- Parse timbres
- Parse categories
- Parse set lists

### Phase 3: Editing
- Modify patch names
- Modify categories
- Toggle favorites
- Edit basic parameters

### Phase 4: Advanced Features
- Copy/paste operations
- Move/sort patches
- Reference tracking
- Master file support

### Phase 5: Polish
- Complete GUI
- All list generation types
- XML export
- Documentation
- Unit tests

## Testing Strategy

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test with real PCG files from each model
3. **Cross-Platform Tests**: Verify on Windows, macOS, Linux

## Contributing

To contribute to this project:

1. Focus on one model at a time (e.g., Kronos)
2. Use hex editors to analyze PCG file structure
3. Compare with original C# source code
4. Add unit tests for new features
5. Update documentation

## References

- Original PCG Tools: https://github.com/DaBlick/PCG-Tools
- Korg Forums: www.korgforums.com
- PCG file format documentation in original source

## License

Free for non-commercial use, following the original PCG Tools license.
