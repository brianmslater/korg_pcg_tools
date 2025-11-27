# v1.2.0 - Full Parameter Parsing and Editing

**Release Date:** November 26, 2025

## 🎉 Major Features

### Full Parameter Parsing
Parse and display all essential parameters for Programs, Combis, and Timbres:

**Programs:**
- OSC Mode (Single, Double, Drums, EXi, Double Drums)
- Category and SubCategory (0-16, 0-7)
- Favorite flag
- Engine type (HD-1, AL-1, CX-3, STR-1, SGX-1, SGX-2, MOD-7, etc.)

**Combis:**
- Tempo (BPM)
- Category and SubCategory
- Favorite flag

**Timbres:**
- Detune (cents)
- Transpose (semitones)
- Key zones (bottom/top keys)
- Velocity zones (bottom/top velocity)
- Volume, Pan, Status, MIDI channel

### Program/Combi Editing
Professional edit dialogs for Programs and Combis:
- Edit name (24 characters max)
- Edit category/subcategory with spinboxes
- Toggle favorite flag
- Changes persist correctly to file

### Qt GUI Integration
Seamless editing experience:
- Double-click any program/combi to edit
- Click "Edit" button to edit selected item
- Changes reflected immediately in table
- Dirty flag (*) in title indicates unsaved changes

## 🔧 Technical Improvements

- Enhanced `pcg_parser.py` with parameter extraction methods
- Updated `models.py` with all parsed parameters
- Redesigned `edit_dialog.py` with proper byte-level write-back
- Integrated editing into `gui_qt.py`

## 📊 Testing

All features thoroughly tested:
- ✅ Parameter parsing verified with real PCG files
- ✅ Edit functionality tested programmatically
- ✅ Changes persist correctly after save/reload
- ✅ 100% test pass rate

## 📝 Documentation

Complete documentation included:
- Updated CHANGELOG.md
- Implementation details in dev_notes/
- Manual testing guide
- Test scripts for verification

## 🔄 Comparison with C# PCG Tools

v1.2.0 now matches the C# GUI for:
- ✅ Program editing (name, category, subcategory, favorite)
- ✅ Combi editing (name, category, subcategory, favorite)
- ✅ Parameter parsing (all essential parameters)
- ✅ Setlist editing (completed in v1.1.0)

**Coming in v1.3.0:**
- Timbres editor window
- Timbre reordering
- Bulk operations

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/brianmslater/korg_pcg_tools.git
cd korg_pcg_tools

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python3 -m pcg_tools.gui_qt

# Or run the simple setlist editor
python3 simple_setlist_editor.py
```

## 📖 Usage

1. Open a PCG file (File → Open PCG)
2. Navigate to Programs or Combis tab
3. Select a program/combi
4. Click "Edit" or double-click to edit
5. Make your changes
6. Click OK to save changes
7. Save the file (Ctrl+S)

## 🐛 Known Limitations

1. Edit dialog uses Tkinter (not Qt) - temporary solution
2. Category names shown as numbers (0-16) not text names in tables
3. Tempo editing parsed but not yet editable in GUI
4. OSC Mode is read-only (displayed but not editable)
5. Timbres editor not yet implemented (planned for v1.3.0)

## 🙏 Acknowledgments

- Based on the original C# PCG Tools by Michel Keijzers
- Thanks to the Korg Kronos community for testing and feedback

## 📞 Support

- **Issues:** https://github.com/brianmslater/korg_pcg_tools/issues
- **Documentation:** See README.md and QUICKSTART.md
- **Full Release Notes:** See RELEASE_NOTES_v1.2.0.md

---

**Full Changelog:** https://github.com/brianmslater/korg_pcg_tools/blob/main/CHANGELOG.md
