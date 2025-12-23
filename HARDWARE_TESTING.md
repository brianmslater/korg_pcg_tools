# Hardware Testing Checklist - PCG Tools v1.4.x

**Test Date**: December 22, 2025  
**Tester**: _______________  
**Kronos Model**: _______________  
**Kronos OS Version**: _______________

---

## Quick Test List

Copy this checklist to track progress:

```
HARDWARE TESTING - December 2025

Pre-Test:
- [ ] Kronos powered on
- [ ] USB/SD card ready
- [ ] PCG Tools GUI running
- [ ] Test PCG file created and copied to USB/SD

Tests:
- [ ] 1. Round-Trip (load/save without corruption)
- [ ] 2. Program Name Edit
- [ ] 3. Program Category/Favorite
- [ ] 4. Combi Name Edit
- [ ] 5. Timbre Volume
- [ ] 6. Timbre MIDI Channel
- [ ] 7. Timbre Transpose
- [ ] 8. Timbre Key Zone
- [ ] 9. Setlist Name Edit
- [ ] 10. Slot Name Edit
- [ ] 11. Slot Color
- [ ] 12. Slot Volume
- [ ] 13. Slot Transpose
- [ ] 14. Slot Description
- [ ] 15. Copy/Paste Program
- [ ] 16. Copy/Paste Combi
- [ ] 17. Batch Sort
- [ ] 18. Undo/Redo

Result: ___ / 18 PASSED
```

---

## Pre-Test Setup

### 1. Prepare Test Environment
- [ ] Kronos powered on and functioning
- [ ] USB drive or SD card ready
- [ ] Backup of current Kronos data (recommended)
- [ ] PCG Tools GUI running: `python3 -m pcg_tools.gui_qt`

### 2. Create Test PCG File
- [ ] Open a known-good PCG file in PCG Tools
- [ ] Save As → `hardware_test_dec2025.PCG`
- [ ] Copy to USB/SD card: `cp hardware_test_dec2025.PCG /Volumes/KEYBOARD/`

---

## Test 1: Basic File Load/Save Round-Trip

**Purpose**: Verify file can be loaded and saved without corruption

### Steps:
1. [ ] Open original PCG file in PCG Tools
2. [ ] Save As → `roundtrip_test.PCG`
3. [ ] Copy to Kronos USB/SD
4. [ ] Load on Kronos (DISK mode → Load PCG)
5. [ ] Verify file loads without errors
6. [ ] Navigate to a few programs/combis to verify data intact

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 2: Program Name Editing

**Purpose**: Verify program name changes persist on hardware

### Steps:
1. [ ] In PCG Tools, select a program (e.g., I-A000)
2. [ ] Double-click to edit
3. [ ] Change name to "HW TEST PROG"
4. [ ] Save file
5. [ ] Copy to Kronos, load file
6. [ ] Navigate to I-A000
7. [ ] Verify name shows "HW TEST PROG"

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 3: Program Category/Favorite Editing

**Purpose**: Verify category and favorite flag changes

### Steps:
1. [ ] Select a program
2. [ ] Edit → change category to "Keyboard"
3. [ ] Edit → toggle favorite ON
4. [ ] Save, copy to Kronos, load
5. [ ] Verify category shows "Keyboard"
6. [ ] Verify favorite star is displayed

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 4: Combi Name Editing

**Purpose**: Verify combi name changes persist

### Steps:
1. [ ] Select a combi (e.g., I-A000)
2. [ ] Double-click to edit
3. [ ] Change name to "HW TEST COMBI"
4. [ ] Save, copy to Kronos, load
5. [ ] Navigate to combi I-A000
6. [ ] Verify name shows "HW TEST COMBI"

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 5: Combi Timbre Volume

**Purpose**: Verify timbre volume changes

### Steps:
1. [ ] Select a combi with multiple timbres
2. [ ] Open timbre editor (double-click combi → Timbres tab)
3. [ ] Change Timbre 1 volume to 50
4. [ ] Change Timbre 2 volume to 100
5. [ ] Save, copy to Kronos, load
6. [ ] On Kronos, go to combi → TIMBRE/TRACK → Mixer
7. [ ] Verify Timbre 1 = 50, Timbre 2 = 100

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 6: Combi Timbre MIDI Channel

**Purpose**: Verify MIDI channel assignment

### Steps:
1. [ ] Select a combi
2. [ ] Open timbre editor
3. [ ] Change Timbre 1 MIDI channel to 5
4. [ ] Save, copy to Kronos, load
5. [ ] On Kronos, verify Timbre 1 shows Ch 5

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 7: Combi Timbre Transpose

**Purpose**: Verify transpose changes

### Steps:
1. [ ] Select a combi
2. [ ] Open timbre editor
3. [ ] Change Timbre 1 transpose to +12
4. [ ] Save, copy to Kronos, load
5. [ ] Verify Timbre 1 transpose = +12
6. [ ] Play keys - should sound one octave higher

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 8: Combi Timbre Key Zone

**Purpose**: Verify key zone limits

### Steps:
1. [ ] Select a combi
2. [ ] Open timbre editor
3. [ ] Set Timbre 1 key zone: C3 (48) to C5 (72)
4. [ ] Save, copy to Kronos, load
5. [ ] Play keys below C3 - should NOT sound on Timbre 1
6. [ ] Play keys C3-C5 - should sound
7. [ ] Play keys above C5 - should NOT sound on Timbre 1

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 9: Setlist Name Editing

**Purpose**: Verify setlist name changes

### Steps:
1. [ ] Go to Setlists tab
2. [ ] Select Setlist 0
3. [ ] Edit name to "HW TEST SETLIST"
4. [ ] Save, copy to Kronos, load
5. [ ] On Kronos, go to SET LIST mode
6. [ ] Verify setlist name shows "HW TEST SETLIST"

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 10: Setlist Slot Name

**Purpose**: Verify slot name changes

### Steps:
1. [ ] Select a setlist slot (e.g., Slot 0)
2. [ ] Double-click to edit
3. [ ] Change slot name to "TEST SLOT"
4. [ ] Save, copy to Kronos, load
5. [ ] On Kronos, verify slot shows "TEST SLOT"

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 11: Setlist Slot Color

**Purpose**: Verify slot color changes

### Steps:
1. [ ] Select a setlist slot
2. [ ] Edit → change color to Red (or another distinct color)
3. [ ] Save, copy to Kronos, load
4. [ ] On Kronos, verify slot displays with red background

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 12: Setlist Slot Volume

**Purpose**: Verify slot volume changes

### Steps:
1. [ ] Select a setlist slot
2. [ ] Edit → change volume to 80
3. [ ] Save, copy to Kronos, load
4. [ ] On Kronos, check slot volume = 80

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 13: Setlist Slot Transpose

**Purpose**: Verify slot transpose changes

### Steps:
1. [ ] Select a setlist slot
2. [ ] Edit → change transpose to +5
3. [ ] Save, copy to Kronos, load
4. [ ] On Kronos, verify transpose = +5
5. [ ] Play keys - should sound 5 semitones higher

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 14: Setlist Slot Description

**Purpose**: Verify slot description/notes

### Steps:
1. [ ] Select a setlist slot
2. [ ] Edit → add description "Test description text"
3. [ ] Save, copy to Kronos, load
4. [ ] On Kronos, check slot description shows the text

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 15: Copy/Paste Program Within File

**Purpose**: Verify internal copy/paste

### Steps:
1. [ ] Select program I-A000
2. [ ] Copy (Ctrl+C)
3. [ ] Select empty slot (e.g., U-A000)
4. [ ] Paste (Ctrl+V)
5. [ ] Save, copy to Kronos, load
6. [ ] Verify U-A000 has same name/sound as I-A000

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 16: Copy/Paste Combi Within File

**Purpose**: Verify combi copy preserves timbres

### Steps:
1. [ ] Select combi I-A000
2. [ ] Copy (Ctrl+C)
3. [ ] Select empty combi slot (e.g., U-A000)
4. [ ] Paste (Ctrl+V)
5. [ ] Save, copy to Kronos, load
6. [ ] Verify U-A000 combi has same timbres/sound

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 17: Batch Sort Operation

**Purpose**: Verify sort doesn't corrupt data

### Steps:
1. [ ] Select multiple programs in a bank
2. [ ] Edit → Sort → By Name
3. [ ] Verify programs are reordered alphabetically
4. [ ] Save, copy to Kronos, load
5. [ ] Verify sorted programs load and play correctly

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Test 18: Undo/Redo

**Purpose**: Verify undo restores previous state

### Steps:
1. [ ] Make an edit (e.g., rename a program)
2. [ ] Press Ctrl+Z (Undo)
3. [ ] Verify name reverts to original
4. [ ] Press Ctrl+Shift+Z (Redo)
5. [ ] Verify name changes back

**Result**: [ ] PASS  [ ] FAIL

**Notes**: _______________

---

## Summary

| Test | Result |
|------|--------|
| 1. Round-Trip | |
| 2. Program Name | |
| 3. Program Category/Favorite | |
| 4. Combi Name | |
| 5. Timbre Volume | |
| 6. Timbre MIDI Channel | |
| 7. Timbre Transpose | |
| 8. Timbre Key Zone | |
| 9. Setlist Name | |
| 10. Slot Name | |
| 11. Slot Color | |
| 12. Slot Volume | |
| 13. Slot Transpose | |
| 14. Slot Description | |
| 15. Copy/Paste Program | |
| 16. Copy/Paste Combi | |
| 17. Batch Sort | |
| 18. Undo/Redo | |

**Total Passed**: ___ / 18  
**Overall Result**: [ ] ALL PASS  [ ] ISSUES FOUND

---

## Previous Test Results (Historical)

### November 2024 Testing
- ✅ Timbre Volume editing - PASSED
- ✅ Timbre MIDI Channel - PASSED  
- ✅ Timbre Transpose - PASSED
- ✅ Timbre Status - PASSED
- ✅ Timbre Key Zones - PASSED
- ✅ Timbre Velocity Zones - PASSED
- ✅ All 16 timbres simultaneous edit - PASSED
- ✅ Checksum calculation - PASSED

---

## Troubleshooting

### File Won't Load on Kronos
- Checksum may be incorrect - file should auto-calculate on save
- File may be corrupted - try fresh save
- Check file size matches original

### Changes Don't Appear
- Verify correct bank/slot selected
- Check that file was saved before copying
- Ensure USB/SD was properly ejected

### Kronos Shows Error Message
- Note the exact error message
- Try loading original unmodified file to verify hardware works
- Check PCG Tools console for any warnings during save
