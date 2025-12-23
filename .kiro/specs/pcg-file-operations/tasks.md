# Implementation Plan: PCG File Operations

## Overview

This implementation plan covers the core file operation features for PCG Tools: cross-file copy/paste, missing bank creation, engine type validation, Save As functionality, and undo support. All features except undo are verified against the C# PCG Tools implementation.

## Tasks

- [x] 1. Cross-File Copy/Paste System
  - [x] 1.1 Implement window tracking for cross-file operations
    - Add `_open_windows` class variable to `PcgMainWindow`
    - Register/unregister windows on open/close
    - _Requirements: 1.1_
  
  - [x] 1.2 Implement paste from other window dialog
    - Create `paste_from_other_window()` method in gui_qt.py
    - Show dialog listing other open windows
    - Allow selection of source patches
    - _Requirements: 1.1, 1.2_
  
  - [x] 1.3 Implement program paste from source PCG
    - Create `_paste_programs_from_source()` method
    - Deep copy program data to destination slot
    - Set dirty flag after paste
    - _Requirements: 1.2, 1.5_
  
  - [x] 1.4 Implement combi paste with timbre preservation
    - Create `_paste_combis_from_source()` method
    - Preserve timbre program references
    - Option to copy referenced programs
    - _Requirements: 1.3, 1.4, 1.5_

- [x]* 1.5 Write property test for program copy/paste round trip
    - **Property 1: Program Copy/Paste Round Trip**
    - **Validates: Requirements 1.1, 1.2**

- [x]* 1.6 Write property test for combi timbre preservation
    - **Property 2: Combi Copy/Paste Preserves Timbre References**
    - **Validates: Requirements 1.3, 1.4**

- [x] 2. Missing Bank Creation System
  - [x] 2.1 Implement bank detection and creation module
    - Create `bank_creator.py` module
    - Implement `get_missing_banks()` function
    - Implement `insert_bank_into_pcg()` function
    - _Requirements: 2.1, 2.2_
  
  - [x] 2.2 Implement PBK1 chunk creation
    - Create `create_pbk1_chunk()` function
    - Generate correct chunk header (4-byte type, 4-byte size)
    - Initialize 128 empty program slots
    - _Requirements: 2.2, 2.3_
  
  - [x] 2.3 Integrate bank creation into paste workflow
    - Check for missing banks before paste
    - Prompt user to create missing banks
    - Create banks and continue paste
    - _Requirements: 2.1, 2.4_
  
  - [x] 2.4 Add manual bank creation menu option
    - Add "Create User Bank..." to Tools menu
    - Show dialog for bank selection
    - Create selected bank
    - _Requirements: 2.2, 2.3_

- [x]* 2.5 Write property test for bank creation integrity
    - **Property 4: Bank Creation Integrity**
    - **Validates: Requirements 2.2, 2.3, 2.4**

- [x] 3. Engine Type Validation System
  - [x] 3.1 Implement engine type detection
    - Add `_extract_engine()` to pcg_parser.py
    - Detect HD-1 vs EXi from OSC Mode at offset 2558
    - _Requirements: 3.1_
  
  - [x] 3.2 Implement engine compatibility validation
    - Create `_validate_engine_compatibility()` in gui_qt.py
    - Check source program engine vs destination bank engine
    - Return error message if incompatible
    - _Requirements: 3.2, 3.3_
  
  - [x] 3.3 Implement bank engine type detection
    - Create `_get_bank_engine_type()` method
    - Determine bank engine from existing programs
    - Return None for empty banks
    - _Requirements: 3.4_
  
  - [x] 3.4 Integrate validation into paste workflow
    - Call validation before paste operations
    - Display error dialog on mismatch
    - Allow paste to empty banks
    - _Requirements: 3.2, 3.3, 3.4_

- [x]* 3.5 Write property test for engine detection consistency
    - **Property 5: Engine Type Detection Consistency**
    - **Validates: Requirements 3.1**

- [x]* 3.6 Write property test for engine mismatch blocking
    - **Property 6: Engine Mismatch Blocks Paste**
    - **Validates: Requirements 3.2, 3.3**

- [x] 4. Save As Functionality
  - [x] 4.1 Implement Save As method
    - Create `save_as_file()` in gui_qt.py
    - Display file save dialog
    - Write PCG data to new path
    - _Requirements: 4.1, 4.2_
  
  - [x] 4.2 Update file state after Save As
    - Update `filepath` to new path
    - Clear `is_dirty` flag
    - Update window title
    - _Requirements: 4.3, 4.4_
  
  - [x] 4.3 Add Save As menu action
    - Add "Save As..." to File menu
    - Connect to `save_as_file()` method
    - _Requirements: 4.1_

- [x]* 4.4 Write property test for Save As round trip
    - **Property 8: Save As Round Trip**
    - **Validates: Requirements 4.2, 4.3, 4.4**

- [x] 5. Checkpoint - Verify C# Feature Parity
  - Ensure all tests pass
  - Verify cross-file paste works with real PCG files
  - Verify bank creation produces valid PCG structure
  - Verify engine validation matches C# behavior
  - Ask the user if questions arise

- [x] 6. Undo/Redo System (Python Enhancement)
  - [x] 6.1 Implement UndoManager class
    - Create `undo.py` module
    - Implement `Action` dataclass
    - Implement `UndoManager` with undo/redo stacks
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [x] 6.2 Implement UndoableEdit factory methods
    - Create `create_paste_action()` method
    - Create `create_patch_edit()` method
    - Create `create_move_action()` method
    - _Requirements: 5.1_
  
  - [x] 6.3 Integrate undo into GUI
    - Add undo/redo menu actions (Ctrl+Z, Ctrl+Shift+Z)
    - Update menu state based on stack availability
    - Connect to UndoManager
    - _Requirements: 5.2, 5.4_
  
  - [x] 6.4 Add undo support to edit operations
    - Wrap paste operations with undo actions
    - Wrap patch edits with undo actions
    - Clear redo on new edit
    - _Requirements: 5.1, 5.5_

- [x]* 6.5 Write property test for undo stack behavior
    - **Property 9: Undo Stack Behavior**
    - **Validates: Requirements 5.1, 5.2, 5.3**

- [x]* 6.6 Write property test for undo availability
    - **Property 10: Undo Availability**
    - **Validates: Requirements 5.4**

- [x]* 6.7 Write property test for redo clearing
    - **Property 11: Redo Cleared on New Edit**
    - **Validates: Requirements 5.5**

- [x] 7. Final Checkpoint - All Features Complete
  - Ensure all tests pass
  - Run `test_new_features.py` to validate all functionality
  - Verify undo/redo works with all edit operations
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional property-based tests
- Requirements 1-4 are verified against C# PCG Tools implementation
- Requirement 5 (Undo) is a Python-only enhancement not in C#
- All implementations should maintain PCG file integrity
- Cross-file paste requires multiple windows to be open
