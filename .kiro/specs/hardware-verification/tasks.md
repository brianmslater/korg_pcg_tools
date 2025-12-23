# Implementation Plan: Hardware Verification

## Overview

Manual hardware verification tests for PCG Tools v1.4.x on Korg Kronos. Run these tests on a Mac connected to your Kronos via USB/SD card.

## Pre-Test Setup

- [ ] 0.1 Kronos powered on and functioning
- [ ] 0.2 USB drive or SD card ready and mounted
- [ ] 0.3 PCG Tools GUI running: `python3 -m pcg_tools.gui_qt`
- [ ] 0.4 Test PCG file opened (use any file from files_2_test/)

## Tasks

- [ ] 1. File Round-Trip Test
  - [ ] 1.1 Open a PCG file, Save As → `roundtrip_test.PCG`
    - Copy to Kronos USB/SD
    - Load on Kronos (DISK mode)
    - Verify file loads without errors
    - _Requirements: 1.1, 1.2_

- [ ] 2. Program Editing Tests
  - [ ] 2.1 Edit program name
    - Select program I-A000
    - Double-click, change name to "HW TEST PROG"
    - Save, copy to Kronos, load
    - Verify name shows "HW TEST PROG"
    - _Requirements: 2.1_

  - [ ] 2.2 Edit program category and favorite
    - Select a program
    - Edit → change category to "Keyboard"
    - Edit → toggle favorite ON
    - Save, copy to Kronos, load
    - Verify category and favorite star
    - _Requirements: 2.2, 2.3_

- [ ] 3. Combi Editing Tests
  - [ ] 3.1 Edit combi name
    - Select combi I-A000
    - Double-click, change name to "HW TEST COMBI"
    - Save, copy to Kronos, load
    - Verify name shows "HW TEST COMBI"
    - _Requirements: 3.1_

- [ ] 4. Timbre Parameter Tests
  - [ ] 4.1 Edit timbre volume
    - Select a combi with multiple timbres
    - Open timbre editor
    - Change Timbre 1 volume to 50, Timbre 2 to 100
    - Save, copy to Kronos, load
    - On Kronos: TIMBRE/TRACK → Mixer
    - Verify volumes match
    - _Requirements: 4.1_

  - [ ] 4.2 Edit timbre MIDI channel
    - Select a combi
    - Open timbre editor
    - Change Timbre 1 MIDI channel to 5
    - Save, copy to Kronos, load
    - Verify Timbre 1 shows Ch 5
    - _Requirements: 4.2_

  - [ ] 4.3 Edit timbre transpose
    - Select a combi
    - Open timbre editor
    - Change Timbre 1 transpose to +12
    - Save, copy to Kronos, load
    - Verify transpose = +12
    - Play keys - should sound one octave higher
    - _Requirements: 4.3_

  - [ ] 4.4 Edit timbre key zone
    - Select a combi
    - Open timbre editor
    - Set Timbre 1 key zone: C3 (48) to C5 (72)
    - Save, copy to Kronos, load
    - Play keys below C3 - should NOT sound
    - Play keys C3-C5 - should sound
    - Play keys above C5 - should NOT sound
    - _Requirements: 4.4_

- [ ] 5. Setlist Editing Tests
  - [ ] 5.1 Edit setlist name
    - Go to Setlists tab
    - Select Setlist 0
    - Edit name to "HW TEST SETLIST"
    - Save, copy to Kronos, load
    - On Kronos: SET LIST mode
    - Verify setlist name
    - _Requirements: 5.1_

  - [ ] 5.2 Edit slot name
    - Select a setlist slot
    - Double-click to edit
    - Change slot name to "TEST SLOT"
    - Save, copy to Kronos, load
    - Verify slot shows "TEST SLOT"
    - _Requirements: 5.2_

  - [ ] 5.3 Edit slot color
    - Select a setlist slot
    - Edit → change color to Red
    - Save, copy to Kronos, load
    - Verify slot displays with red background
    - _Requirements: 5.3_

  - [ ] 5.4 Edit slot volume
    - Select a setlist slot
    - Edit → change volume to 80
    - Save, copy to Kronos, load
    - Check slot volume = 80
    - _Requirements: 5.4_

  - [ ] 5.5 Edit slot transpose
    - Select a setlist slot
    - Edit → change transpose to +5
    - Save, copy to Kronos, load
    - Verify transpose = +5
    - Play keys - should sound 5 semitones higher
    - _Requirements: 5.5_

  - [ ] 5.6 Edit slot description
    - Select a setlist slot
    - Edit → add description "Test description"
    - Save, copy to Kronos, load
    - Check slot description shows the text
    - _Requirements: 5.6_

- [ ] 6. Copy/Paste Tests
  - [ ] 6.1 Copy/paste program within file
    - Select program I-A000
    - Copy (Ctrl+C)
    - Select empty slot U-A000
    - Paste (Ctrl+V)
    - Save, copy to Kronos, load
    - Verify U-A000 matches I-A000
    - _Requirements: 6.1_

  - [ ] 6.2 Copy/paste combi within file
    - Select combi I-A000
    - Copy (Ctrl+C)
    - Select empty combi slot U-A000
    - Paste (Ctrl+V)
    - Save, copy to Kronos, load
    - Verify U-A000 combi has same timbres
    - _Requirements: 6.2_

- [ ] 7. Batch Operation Tests
  - [ ] 7.1 Sort programs
    - Select multiple programs in a bank
    - Edit → Sort → By Name
    - Verify programs reordered alphabetically
    - Save, copy to Kronos, load
    - Verify sorted programs load correctly
    - _Requirements: 7.1_

  - [ ] 7.2 Undo/Redo
    - Make an edit (rename a program)
    - Press Ctrl+Z (Undo)
    - Verify name reverts
    - Press Ctrl+Shift+Z (Redo)
    - Verify name changes back
    - _Requirements: 7.2_

- [ ] 8. Final Checkpoint
  - Record test results in HARDWARE_TESTING.md
  - Update feature-parity-review tasks.md task 10.2.2 if all pass

## Notes

- All tests require physical Kronos hardware
- USB/SD card typically mounts at `/Volumes/KEYBOARD/`
- If a test fails, note the exact error and what was changed
- Tests can be run in any order after setup
