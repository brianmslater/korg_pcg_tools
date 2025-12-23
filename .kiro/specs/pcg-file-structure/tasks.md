# Implementation Plan: PCG File Structure Deep Dive

This implementation plan focuses on documenting and validating the PCG file structure understanding. The primary deliverable is a comprehensive reference document and property-based tests that validate the binary structure parsing.

- [x] 1. Create PCG Structure Reference Module
  - [x] 1.1 Create `pcg_tools/pcg_structure.py` with documented constants
    - Define all chunk IDs as constants (PCG1, PRG1, CMB1, SLS1, etc.)
    - Define all byte offsets for Kronos program structure
    - Define all byte offsets for Kronos combi structure
    - Define all byte offsets for Kronos timbre structure
    - Define all byte offsets for Kronos set list slot structure
    - Add docstrings referencing C# source files
    - _Requirements: 1.1-1.9, 4.1-4.11, 5.1-5.6, 6.1-6.6, 7.1-7.6, 8.1-8.17, 10.1-10.13_

  - [x] 1.2 Create bank ID mapping functions
    - Implement `bank_name_to_pcgid(bank_name, context)` for chunk headers vs timbre refs
    - Implement `pcgid_to_bank_name(pcgid, context)` for decoding
    - Implement `slot_bank_id_to_name(bank_id)` for set list slot references
    - Add comprehensive docstrings with examples
    - _Requirements: 11.1-11.7_

  - [x] 1.3 Write property test for bank ID round-trip
    - **Property 5: Bank ID Encoding Round-Trip**
    - **Validates: Requirements 11.1-11.7**

- [x] 2. Validate Existing Parser Against Structure Reference
  - [x] 2.1 Add structure validation to `pcg_parser.py`
    - Add assertions for expected offsets during parsing
    - Log warnings when actual offsets differ from expected
    - Create validation report function
    - _Requirements: 2.1-2.6, 4.1-4.11_

  - [x] 2.2 Write property test for PCG file round-trip
    - **Property 1: PCG File Round-Trip Integrity**
    - **Validates: Requirements 1.1-1.9, 2.1-2.6**

- [x] 3. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Enhance Program Parameter Handling
  - [x] 4.1 Update program parameter reading in `pcg_parser.py`
    - Verify OSC mode offset (2558) and bit extraction
    - Verify favorite flag offset (2558, bit 5)
    - Verify category offset (2568) and bit extraction
    - Add engine type detection at offset 0x58
    - _Requirements: 5.1-5.6_

  - [x] 4.2 Write property test for program parameter round-trip
    - **Property 2: Program Parameter Round-Trip**
    - **Validates: Requirements 5.1-5.6**

- [x] 5. Enhance Timbre Parameter Handling
  - [x] 5.1 Update timbre parameter reading in `pcg_parser.py`
    - Verify all 16 timbre parameter offsets against C# reference
    - Ensure signed value handling for transpose, detune, portamento
    - Verify bit field extraction for status, osc_mode, osc_select
    - _Requirements: 8.1-8.17_

  - [x] 5.2 Write property test for timbre parameter round-trip
    - **Property 3: Timbre Parameter Round-Trip**
    - **Validates: Requirements 8.1-8.17**

- [x] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Enhance Set List Slot Parameter Handling
  - [x] 7.1 Update slot parameter reading in `pcg_parser.py`
    - Verify split bit field handling for transpose (bytes 25, 29)
    - Verify split bit field handling for text size (bytes 24, 29)
    - Verify color value mapping
    - Verify description reading at offset 30
    - _Requirements: 10.1-10.13_

  - [x] 7.2 Write property test for slot parameter round-trip
    - **Property 4: Set List Slot Parameter Round-Trip**
    - **Validates: Requirements 10.1-10.13**

- [x] 8. Add Reference Validation
  - [x] 8.1 Implement reference validation functions
    - Add `validate_timbre_references(combi, pcg_file)` function
    - Add `validate_slot_references(slot, pcg_file)` function
    - Return list of invalid references with details
    - _Requirements: 8.1-8.2, 10.2-10.6_

  - [x] 8.2 Write property test for reference validity
    - **Property 7: Combi Timbre Reference Validity**
    - **Property 8: Set List Slot Reference Validity**
    - **Validates: Requirements 8.1-8.2, 10.2-10.6**

- [x] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Document Chunk Navigation
  - [x] 10.1 Add chunk iteration utilities
    - Implement `iterate_chunks(pcg_data)` generator
    - Handle alignment gaps correctly
    - Log chunk boundaries for debugging
    - _Requirements: 2.1-2.6_

  - [x] 10.2 Write property test for chunk navigation
    - **Property 6: Chunk Navigation Consistency**
    - **Validates: Requirements 2.1-2.6**

- [x] 11. Implement Checksum Algorithm Enhancements
  - [x] 11.1 Add INI2/INI3 checksum support to `checksum.py`
    - Implement `find_ini2_offset(data, chunk_name, occurrence)` function
    - Add INI3 marker detection for Kronos OS 1.5/1.6
    - Update checksums in both chunk header (+11) and INI2 entry
    - _Requirements: 18.1-18.8_

  - [x] 11.2 Write property test for checksum correctness
    - **Property 9: Checksum Calculation Correctness**
    - **Validates: Requirements 18.1-18.8**

- [x] 12. Implement DIV1 Bank Presence Parsing
  - [x] 12.1 Add DIV1 parsing to `pcg_parser.py`
    - Implement `parse_div1_chunk(pcg, offset)` function
    - Read program bank flags at offset +8
    - Read extended program bank flags at offset +12
    - Read combi bank flags at offset +16
    - Use flags to skip missing banks during parsing
    - _Requirements: 19.1-19.6_

  - [x] 12.2 Write property test for DIV1 consistency
    - **Property 10: DIV1 Bank Flag Consistency**
    - **Validates: Requirements 19.1-19.6**

- [x] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. Implement Drum Kit Parsing
  - [x] 14.1 Add DKT1/DBK1 parsing to `pcg_parser.py`
    - Implement `parse_dkt1_chunk(pcg)` function
    - Implement `_parse_dbk1_chunk(pcg, offset)` function
    - Create DrumKit model class in `models.py`
    - Parse drum kit names and bank IDs
    - _Requirements: 20.1-20.8_

  - [x] 14.2 Write property test for drum kit round-trip
    - **Property 11: Drum Kit Name Round-Trip**
    - **Validates: Requirements 20.1-20.8**

- [x] 15. Implement Wave Sequence Parsing
  - [x] 15.1 Add WSQ1/WBK1 parsing to `pcg_parser.py`
    - Implement `parse_wsq1_chunk(pcg)` function
    - Implement `_parse_wbk1_chunk(pcg, offset)` function
    - Create WaveSequence model class in `models.py`
    - Parse wave sequence names and bank IDs
    - _Requirements: 21.1-21.8_

  - [x] 15.2 Write property test for wave sequence round-trip
    - **Property 12: Wave Sequence Name Round-Trip**
    - **Validates: Requirements 21.1-21.8**

- [x] 16. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Implement Global Category Name Parsing
  - [x] 17.1 Add GLB1 category parsing to `pcg_parser.py`
    - Implement `parse_glb1_categories(pcg)` function
    - Calculate category name offsets using formula
    - Read 18 main categories × 8 sub-categories × 24 bytes
    - Store category names in PcgFile model
    - _Requirements: 22.1-22.6_

  - [x] 17.2 Write property test for category name round-trip
    - **Property 13: Category Name Round-Trip**
    - **Validates: Requirements 22.1-22.6**

- [x] 18. Implement Extended Data Chunk Support (PRG2/CMB2/STL2)
  - [x] 18.1 Add PRG2/CMB2/STL2 detection and preservation
    - Detect Kronos OS 1.5+ by INI3 presence
    - Track PRG2/CMB2/STL2 chunk offsets during parsing
    - Preserve extended data during copy operations
    - _Requirements: 23.1-23.8_

  - [x] 18.2 Write property test for extended data preservation
    - **Property 14: Extended Data Preservation**
    - **Validates: Requirements 23.1-23.8**

- [x] 19. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

