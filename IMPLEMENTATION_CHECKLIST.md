# Implementation Checklist
## PCG Tools Python - Feature Parity with C# Version

**Last Updated**: November 25, 2025  
**Status**: Planning Complete, Ready to Start

---

## Phase 1: Foundation ⏳

### Bit Utilities Module ✅ COMPLETE
- [x] Create `pcg_tools/bit_utils.py`
- [x] Implement `get_bits(data, byte_offset, high_bit, low_bit)`
- [x] Implement `set_bits(data, byte_offset, high_bit, low_bit, value)`
- [x] Implement `to_signed_bit(num_bits, value)`
- [x] Implement `from_signed_bit(num_bits, value)`
- [x] Write unit tests for all functions
- [x] Test with known values from C# code
- [x] Verify edge cases (sign bits, overflow)

### OS Version Detection
- [ ] Create `pcg_tools/os_version.py`
- [ ] Define `KronosOsVersion` enum
- [ ] Implement `detect_os_version(pcg_data)`
- [ ] Implement `get_slot_offsets(os_version)`
- [ ] Test with PCG files from each OS version
- [ ] Verify chunk detection (STL1/SBK1)
- [ ] Validate offset calculations

---

## Phase 2: Text Size Implementation ⏳

### Text Size Reading
- [ ] Add `TextSize` enum to `models.py`
- [ ] Implement `text_size` property getter in `SetListSlot`
- [ ] Handle split bit fields (byte +29 bit 4, byte +24 bits 7-6)
- [ ] Test reading from existing files
- [ ] Verify all 5 sizes parse correctly
- [ ] Test with different OS versions

### Text Size Writing & GUI
- [ ] Implement `text_size` property setter in `SetListSlot`
- [ ] Update `writer.py` to persist text size
- [ ] Add text size combo box to GUI
- [ ] Connect GUI to model
- [ ] Test writing and verify in hex editor
- [ ] Load modified file on Kronos and verify display
- [ ] Test all 5 sizes (S, XS, M, L, XL)

---

## Phase 3: Enhanced Transpose Handling ⏳

### Fix Transpose Reading/Writing
- [ ] Review current transpose implementation
- [ ] Implement correct split bit field reading (byte +25 bits 7-5, byte +29 bits 7-5)
- [ ] Implement correct split bit field writing
- [ ] Handle signed 6-bit conversion
- [ ] Test negative transpose values (-24 to -1)
- [ ] Test positive transpose values (0 to +24)
- [ ] Verify on Kronos hardware

---

## Phase 4: Patch Reference Editing ⏳

### Patch Reference Model
- [ ] Add `patch_type` property (Program/Combi/Song)
- [ ] Add `patch_bank_id` property
- [ ] Add `patch_index` property
- [ ] Implement getters for all properties
- [ ] Implement setters for all properties
- [ ] Test reading existing patch references
- [ ] Test changing references
- [ ] Verify with Programs, Combis, and Songs

### Patch Reference GUI
- [ ] Create `PatchReferenceWidget` class
- [ ] Add type selector (Program/Combi/Song)
- [ ] Add bank selector
- [ ] Add patch selector
- [ ] Implement type change handler
- [ ] Populate bank list dynamically
- [ ] Populate patch list dynamically
- [ ] Test selecting different patch types
- [ ] Test browsing banks and patches
- [ ] Apply changes and verify

---

## Phase 5: Description Persistence ⏳

### Verify Description Writing
- [ ] Investigate current description handling
- [ ] Verify 512-character limit
- [ ] Test multi-line descriptions (\r\n)
- [ ] Implement `write_setlist_slot_description()`
- [ ] Test writing short descriptions
- [ ] Test writing 512-character descriptions
- [ ] Test writing multi-line descriptions
- [ ] Verify on Kronos

### Description Editor GUI
- [ ] Replace single-line with `QTextEdit`
- [ ] Add character counter (0 / 512)
- [ ] Implement character limit warning
- [ ] Test multi-line text entry
- [ ] Test character limit enforcement
- [ ] Verify persistence after save

---

## Phase 6: Clear Slot Operation ⏳

### Clear Slot Implementation
- [ ] Create `clear_setlist_slot(slot)` function
- [ ] Clear name (24 bytes)
- [ ] Reset to Program type
- [ ] Reset to bank I-A (0x00)
- [ ] Reset to patch 0
- [ ] Reset volume to 127
- [ ] Reset transpose to 0
- [ ] Reset text size to M
- [ ] Clear description (512 bytes)
- [ ] Test clearing various slots
- [ ] Verify all fields reset
- [ ] Test on Kronos

### Clear Slot GUI
- [ ] Add "Clear Slot" to context menu
- [ ] Implement `clear_selected_slots()` method
- [ ] Add confirmation dialog
- [ ] Test clearing single slot
- [ ] Test clearing multiple slots
- [ ] Verify UI refresh after clear

---

## Phase 7: Advanced Features ⏳

### Swap Slots Operation
- [ ] Implement `swap_setlist_slots(slot1, slot2)`
- [ ] Swap raw data
- [ ] Update indices
- [ ] Add to GUI (context menu or button)
- [ ] Test swapping adjacent slots
- [ ] Test swapping non-adjacent slots

### Batch Operations
- [ ] Implement `batch_set_volume(slots, volume)`
- [ ] Implement `batch_set_transpose(slots, transpose)`
- [ ] Implement `batch_set_text_size(slots, text_size)`
- [ ] Add batch operations dialog to GUI
- [ ] Test with multiple selections
- [ ] Verify all slots updated

### Status Bar
- [ ] Create `StatusBar` class
- [ ] Implement `update_stats(pcg_file)` method
- [ ] Show program count
- [ ] Show combi count
- [ ] Show setlist count
- [ ] Show model type
- [ ] Add to main window
- [ ] Test with different files

### Dirty Flag & Revert
- [ ] Add `is_dirty` flag to window
- [ ] Add `original_data` storage
- [ ] Implement `mark_dirty()` method
- [ ] Implement `update_title()` with asterisk
- [ ] Implement `revert_to_saved()` method
- [ ] Add confirmation dialog
- [ ] Add to File menu
- [ ] Test marking dirty on edits
- [ ] Test revert functionality

---

## Phase 8: Testing & Validation ⏳

### Comprehensive Test Suite
- [ ] Create `test_advanced_setlist_features.py`
- [ ] Test `test_text_size_all_values()`
- [ ] Test `test_transpose_negative_values()`
- [ ] Test `test_patch_reference_editing()`
- [ ] Test `test_description_512_chars()`
- [ ] Test `test_clear_slot()`
- [ ] Test `test_swap_slots()`
- [ ] Test `test_batch_operations()`
- [ ] All tests passing

### Hardware Validation
- [ ] Create test PCG with all features
- [ ] Load on Kronos
- [ ] Verify text sizes display correctly
- [ ] Verify transpose works
- [ ] Verify patch references are correct
- [ ] Verify descriptions show properly
- [ ] Verify colors display correctly
- [ ] Document any issues found
- [ ] Fix any issues
- [ ] Re-test on hardware

---

## Phase 9: Documentation ⏳

### User Documentation
- [ ] Update `USAGE.md` with new features
- [ ] Update `QUICK_REFERENCE.md`
- [ ] Create `ADVANCED_SETLIST_EDITING.md`
- [ ] Add screenshots of new features
- [ ] Add examples of common workflows

### Developer Documentation
- [ ] Update `TECHNICAL_REFERENCE.md` with bit field details
- [ ] Document OS version differences
- [ ] Update `CONTRIBUTING.md` with new modules
- [ ] Add code examples for new features
- [ ] Document testing procedures

---

## Final Checklist ✅

### Code Quality
- [ ] All code follows PEP 8
- [ ] All functions have docstrings
- [ ] Complex logic has comments
- [ ] No debug print statements
- [ ] No TODO comments remaining

### Testing
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Hardware validation complete
- [ ] No known bugs

### Documentation
- [ ] User documentation complete
- [ ] Developer documentation complete
- [ ] CHANGELOG.md updated
- [ ] README.md updated

### Release Preparation
- [ ] Version number updated to 3.0
- [ ] Git tags created
- [ ] Release notes written
- [ ] GitHub release created

---

## Progress Tracking

**Phase 1**: ✅✅✅✅✅✅✅✅ 8/8 tasks (100%) ✅ COMPLETE  
**Phase 2**: ⬜⬜⬜⬜⬜⬜⬜ 0/7 tasks  
**Phase 3**: ⬜⬜⬜⬜⬜⬜⬜ 0/7 tasks  
**Phase 4**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/10 tasks  
**Phase 5**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/12 tasks  
**Phase 6**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/12 tasks  
**Phase 7**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/16 tasks  
**Phase 8**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/17 tasks  
**Phase 9**: ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0/10 tasks  

**Overall Progress**: 8/99 tasks (8%)

---

## Notes

- Update this checklist as tasks are completed
- Mark completed tasks with [x]
- Add notes for any blockers or issues
- Update progress bars weekly

**Status**: Ready to begin Phase 1  
**Next Task**: Create bit_utils.py module
