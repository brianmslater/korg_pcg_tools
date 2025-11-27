# PCG Tools v1.2.1 Release Notes

**Release Date:** November 26, 2025  
**Type:** Hotfix Release

## 🎯 What's Fixed

### Native Qt Edit Dialog
Replaced the Tkinter-based edit dialog with a pure Qt implementation, fixing the crash issue on macOS.

## 🐛 Bug Fixes

### macOS Crash Fixed
**Problem:** In v1.2.0, editing programs or combis crashed on macOS with:
```
NSInvalidArgumentException: -[QNSApplication _setup:]: unrecognized selector
```

**Root Cause:** Tkinter and PySide6 (Qt) cannot coexist in the same process on macOS.

**Solution:** Created a native Qt edit dialog (`qt_edit_dialog.py`) that replaces the Tkinter version.

**Result:** ✅ Edit functionality now works perfectly on all platforms!

## ✨ Improvements

### Better User Experience
- **Native Look**: Dialog matches the Qt GUI style
- **Cross-Platform**: Works identically on macOS, Windows, and Linux
- **No Dependencies**: Removed Tkinter dependency from GUI editing
- **Same Features**: All editing functionality preserved

## 📦 What's Included

### New Files
- `pcg_tools/qt_edit_dialog.py` - Pure Qt edit dialog implementation
- `test_qt_dialog.py` - Test script for the Qt dialog

### Modified Files
- `pcg_tools/gui_qt.py` - Uses Qt dialog instead of Tkinter
- `CHANGELOG.md` - Added v1.2.1 entry
- `setup.py` - Version bumped to 1.2.1
- `KNOWN_ISSUES.md` - Marked issue as fixed

## 🚀 Upgrade Instructions

### From v1.2.0
Simply update to v1.2.1 - the crash is fixed!

```bash
# Pull latest changes
git pull origin main

# Or download the release
# https://github.com/brianmslater/korg_pcg_tools/releases/tag/v1.2.1
```

## ✅ Testing

The Qt dialog has been tested and works correctly:
- ✅ Opens without crashing
- ✅ Edits program name, category, favorite
- ✅ Edits combi name, category, favorite
- ✅ Changes persist to file
- ✅ Works on macOS (primary fix)
- ✅ Cross-platform compatible

## 📝 Usage

Same as before - no changes to user workflow:

1. Open PCG file in Qt GUI
2. Go to Programs or Combis tab
3. Double-click or click "Edit" button
4. Make your changes
5. Click OK
6. Save the file

## 🎉 What's Next

With the crash fixed, we can now focus on:
- v1.3.0: Timbres editor window
- Additional editing features
- More parameter support

## 📞 Support

- **Issues:** https://github.com/brianmslater/korg_pcg_tools/issues
- **Documentation:** See README.md and QUICKSTART.md

---

**Full Changelog:** See CHANGELOG.md for complete list of changes
