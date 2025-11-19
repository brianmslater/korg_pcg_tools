# Advanced Features Implementation Plan

**Goal**: Match 100% of original PCG Tools functionality

## Current Status

The Python version has basic copy/paste but is missing the advanced features that make the original PCG Tools powerful.

## Missing Features (Critical)

### 1. Program Reference Tracking ⚠️
**Status**: Foundation created (`reference_tracker.py`)

**What's needed**:
- [x] ReferenceTracker class - tracks which programs are used by combis
- [x] ProgramRemapper class - handles remapping when copying
- [ ] Integrate into GUI to show program usage
- [ ] Display "Used by X combis" in program list
- [ ] Show program references in combi view

### 2. Smart Copy/Paste with Remapping ⚠️
**Status**: Dialog created (`copy_paste_dialog.py`)

**What's needed**:
- [x] Copy/Paste settings dialog
- [ ] Copy combis WITH their referenced programs
- [ ] Detect duplicate programs (bytewise, name, like-name)
- [ ] Automatically remap program references when pasting
- [ ] Handle conflicts and ask user
- [ ] Update clipboard.py to use new system
- [ ] Update operations.py to use remapping

### 3. Advanced Copy Options
**What's needed**:
- [ ] Copy with dependencies
- [ ] Duplicate detection modes:
  - Bytewise (exact binary match)
  - Name match (same name = duplicate)
  - Like-name match (similar name = duplicate, ignore numbers)
- [ ] Skip duplicates option
- [ ] Merge vs Replace options

### 4. Advanced Paste Options
**What's needed**:
- [ ] Paste with automatic remapping
- [ ] Skip empty slots option
- [ ] Overwrite vs Insert modes
- [ ] Show remap preview before pasting
- [ ] Undo support for paste operations

### 5. Bank Reference Display
**What's needed**:
- [ ] Show program usage count in tree view
- [ ] "Used by" column showing combi references
- [ ] Click to navigate to using combis
- [ ] Highlight unused programs
- [ ] Warning when deleting used programs

### 6. Master File Support
**What's needed**:
- [ ] Load master PCG files
- [ ] Reference programs from master files
- [ ] Show master file programs in separate section
- [ ] Copy from master to current file
- [ ] Master file settings

## Implementation Priority

### Phase 1: Core Remapping (CRITICAL)
1. Integrate ReferenceTracker into PcgFile model
2. Update clipboard to track referenced programs
3. Implement basic remapping in paste operations
4. Test with real files

### Phase 2: UI Integration
1. Add "Used by" display in program list
2. Show program references in combi details
3. Add copy/paste settings menu
4. Integrate settings dialog

### Phase 3: Advanced Features
1. Duplicate detection algorithms
2. Master file support
3. Advanced paste options
4. Remap preview dialog

### Phase 4: Polish
1. Undo/redo for all operations
2. Progress indicators for long operations
3. Comprehensive testing
4. Documentation

## Files to Modify

### New Files Created
- ✅ `pcg_tools/reference_tracker.py` - Reference tracking and remapping
- ✅ `pcg_tools/copy_paste_dialog.py` - Settings dialog
- ⚠️ `pcg_tools/remap_preview.py` - Preview remapping before paste
- ⚠️ `pcg_tools/master_file.py` - Master file support

### Files to Update
- ⚠️ `pcg_tools/models.py` - Add reference tracking to PcgFile
- ⚠️ `pcg_tools/clipboard.py` - Use new remapping system
- ⚠️ `pcg_tools/operations.py` - Implement smart paste
- ⚠️ `pcg_tools/gui.py` - Add UI for references and settings
- ⚠️ `pcg_tools/writer.py` - Ensure remapped references are saved

## Testing Requirements

### Test Cases Needed
1. Copy combi with programs → Paste → Verify references work
2. Copy combi → Paste to different bank → Verify remapping
3. Copy multiple combis sharing programs → Verify no duplicates
4. Copy with duplicate detection → Verify correct behavior
5. Paste with conflicts → Verify user is prompted
6. Undo/redo copy/paste → Verify state restoration

### Test Files Needed
- PCG with combis using programs from multiple banks
- PCG with duplicate programs (same name, different data)
- PCG with complex combi dependencies

## Estimated Complexity

**Total Effort**: ~40-60 hours of development

**Breakdown**:
- Reference tracking integration: 8 hours
- Smart copy/paste: 12 hours
- Duplicate detection: 6 hours
- UI integration: 10 hours
- Master file support: 8 hours
- Testing: 8 hours
- Documentation: 4 hours
- Bug fixes: 4-12 hours

## Next Steps

1. **Immediate**: Integrate ReferenceTracker into PcgFile
2. **Next**: Update clipboard to use remapping
3. **Then**: Implement smart paste with remapping
4. **Finally**: Add UI elements and test thoroughly

## Notes

The original PCG Tools has years of development and refinement. This is complex functionality that requires:
- Deep understanding of PCG file format
- Careful handling of program references
- Robust duplicate detection
- Comprehensive testing

This is not a "quick fix" - it's a major feature addition that will take significant time to implement correctly.

---

**Status**: Foundation laid, implementation in progress
**Priority**: HIGH - These are core features users expect
**Complexity**: HIGH - Requires careful design and testing

