# Hotfix for v1.2.0 - macOS Crash Issue

**Date:** November 26, 2025  
**Issue:** Program/Combi editing crashes on macOS  
**Status:** Hotfix applied, needs v1.2.1 release

## Problem

When running the Qt GUI on macOS and trying to edit a program or combi (double-click or Edit button), the application crashes with:

```
NSInvalidArgumentException: -[QNSApplication _setup:]: unrecognized selector sent to instance
```

## Root Cause

**Tkinter and PySide6 (Qt) cannot coexist in the same process on macOS.**

The edit dialog (`edit_dialog.py`) uses Tkinter, which tries to initialize its own event loop. When Tkinter's `tk.Tk()` is called while Qt is already running, macOS throws an exception because both frameworks try to manage the NSApplication.

## Hotfix Applied

Temporarily disabled the Tkinter edit dialogs in `gui_qt.py`:
- `edit_program()` now shows an info dialog instead
- `edit_combi()` now shows an info dialog instead
- GUI no longer crashes
- Users see a message explaining the temporary limitation

## What Still Works

1. **Parameter Parsing** ✅
   - All program/combi/timbre parameters parse correctly
   - Data is read and displayed properly in tables

2. **Programmatic Editing** ✅
   - `test_edit_programmatic.py` works fine
   - Direct API usage works
   - Changes persist correctly

3. **Simple Setlist Editor** ✅
   - `simple_setlist_editor.py` works perfectly
   - Uses Tkinter exclusively (no Qt conflict)
   - All setlist editing features work

4. **CLI Tools** ✅
   - All command-line tools work
   - No GUI conflicts

## Permanent Fix (v1.2.1)

Replace Tkinter edit dialog with native Qt dialog:

### Option 1: Quick Qt Dialog (Recommended)
Create a simple Qt-based edit dialog:
```python
class QtEditDialog(QDialog):
    def __init__(self, parent, patch, patch_type):
        # Use QLineEdit, QSpinBox, QCheckBox
        # Pure Qt, no Tkinter
```

### Option 2: Inline Editing
Add inline editing to the table:
- Double-click to edit name directly in table
- Right-click menu for category/favorite

### Option 3: Side Panel
Add an edit panel to the right side of the GUI:
- Select item to see properties
- Edit in place without dialog

## Timeline

- **v1.2.0**: Released with hotfix (edit disabled)
- **v1.2.1**: Will include Qt-based edit dialog
- **ETA**: 1-2 days

## Workarounds for Users

### For Setlist Editing
Use the Simple Setlist Editor (no issues):
```bash
python3 simple_setlist_editor.py
```

### For Program/Combi Editing
Wait for v1.2.1, or use programmatic editing:
```python
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

pcg = read_pcg_file("file.PCG")
program = pcg.get_all_programs()[0]
program.name = "New Name"
program.favorite = True
# Update raw_data (see test_edit_programmatic.py)
write_pcg_file(pcg, "file.PCG")
```

## Testing

After hotfix:
```bash
# Should NOT crash
python3 -m pcg_tools.gui_qt
# Open file, go to Programs tab, double-click
# Should show info dialog instead of crashing
```

## Files Modified

- `pcg_tools/gui_qt.py` - Disabled Tkinter edit dialogs
- `KNOWN_ISSUES.md` - Documented the issue
- `HOTFIX_v1.2.0_macOS.md` - This file

## Lessons Learned

1. **Don't mix GUI frameworks** - Tkinter + Qt = crash on macOS
2. **Test on target platform** - This only affects macOS
3. **Have fallback plans** - Programmatic editing still works
4. **Document workarounds** - Users need alternatives

## Next Steps

1. Commit hotfix
2. Update v1.2.0 release notes
3. Start work on v1.2.1 with Qt dialog
4. Test on macOS before release

---

**Status:** Hotfix complete, GUI stable, edit functionality temporarily disabled
