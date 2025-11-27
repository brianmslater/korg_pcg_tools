# Manual GUI Testing Guide for v1.2.0

## Test the Edit Functionality

### Setup
1. Run the GUI: `python3 -m pcg_tools.gui_qt`
2. Open a test PCG file: `test_files/files/GLAM V3/GLAMV3.PCG`

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
