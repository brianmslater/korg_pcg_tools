# PCG Tools Python - Project Summary

## What Was Created

A cross-platform Python rewrite of PCG Tools for editing Korg synthesizer PCG files, enabling macOS compatibility alongside Windows and Linux.

## Project Structure

```
pcg_tools_python/
├── README.md                    # Project overview
├── QUICKSTART.md               # Quick start guide
├── USAGE.md                    # Detailed usage instructions
├── IMPLEMENTATION_NOTES.md     # Technical implementation details
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation script
├── test_basic.py              # Basic functionality tests
│
├── pcg_tools/                  # Main package
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # Entry point for python -m
│   ├── models.py              # Data structures (PcgFile, Program, Combi, etc.)
│   ├── reader.py              # PCG file parser
│   ├── writer.py              # PCG file writer
│   ├── cli.py                 # Command-line interface
│   └── gui.py                 # Graphical user interface (tkinter)
│
└── examples/
    └── basic_usage.py         # Usage examples
```

## Key Features

### ✓ Implemented

1. **Cross-Platform Support**
   - Windows, macOS, Linux
   - Native look and feel on each platform

2. **Command-Line Interface**
   - Display PCG file information
   - List all patches
   - Export to CSV/TXT formats
   - Launch GUI from command line

3. **Graphical User Interface**
   - Open/Save PCG files
   - Browse programs and combis
   - View patch names and properties
   - Export patch lists

4. **Python API**
   - Read PCG files
   - Access programs and combis
   - Iterate through banks
   - Write modified files

5. **Model Support Framework**
   - Kronos / Kronos X
   - Oasys
   - Triton (all variants)
   - Karma
   - M3 / M50
   - Krome
   - Trinity

### ⚠ Framework Ready (Needs Binary Format Details)

- Full program parameter parsing
- Full combi parameter parsing
- Timbre data extraction
- Set list management
- Category/favorite editing

### 📋 Planned for Future

- Copy/paste operations
- Move/sort patches
- Advanced list generation
- Master file connections
- SNG file support
- Complete parameter editing

## Technology Stack

- **Language**: Python 3.8+
- **CLI Framework**: Click
- **GUI Framework**: tkinter (built-in)
- **Binary Parsing**: struct (built-in)
- **No external dependencies** except Click

## Installation

```bash
cd pcg_tools_python
pip install -r requirements.txt
```

## Usage Examples

### Command Line

```bash
# Get file info
python -m pcg_tools info myfile.pcg

# List patches
python -m pcg_tools list-patches myfile.pcg

# Export to CSV
python -m pcg_tools export myfile.pcg output.csv

# Launch GUI
python -m pcg_tools gui
```

### Python API

```python
from pcg_tools.reader import read_pcg_file

pcg = read_pcg_file("myfile.pcg")
print(f"Model: {pcg.header.model.value}")

for program in pcg.get_all_programs():
    print(f"{program.id}: {program.name}")
```

## Testing

Run basic tests:
```bash
python test_basic.py
```

Expected output:
```
✓ Header creation works
✓ Program creation works
✓ Bank creation works
✓ PCG file creation works
✓ CLI module imports successfully
✓ GUI module imports successfully
```

## Advantages Over Original

1. **Cross-Platform**: Works on macOS, not just Windows
2. **Lightweight**: No .NET Framework required
3. **Scriptable**: Can be used as a Python library
4. **Open Source**: Easy to extend and modify
5. **Modern**: Uses current Python best practices

## Limitations

This is a foundational rewrite focusing on:
- Core file structure
- Basic reading/writing
- User interface framework

Full binary parsing of all patch parameters requires detailed reverse engineering of the PCG format for each model. The framework is in place to add this incrementally.

## Next Steps for Development

1. **Phase 1**: Implement full Kronos program parsing
2. **Phase 2**: Add combi parsing with timbres
3. **Phase 3**: Implement editing features
4. **Phase 4**: Add copy/paste operations
5. **Phase 5**: Support additional models

## Comparison with Original

| Feature | Original (C#) | Python Port |
|---------|--------------|-------------|
| Platform | Windows only | Windows/Mac/Linux |
| GUI | WPF | tkinter |
| CLI | Limited | Full featured |
| API | N/A | Python library |
| Dependencies | .NET Framework | Python 3.8+ |
| File Size | ~5 MB + .NET | ~100 KB |
| Parsing | Complete | Framework ready |
| Editing | Full | Basic |
| Copy/Paste | Yes | Planned |

## Documentation

- **QUICKSTART.md**: Get started in 5 minutes
- **USAGE.md**: Comprehensive usage guide
- **IMPLEMENTATION_NOTES.md**: Technical details
- **examples/basic_usage.py**: Code examples

## License

Free for non-commercial use, following the original PCG Tools license by Michel Keijzers.

## Credits

- **Original PCG Tools**: Michel Keijzers (MikeSoft)
- **Python Port**: Cross-platform rewrite
- **Community**: Korg Forums users and contributors

## Support

For issues or questions:
1. Check the documentation files
2. Review example scripts
3. Refer to original PCG Tools documentation
4. Consult Korg Forums community

## Future Vision

This project provides a solid foundation for a modern, cross-platform PCG editor. With community contributions, it can evolve to match and exceed the original's functionality while remaining lightweight and accessible on all platforms.

The modular architecture makes it easy to:
- Add new Korg models
- Implement new features
- Create custom tools and scripts
- Integrate with other music production software

---

**Status**: Foundation complete, ready for incremental feature development
**Version**: 2.0.0
**Date**: November 2025
