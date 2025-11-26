# Simple Setlist Editor

## What It Is

A clean, focused GUI for editing PCG setlist names that **actually works on hardware**!

## Features

✅ **Hardware Tested** - Uses the working writer code directly
✅ **Simple Interface** - Just load, edit, save
✅ **No Extra Modifications** - Only changes what you edit
✅ **Safe** - Doesn't break files like the main GUI

## How to Use

### Launch the Editor
```bash
cd korg_pcg_tools
./edit-setlists
```

Or:
```bash
cd korg_pcg_tools
python3 simple_setlist_editor.py
```

### Edit Setlist Names

1. **Load File**
   - Click "Browse..." 
   - Select your PCG file

2. **Edit Names**
   - Double-click a setlist in the list
   - Or select it and click "Edit Name"
   - Type the new name (max 24 characters)
   - Click "Save" or press Enter

3. **Save File**
   - Click "Save File" to overwrite original
   - Or "Save As..." to create a new file

4. **Test on Kronos**
   - Copy the saved file to USB drive
   - Load on Kronos - it will work! ✅

## Why This Works

This editor:
- Uses the **fixed writer code** directly
- **Only modifies setlist names** - nothing else
- **No extra processing** that breaks files
- **Tested and confirmed working** on hardware

## Interface

```
┌─ Simple Setlist Name Editor ──────────────────┐
│                                               │
│ PCG File: [soundcheck.PCG        ] [Browse...] │
│ ──────────────────────────────────────────── │
│                                               │
│ Setlists:                                     │
│ ┌─────────────────────────────┐  [Edit Name]  │
│ │  1. NIGHTWISH LEGACY        │  [Save File]  │
│ │  2. ULTIMATE COVERS         │  [Save As...] │
│ │  3. MOVIE & TV THEMES       │               │
│ │  4. Set List 004            │               │
│ │  5. Set List 005            │               │
│ │  ...                        │               │
│ └─────────────────────────────┘               │
│                                               │
│ Status: Ready - Load a PCG file to start     │
└───────────────────────────────────────────────┘
```

## Keyboard Shortcuts

- **Double-click** setlist to edit
- **Enter** to save name in edit dialog
- **Escape** to cancel edit

## File Safety

- Original files are never modified unless you click "Save File"
- Use "Save As..." to create copies
- Always test files on hardware before replacing originals

## Limitations

- **Setlist names only** - doesn't edit slot names (yet)
- **24 character limit** - enforced by Kronos format
- **ASCII characters only** - special characters may not work

## Troubleshooting

### "Failed to load file"
- Make sure it's a valid PCG file
- Check file permissions

### "Failed to save file"
- Check disk space
- Make sure you have write permissions
- Try "Save As..." to a different location

### File doesn't load on Kronos
- This shouldn't happen with this editor!
- If it does, please report the issue

## Comparison with Main GUI

| Feature | Simple Editor | Main GUI |
|---------|---------------|----------|
| Setlist names | ✅ Works | ❌ Breaks files |
| Slot editing | ❌ Not yet | ✅ Full featured |
| Hardware compatibility | ✅ Tested | ❌ Files rejected |
| Interface | Simple | Complex |

## Future Enhancements

Planned features:
- Slot name editing
- Batch rename operations
- Undo/redo
- File backup

## Status

✅ **Ready for daily use**
✅ **Hardware tested and working**
✅ **Safe and reliable**

---

**Use this editor for setlist name changes until the main GUI is fixed!**
