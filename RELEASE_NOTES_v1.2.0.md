# PCG Tools v1.2.0 Release Notes

**Release Date:** November 26, 2025

## 🎉 What's New in v1.2.0

### Full Parameter Parsing and Editing

v1.2.0 adds comprehensive parameter parsing and editing capabilities for Programs and Combis, bringing the Python version closer to feature parity with the C# PCG Tools.

## ✨ New Features

### 1. Program Parameter Parsing
Parse and display all essential program parameters:
- **OSC Mode**: Single, Double, Drums, EXi, Double Drums
- **Category/SubCategory**: Numeric values (0-16, 0-7)
- **Favorite Flag**: Mark programs as favorites
- **Engine Type**: HD-1, AL-1, CX-3, STR-1, SGX-1, SGX-2, MOD-7, etc.

### 2. Combi Parameter Parsing
Parse and display all essential combi parameters:
- **Tempo**: BPM value
- **Category/SubCategory**: Numeric values (0-16, 0-7)
- **Favorite Flag**: Mark combis as favorites

### 3. Timbre Parameter Parsing
Parse detailed timbre parameters within combis:
- **Detune**: Cents (-1200 to +1200)
- **Transpose**: Semitones (-24 to +24)
- **Key Zones**: Bottom and top key (0-127)
- **Velocity Zones**: Bottom and top velocity (1-127)
- **Volume, Pan, Status, MIDI Channel**: Already existed, now enhanced

### 4. Program/Combi Editing
New edit dialog for programs and combis:
- Edit name (24 characters max)
- Edit category/subcategory using spinboxes
- Toggle favorite flag
- Changes persist correctly when saved

### 5. Qt GUI Integration
Edit functionality fully integrated into main GUI:
- Double-click any program/combi to edit
- Click "Edit" button to edit selected item
- Changes reflected immediately in table
- Dirty flag (*) in title indicates unsaved changes
- All changes persist correctly to file

## 🔧 Technical Improvements

### Parser Enhancements
- `_extract_program_params()`: Extract OSC Mode, Category, Favorite
- `_extract_combi_params()`: Extract Tempo, Category, Favorite
- Enhanced `_parse_timbres()`: Extract Detune, Transpose, Key/Velocity zones

### Edit Dialog Improvements
- Redesigned to match C# PCG Tools layout
- Proper byte-level write-back at correct offsets
- Category number to name mapping
- Validation for all fields

### Data Model Updates
- Added `osc_mode` to Program class
- Added `tempo` to Combi class
- Added `detune`, `transpose`, key/velocity zones to Timbre class
- Added `_raw_offset` tracking for write-back

## 📊 Testing

All features have been thoroughly tested:
- ✅ Parameter parsing verified with real PCG files
- ✅ Edit dialog tested with programs and combis
- ✅ Changes persist correctly after save/reload
- ✅ All tests pass with 100% success rate

Test scripts included:
- `test_parameter_parsing.py`: Verify parsing
- `test_edit_programmatic.py`: Test editing and persistence
- `test_gui_manual.md`: Manual GUI testing guide

## 📝 Documentation

New documentation added:
- `dev_notes/v1.2.0_parameter_parsing.md`: Implementation details
- `dev_notes/v1.2.0_complete.md`: Feature completion summary
- `test_gui_manual.md`: Manual testing guide

## 🔄 Comparison with C# PCG Tools

v1.2.0 now matches the C# GUI for:
- ✅ Program editing (name, category, subcategory, favorite)
- ✅ Combi editing (name, category, subcategory, favorite)
- ✅ Parameter parsing (all essential parameters)
- ⏳ Timbres editor (planned for v1.3.0)

## 🚀 Upgrade Instructions

### From v1.1.0
Simply update to v1.2.0 - all existing files and features remain compatible.

### Installation
```bash
# From source
cd korg_pcg_tools
pip install -e .

# Or run directly
python3 -m pcg_tools.gui_qt
```

## 🐛 Known Limitations

1. **Edit Dialog UI**: Uses Tkinter (not Qt) - temporary solution
2. **Category Names**: Shown as numbers (0-16) not text names in tables
3. **Tempo Editing**: Parsed but not yet editable in GUI
4. **OSC Mode**: Read-only (displayed but not editable)
5. **Timbres Editor**: Not yet implemented (planned for v1.3.0)

## 🔮 What's Next (v1.3.0)

Planned features for the next release:
1. **Timbres Editor Window**: Table view for editing all 16 timbres
2. **Timbre Reordering**: Up/Down buttons to reorder timbres
3. **Bulk Operations**: Clear, Assign program to all timbres
4. **Qt Edit Dialog**: Replace Tkinter with native Qt dialog
5. **Category Name Display**: Show text names instead of numbers

## 🙏 Acknowledgments

- Based on the original C# PCG Tools by Michel Keijzers
- Thanks to the Korg Kronos community for testing and feedback

## 📞 Support

- **Issues**: https://github.com/brianmslater/korg_pcg_tools/issues
- **Documentation**: See README.md and QUICKSTART.md
- **Testing**: See test_gui_manual.md for manual testing guide

---

**Full Changelog**: See CHANGELOG.md for complete list of changes
