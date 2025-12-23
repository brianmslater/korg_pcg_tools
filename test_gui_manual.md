# Manual GUI Testing Guide for v1.3.0+

## Test Files
Use the PCG file in `files_2_test/nw.PCG` for testing.

## New Features to Test

### Feature 1: Undo/Redo Support
1. Run the GUI: `python3 -m pcg_tools.gui_qt`
2. Open `files_2_test/nw.PCG`
3. Edit a program name
4. Press **Ctrl+Z** (or Edit → Undo)
5. Verify the name reverts to original
6. Press **Ctrl+Shift+Z** (or Edit → Redo)
7. Verify the name changes back
8. Make multiple edits, verify undo stack works for all

### Feature 2: Cross-File Copy/Paste
1. Open a PCG file in the first window
2. File → New Window to open a second window
3. Open a different PCG file in the second window
4. In the destination window, select a program slot
5. Edit → Paste from Other Window...
6. Select the source file and patches to copy
7. Click OK and verify patches are copied
8. For combis, verify program remapping dialog appears

### Feature 3: Engine Type Validation
1. Open a PCG file with HD-1 programs in a bank
2. Try to paste an EXi program (AL-1, CX-3, etc.) into that bank
3. Verify warning message appears about engine mismatch
4. Verify paste is blocked to prevent hardware errors

### Feature 4: Save As
1. Open a PCG file
2. File → Save As...
3. Choose a new filename
4. Verify new file is created
5. Verify original file is unchanged
6. Open the new file and verify contents match

### Feature 5: Create User Bank
1. Open a PCG file
2. Tools → Create User Bank...
3. Select a bank that doesn't exist (e.g., U-A, U-B)
4. Click OK
5. Verify the new bank appears in the bank list
6. Verify the bank has 128 empty program slots
7. Save the file and reload to verify persistence

### Feature 6: Missing Bank Auto-Creation
1. Open two PCG files in separate windows
2. In the source file, select programs from a user bank (e.g., U-FF)
3. In the destination file (which doesn't have U-FF), try to paste
4. Edit → Paste from Other Window...
5. If the destination doesn't have the source bank, verify prompt appears
6. Click Yes to create the missing bank
7. Verify the bank is created and paste succeeds

---

## Test the Edit Functionality

### Setup
1. Run the GUI: `python3 -m pcg_tools.gui_qt`
2. Open a test PCG file

### Test 1: Edit Program
1. Go to the **Programs** tab
2. Select any program (e.g., "UPTOWN EP")
3. Click the **Edit** button (or double-click the row)
4. The edit dialog should appear with:
   - ID (read-only)
   - Name field
   - Category spinbox (0-16)
   - SubCategory spinbox (0-7)
   - "Is Favorite" checkbox
5. Make changes:
   - Change the name to "TEST PROGRAM"
   - Change category to 7 (Synth Lead)
   - Change subcategory to 1
   - Check the "Is Favorite" box
6. Click **OK**
7. Verify the table updates with your changes
8. The window title should show an asterisk (*) indicating unsaved changes

### Test 2: Edit Combi
1. Go to the **Combis** tab
2. Select any combi
3. Click the **Edit** button (or double-click the row)
4. The edit dialog should appear (same layout as programs)
5. Make changes
6. Click **OK**
7. Verify the table updates

### Test 3: Save Changes
1. After editing, click **Save** (or Ctrl+S)
2. The file should be saved
3. The asterisk (*) should disappear from the title
4. Close and reopen the file
5. Verify your changes persisted

### Test 4: Cancel Edit
1. Select a program/combi
2. Click **Edit**
3. Make some changes
4. Click **Cancel**
5. Verify the table did NOT update
6. No asterisk should appear

### Expected Results
- ✅ Edit dialog opens for programs
- ✅ Edit dialog opens for combis
- ✅ Changes are reflected in the table
- ✅ Changes persist after save/reload
- ✅ Cancel button discards changes
- ✅ Dirty flag (*) appears when changes are made
- ✅ Double-click also opens edit dialog

### Known Issues
- The edit dialog uses Tkinter (not Qt) - this is temporary
- Category names are shown as numbers (0-16) not text names
- The dialog may look different on different platforms

## If Tests Fail
1. Check the console for error messages
2. Verify the PCG file loaded correctly
3. Try a different PCG file
4. Report the issue with:
   - OS version
   - Python version
   - Error message
   - Steps to reproduce
