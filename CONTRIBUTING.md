# Contributing to PCG Tools Python

## Project Overview

PCG Tools Python is a cross-platform Korg PCG file editor written in pure Python. It provides both GUI and CLI interfaces for managing synthesizer patches.

## Project Structure

```
pcg_tools_python/
├── pcg_tools/                  # Main package
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # Entry point (python -m pcg_tools)
│   ├── models.py              # Data structures (PcgFile, Program, Combi, etc.)
│   ├── reader.py              # PCG file parser
│   ├── writer.py              # PCG file writer
│   ├── pcg_parser.py          # Low-level binary parser
│   ├── clipboard.py           # Copy/paste operations
│   ├── operations.py          # Patch management (move, sort, etc.)
│   ├── edit_dialog.py         # Edit dialog UI
│   ├── list_generators.py     # Report generation
│   ├── gui.py                 # GUI implementation (tkinter)
│   └── cli.py                 # CLI implementation (click)
│
├── docs/                       # Additional documentation
├── examples/                   # Usage examples
├── test_files/                 # Test PCG files
├── test_output/                # Generated test files
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── USAGE.md                   # Detailed usage
├── QUICK_REFERENCE.md         # Quick reference card
├── FEATURE_COMPARISON.md      # vs original PCG Tools
├── IMPLEMENTATION_NOTES.md    # Technical details
├── KRONOS_BANK_STRUCTURE.md   # PCG format reference
├── PROJECT_SUMMARY.md         # Project overview
│
├── test_complete.py           # Comprehensive test suite
├── create_blank_pcg.py        # Utility: create blank PCG files
├── create_complete_blank_pcg.py  # Utility: create full blank PCG
│
├── launch_gui.bat             # Windows GUI launcher
├── run_tests.bat              # Windows test runner
├── requirements.txt           # Python dependencies
└── setup.py                   # Package installation
```

## Development Setup

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- click library

### Installation
```bash
cd pcg_tools_python
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### Running Tests
```bash
python test_complete.py
```

Or on Windows:
```bash
run_tests.bat
```

## Code Organization

### Core Modules

**models.py** - Data structures
- `PcgFile`: Main container
- `Program`: Individual program patch
- `Combi`: Combination patch
- `Bank`: Collection of patches
- `SetList`, `SetListSlot`: Performance organization

**reader.py** - High-level file reading
- `read_pcg_file()`: Main entry point
- Delegates to `pcg_parser.py` for binary parsing

**writer.py** - File writing
- `write_pcg_file()`: Save modified PCG files
- Preserves binary structure

**pcg_parser.py** - Low-level binary parsing
- Chunk-based parsing (PCG1, PRG1, CMB1, etc.)
- Handles multiple file format versions
- Flexible offset handling

**clipboard.py** - Copy/paste logic
- Cross-window clipboard
- Handles program and combi copying
- Manages patch references in combis

**operations.py** - Patch operations
- Move, sort, compact patches
- Clear patches (reset to init)
- Batch operations

**gui.py** - Graphical interface
- Multi-window MDI interface
- Tree view for banks
- Context menus and keyboard shortcuts

**cli.py** - Command-line interface
- 7 commands: info, list-patches, export, etc.
- Uses click framework

## Adding Features

### Adding a New CLI Command

1. Add command to `cli.py`:
```python
@cli.command()
@click.argument('input_file')
def my_command(input_file):
    """My new command."""
    pcg = read_pcg_file(input_file)
    # Your logic here
```

2. Test it:
```bash
python -m pcg_tools my-command test.pcg
```

### Adding a New GUI Feature

1. Add method to `PcgWindow` class in `gui.py`
2. Add menu item or context menu entry
3. Bind keyboard shortcut if needed
4. Test with real PCG files

### Adding Support for a New Model

1. Update `KorgModel` enum in `models.py`
2. Add model detection in `pcg_parser.py`
3. Add model-specific parsing if needed
4. Test with files from that model

## Binary Format Notes

### PCG File Structure
```
PCG1 (Main container)
├── PRG1 (Programs)
│   ├── PBK1 (Program Bank - standard)
│   └── MBK1 (Model Bank - EXi)
├── CMB1 (Combis)
│   └── CBK1 (Combi Bank)
└── SLS1 (Set Lists)
```

### Important Offsets
- Program banks: Patches start at offset +24 or +32
- Combi banks: Patches start at offset +24 or +40
- Bank IDs: At offset +20 or +28 depending on format

See `KRONOS_BANK_STRUCTURE.md` for detailed format information.

## Testing

### Test Files
- Place test PCG files in `test_files/`
- Generated files go to `test_output/`

### Test Suite
`test_complete.py` includes:
1. Basic file operations
2. Clipboard operations
3. Patch operations
4. List generators
5. Edit operations
6. File writing

### Manual Testing
```bash
# Create a blank PCG for testing
python create_blank_pcg.py

# Launch GUI with test file
python -m pcg_tools gui test_output/blank_kronos_full.pcg
```

## Code Style

- Follow PEP 8
- Use type hints where helpful
- Add docstrings to public functions
- Keep functions focused and small
- Comment complex binary parsing logic

## Common Tasks

### Debugging Binary Parsing
```python
# Enable debug output in pcg_parser.py
DEBUG = True

# Or use the examine utility
python examine_pcg.py yourfile.pcg
```

### Creating Test Files
```python
# Minimal test file
python create_blank_pcg.py

# Full 7-bank test file
python create_complete_blank_pcg.py
```

## Known Limitations

1. **Set Lists**: Parsed but not fully editable
2. **Program Parameters**: Basic parsing only
3. **Combi Timbres**: Structure parsed, details limited
4. **Undo/Redo**: Not implemented
5. **Drag and Drop**: Not implemented

## Future Enhancements

### High Priority
- Complete set list editing
- Full parameter editing
- Undo/redo support

### Medium Priority
- Drag and drop between windows
- More export formats
- Batch processing tools

### Low Priority
- Theme support
- Plugin system
- SNG file support

## Getting Help

1. Check existing documentation
2. Review code comments
3. Look at test files for examples
4. Check original PCG Tools for reference

## License

Free for non-commercial use, following the original PCG Tools license.

## Credits

- **Original PCG Tools**: Michel Keijzers (MikeSoft)
- **Python Port**: Complete rewrite for cross-platform support
- **Community**: Korg Forums users

---

**Questions?** Check the documentation or review the code - it's well-commented!
