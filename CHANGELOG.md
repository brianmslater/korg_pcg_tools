# Changelog

All notable changes to PCG Tools Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - GM2 Bank Support
- **GM2 Banks Display**: Added support for viewing GM2 banks g(1)-g(9) and g(d)
- **Read-Only ROM Banks**: GM2 banks are marked as read-only with [ROM] indicator
- **Program Names**: 10 GM2 banks with descriptive program names
  - g(1): Piano variations (Grand Piano KSP, Piano Strings, etc.)
  - g(2): Chromatic Percussion (Celesta, Glockenspiel, etc.)
  - g(3): Organ variations (Drawbar Organ, Rock Organ, etc.)
  - g(4): Guitar variations (Nylon Guitar, Jazz Guitar, etc.)
  - g(5): Bass variations (Acoustic Bass, Fingered Bass, etc.)
  - g(6): Strings/Orchestra (Violin, Viola, Cello, etc.)
  - g(7): Ensemble (String Ensemble, Choir Aahs, etc.)
  - g(8): Brass (Trumpet, Trombone, French Horn, etc.)
  - g(9): Reed/Pipe (Soprano Sax, Alto Sax, Oboe, Flute, etc.)
  - g(d): Drum kits (Standard Kit, Room Kit, Power Kit, etc.)
- **Category Information**: GM2 programs include proper category metadata
- **GUI Integration**: 
  - ROM banks show [ROM] indicator in bank selector
  - Edit and Paste buttons disabled for ROM banks
  - Copy from ROM banks is allowed
  - Helpful error messages when trying to edit ROM banks
- **Documentation**: Complete GM2 reference guide and implementation docs

### Technical
- Added `pcg_tools/gm2_data.py` with GM2 program definitions
- Added `is_read_only` flag to Bank model
- Updated GUI to handle read-only banks
- Added `test_gm2_banks.py` and `test_gm_readonly.py` test scripts

## [1.3.0] - 2025-12-01 "Feature Complete"

### 🎉 Major Milestone: Feature Parity Achieved!

This release represents **near-complete feature parity** with the C# version plus improvements.

### Added - Final Features
- **Filter Programs**: Filter by text and favorite status
- **Cut Operation**: Copy + clear in one action (Ctrl+X)
- **Sort Slots**: Sort setlist slots by name or patch
- **Filter UI**: Search bar and favorite filter on Programs tab

### Summary of v1.2.2 → v1.3.0
- **9 major features** added in one session
- **All high-priority features** complete
- **Most medium-priority features** complete
- **Production ready** for daily use

## [1.2.6] - 2025-12-01

### Added - Medium Priority Features
- **Revert to Saved**: Discard all changes and reload last saved version
- **Clear/Initialize**: Reset programs or combis to initialized state
- **Auto-Fill Setlist Slots**: Automatically populate empty slots with programs or combis
- **Auto-Backup**: Always enabled - creates .backup file before overwriting (v1.2.3)
- **File Validation**: Checks file integrity before writing (v1.2.3)

### Technical
- Added `revert_to_saved()` method with confirmation dialog
- Added `clear_selected()` for programs and combis
- Added `auto_fill_slots()` with dialog for patch type selection
- Auto-backup always enabled in writer

## [1.2.5] - 2025-12-01

### Added - Move Up/Down
- **Move Up/Down**: Reorder programs, combis, and setlist slots
- **Keyboard Shortcuts**: Ctrl+Up and Ctrl+Down
- **Context Menus**: Move Up/Down in all context menus
- **Edit Menu**: Move Up/Down commands in Edit menu
- **Selection Preserved**: Selected item stays selected after move

### Technical
- Added `move_patch_up()`, `move_patch_down()` to BatchOperations
- Added `move_slot_up()`, `move_slot_down()` for setlists
- Keyboard shortcuts integrated across all tabs

## [1.2.4] - 2025-12-01

### Added - Batch Operations
- **Sort Bank**: Sort programs/combis by name, category, favorite, engine, or tempo
- **Compact Bank**: Remove empty patches (Init, [Empty, blank names)
- **Remove Duplicates**: Remove duplicate patches by name
- **Capitalize Names**: Apply title case, UPPER, lower, or sentence case
- **Move Favorites to Top**: Reorder bank with favorites first
- **Tools Menu**: New menu with all batch operations
- **Dialogs**: User-friendly dialogs for all operations with previews

### Technical
- New `batch_operations.py` module with BatchOperations class
- Sort, compact, remove duplicates, capitalize, move favorites methods
- Test script: `test_batch_operations.py`

## [1.2.3] - 2025-12-01

### Added - Program Copy/Paste & Patch Assignment
- **Program Copy/Paste**: Copy and paste individual programs
  - Keyboard shortcuts: Ctrl+C (copy), Ctrl+V (paste)
  - Context menus for Programs and Combis tables
  - Preserves destination program ID (doesn't move programs)
  - Copies all properties: name, category, favorite, engine, OSC mode
- **Assign Program to Slot**: Set which program/combi a setlist slot references
  - Enhanced slot edit dialog with patch assignment section
  - Dropdown lists all programs or combis
  - Shows patch ID and name for easy selection
- **Context Menus**: Right-click menus for all tables
  - Programs table: Edit, Copy, Paste
  - Combis table: Edit, Copy (with programs), Paste
  - Slots table: Edit, Copy, Paste, Clear

### Technical
- Extended `Clipboard` class to support programs
- Added `copy_program()` and `paste_program()` methods
- Enhanced slot edit dialog with patch type and patch selectors
- Context menus for programs, combis, and slots tables
- Test script: `test_program_copy_paste.py`

## [1.2.2] - 2025-12-01

### Added - Setlist Slot Copy/Paste
- **Copy/Paste Slots**: Copy and paste setlist slots with all properties
  - Keyboard shortcuts: Ctrl+C (copy), Ctrl+V (paste)
  - Edit menu: Copy and Paste commands
  - Context menu: Right-click for copy/paste/clear options
- **Slot Properties Copied**: Name, patch reference, transpose, volume, color, text size, notes
- **Cross-Setlist Support**: Copy slots between different setlists
- **Clear Slot**: Remove slots via context menu with confirmation
- **Documentation**: New SETLIST_COPY_PASTE.md guide

### Technical
- Extended `Clipboard` class to support setlist slots
- Added `copy_slot()` and `paste_slot()` methods
- Context menu for slots table with edit/copy/paste/clear
- Test script: `test_slot_copy_paste.py`

## [1.2.1] - 2025-11-26

### Fixed - macOS Crash Issue
- **Native Qt Edit Dialog**: Replaced Tkinter dialog with pure Qt implementation
- **macOS Compatibility**: Fixed crash when editing programs/combis on macOS
- **Cross-Platform**: Edit dialog now works on all platforms (macOS, Windows, Linux)

### Technical
- New `qt_edit_dialog.py` - Pure Qt implementation
- Removed Tkinter dependency from GUI editing
- Same functionality, better compatibility

## [1.2.0] - 2025-11-26

### Added - Full Parameter Parsing and Editing
- **Program Parameter Parsing**: Parse all essential program parameters
  - OSC Mode (Single, Double, Drums, EXi, Double Drums)
  - Category and SubCategory (0-16, 0-7)
  - Favorite flag
  - Engine type (HD-1, AL-1, CX-3, STR-1, SGX-1, SGX-2, MOD-7, etc.)
- **Combi Parameter Parsing**: Parse all essential combi parameters
  - Tempo (BPM)
  - Category and SubCategory
  - Favorite flag
- **Timbre Parameter Parsing**: Parse detailed timbre parameters
  - Detune (cents)
  - Transpose (semitones)
  - Key zones (bottom/top keys)
  - Velocity zones (bottom/top velocity)
  - Volume, Pan, Status, MIDI channel
- **Program/Combi Editing**: Edit dialog for programs and combis
  - Edit name (24 characters max)
  - Edit category/subcategory with spinboxes
  - Toggle favorite flag
  - Changes persist correctly to file
- **Qt GUI Integration**: Edit functionality integrated into main GUI
  - Double-click or Edit button to edit programs/combis
  - Changes reflected immediately in table
  - Dirty flag (*) indicates unsaved changes

### Improved
- **Edit Dialog**: Redesigned to match C# PCG Tools layout
- **Category Display**: Show numeric category values in tables
- **Raw Data Write-Back**: Proper byte-level editing at correct offsets
- **Models**: Enhanced with all parsed parameters

### Technical
- New `_extract_program_params()` in pcg_parser.py
- New `_extract_combi_params()` in pcg_parser.py
- Enhanced `_parse_timbres()` for additional parameters
- Updated `EditPatchDialog` with proper raw_data write-back
- Added `_raw_offset` tracking for programs and combis
- Comprehensive test suite for parameter parsing and editing

### Documentation
- **v1.2.0_parameter_parsing.md**: Implementation details
- **v1.2.0_complete.md**: Feature completion summary
- **test_parameter_parsing.py**: Verification script
- **test_edit_programmatic.py**: Edit and persistence tests

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
