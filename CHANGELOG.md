# Changelog

All notable changes to PCG Tools Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-11-16

### Added - The Final 5%!
- **Undo/Redo Support**: Full undo/redo with 50-action history (Ctrl+Z / Ctrl+Y)
- **Set List Editing**: Complete set list slot editing dialog
- **Set List Properties**: Edit set list names and descriptions
- **Revert to Saved**: Explicit revert button to discard changes
- **Enhanced Edit Menu**: Shows undo/redo action descriptions
- **Undo Manager**: Comprehensive undo system with callbacks
- **Action Descriptions**: Clear descriptions of what will be undone/redone

### Improved
- Edit menu now shows what action will be undone/redone
- Better keyboard shortcut integration
- More complete feature parity with original PCG Tools

### Technical
- New `undo.py` module with UndoManager class
- New `setlist_editor.py` module with editing dialogs
- Integrated undo support throughout GUI operations
- Action-based undo system for extensibility

## [2.0.0] - 2025-11-16

### Added
- Complete cross-platform Python rewrite of PCG Tools
- Full GUI with tkinter (works on Windows, macOS, Linux)
- Comprehensive CLI with 7 commands
- Copy/paste operations within and between files
- Patch editing (name, category, favorite)
- Move, sort, and compact operations
- Program usage report generation
- Combi content report generation
- File comparison tool
- Export to CSV and TXT formats
- Multiple window support (MDI)
- Context menus and keyboard shortcuts
- Set list viewing (read-only)
- Support for all Korg models (Kronos, Oasys, Triton, etc.)
- Flexible PCG format parsing (handles multiple format versions)
- EXi bank support (I-AA through I-EE)
- Comprehensive test suite
- Extensive documentation

### Features
- **File Operations**: Open, save, save as
- **Editing**: Patch names, categories, favorites
- **Clipboard**: Copy, cut, paste patches
- **Organization**: Move, sort, compact banks
- **Reports**: Program usage, combi content, file differences
- **Export**: CSV and TXT formats
- **Multi-window**: Work with multiple files simultaneously

### Technical
- Pure Python implementation (no .NET required)
- Minimal dependencies (click for CLI, tkinter built-in)
- Chunk-based PCG file parsing
- Handles multiple PCG format versions automatically
- Preserves all binary data when editing
- Cross-platform file paths
- Comprehensive error handling

### Documentation
- README with quick start guide
- QUICKSTART guide (5 minutes)
- USAGE guide (detailed instructions)
- QUICK_REFERENCE card
- FEATURE_COMPARISON with original
- TECHNICAL_REFERENCE for developers
- CONTRIBUTING guide
- PROJECT_SUMMARY

### Testing
- Comprehensive test suite (test_complete.py)
- Tests all major features
- Verified with real Kronos PCG files
- Cross-platform testing

## [1.0.0] - Original PCG Tools

### Reference
This is a complete rewrite of the original PCG Tools by Michel Keijzers.

Original features:
- Windows-only GUI (.NET Framework)
- Basic file viewing and editing
- Limited command-line support

### Improvements in 2.0.0
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ No .NET Framework required
- ✅ Better CLI (7 commands vs limited)
- ✅ Can be used as Python library
- ✅ Open source and extensible
- ✅ Modern, clean codebase
- ✅ Comprehensive documentation
- ✅ Automated testing

---

## Future Roadmap

### Planned Features
- [ ] Full set list editing
- [ ] Complete parameter editing (oscillators, filters, effects)
- [ ] Undo/redo support
- [ ] Drag and drop between windows
- [ ] More export formats (JSON, XML)
- [ ] Batch processing tools
- [ ] Theme support

### Under Consideration
- [ ] SNG file support (songs)
- [ ] Master file connections
- [ ] Global settings editing
- [ ] Drum track editing
- [ ] Plugin system
- [ ] Web interface

---

## Version History

- **2.0.0** (2025-11-16): Complete Python rewrite, production ready
- **1.0.0** (Original): Windows-only .NET version by Michel Keijzers

---

*For detailed changes, see the git commit history.*
