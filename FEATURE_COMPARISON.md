# PCG Tools - Feature Comparison

## Original C# Version vs Python Port

### ✅ IMPLEMENTED - Core Features

| Feature | Original | Python | Notes |
|---------|----------|--------|-------|
| **File Operations** |
| Open PCG files | ✓ | ✓ | Working |
| Save PCG files | ✓ | ✓ | Working |
| Save As | ✓ | ✓ | Working |
| Multiple file windows | ✓ | ✓ | MDI support added |
| Revert to saved | ✓ | ⚠️ | Needs implementation |
| Dirty flag (*) | ✓ | ✓ | Working |
| **Model Support** |
| Korg Kronos/Kronos X | ✓ | ✓ | Working |
| Korg Oasys | ✓ | ⚠️ | Parser ready, needs testing |
| Korg Triton (all variants) | ✓ | ⚠️ | Parser ready, needs testing |
| Korg Karma | ✓ | ⚠️ | Parser ready, needs testing |
| Korg M3/M50 | ✓ | ⚠️ | Parser ready, needs testing |
| Korg Krome | ✓ | ⚠️ | Parser ready, needs testing |
| Korg Trinity | ✓ | ⚠️ | Parser ready, needs testing |
| **Display** |
| Show programs | ✓ | ✓ | Working |
| Show combis | ✓ | ✓ | Working |
| Show set lists | ✓ | ❌ | Not implemented |
| Show drum kits | ✓ | ❌ | Not implemented |
| Show wave sequences | ✓ | ❌ | Not implemented |
| Show categories | ✓ | ⚠️ | Structure ready, needs parsing |
| Show favorites | ✓ | ⚠️ | Structure ready, needs parsing |
| Bank list view | ✓ | ✓ | Working |
| **Export** |
| Export to CSV | ✓ | ✓ | Working |
| Export to TXT | ✓ | ✓ | Working |
| Export to XML | ✓ | ❌ | Not implemented |
| Patch list | ✓ | ✓ | Working |
| Program usage list | ✓ | ❌ | Not implemented |
| Combi content list | ✓ | ❌ | Not implemented |
| Differences list | ✓ | ❌ | Not implemented |
| File content list | ✓ | ❌ | Not implemented |
| **Command Line** |
| CLI interface | ✓ | ✓ | Working |
| Batch processing | ✓ | ✓ | Working |

### ⚠️ PARTIALLY IMPLEMENTED

| Feature | Status | What's Missing |
|---------|--------|----------------|
| Edit patch names | ⚠️ | GUI for editing not implemented |
| Edit categories | ⚠️ | GUI for editing not implemented |
| Edit favorites | ⚠️ | GUI for editing not implemented |
| Window management | ⚠️ | Tile/cascade implemented, needs refinement |

### ❌ NOT YET IMPLEMENTED - Major Features

| Feature | Priority | Complexity | Notes |
|---------|----------|------------|-------|
| **Copy/Paste Operations** |
| Copy programs | HIGH | Medium | Core feature |
| Copy combis with programs | HIGH | High | Needs reference tracking |
| Copy set list slots | HIGH | High | Needs reference tracking |
| Cut/paste | HIGH | Medium | Extension of copy |
| Drag and drop | HIGH | High | GUI implementation |
| Clipboard management | HIGH | Medium | Cross-window support |
| **Editing** |
| Edit program names | HIGH | Low | Simple text edit |
| Edit combi names | HIGH | Low | Simple text edit |
| Edit set list names | MEDIUM | Low | Simple text edit |
| Edit categories | MEDIUM | Low | Dropdown selection |
| Toggle favorites | MEDIUM | Low | Checkbox |
| Edit set list descriptions | LOW | Low | Text area |
| **Patch Management** |
| Move patches up/down | HIGH | Medium | With reference update |
| Sort patches | MEDIUM | Medium | Multiple sort options |
| Compact patches | MEDIUM | Medium | Move empty down |
| Clear patches | MEDIUM | Low | Reset to init |
| **Timbre Management** |
| Show timbres window | MEDIUM | Medium | Separate window |
| Edit timbres | MEDIUM | High | Complex parameters |
| Move timbres up/down | LOW | Medium | Within combi |
| Clear timbres | LOW | Low | Reset timbre |
| **Set Lists** |
| Show set lists | HIGH | Medium | New tab |
| Edit set list slots | MEDIUM | Medium | Reference management |
| Set list descriptions | LOW | Low | Text editing |
| **Advanced Lists** |
| Program usage list | MEDIUM | Medium | Reference counting |
| Combi content list (short) | MEDIUM | Medium | Timbre summary |
| Combi content list (long) | LOW | High | Detailed parameters |
| Differences list | LOW | High | Compare two files |
| File content list | LOW | Medium | Bank usage summary |
| **Master Files** |
| Master file support | MEDIUM | High | Reference PCG files |
| Auto-load master files | LOW | Medium | Settings integration |
| Show names from master | MEDIUM | Medium | Cross-file references |
| **SNG Files** |
| Open SNG files | LOW | High | Different format |
| Show song names | LOW | Medium | SNG parsing |
| Show samples | LOW | Medium | SNG parsing |
| **Export Formats** |
| XML export | LOW | Low | Add XML writer |
| XSL stylesheets | LOW | Low | Template files |
| ASCII table format | LOW | Low | Formatted text |
| Cubase instrument files | LOW | Medium | Specific format |
| **Settings** |
| Settings dialog | MEDIUM | Medium | Preferences UI |
| Copy/paste settings | MEDIUM | Low | Options dialog |
| Master file settings | LOW | Medium | File associations |
| Language support | LOW | High | i18n framework |
| **UI Features** |
| Status bar updates | MEDIUM | Low | Dynamic info |
| Window position memory | LOW | Low | Save/restore |
| Keyboard shortcuts | MEDIUM | Low | Key bindings |
| Context menus | MEDIUM | Low | Right-click menus |
| Double-click to edit | MEDIUM | Low | Event handler |
| Multi-select | MEDIUM | Low | Tree view feature |

### 🎯 RECOMMENDED IMPLEMENTATION PRIORITY

#### Phase 1: Essential Editing (1-2 weeks)
1. ✅ Edit patch names (programs/combis)
2. ✅ Edit categories and favorites
3. ✅ Save changes properly
4. ✅ Revert to saved

#### Phase 2: Copy/Paste (2-3 weeks)
1. ✅ Copy programs within file
2. ✅ Copy programs between files
3. ✅ Copy combis with referenced programs
4. ✅ Clipboard management
5. ✅ Drag and drop support

#### Phase 3: Patch Management (1-2 weeks)
1. ✅ Move patches up/down
2. ✅ Sort patches
3. ✅ Compact patches
4. ✅ Clear patches

#### Phase 4: Set Lists (1-2 weeks)
1. ✅ Parse set list data
2. ✅ Display set lists
3. ✅ Edit set list slots
4. ✅ Copy set list slots

#### Phase 5: Advanced Features (2-3 weeks)
1. ✅ Timbre window
2. ✅ Program usage list
3. ✅ Combi content lists
4. ✅ Master file support

#### Phase 6: Polish (1 week)
1. ✅ All export formats
2. ✅ Settings dialog
3. ✅ Keyboard shortcuts
4. ✅ Context menus

### 📊 Current Implementation Status

**Overall Progress: ~35%**

- ✅ Core functionality: 80%
- ⚠️ Editing features: 20%
- ❌ Copy/paste: 0%
- ❌ Advanced lists: 0%
- ⚠️ UI polish: 40%

### 🚀 Quick Wins (Easy to Implement)

These features would add significant value with minimal effort:

1. **Edit patch names** - Simple text input dialog
2. **Toggle favorites** - Single bit flip
3. **Clear patches** - Reset to init values
4. **Context menus** - Right-click options
5. **Keyboard shortcuts** - Key bindings
6. **XML export** - Add XML writer (already have CSV)
7. **Revert to saved** - Reload file
8. **Multi-select** - Already supported by TreeView

### 💡 Key Differences from Original

**Advantages of Python Version:**
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ No .NET Framework required
- ✅ Lightweight and portable
- ✅ Can be used as library
- ✅ Command-line interface
- ✅ Easy to extend

**Current Limitations:**
- ❌ No copy/paste yet
- ❌ No set list support yet
- ❌ No timbre editing yet
- ❌ Limited export formats
- ⚠️ Single bank parsing (needs multi-bank)

### 📝 Notes

- The Python version has a solid foundation with proper PCG parsing
- Core file I/O and display features are working
- Main gap is editing and copy/paste functionality
- Most missing features are UI/workflow rather than technical limitations
- The binary parsing framework is in place for all features

### 🎯 Next Steps

To reach feature parity with the original:

1. **Immediate** (this week):
   - Add edit dialogs for names/categories
   - Implement multi-bank parsing
   - Add set list display

2. **Short-term** (next 2 weeks):
   - Implement copy/paste
   - Add move/sort/compact
   - Improve drag-and-drop

3. **Medium-term** (next month):
   - Add all list generators
   - Implement timbre window
   - Add master file support

4. **Long-term** (next 2 months):
   - SNG file support
   - All export formats
   - Settings/preferences
   - Multi-language support
