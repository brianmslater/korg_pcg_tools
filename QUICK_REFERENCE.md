# PCG TOOLS - QUICK REFERENCE CARD

## Launch

### GUI
```bash
python -m pcg_tools gui
```
Or double-click: `launch_gui.bat` (Windows)

### CLI
```bash
python -m pcg_tools --help
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+O** | Open PCG file |
| **Ctrl+N** | New window |
| **Ctrl+S** | Save file |
| **Ctrl+C** | Copy selected patches |
| **Ctrl+X** | Cut selected patches |
| **Ctrl+V** | Paste patches |
| **Delete** | Clear selected patches |
| **Double-click** | Edit patch |

---

## Context Menu (Right-Click)

- **Edit...** - Edit patch name/category/favorite
- **Copy** - Copy to clipboard
- **Cut** - Cut to clipboard
- **Paste** - Paste from clipboard
- **Clear** - Reset to init
- **Move Up** - Move patch up one slot
- **Move Down** - Move patch down one slot
- **Sort...** - Sort patches in bank
- **Compact** - Move empty patches to end

---

## CLI Commands

### File Info
```bash
python -m pcg_tools info yourfile.pcg
```

### List Patches
```bash
python -m pcg_tools list-patches yourfile.pcg
```

### Export Patch List
```bash
python -m pcg_tools export yourfile.pcg output.csv
python -m pcg_tools export yourfile.pcg output.txt
```

### Program Usage Report
```bash
python -m pcg_tools program-usage yourfile.pcg usage.csv
```

### Combi Content Report
```bash
python -m pcg_tools combi-content yourfile.pcg content.csv
python -m pcg_tools combi-content yourfile.pcg content.csv --style long
```

### Compare Files
```bash
python -m pcg_tools differences file1.pcg file2.pcg diff.csv
```

---

## Common Tasks

### Edit a Patch
1. Double-click the patch
2. Edit name (max 24 chars)
3. Select category
4. Toggle favorite
5. Click OK

### Copy Patches Between Files
1. Open both files (File → Open PCG...)
2. Select patches in source file
3. Press Ctrl+C
4. Switch to destination file
5. Select destination slot
6. Press Ctrl+V

### Sort Patches
1. Right-click in patch list
2. Select "Sort..."
3. Choose sort method (name/category)
4. Click Sort

### Compact Bank
1. Right-click in patch list
2. Select "Compact"
3. Confirm
4. Empty patches move to end

### Export Usage Report
1. Open PCG file
2. Tools → Export Patch List...
3. Choose filename
4. Select format (CSV/TXT)
5. Click Save

---

## Tips & Tricks

### Multi-Select
- Hold **Ctrl** and click to select multiple patches
- Hold **Shift** and click to select range
- Works with copy/cut/clear operations

### Window Management
- **Window → Tile Horizontally** - Stack windows
- **Window → Tile Vertically** - Side by side
- **Window → Cascade** - Overlapping windows

### Quick Navigation
- Click bank name to expand/collapse
- Use arrow keys to navigate
- Type to search (if implemented)

### Batch Processing
Use CLI commands in scripts:
```bash
for file in *.pcg; do
    python -m pcg_tools program-usage "$file" "${file%.pcg}_usage.csv"
done
```

---

## File Formats

### Supported Input
- `.pcg` - Korg PCG files (all models)

### Supported Output
- `.pcg` - Korg PCG files
- `.csv` - Comma-separated values
- `.txt` - Plain text

---

## Supported Models

- Korg Kronos / Kronos X
- Korg Oasys
- Korg Triton (all variants)
- Korg Karma
- Korg M3 / M50
- Korg Krome
- Korg Trinity

---

## Troubleshooting

### File Won't Open
- Check file is valid PCG format
- Check file isn't corrupted
- Try with different file

### Can't Paste
- Check clipboard has content
- Check destination slot is selected
- Check file is loaded

### Changes Not Saved
- Click Save or press Ctrl+S
- Check for error messages
- Check file isn't read-only

### GUI Won't Launch
- Check Python is installed
- Check tkinter is available
- Run: `python -m tkinter`

---

## Getting Help

### Documentation
- `README_FINAL.md` - Complete guide
- `QUICKSTART.md` - Quick start
- `USAGE.md` - Detailed usage

### Command Help
```bash
python -m pcg_tools --help
python -m pcg_tools COMMAND --help
```

### Test Files
- Use `test_complete.py` to verify installation
- Check `test_output/` for example exports

---

## Version Info

**Version:** 2.0.0  
**Date:** November 14, 2025  
**Status:** Production Ready  

---

*Keep this card handy for quick reference!*
