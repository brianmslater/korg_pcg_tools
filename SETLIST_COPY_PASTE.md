# Setlist Slot Copy/Paste Feature

## Overview

The PCG Tools GUI now supports copying and pasting setlist slots, making it easy to duplicate slot configurations across your setlists.

## Features

✅ **Copy Slot** - Copy all properties of a setlist slot to clipboard
✅ **Paste Slot** - Paste clipboard slot to any destination slot
✅ **Keyboard Shortcuts** - Ctrl+C to copy, Ctrl+V to paste
✅ **Context Menu** - Right-click for copy/paste/clear options
✅ **Edit Menu** - Copy and Paste commands in Edit menu

## What Gets Copied

When you copy a setlist slot, ALL of these properties are copied:

- **Slot Name** (24 characters max)
- **Patch Reference** (Program/Combi bank and index)
- **Transpose** (-24 to +24 semitones)
- **Volume** (0-127)
- **Color** (16 Kronos colors)
- **Text Size** (XS, S, M, L, XL)
- **Notes/Description** (512 characters)
- **Hold** flag
- **Patch Type** (Program/Combi/Song)

## How to Use

### Method 1: Keyboard Shortcuts

1. Select a slot in the setlist table
2. Press **Ctrl+C** to copy
3. Select destination slot
4. Press **Ctrl+V** to paste

### Method 2: Edit Menu

1. Select a slot in the setlist table
2. Click **Edit → Copy**
3. Select destination slot
4. Click **Edit → Paste**

### Method 3: Context Menu (Right-Click)

1. Right-click on a slot
2. Select **Copy Slot**
3. Right-click on destination slot
4. Select **Paste Slot**

## Additional Context Menu Options

- **Edit Slot** - Open the slot editor dialog
- **Copy Slot** - Copy slot to clipboard
- **Paste Slot** - Paste from clipboard
- **Clear Slot** - Remove the slot (with confirmation)

## Important Notes

### Slot Position Preserved
When you paste a slot, the **slot index** (position in the setlist) is NOT changed. Only the slot's properties are copied. This means:
- Copying slot 5 and pasting to slot 20 creates a duplicate at position 20
- The original slot 5 remains unchanged

### Cross-Setlist Copying
You can copy a slot from one setlist and paste it into a different setlist:
1. Select Setlist 1
2. Copy a slot
3. Select Setlist 2
4. Paste to any slot position

### Empty Slots
- You can paste into empty slot positions
- A new slot will be created at that position
- You can clear slots using the context menu

### Patch References
The patch reference (Program/Combi) is copied as-is. Make sure the referenced patch exists in your PCG file, or the slot may not work correctly on the Kronos.

## Technical Details

### Implementation
- Uses the `Clipboard` class in `pcg_tools/clipboard.py`
- Supports both Combi copy/paste (with program remapping) and Slot copy/paste
- Preserves all slot properties including raw binary data
- Updates raw_data fields for proper file writing

### File Format
- Slot names are stored in the SLS1 chunk
- Slot metadata (color, transpose, volume) is stored in STL1/SBK1 chunks
- The writer preserves raw_data to maintain all properties

## Testing

Run the test script to verify copy/paste functionality:

```bash
python3 test_slot_copy_paste.py
```

This test:
- Copies a slot from position 0
- Pastes it to position 10
- Verifies all properties match
- Saves and validates the file

## Future Enhancements

Potential improvements for future versions:

- **Multi-select** - Copy/paste multiple slots at once
- **Drag and drop** - Drag slots to reorder
- **Batch operations** - Apply changes to multiple slots
- **Slot templates** - Save favorite slot configurations
- **Undo/redo** - Revert copy/paste operations

## See Also

- [GUI_TIMBRE_EDITING.md](GUI_TIMBRE_EDITING.md) - Combi timbre editing with copy/paste
- [SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md) - Simple setlist editor guide
- [USAGE.md](USAGE.md) - General usage instructions

---

**Version:** 1.2.2 (feature added December 2025)
