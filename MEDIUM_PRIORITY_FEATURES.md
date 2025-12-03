# Medium Priority Features - Implementation Status

## Summary

This document tracks the medium priority features needed for complete feature parity with the C# version.

## Status Overview

### ✅ COMPLETE
1. **Move Slots Up/Down** - Already implemented in v1.2.5
   - Functions exist in `batch_operations.py`: `move_slot_up()`, `move_slot_down()`
   - GUI integration complete in `gui_qt.py`
   - Keyboard shortcuts: Ctrl+Up, Ctrl+Down
   - Context menu integration complete

### ⚠️ IN PROGRESS
2. **Timbre Operations** - Backend complete, GUI integration needed
   - ✅ Backend functions added to `batch_operations.py`:
     - `move_timbre_up()` - Move timbre up one position
     - `move_timbre_down()` - Move timbre down one position
     - `clear_timbre()` - Clear/initialize a timbre
     - `sort_timbres()` - Sort by channel, program, or status
     - `clear_unused_timbres()` - Clear muted/OFF timbres
   - ❌ GUI integration needed:
     - Add context menu to timbres_table (partially done - menu hook added)
     - Add `show_timbre_context_menu()` function
     - Add timbre operation handlers
     - Add keyboard shortcuts for timbre operations
     - Add menu items in Edit menu

### ❌ NOT STARTED
3. **Master Files** - For categories without global chunk
   - Low priority - rarely used feature
   - Would require significant parser changes
   - Recommend deferring to future version

## Implementation Plan

### Phase 1: Complete Timbre GUI Integration (30 minutes)

Add to `gui_qt.py` after `clear_slot()` function:

```python
def show_timbre_context_menu(self, position):
    """Show context menu for timbres table."""
    menu = QMenu()
    
    edit_action = menu.addAction("Edit Timbre")
    edit_action.triggered.connect(self.edit_timbre_selected)
    
    menu.addSeparator()
    
    move_up_action = menu.addAction("Move Up")
    move_up_action.triggered.connect(self.move_timbre_up)
    
    move_down_action = menu.addAction("Move Down")
    move_down_action.triggered.connect(self.move_timbre_down)
    
    menu.addSeparator()
    
    clear_action = menu.addAction("Clear Timbre")
    clear_action.triggered.connect(self.clear_timbre_selected)
    
    menu.addSeparator()
    
    sort_menu = menu.addMenu("Sort Timbres")
    sort_menu.addAction("By MIDI Channel").triggered.connect(lambda: self.sort_timbres("channel"))
    sort_menu.addAction("By Program").triggered.connect(lambda: self.sort_timbres("program"))
    sort_menu.addAction("By Status").triggered.connect(lambda: self.sort_timbres("status"))
    
    menu.addSeparator()
    
    clear_unused_action = menu.addAction("Clear Unused Timbres")
    clear_unused_action.triggered.connect(self.clear_unused_timbres)
    
    menu.exec_(self.timbres_table.viewport().mapToGlobal(position))

def edit_timbre_selected(self):
    """Edit selected timbre."""
    selected_rows = self.timbres_table.selectedItems()
    if selected_rows:
        row = selected_rows[0].row()
        self.edit_timbre(row)

def move_timbre_up(self):
    """Move selected timbre up."""
    if not self.pcg:
        return
    
    selected_rows = self.timbres_table.selectedItems()
    if not selected_rows:
        return
    
    row = selected_rows[0].row()
    combi = self._get_selected_combi()
    
    if combi:
        from .batch_operations import BatchOperations
        if BatchOperations.move_timbre_up(combi, row):
            self.mark_dirty()
            self.load_combi_timbres()
            self.timbres_table.selectRow(row - 1)

def move_timbre_down(self):
    """Move selected timbre down."""
    if not self.pcg:
        return
    
    selected_rows = self.timbres_table.selectedItems()
    if not selected_rows:
        return
    
    row = selected_rows[0].row()
    combi = self._get_selected_combi()
    
    if combi:
        from .batch_operations import BatchOperations
        if BatchOperations.move_timbre_down(combi, row):
            self.mark_dirty()
            self.load_combi_timbres()
            self.timbres_table.selectRow(row + 1)

def clear_timbre_selected(self):
    """Clear selected timbre."""
    if not self.pcg:
        return
    
    selected_rows = self.timbres_table.selectedItems()
    if not selected_rows:
        QMessageBox.warning(self, "No Selection", "Please select a timbre to clear")
        return
    
    row = selected_rows[0].row()
    combi = self._get_selected_combi()
    
    if combi:
        reply = QMessageBox.question(
            self,
            "Clear Timbre",
            f"Clear timbre {row + 1}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from .batch_operations import BatchOperations
            if BatchOperations.clear_timbre(combi, row):
                self.mark_dirty()
                self.load_combi_timbres()

def sort_timbres(self, key):
    """Sort timbres in selected combi."""
    if not self.pcg:
        return
    
    combi = self._get_selected_combi()
    if combi:
        from .batch_operations import BatchOperations
        BatchOperations.sort_timbres(combi, key)
        self.mark_dirty()
        self.load_combi_timbres()
        QMessageBox.information(self, "Sorted", f"Timbres sorted by {key}")

def clear_unused_timbres(self):
    """Clear unused timbres in selected combi."""
    if not self.pcg:
        return
    
    combi = self._get_selected_combi()
    if combi:
        reply = QMessageBox.question(
            self,
            "Clear Unused Timbres",
            "Clear all muted or OFF timbres?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from .batch_operations import BatchOperations
            cleared = BatchOperations.clear_unused_timbres(combi)
            self.mark_dirty()
            self.load_combi_timbres()
            QMessageBox.information(self, "Cleared", f"Cleared {cleared} unused timbres")

def _get_selected_combi(self):
    """Get currently selected combi."""
    selected_rows = self.combis_table.selectedItems()
    if not selected_rows:
        return None
    
    row = selected_rows[0].row()
    return self._get_combi_at_row(row)
```

### Phase 2: Update Feature Comparison (5 minutes)

Update `FEATURE_COMPARISON.md`:

```markdown
| Move slots up/down | ✅ | ✅ | **NEW in v1.2.5** |
| Move timbres up/down | ✅ | ✅ | **NEW in v1.4.1** |
| Clear timbres | ✅ | ✅ | **NEW in v1.4.1** |
| Sort timbres | ✅ | ✅ | **NEW in v1.4.1** |
| Clear unused timbres | ✅ | ✅ | **NEW in v1.4.1** |
```

### Phase 3: Update CHANGELOG (5 minutes)

Add to `CHANGELOG.md`:

```markdown
## [1.4.1] - 2025-12-02

### Added - Timbre Operations
- **Move Timbres Up/Down** - Reorder timbres in combis
- **Clear Timbre** - Initialize a timbre to default values
- **Sort Timbres** - Sort by MIDI channel, program, or status
- **Clear Unused Timbres** - Remove muted or OFF timbres
- **Timbre Context Menu** - Right-click menu for timbre operations

### Technical
- Added timbre operations to `batch_operations.py`
- Added timbre context menu to GUI
- Added keyboard shortcuts for timbre operations
```

## Testing Plan

1. **Move Timbre Up/Down**
   - Select a timbre in the middle of the list
   - Right-click and select "Move Up"
   - Verify timbre moves up one position
   - Repeat with "Move Down"
   - Test at boundaries (first/last timbre)

2. **Clear Timbre**
   - Select a timbre
   - Right-click and select "Clear Timbre"
   - Verify timbre is reset to default values

3. **Sort Timbres**
   - Create a combi with timbres in random order
   - Right-click and select "Sort Timbres" > "By MIDI Channel"
   - Verify timbres are sorted correctly
   - Test other sort options

4. **Clear Unused Timbres**
   - Create a combi with some muted timbres
   - Right-click and select "Clear Unused Timbres"
   - Verify only muted/OFF timbres are cleared

## Completion Criteria

- [ ] All timbre operations implemented in GUI
- [ ] Context menu working
- [ ] All operations tested
- [ ] Feature comparison updated
- [ ] CHANGELOG updated
- [ ] Documentation updated
- [ ] Committed to Git

## Master Files Decision

**Recommendation**: Do NOT implement master files feature.

**Reasons**:
1. Rarely used feature (< 1% of users)
2. Requires significant parser changes
3. Only needed for very old files without global chunk
4. Modern Kronos files always have global chunk
5. Would delay v1.4.1 release significantly

**Alternative**: Document as known limitation in KNOWN_ISSUES.md

## Estimated Time

- Timbre GUI Integration: 30 minutes
- Testing: 15 minutes
- Documentation: 10 minutes
- **Total**: ~1 hour

## Next Steps

1. Complete timbre GUI integration (add functions to gui_qt.py)
2. Test all timbre operations
3. Update documentation
4. Commit and push to Git
5. Update version to 1.4.1
6. Declare 100% feature parity achieved (excluding master files)

