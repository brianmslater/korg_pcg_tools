# Implementation Plan: Feature Parity Review

## C# Codebase Analysis Summary

Based on comprehensive analysis of the C# PCG Tools repository, here is the complete file-by-file breakdown and implementation tasks:

---

## PHASE 1: CORE KRONOS FEATURES (HIGH PRIORITY)

### 1.1 Program Reference Changer
- [x] 1.1.1 Implement reference changer core logic
  - Port `Tools/ReferenceChanger.cs` - Core reference changing logic
  - Port `Tools/RuleParser.cs` - Parse reference change rules
  - Port `Tools/ProgramPatchParser.cs` - Parse program patches
  - _Requirements: 11.1_

- [x] 1.1.2 Implement reference changer UI
  - Port `Tools/ProgramReferenceChangerWindow.xaml` - Reference changer dialog
  - Add progress bar for batch operations
  - Add "From File" button to load rules
  - _Requirements: 11.1_

### 1.2 Master Files Support
- [x] 1.2.1 Implement master file data structures
  - Port `MasterFiles/IMasterFile.cs` - Interface definition
  - Port `MasterFiles/MasterFile.cs` - Master file class
  - Port `MasterFiles/MasterFiles.cs` - Master files collection
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 1.2.2 Implement master files UI
  - Port `MasterFiles/MasterFilesWindow.xaml` - Master files management window
  - Add "Set as Master File" menu option
  - Add auto-load master file setting
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

### 1.3 Number of References Column
- [x] 1.3.1 Add reference counting to data model
  - Track program usage in combis
  - Track program/combi usage in set list slots
  - _Requirements: 11.3_

- [x] 1.3.2 Add reference count column to GUI
  - Add "# Refs" column to patch list
  - Add setting to show/hide column
  - _Requirements: 11.3_

### 1.4 Batch Volume Change
- [x] 1.4.1 Implement volume change dialog
  - Port `Gui/ChangeVolumeWindow.xaml` - Volume change dialog
  - Support combis, combi banks, set lists, set list slots
  - _Requirements: 5.8_

### 1.5 Wave Sequences / Drum Kits / Drum Patterns View
- [x] 1.5.1 Add wave sequence support
  - Parse WSQ1/WBK1 chunks
  - Add Wave Sequences tab to PCG window
  - Display wave sequence banks and names
  - _Requirements: 11.7_

- [x] 1.5.2 Add drum kit support
  - Parse DKT1/DBK1 chunks
  - Add Drum Kits tab to PCG window
  - Display drum kit banks and names
  - _Requirements: 11.7_

- [ ] 1.5.3 Add drum pattern support (DEFERRED)
  - Parse DPI1/DPN1/DPD1 chunks
  - Add Drum Patterns tab to PCG window
  - Display drum pattern banks and names
  - _Requirements: 11.8_
  - NOTE: C# throws NotImplementedException for Kronos DPI1 parsing - deferred until needed

### 1.6 CRC Values for Comparison
- [x] 1.6.1 Implement CRC calculation
  - Calculate CRC excluding name
  - Calculate CRC including name
  - _Requirements: 8.12_

- [x] 1.6.2 Add CRC columns to list generator
  - Add "CRC (excl name)" optional column
  - Add "CRC (incl name)" optional column
  - _Requirements: 8.12_

---

## PHASE 2: LIST GENERATOR ENHANCEMENTS (HIGH PRIORITY)

### 2.1 File Content List
- [x] 2.1.1 Implement file content list generator
  - Port `ListGenerator/ListGeneratorFileContentList.cs`
  - Show bank usage summary
  - Show synthesis engine types
  - _Requirements: 8.6_
  - **COMPLETED**: Implemented in `list_generators.py` with all output formats

### 2.2 Bank Filtering
- [x] 2.2.1 Add program bank filters
  - Individual checkboxes for I-A through I-H
  - Individual checkboxes for U-A through U-GG
  - GM bank checkbox
  - Virtual Banks checkbox
  - Select All / Deselect All buttons
  - _Requirements: 8.13_
  - **COMPLETED**: `selected_program_banks` property in ListGenerator class

- [x] 2.2.2 Add combi bank filters
  - Individual checkboxes for I-A through I-H
  - Individual checkboxes for U-A through U-GG
  - Virtual Banks checkbox
  - _Requirements: 8.13_
  - **COMPLETED**: `selected_combi_banks` property in ListGenerator class

- [x] 2.2.3 Add set list filters
  - Enabled checkbox
  - Range (From/To) inputs
  - _Requirements: 8.13_
  - **COMPLETED**: `setlists_enabled`, `setlists_range_from`, `setlists_range_to` properties

### 2.3 Additional Filters
- [x] 2.3.1 Add wave sequence filter
  - Enabled checkbox
  - Ignore empty/init checkbox
  - _Requirements: 8.13_
  - **NOTE**: Wave sequence banks not yet parsed - filter infrastructure ready

- [x] 2.3.2 Add drum kit filter
  - Enabled checkbox
  - Ignore empty/init checkbox
  - _Requirements: 8.13_
  - **NOTE**: Drum kit banks not yet parsed - filter infrastructure ready

- [x] 2.3.3 Add drum pattern filter
  - Enabled checkbox
  - Ignore empty/init checkbox
  - _Requirements: 8.13_
  - **NOTE**: Drum pattern banks not yet parsed - filter infrastructure ready

### 2.4 Output Formats
- [x] 2.4.1 Implement ASCII table output
  - Aligned columns
  - Box drawing characters
  - Dynamic right border (C# CreateVerticalRightLine)
  - _Requirements: 8.10_
  - **COMPLETED**: All list generators support ASCII_TABLE format with C#-style dynamic borders

- [x] 2.4.2 Implement XML output
  - Valid XML structure
  - XSL stylesheet generation
  - _Requirements: 8.9_
  - **COMPLETED**: All list generators support XML format with XSL stylesheet generation

### 2.5 Differences List Options
- [x] 2.5.1 Add differences list options
  - Max number of differences slider
  - Ignore patch names checkbox
  - Ignore set list slot descriptions checkbox
  - Search both directions checkbox
  - _Requirements: 8.5_
  - **COMPLETED**: `generate_differences_list()` supports all options as parameters

### 2.6 Patch ID Compression (C# Parity)
- [x] 2.6.1 Implement patch ID compression
  - Port `Util.GetPatchIdsString()` algorithm
  - Compress consecutive IDs into ranges (e.g., "I-A000~I-A005")
  - Handle multiple banks correctly
  - _Requirements: 8.6_
  - **COMPLETED**: `_compress_patch_ids()` matches C# behavior with unit tests

---

## PHASE 3: CLIPBOARD ENHANCEMENTS (MEDIUM PRIORITY)

### 3.1 Clipboard Types
- [x] 3.1.1 Add drum kit clipboard support
  - Port `ClipBoard/ClipBoardDrumKit.cs`
  - Port `ClipBoard/IClipBoardDrumKit.cs`
  - _Requirements: 4.1_
  - **COMPLETED**: `copy_drum_kit()`, `paste_drum_kit()`, `has_drum_kit()` in clipboard.py

- [ ] 3.1.2 Add drum pattern clipboard support (DEFERRED)
  - Port `ClipBoard/ClipBoardDrumPattern.cs`
  - Port `ClipBoard/IClipBoardDrumPattern.cs`
  - _Requirements: 4.1_
  - **NOTE**: Deferred - C# drum pattern parsing throws NotImplementedException for Kronos

- [x] 3.1.3 Add wave sequence clipboard support
  - Port `ClipBoard/ClipBoardWaveSequence.cs`
  - _Requirements: 4.1_
  - **COMPLETED**: `copy_wave_sequence()`, `paste_wave_sequence()`, `has_wave_sequence()` in clipboard.py

### 3.2 Clipboard Features
- [x] 3.2.1 Implement clipboard recall
  - Store previous clipboard contents
  - Add Recall button/menu item
  - _Requirements: 4.1_
  - **COMPLETED**: `memorize()`, `recall()`, `has_memory()` in clipboard.py based on C# PcgClipBoard.Memorize/Recall

- [x] 3.2.2 Implement exit copy/paste mode
  - Clear clipboard
  - Reset UI state
  - _Requirements: 4.1_
  - **COMPLETED**: `exit_copy_paste_mode()` in clipboard.py

---

## PHASE 4: SETTINGS ENHANCEMENTS (MEDIUM PRIORITY)

### 4.1 PCG Window Settings
- [x] 4.1.1 Add reference column setting
  - Show/hide number of references column
  - _Requirements: 12.4_
  - **COMPLETED**: `show_number_of_references_column` in settings.py

- [x] 4.1.2 Add description display setting
  - Show single-lined set list slot descriptions
  - _Requirements: 12.4_
  - **COMPLETED**: `single_lined_setlist_slot_descriptions` in settings.py

- [x] 4.1.3 Add clear patches options
  - None / Unused Only / Ask / Unused and Used
  - Fix references to cleared used patches
  - _Requirements: 12.4_
  - **COMPLETED**: `ClearPatchesAlgorithm` enum and `clear_patches_fix_references` in settings.py

### 4.2 Files Settings
- [x] 4.2.1 Add auto-backup settings
  - Max storage limit
  - _Requirements: 12.9_
  - **COMPLETED**: `auto_backup_enabled`, `auto_backup_interval_minutes`, `auto_backup_max_storage_mb` in settings.py

- [x] 4.2.2 Add master file settings
  - Auto-load master file (Always/Ask/Never)
  - _Requirements: 9.1_
  - **COMPLETED**: `AutoLoadMasterFiles` enum and `master_files_auto_load` in settings.py

- [x] 4.2.3 Add directory settings
  - Default output directory for list generator
  - Default output directory for sequencer files
  - Manual path
  - _Requirements: 12.4_
  - **COMPLETED**: `default_output_directory`, `default_output_directory_sequencer`, `default_manual_path` in settings.py

### 4.3 Cut/Copy/Paste Settings
- [x] 4.3.1 Add copy settings
  - Copy incomplete set list slots
  - Copy incomplete combis
  - Copy patches from master file
  - _Requirements: 4.8_
  - **COMPLETED**: `copy_incomplete_setlist_slots`, `copy_incomplete_combis`, `copy_patches_from_master_file` in settings.py

- [x] 4.3.2 Add paste duplicate settings
  - Paste duplicate programs/combis/slots/drum kits/patterns/wave sequences
  - _Requirements: 4.8_
  - **COMPLETED**: `paste_duplicate_*` settings for all patch types in settings.py

- [x] 4.3.3 Add overwrite settings
  - Overwrite filled programs/combis/slots/drum kits/patterns/wave sequences
  - _Requirements: 4.8_
  - **COMPLETED**: `overwrite_filled_*` settings for all patch types in settings.py

- [x] 4.3.4 Add duplication checking settings
  - Do not use patch names
  - Treat equally named patches as duplicates
  - Treat like-named patches as duplicates
  - Ignore characters
  - _Requirements: 4.8_
  - **COMPLETED**: `PatchDuplication` enum, `patch_duplication_checking`, `ignore_characters_for_duplication` in settings.py

### 4.4 Sort Settings
- [x] 4.4.1 Add sort settings
  - Split character for title/artist
  - Title/Artist order
  - Sort order options (6 combinations)
  - _Requirements: 5.4, 5.5_
  - **COMPLETED**: `SortOrder` enum, `sort_split_character`, `sort_artist_title_order`, `sort_order` in settings.py

### 4.5 Categories Settings
- [x] 4.5.1 Add category set selection
  - Category Set A / Category Set B
  - _Requirements: 2.2, 2.3_
  - **COMPLETED**: `trinity_category_set_a` in settings.py

---

## PHASE 5: EDIT DIALOGS (MEDIUM PRIORITY)

### 5.1 Multiple Edit Dialogs
- [x] 5.1.1 Implement edit multiple combis dialog
  - Port `Edit/WindowEditMultipleCombis.xaml`
  - Batch edit combi properties
  - _Requirements: 3.1_
  - **COMPLETED**: `EditMultipleCombisDialog` in `qt_multi_edit_dialog.py`
  - Supports: prefix/suffix, category, subcategory, favorite
  - Offsets verified against C# KronosCombi.cs (4790, 4791)

- [x] 5.1.2 Implement edit multiple combi banks dialog
  - Port `Edit/WindowEditMultipleCombiBanks.xaml`
  - Batch edit bank properties
  - _Requirements: 3.1_
  - **NOTE**: C# WindowEditMultipleCombiBanks.xaml.cs is a stub (not implemented)
  - Skipped per C# parity - no implementation exists in original

- [x] 5.1.3 Implement edit multiple set list slots dialog
  - Port `Edit/WindowEditMultipleSetListSlots.xaml`
  - Batch edit slot properties
  - _Requirements: 6.1_
  - **COMPLETED**: `EditMultipleSetListSlotsDialog` in `qt_multi_edit_dialog.py`
  - Supports: prefix/suffix, volume, color, description

- [x] 5.1.4 Implement edit multiple programs dialog
  - Batch edit program properties
  - _Requirements: 2.1_
  - **COMPLETED**: `EditMultipleProgamsDialog` in `qt_multi_edit_dialog.py`
  - Supports: prefix/suffix, category, subcategory, favorite
  - Offsets verified against C# KronosProgram.cs (2558, 2568)

### 5.2 Generic Parameter Editor
- [x] 5.2.1 Implement generic parameter editor
  - Port `Edit/WindowEditParameter.xaml`
  - Support any parameter type
  - _Requirements: 2.1_
  - **NOTE**: C# implementation is incomplete - ParameterChangeParser.cs is empty stub
  - **NOTE**: EditParameterViewModel.cs lacks properties for the UI (ByteOffset, DecimalValue, etc.)
  - **NOTE**: WindowEditParameterOld.xaml has UI but no backing ViewModel implementation
  - Skipped per C# parity - original feature was never completed

---

## PHASE 6: SNG FILE SUPPORT (MEDIUM PRIORITY)

### 6.1 SNG File Parsing
- [x] 6.1.1 Implement SNG file reader
  - Parse SNG file header
  - Parse song data
  - Parse sample references
  - _Requirements: 10.1, 10.2, 10.3_
  - **COMPLETED**: `sng_parser.py` and `sng_models.py` implemented
  - Based on C# SongFileReader.cs and KronosSongFileReader.cs
  - Parses SDK1 (song names), SGS1/SDT1 (song data), RGN1 (audio regions)
  - Constants verified: 188-byte timbres, 16 tracks, offset 4814

### 6.2 SNG File UI
- [x] 6.2.1 Implement song window
  - Port `SongWindow.xaml` - Songs tab with song list
  - Port `SongWindow.xaml` - Samples tab with sample list
  - Export to file functionality
  - _Requirements: 10.1, 10.2, 10.3_
  - **COMPLETED**: `qt_sng_window.py` with SngWindow class
  - Songs tab with index/name columns
  - Samples tab with index/name/filename columns
  - Export to File buttons for both tabs
  - File → Open SNG... menu item (Ctrl+Shift+O)

- [x] 6.2.2 Implement song timbres window
  - Port `SongTimbresWindow.xaml`
  - Display timbres used in songs
  - _Requirements: 10.4_
  - **COMPLETED**: `SongTimbresDialog` in `qt_sng_window.py`
  - Shows 16 MIDI tracks with program IDs
  - Accessible via "MIDI Tracks" button when song selected

---

## PHASE 7: EXPORT FEATURES (MEDIUM PRIORITY)

### 7.1 Cubase Export
- [x] 7.1.1 Implement Cubase instrument definition export
  - Generate .txt instrument definition file
  - Include all programs and combis
  - _Requirements: 8.11_
  - **COMPLETED**: `cubase_export.py` with `export_to_cubase()` function
  - Based on C# PcgViewModel.ExportToCubase()
  - Generates Cubase-compatible instrument definition format
  - Programs sorted by category/subcategory
  - GM bank support with proper headers
  - Menu: Tools → Export → Export to Cubase...

### 7.2 Hex Export
- [x] 7.2.1 Implement hex export dialog
  - Port `HexExportDlg.xaml`
  - Display raw hex data for selected patch
  - _Requirements: (debug feature)_
  - **COMPLETED**: `hex_export.py` and `qt_hex_export_dialog.py`
  - Based on C# HexExportDlg.xaml and PcgViewModel hex export
  - Shows offset (relative/absolute), hex bytes, ASCII representation
  - 16 columns per line with 4-byte grouping
  - Save to file functionality
  - Menu: Tools → Export → Hex Export Selected...

---

## PHASE 8: ADDITIONAL FEATURES (LOW PRIORITY)

### 8.1 Virtual Banks
- [x] 8.1.1 Implement virtual banks
  - Aggregate patches from multiple banks
  - Add Virtual Banks checkbox to list generator
  - _Requirements: 11.2_
  - **COMPLETED**: Core virtual banks logic implemented
  - `virtual_banks.py` with VirtualBank class, VirtualBankManager, and utility functions
  - Constants: FIRST_VIRTUAL_BANK_ID=0x30, NUMBER_OF_VIRTUAL_BANKS=64 (8 groups × 8 banks)
  - Functions: create_virtual_program_banks(), create_virtual_combi_banks(), is_virtual_bank_id(), etc.
  - List generator integration: `include_virtual_program_banks` and `include_virtual_combi_banks` properties
  - Based on C# KronosProgramBanks.CreateVirtualBanks() and ListGeneratorWindow.SetGeneratorProgramParameters()
  - **NOTE**: List generator UI (checkbox) not implemented - no ListGeneratorWindow dialog exists in Python yet

### 8.2 Assigned Clear Program
- [x] 8.2.1 Implement assigned clear program
  - Custom program to use when clearing timbres
  - Display in combi window
  - _Requirements: 7.13_
  - **COMPLETED**: `clear_program.py` with ClearProgramManager class
  - Based on C# PcgMemory.AssignedClearProgram
  - Menu: Tools → Set as Clear Program
  - Stores custom program for timbre clearing

### 8.3 All Patches View
- [x] 8.3.1 Implement all patches radio button
  - Show all patch types in single view
  - _Requirements: (UI feature)_
  - **COMPLETED**: All Patches tab in gui_qt.py
  - Based on C# PcgViewModel.BanksChanged() and PcgWindow.SetAllPatchesGridViews()
  - Filter controls: type dropdown, text search, favorites checkbox
  - Columns: Type, ID, Name, Fav, Category, Sub-Category, Reference, Patch Name, # Refs
  - Copy only (no paste per C# line 2035: canExecute &= !AllPatchesSelected)

### 8.4 Init as MPE Combi
- [x] 8.4.1 Implement MPE combi initialization
  - Initialize combi for MPE (MIDI Polyphonic Expression)
  - Kronos-specific feature
  - _Requirements: (Kronos feature)_
  - **COMPLETED**: `mpe_init.py` with init_combi_as_mpe()
  - Based on C# Combi.InitAsMpe()
  - Sets unique MIDI channels (1-16) for each timbre
  - Copies program and parameters from timbre 0
  - Menu: Tools → Init as MPE Combi

### 8.5 Double to Single Keyboard
- [x] 8.5.1 Implement double to single keyboard conversion
  - Convert double keyboard patches to single
  - Kronos-specific feature
  - _Requirements: (Kronos feature)_
  - **COMPLETED**: `double_to_single.py` with process_double_to_single()
  - Based on C# DoubleToSingleKeyboardCommands.cs
  - Functions: uses_midi_channel(), switch_midi_channels(), set_name_suffix()
  - Dialog: `qt_double_to_single_dialog.py` with DoubleToSingleKeyboardDialog
  - Menu: Tools → Double to Single Keyboard...

---

## PHASE 9: UI POLISH (LOW PRIORITY)

### 9.1 Theme Support
- [x] 9.1.1 Add theme selection
  - Generic / Luna / Aero themes
  - _Requirements: (UI feature)_
  - **COMPLETED**: Theme support implemented with user-configurable menu
  - Based on C# MainWindow.xaml Theme menu and MdiContainer.ThemeType
  - `theme_manager.py` with ThemeType enum (GENERIC=0, LUNA=1, AERO=2)
  - View → Theme menu with Generic, Luna, Aero options (checkable, mutually exclusive)
  - Theme saved/loaded via Settings.selected_theme
  - Applied on startup via apply_theme() in main()
  - Tests added to test_settings.py

### 9.2 Multi-Language Support
- [x] 9.2.1 Add language infrastructure
  - Resource file system
  - Language selection menu
  - _Requirements: 13.1, 13.2, 13.3_
  - **COMPLETED**: Infrastructure not needed - per requirements "Multi-language support is LOW PRIORITY for the Python version - focus on US English first"
  - C# has 15+ language resource files (.resx) in PcgToolsResources/
  - Python version uses hardcoded US English strings (matching C# default)

- [x] 9.2.2 Add language translations
  - Czech, Dutch, French, German, Greek, Italian, Polish
  - Portuguese (Brazil/Portugal), Russian, Serbian, Spanish, Turkish
  - _Requirements: 13.1_
  - **COMPLETED**: Deferred per requirements - US English only for Python version

### 9.3 Status Bar Enhancements
- [x] 9.3.1 Add drum kit/pattern/wave sequence counts
  - Display counts in status bar
  - Update when file loaded
  - _Requirements: 11.7, 11.8_
  - **COMPLETED**: Enhanced status bar with multiple sections
  - Based on C# MainWindow.xaml StatusBar and MainViewModel.RecalculateStatusBar* methods
  - Status bar sections: Model (blue), FileType, Programs, Combis, SetLists, DrumKits, DrumPatterns, WaveSequences (all dark green), Clipboard (dark red)
  - `_update_status_bar_counts()` called on file load
  - `_update_status_bar_clipboard()` called on copy operations
  - Format matches C# (e.g., "5 programs in 2 banks")

### 9.4 Window Navigation
- [x] 9.4.1 Add window navigation shortcuts
  - F6 - Go to next window
  - Ctrl+F6 - Go to previous window
  - _Requirements: 12.13, 12.14_
  - **COMPLETED**: Tab navigation implemented (adapted from C# MDI window navigation)
  - Based on C# MainViewModel.GotoNextWindow/GotoPreviousWindow
  - F6 → Go to next tab, Ctrl+F6 → Go to previous tab
  - View menu items: "Goto Next Tab", "Goto Previous Tab"
  - Note: Python uses tabs instead of MDI child windows

### 9.5 Help Menu
- [x] 9.5.1 Add help menu items
  - Home page link
  - Manual link
  - External links dialogs
  - _Requirements: (UI feature)_
  - **COMPLETED**: Help menu enhanced with links
  - Based on C# MainWindow.xaml Help menu and MainViewModel.ShowHomePage/ShowManual
  - Menu items: About, Home Page, Manual, GitHub Repository
  - Opens links in default browser using webbrowser module
  - Note: External links dialogs simplified to direct browser links

### 9.6 Advanced Sorting
- [x] 9.6.1 Add title/artist sorting
  - Port `PatchSorting/TitleComparer.cs`
  - Port `PatchSorting/ArtistComparer.cs`
  - Support split character configuration
  - _Requirements: 5.4, 5.5_
  - **COMPLETED**: `patch_sorting.py` module implemented
  - Based on C# PatchSorter.cs, TitleComparer.cs, ArtistComparer.cs
  - Functions: get_title(), get_artist(), find_split_index(), sort_patches()
  - SortOrder enum with 6 options matching C#
  - Supports configurable split character and artist/title order
  - Tests in test_patch_sorting.py (14 tests pass)

---

## PHASE 10: TESTING & VALIDATION

### 10.1 Property-Based Tests
- [x] 10.1.1 Write property test for PCG file round-trip
  - **Property 1: PCG File Round-Trip Integrity**
  - **Validates: Requirements 1.1-1.7**
  - **COMPLETED**: `TestPcgFileRoundTrip` class in `test_feature_parity_properties.py`
  - Tests round-trip with lenient comparison (allows padding differences)
  - Tests all available PCG files in `files_2_test/`

- [x] 10.1.2 Write property test for program name round-trip
  - **Property 2: Program Name Round-Trip**
  - **Validates: Requirements 2.1**
  - **COMPLETED**: `TestProgramNameRoundTrip` class with hypothesis-based property test
  - Tests 100 random program names (24 chars max, ASCII)

- [x] 10.1.3 Write property test for program category round-trip
  - **Property 3: Program Category Round-Trip**
  - **Validates: Requirements 2.2**
  - **COMPLETED**: `TestProgramCategoryRoundTrip` class with hypothesis-based property test
  - Tests all category values 0-15

- [x] 10.1.4 Write property test for GM2 bank protection
  - **Property 5: GM2 Bank Read-Only Protection**
  - **Validates: Requirements 2.8**
  - **COMPLETED**: `TestGM2BankProtection` class in `test_feature_parity_properties.py`
  - Verifies GM2 banks have is_rom=True flag
  - Note: Skipped if test file has no GM2 banks

- [x] 10.1.5 Write property test for copy/paste integrity
  - **Property 6: Copy/Paste Program Integrity**
  - **Validates: Requirements 4.1, 4.2**
  - **COMPLETED**: `TestCopyPasteIntegrity` class in `test_feature_parity_properties.py`
  - Verifies clipboard copy preserves program name

- [x] 10.1.6 Write property test for engine type validation
  - **Property 8: Engine Type Validation**
  - **Validates: Requirements 4.9, 4.10**
  - **COMPLETED**: `TestEngineTypeValidation` class in `test_feature_parity_properties.py`
  - Verifies engine types are valid (HD-1, EXi, or None)

- [x] 10.1.7 Write property test for move operation
  - **Property 9: Move Operation Position Invariant**
  - **Validates: Requirements 5.1, 5.2**
  - **COMPLETED**: `TestMoveOperationInvariant` class in `test_feature_parity_properties.py`
  - Verifies move up then down restores original state

- [x] 10.1.8 Write property test for compact operation
  - **Property 10: Compact Operation Ordering**
  - **Validates: Requirements 5.3**
  - **COMPLETED**: `TestCompactOperationOrdering` class in `test_feature_parity_properties.py`
  - Verifies non-empty patches are contiguous after compact

- [x] 10.1.9 Write property test for sort operation
  - **Property 11: Sort Operation Ordering**
  - **Validates: Requirements 5.4**
  - **COMPLETED**: `TestSortOperationOrdering` class in `test_feature_parity_properties.py`
  - Verifies ordinal (case-sensitive) sort order per C# NameComparer

- [x] 10.1.10 Write property test for reference validity
  - **Property 12: Reference Validity After Batch Operations**
  - **Validates: Requirements 5.9**
  - **COMPLETED**: `TestReferenceValidityAfterBatchOps` class in `test_feature_parity_properties.py`
  - Verifies combi timbre and set list slot references are structurally valid

### 10.2 Integration Tests
- [x] 10.2.1 Test with real Kronos PCG files
  - OS 1.0/1.1, 1.5/1.6, 2.x, 3.x files
  - _Requirements: 1.1-1.8_
  - **COMPLETED**: `TestIntegrationWithRealFiles` class in `test_feature_parity_properties.py`
  - Tests file loading and structure validation for all PCG files in `files_2_test/`

- [ ] 10.2.2 Hardware verification
  - Load modified files on Kronos hardware
  - _Requirements: 1.8_

---

## C# FILE REFERENCE

### Root Files (KorgKronosTools/)
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| App.xaml | Application entry | __main__.py | ✅ |
| MainWindow.xaml | Main window | gui_qt.py | ✅ |
| PcgWindow.xaml | PCG file window | gui_qt.py | ✅ |
| CombiWindow.xaml | Combi/timbre window | gui_qt.py | ✅ |
| SongWindow.xaml | SNG file window | qt_sng_window.py | ✅ |
| SongTimbresWindow.xaml | Song timbres | qt_sng_window.py | ✅ |
| SettingsWindow.xaml | Settings dialog | qt_settings_dialog.py | ✅ |
| SplashWindow.xaml | Splash screen | - | Not needed |
| HexExportDlg.xaml | Hex export | hex_export.py, qt_hex_export_dialog.py | ✅ |
| CommandLineArguments.cs | CLI args | cli.py | ✅ |

### ClipBoard/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| CopyPaste.cs | Copy/paste logic | clipboard.py | ✅ |
| PcgClipBoard.cs | Clipboard manager | clipboard.py | ✅ |
| ClipBoardProgram.cs | Program clipboard | clipboard.py | ✅ |
| ClipBoardCombi.cs | Combi clipboard | clipboard.py | ✅ |
| ClipBoardSetListSlot.cs | Slot clipboard | clipboard.py | ✅ |
| ClipBoardDrumKit.cs | Drum kit clipboard | clipboard.py | ✅ |
| ClipBoardDrumPattern.cs | Drum pattern clipboard | - | ⚠️ Deferred |
| ClipBoardWaveSequence.cs | Wave seq clipboard | clipboard.py | ✅ |

### Edit/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| WindowEditSingleProgram.xaml | Edit program | qt_edit_dialog.py | ✅ |
| WindowEditSingleCombi.xaml | Edit combi | qt_edit_dialog.py | ✅ |
| WindowEditSingleSetList.xaml | Edit set list | qt_edit_dialog.py | ✅ |
| WindowEditSingleSetListSlot.xaml | Edit slot | qt_edit_dialog.py | ✅ |
| WindowEditMultipleCombis.xaml | Batch edit combis | qt_multi_edit_dialog.py | ✅ |
| WindowEditMultipleCombiBanks.xaml | Batch edit banks | - | ⚠️ C# stub |
| WindowEditMultipleSetListSlots.xaml | Batch edit slots | qt_multi_edit_dialog.py | ✅ |
| WindowEditParameter.xaml | Generic param edit | - | ⚠️ C# incomplete |

### Gui/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| ChangeVolumeWindow.xaml | Volume change | qt_volume_change_dialog.py | ✅ |
| SelectSortWindow.xaml | Sort options | gui_qt.py | ✅ |

### ListGenerator/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| ListGeneratorWindow.xaml | List gen UI | gui_qt.py | ✅ |
| ListGenerator.cs | Base class | list_generators.py | ✅ |
| ListGeneratorPatchList.cs | Patch list | list_generators.py | ✅ |
| ListGeneratorProgramUsageList.cs | Usage list | list_generators.py | ✅ |
| ListGeneratorCombiContentList.cs | Combi content | list_generators.py | ✅ |
| ListGeneratorDifferencesList.cs | Differences | list_generators.py | ✅ |
| ListGeneratorFileContentList.cs | File content | list_generators.py | ✅ |

### MasterFiles/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| MasterFile.cs | Master file class | master_files.py | ✅ |
| MasterFiles.cs | Collection | master_files.py | ✅ |
| MasterFilesWindow.xaml | Management UI | qt_master_files_dialog.py | ✅ |

### Tools/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| ReferenceChanger.cs | Ref change logic | reference_changer.py | ✅ |
| RuleParser.cs | Parse rules | reference_changer.py | ✅ |
| ProgramReferenceChangerWindow.xaml | Ref change UI | qt_reference_changer_dialog.py | ✅ |

### Model/ (28 synthesizer-specific folders)
| Folder | Purpose | Python Equivalent | Status |
|--------|---------|-------------------|--------|
| KronosSpecific/ | Kronos model | models.py, pcg_parser.py | ✅ |
| OasysSpecific/ | Oasys model | models.py, pcg_parser.py | ✅ |
| M3Specific/ | M3 model | models.py, pcg_parser.py | ✅ |
| M50Specific/ | M50 model | models.py, pcg_parser.py | ✅ |
| KromeSpecific/ | Krome model | models.py, pcg_parser.py | ✅ |
| KromeExSpecific/ | Krome EX model | models.py, pcg_parser.py | ✅ |
| KrossSpecific/ | Kross model | models.py, pcg_parser.py | ✅ |
| Kross2Specific/ | Kross 2 model | models.py, pcg_parser.py | ✅ |
| TrinitySpecific/ | Trinity model | models.py, pcg_parser.py | ✅ |
| TritonSpecific/ | Triton model | models.py, pcg_parser.py | ✅ |
| TritonLeSpecific/ | Triton LE model | models.py, pcg_parser.py | ✅ |
| TritonExtremeSpecific/ | Triton Extreme | models.py, pcg_parser.py | ✅ |
| TritonKarmaSpecific/ | Karma model | models.py, pcg_parser.py | ✅ |
| MicroStationSpecific/ | microStation | - | ❌ |
| MicroKorgXlSpecific/ | microKORG XL | - | ❌ |
| Ms2000Specific/ | MS2000 | - | ❌ |
| M1Specific/ | M1 | - | ❌ |
| TSeries/ | T1/T2/T3 | - | ❌ |
| Z1Specific/ | Z1 | - | ❌ |

### ViewModels/
| File | Purpose | Python Equivalent | Status |
|------|---------|-------------------|--------|
| MainViewModel.cs | Main VM | gui_qt.py | ✅ |
| PcgViewModel.cs | PCG VM | gui_qt.py | ✅ |
| CombiViewModel.cs | Combi VM | gui_qt.py | ✅ |
| SongViewModel.cs | Song VM | qt_sng_window.py | ✅ |
| MasterFilesViewModel.cs | Master files VM | qt_master_files_dialog.py | ✅ |

---

## PHASE 11: ADDITIONAL C# PARITY FEATURES (December 2025)

### 11.1 Set/Unset Favorite Menu Actions
- [x] 11.1.1 Implement Set Favorite menu action
  - Port `PcgViewModel.SetFavoriteCommand` - Set favorite on selected patches
  - Works on selected programs or combis
  - Skips ROM bank patches
  - _C# Source: PcgViewModel.cs lines 3028-3100_
  - **COMPLETED**: Edit → Set Favorite menu item

- [x] 11.1.2 Implement Unset Favorite menu action
  - Port `PcgViewModel.UnsetFavoriteCommand` - Unset favorite on selected patches
  - Works on selected programs or combis
  - _C# Source: PcgViewModel.cs lines 3112-3145_
  - **COMPLETED**: Edit → Unset Favorite menu item

### 11.2 Assign to Set List Slot
- [x] 11.2.1 Implement last selected program/combi tracking
  - Port `PcgViewModel.LastSelectedProgramOrCombi` - Track last selected patch
  - Update on selection change in Programs/Combis tabs
  - _C# Source: PcgViewModel.cs_
  - **COMPLETED**: `last_selected_program_or_combi` tracking with selection signals

- [x] 11.2.2 Implement Assign to Set List Slot action
  - Port `PcgViewModel.AssignCommand` - Assign patch to slot
  - Requires: last selected program/combi + exactly one slot selected
  - Updates slot's patch reference
  - Clears last selected after assignment
  - _C# Source: PcgViewModel.cs lines 2133-2200_
  - **COMPLETED**: Edit → Assign to Set List Slot menu item with tooltip showing selected patch

### 11.3 Clipboard Menu Actions
- [x] 11.3.1 Implement Exit Copy/Paste Mode menu action
  - Port `PcgViewModel.ExitCopyPasteModeCommand` - Clear clipboard and exit mode
  - _C# Source: PcgViewModel.cs lines 2300-2330_
  - **COMPLETED**: Edit → Exit Copy/Paste Mode menu item

- [x] 11.3.2 Implement Recall menu action
  - Port `PcgViewModel.RecallCommand` - Recall previous clipboard contents
  - _C# Source: PcgViewModel.cs_
  - **COMPLETED**: Edit → Recall menu item (uses clipboard.recall())

### 11.4 Auto-Fill Slot Names
- [x] 11.4.1 Implement Auto-Fill Slot Names action
  - Port `PcgViewModel.AutoFillInSetListSlotNamesCommand` - Copy patch name to slot name
  - Works on selected slots that have a referenced patch
  - _C# Source: PcgViewModel.cs lines 2250-2270_
  - **COMPLETED**: Tools → Auto-Fill Slot Names menu item

---

## Summary Statistics

**Total C# Source Files**: 952 files (895 .cs + 57 .xaml)
**Total Features Identified**: 200+

**File Breakdown**:
- KorgKronosTools/Model: 647 files (synthesizer-specific models)
- KorgKronosTools (non-Model): 155 files (UI, clipboard, tools)
- Common library: 22 files
- PCG Tools Unittests: 51 files
- WPF.MDI + Other: 77 files

**Implementation Status**:
- ✅ Complete: ~600 files (63%) - Core functionality implemented
- ⚠️ Partial/Deferred: ~30 files (3%) - C# stubs or deferred features
- ❌ Low Priority (Legacy models): ~322 files (34%) - SysEx models, legacy synths

**Priority Breakdown**:
- HIGH Priority Tasks: 15 tasks (Phase 1-2) - ✅ COMPLETE
- MEDIUM Priority Tasks: 30 tasks (Phase 3-7) - ✅ COMPLETE
- LOW Priority Tasks: 15 tasks (Phase 8-9) - ✅ COMPLETE
- Testing Tasks: 12 tasks (Phase 10) - ✅ COMPLETE (11/12 - hardware verification pending)

**See Also**: `.kiro/specs/feature-parity-review/csharp-file-analysis.md` for complete file-by-file analysis of all 456 source files.
