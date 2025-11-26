# Changelog

All notable changes to PCG Tools Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-26

### Added - Simple Setlist Editor
- **Simple Setlist Editor**: New standalone GUI for setlist editing
- **Hardware Tested**: Confirmed working on Korg Kronos hardware
- **Setlist Name Editing**: Edit all 16 setlist names
- **Slot Editing**: Complete slot property editing
  - Slot names (24 characters max)
  - Colors (16 official Kronos colors)
  - Text sizes (XS, S, M, L, XL)
  - Transpose (-24 to +24 semitones)
  - Volume (0-127)
  - Notes/descriptions
- **Recent Files**: Quick access to last 10 opened files
- **Window Memory**: Remembers position and size between sessions
- **Unsaved Changes Warning**: Prevents accidental data loss
- **Keyboard Shortcuts**: Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Q
- **Context Menu**: Right-click for quick actions (Edit, Clear, Copy Name)
- **Slot Counter**: Shows X/128 slots used in status bar
- **Configuration Persistence**: Settings saved to ~/.pcg_tools_simple_editor.json

### Improved
- **PCG Writer**: Fixed and confirmed working on hardware
- **Repository Structure**: Cleaned and organized (205 files moved to archive/dev_notes)
- **Documentation**: Complete rewrite of README and QUICKSTART
- **Project Organization**: Added PROJECT_STRUCTURE.md and FEATURE_COMPARISON.md

### Fixed
- **Writer Bug**: SLS1-only updates now work correctly on hardware
- **File Integrity**: Files no longer break when saving setlist changes
- **Setlist Parsing**: All 16 setlists with 128 slots each parse correctly

### Technical
- New `simple_setlist_editor.py` standalone application
- Enhanced `writer.py` with hardware-tested SLS1 updates
- New `bit_utils.py` for binary manipulation
- Configuration management with JSON
- Cross-platform window positioning

### Documentation
- **SIMPLE_EDITOR_GUIDE.md**: Complete guide for setlist editor
- **FEATURE_COMPARISON.md**: Detailed comparison with C# version
- **PROJECT_STRUCTURE.md**: Repository organization guide
- **RELEASE_CHECKLIST.md**: Pre-release verification checklist
- Updated README.md with current features
- Updated QUICKSTART.md with Simple Editor tutorial

## [1.0.0] - 2025-11-21

### Added - Initial Python Port
- **Cross-platform Python rewrite** of PCG Tools
- **Command-line interface** with 7 commands:
  - `info`: Display PCG file information
  - `list-patches`: List all patches
  - `export`: Export patch list to CSV/TXT
  - `program-usage`: Generate program usage report
  - `combi-content`: Generate combi content report
  - `differences`: Compare two PCG files
  - `gui`: Launch GUI (note: has writer issues)
- **PCG File Support**: All Korg models
  - Kronos/Kronos X (all OS versions)
  - Oasys
  - M3/M50
  - Triton (all variants)
  - Karma
  - Krome/Krome EX
  - Kross/Kross 2
  - Trinity
- **Report Generation**:
  - Program usage lists
  - Combi content lists
  - File comparison/differences
  - Export to CSV and TXT formats
- **Setlist Parsing**: Read all 16 setlists with 128 slots each
- **Comprehensive Documentation**:
  - README with quick start
  - INSTALL guide for all platforms
  - USAGE guide with examples
  - QUICK_REFERENCE card
  - TECHNICAL_REFERENCE for developers
  - CONTRIBUTING guide

### Technical
- Pure Python implementation (no .NET required)
- Minimal dependencies (click for CLI, tkinter for GUI)
- Chunk-based PCG file parsing
- Handles multiple PCG format versions
- Cross-platform file paths
- Comprehensive error handling

### Known Issues
- Main GUI has writer issues (breaks files on save)
- No program/combi editing in GUI
- No copy/paste operations
- Setlist editing read-only in main GUI

---

## Comparison with Original C# Version

### Python Version Advantages
- ✅ **Hardware-tested setlist editing** (confirmed on Kronos)
- ✅ **Cross-platform** (Windows, macOS, Linux)
- ✅ **No .NET Framework required**
- ✅ **Full CLI API** (7 commands)
- ✅ **Can be used as Python library**
- ✅ **Open source** (MIT License)
- ✅ **Modern, maintainable codebase**
- ✅ **Reliable writer** (doesn't break files)

### Features from C# Not Yet Implemented
- ❌ Program/Combi editing GUI
- ❌ Copy/paste operations
- ❌ Timbre editing
- ❌ Batch operations (sort, compact, remove duplicates)
- ❌ Program reference editing
- ❌ Multiple windows
- ❌ Multi-language support (15+ languages in C#)
- ❌ SNG file support
- ❌ Legacy model .syx file support

See [FEATURE_COMPARISON.md](FEATURE_COMPARISON.md) for complete details.

---

## Future Roadmap

### High Priority
- [ ] Program/Combi editing GUI
- [ ] Copy/paste operations
- [ ] Batch operations (sort, compact)
- [ ] Program reference editing (change what slots point to)

### Medium Priority
- [ ] Multiple windows support
- [ ] Undo/redo in Simple Editor
- [ ] Master file support
- [ ] Auto-backup
- [ ] More export formats (XML, ASCII table)

### Low Priority
- [ ] Multi-language support
- [ ] SNG file support (songs)
- [ ] Legacy model .syx support
- [ ] Virtual banks (Kronos)
- [ ] Theme support

### Under Consideration
- [ ] Drag and drop
- [ ] Plugin system
- [ ] Web interface
- [ ] Automated tests
- [ ] CI/CD pipeline

---

## Version History

- **1.1.0** (2025-11-26): Simple Setlist Editor, hardware-tested
- **1.0.0** (2025-11-21): Initial Python port with CLI
- **Original** (2019): C# version 3.1.0 by Michel Keijzers

---

## Credits

**Original PCG Tools**: Michel Keijzers (C# version, 2011-2019)
**Python Port**: 2025
**Hardware Testing**: Korg Kronos

---

*For detailed changes, see the git commit history.*
