# Requirements Document: PCG File Structure Deep Dive

## Introduction

This document specifies the detailed binary structure of Korg PCG files, with primary focus on Kronos format. It serves as a comprehensive reference for understanding where data is stored in PCG files, based on analysis of the original C# PCG Tools implementation and official Korg documentation.

## Glossary

- **PCG File**: Korg's proprietary binary file format for storing synthesizer patch data
- **Chunk**: A self-contained data block within a PCG file, identified by a 4-character ID
- **Big-Endian**: Multi-byte integers stored with most significant byte first (Korg standard)
- **PBK1**: Program Bank chunk for HD-1 (sample-based) programs
- **MBK1**: Model Bank chunk for EXi (modeled synthesis) programs
- **CBK1**: Combi Bank chunk
- **SLS1**: Set List chunk (slot names and display data)
- **STL1**: Set List data chunk (actual slot parameters)
- **SBK1**: Set List Bank chunk (slot data within STL1)
- **SLD1**: Set List Display chunk (combi-like slot data)
- **SDB1**: Set List Database chunk (browser display names)
- **DIV1**: Division chunk (bank presence flags)
- **GLB1**: Global settings chunk
- **DKT1**: Drum Kit container chunk
- **DBK1**: Drum Kit Bank chunk
- **WSQ1**: Wave Sequence container chunk
- **WBK1**: Wave Sequence Bank chunk
- **DPI1**: Drum Pattern container chunk
- **INI2/INI3**: Initialization chunks (checksum type indicators)
- **PRG2/CMB2/STL2**: Extended data chunks (Kronos OS 1.5+)
- **Timbre**: A program slot within a combi (16 per combi on Kronos)
- **PcgId**: Internal bank identifier used in binary data

## Requirements

### Requirement 1: PCG File Header Structure

**User Story:** As a developer, I want to understand the PCG file header structure, so that I can correctly identify and parse Korg PCG files.

#### Acceptance Criteria

1. WHEN parsing a PCG file THEN the System SHALL read the 4-byte magic number "KORG" at offset 0x00
2. WHEN parsing a PCG file THEN the System SHALL read the product ID byte at offset 0x04 to identify the synthesizer model
3. WHEN parsing a PCG file THEN the System SHALL read the file type byte at offset 0x05 (0x00=PCG, 0x01=SNG)
4. WHEN parsing a PCG file THEN the System SHALL read the major version byte at offset 0x06
5. WHEN parsing a PCG file THEN the System SHALL read the minor version byte at offset 0x07
6. WHEN parsing a PCG file THEN the System SHALL read the checksum flag byte at offset 0x08 (0x00=none, 0x01=checksum)
7. WHEN parsing a Kronos PCG file THEN the System SHALL identify product ID 0x68 as Kronos
8. WHEN parsing an Oasys PCG file THEN the System SHALL identify product ID 0x70 as Oasys
9. WHEN parsing an M3 PCG file THEN the System SHALL identify product ID 0x75 as M3

### Requirement 2: Chunk Structure

**User Story:** As a developer, I want to understand the chunk structure, so that I can navigate and parse PCG file contents.

#### Acceptance Criteria

1. WHEN parsing a chunk THEN the System SHALL read the 4-byte chunk ID at offset +0
2. WHEN parsing a chunk THEN the System SHALL read the 4-byte chunk size (big-endian) at offset +4
3. WHEN parsing a chunk THEN the System SHALL read chunk data starting at offset +8
4. WHEN navigating between chunks THEN the System SHALL account for 4-byte alignment gaps
5. WHEN parsing nested chunks THEN the System SHALL recursively parse child chunks within parent chunk data
6. WHEN encountering unknown chunks THEN the System SHALL skip the chunk using its size field

### Requirement 3: DIV1 Bank Presence Flags

**User Story:** As a developer, I want to understand the DIV1 chunk, so that I can determine which banks are present in a PCG file.

#### Acceptance Criteria

1. WHEN parsing DIV1 THEN the System SHALL read program bank presence flags at offset +8 (2 bytes, bit flags)
2. WHEN parsing DIV1 THEN the System SHALL read extended program bank flags at offset +12 (2 bytes for U-DD through U-GG)
3. WHEN parsing DIV1 THEN the System SHALL read combi bank presence flags at offset +16 (2 bytes)
4. WHEN parsing DIV1 THEN the System SHALL read drum kit bank presence flags at offset +24 (2 bytes)
5. WHEN parsing DIV1 THEN the System SHALL read wave sequence bank presence flags at offset +32 (2 bytes)
6. WHEN parsing DIV1 THEN the System SHALL read global/setlist presence flags at offset +40

### Requirement 4: Program Bank Structure (PBK1/MBK1)

**User Story:** As a developer, I want to understand program bank structure, so that I can correctly parse and write program data.

#### Acceptance Criteria

1. WHEN parsing PBK1 THEN the System SHALL read the number of programs at offset +12 (4 bytes, big-endian)
2. WHEN parsing PBK1 THEN the System SHALL read the program size at offset +16 (4 bytes, big-endian)
3. WHEN parsing PBK1 THEN the System SHALL read the bank ID at offset +20 (4 bytes, big-endian)
4. WHEN parsing PBK1 THEN the System SHALL read program data starting at offset +24
5. WHEN parsing MBK1 THEN the System SHALL read the number of programs at offset +12 (4 bytes)
6. WHEN parsing MBK1 THEN the System SHALL read the program size at offset +16 (4 bytes)
7. WHEN parsing MBK1 THEN the System SHALL read the bank ID at offset +20 (4 bytes)
8. WHEN decoding bank ID THEN the System SHALL map 0x00-0x05 to I-A through I-F
9. WHEN decoding bank ID THEN the System SHALL map 0x8000 to I-F (special case)
10. WHEN decoding bank ID THEN the System SHALL map 0x20000-0x20006 to U-A through U-G
11. WHEN decoding bank ID THEN the System SHALL map 0x20007-0x2000D to U-AA through U-GG

### Requirement 5: Kronos Program Data Structure

**User Story:** As a developer, I want to understand Kronos program data layout, so that I can read and write program parameters.

#### Acceptance Criteria

1. WHEN parsing a Kronos program THEN the System SHALL read the 24-byte name at offset +0
2. WHEN parsing a Kronos program THEN the System SHALL read the OSC mode at offset +2558 (2 bytes, bits 0-2)
3. WHEN parsing a Kronos program THEN the System SHALL read the favorite flag at offset +2558 (bit 5)
4. WHEN parsing a Kronos program THEN the System SHALL read the category at offset +2568 (bits 0-4)
5. WHEN parsing a Kronos program THEN the System SHALL read the sub-category at offset +2568 (bits 5-7)
6. WHEN parsing a Kronos program THEN the System SHALL read the engine type indicator at offset +0x58

### Requirement 6: Combi Bank Structure (CBK1)

**User Story:** As a developer, I want to understand combi bank structure, so that I can correctly parse and write combi data.

#### Acceptance Criteria

1. WHEN parsing CBK1 THEN the System SHALL read the number of combis at offset +12 (4 bytes)
2. WHEN parsing CBK1 THEN the System SHALL read the combi size at offset +16 (4 bytes)
3. WHEN parsing CBK1 THEN the System SHALL read the bank ID at offset +20 (4 bytes)
4. WHEN parsing CBK1 THEN the System SHALL read combi data starting at offset +24
5. WHEN decoding combi bank ID THEN the System SHALL map 0x00-0x06 to I-A through I-G
6. WHEN decoding combi bank ID THEN the System SHALL map 0x20000-0x20006 to U-A through U-G

### Requirement 7: Kronos Combi Data Structure

**User Story:** As a developer, I want to understand Kronos combi data layout, so that I can read and write combi parameters.

#### Acceptance Criteria

1. WHEN parsing a Kronos combi THEN the System SHALL read the 24-byte name at offset +0
2. WHEN parsing a Kronos combi THEN the System SHALL read the tempo at offset +1304 (2 bytes, divide by 100 for BPM)
3. WHEN parsing a Kronos combi THEN the System SHALL read the category at offset +4790 (bits 0-4)
4. WHEN parsing a Kronos combi THEN the System SHALL read the sub-category at offset +4790 (bits 5-7)
5. WHEN parsing a Kronos combi THEN the System SHALL read the favorite flag at offset +4791 (bit 0)
6. WHEN parsing a Kronos combi THEN the System SHALL read timbre data starting at offset +4802

### Requirement 8: Kronos Timbre Data Structure

**User Story:** As a developer, I want to understand Kronos timbre data layout, so that I can read and write timbre parameters.

#### Acceptance Criteria

1. WHEN parsing a Kronos timbre THEN the System SHALL read the program index at offset +0 (1 byte)
2. WHEN parsing a Kronos timbre THEN the System SHALL read the program bank ID at offset +1 (1 byte)
3. WHEN parsing a Kronos timbre THEN the System SHALL read the status at offset +2 (bits 5-7: 0=Off, 1=Int, 2=Both, 3=Ext, 4=Ex2)
4. WHEN parsing a Kronos timbre THEN the System SHALL read the MIDI channel at offset +2 (bits 0-4)
5. WHEN parsing a Kronos timbre THEN the System SHALL read the volume at offset +5 (1 byte, 0-127)
6. WHEN parsing a Kronos timbre THEN the System SHALL read the transpose at offset +7 (1 byte, signed)
7. WHEN parsing a Kronos timbre THEN the System SHALL read the detune at offset +8 (2 bytes, signed, little-endian)
8. WHEN parsing a Kronos timbre THEN the System SHALL read the mute flag at offset +34 (bit 7)
9. WHEN parsing a Kronos timbre THEN the System SHALL read the priority flag at offset +35 (bit 4)
10. WHEN parsing a Kronos timbre THEN the System SHALL read the OSC mode at offset +35 (bits 0-1)
11. WHEN parsing a Kronos timbre THEN the System SHALL read the OSC select at offset +35 (bits 2-3)
12. WHEN parsing a Kronos timbre THEN the System SHALL read the portamento at offset +36 (1 byte, signed)
13. WHEN parsing a Kronos timbre THEN the System SHALL read the top key at offset +37 (1 byte)
14. WHEN parsing a Kronos timbre THEN the System SHALL read the bottom key at offset +38 (1 byte)
15. WHEN parsing a Kronos timbre THEN the System SHALL read the top velocity at offset +40 (1 byte)
16. WHEN parsing a Kronos timbre THEN the System SHALL read the bottom velocity at offset +41 (1 byte)
17. WHEN calculating timbre offset THEN the System SHALL use timbre size of 188 bytes per timbre

### Requirement 9: Set List Structure (SLS1/STL1/SBK1)

**User Story:** As a developer, I want to understand set list structure, so that I can correctly parse and write set list data.

#### Acceptance Criteria

1. WHEN parsing SLS1 THEN the System SHALL locate the SLD1 sub-chunk for display data
2. WHEN parsing SLS1 THEN the System SHALL locate the SDB1 sub-chunk for browser names
3. WHEN parsing SLS1 THEN the System SHALL locate the STL1 sub-chunk for slot data
4. WHEN parsing STL1 THEN the System SHALL locate the SBK1 sub-chunk containing actual slot data
5. WHEN parsing SBK1 THEN the System SHALL read the number of set lists at offset +8 (4 bytes)
6. WHEN parsing SBK1 THEN the System SHALL read the total chunk size at offset +12 (4 bytes)
7. WHEN parsing SBK1 THEN the System SHALL calculate slot size as total_size / num_setlists / 128

### Requirement 10: Kronos Set List Slot Data Structure

**User Story:** As a developer, I want to understand Kronos set list slot data layout, so that I can read and write slot parameters.

#### Acceptance Criteria

1. WHEN parsing a Kronos slot THEN the System SHALL read the 24-byte name at offset +0
2. WHEN parsing a Kronos slot THEN the System SHALL read the patch type at offset +24 (bits 0-1: 0=Program, 1=Combi, 2=Song)
3. WHEN parsing a Kronos slot THEN the System SHALL read the color at offset +24 (byte value for color index)
4. WHEN parsing a Kronos slot THEN the System SHALL read the bank ID at offset +25 (bits 0-4)
5. WHEN parsing a Kronos slot THEN the System SHALL read the transpose MSB at offset +25 (bits 5-7)
6. WHEN parsing a Kronos slot THEN the System SHALL read the patch index at offset +26 (1 byte)
7. WHEN parsing a Kronos slot THEN the System SHALL read the volume at offset +28 (1 byte, 0-127)
8. WHEN parsing a Kronos slot THEN the System SHALL read the transpose LSB at offset +29 (bits 5-7)
9. WHEN parsing a Kronos slot THEN the System SHALL read the text size MSB at offset +29 (bit 4)
10. WHEN parsing a Kronos slot THEN the System SHALL read the text size LSB at offset +24 (bits 6-7)
11. WHEN parsing a Kronos slot THEN the System SHALL read the 512-byte description at offset +30
12. WHEN calculating transpose THEN the System SHALL combine MSB and LSB as signed 6-bit value (-24 to +24)
13. WHEN calculating text size THEN the System SHALL combine MSB and LSB as 3-bit value (0-4: S, XS, M, L, XL)

### Requirement 11: Bank ID to PcgId Mapping

**User Story:** As a developer, I want to understand bank ID encoding, so that I can correctly map between display names and binary values.

#### Acceptance Criteria

1. WHEN encoding program bank I-A through I-E THEN the System SHALL use PcgId 0-4
2. WHEN encoding program bank I-F THEN the System SHALL use PcgId 5 (or 0x8000 in chunk header)
3. WHEN encoding program bank GM THEN the System SHALL use PcgId 6
4. WHEN encoding program bank U-A through U-G THEN the System SHALL use PcgId 17-23 (timbre reference) or 0x20000-0x20006 (chunk header)
5. WHEN encoding program bank U-AA through U-GG THEN the System SHALL use PcgId 24-30 (timbre reference) or 0x20007-0x2000D (chunk header)
6. WHEN encoding combi bank I-A through I-G THEN the System SHALL use PcgId 0-6
7. WHEN encoding combi bank U-A through U-G THEN the System SHALL use PcgId 0x20000-0x20006

### Requirement 12: Checksum Calculation

**User Story:** As a developer, I want to understand checksum calculation, so that I can write valid PCG files.

#### Acceptance Criteria

1. WHEN writing a Kronos OS 1.5/1.6 PCG file THEN the System SHALL calculate INI3 checksums
2. WHEN writing a Kronos OS 2.x/3.x PCG file THEN the System SHALL calculate INI2 checksums
3. WHEN calculating checksums THEN the System SHALL process each chunk according to model-specific algorithm
4. WHEN the checksum flag is 0x00 THEN the System SHALL skip checksum calculation

### Requirement 13: Extended Data Chunks (PRG2/CMB2/STL2)

**User Story:** As a developer, I want to understand extended data chunks, so that I can support Kronos OS 1.5+ features.

#### Acceptance Criteria

1. WHEN parsing a Kronos OS 1.5+ file THEN the System SHALL locate PRG2 chunks for extended program data
2. WHEN parsing a Kronos OS 1.5+ file THEN the System SHALL locate CMB2 chunks for extended combi data
3. WHEN parsing a Kronos OS 1.5+ file THEN the System SHALL locate STL2 chunks for extended set list data
4. WHEN writing extended data THEN the System SHALL preserve PRG2/CMB2/STL2 chunk offsets

### Requirement 14: Drum Kit Structure (DKT1/DBK1)

**User Story:** As a developer, I want to understand drum kit structure, so that I can parse and display drum kit data.

#### Acceptance Criteria

1. WHEN parsing DKT1 THEN the System SHALL iterate through DBK1 sub-chunks
2. WHEN parsing DBK1 THEN the System SHALL read the number of drum kits at offset +12
3. WHEN parsing DBK1 THEN the System SHALL read the drum kit size at offset +16
4. WHEN parsing DBK1 THEN the System SHALL read the bank ID at offset +20
5. WHEN decoding drum kit bank ID THEN the System SHALL map 0 to INT, 0x20000+ to USER banks

### Requirement 15: Wave Sequence Structure (WSQ1/WBK1)

**User Story:** As a developer, I want to understand wave sequence structure, so that I can parse and display wave sequence data.

#### Acceptance Criteria

1. WHEN parsing WSQ1 THEN the System SHALL iterate through WBK1 sub-chunks
2. WHEN parsing WBK1 THEN the System SHALL read the number of wave sequences at offset +12
3. WHEN parsing WBK1 THEN the System SHALL read the wave sequence size at offset +16
4. WHEN parsing WBK1 THEN the System SHALL read the bank ID at offset +20
5. WHEN decoding wave sequence bank ID THEN the System SHALL map 0 to INT, 0x20000+ to USER banks

### Requirement 16: Global Settings Structure (GLB1)

**User Story:** As a developer, I want to understand global settings structure, so that I can read category names and other global data.

#### Acceptance Criteria

1. WHEN parsing GLB1 THEN the System SHALL read the chunk size at offset +4
2. WHEN parsing GLB1 THEN the System SHALL store the byte offset for category name lookup
3. WHEN a file lacks GLB1 THEN the System SHALL use master file for category names

### Requirement 17: SDB1 Browser Names

**User Story:** As a developer, I want to understand SDB1 structure, so that I can update browser display names when saving.

#### Acceptance Criteria

1. WHEN parsing SDB1 THEN the System SHALL locate set list names at calculated offsets
2. WHEN parsing SDB1 THEN the System SHALL locate slot names within each set list block
3. WHEN writing SDB1 THEN the System SHALL update set list names to match STL1 data
4. WHEN writing SDB1 THEN the System SHALL update slot names to match STL1 data
5. WHEN calculating SDB1 offsets THEN the System SHALL use 0xE1C bytes per set list block

### Requirement 18: Checksum Calculation Algorithm

**User Story:** As a developer, I want to understand the exact checksum algorithm, so that I can write valid PCG files that load on hardware.

#### Acceptance Criteria

1. WHEN calculating a chunk checksum THEN the System SHALL sum all bytes from offset+12 to offset+12+chunk_size
2. WHEN calculating a chunk checksum THEN the System SHALL apply modulo 256 to get a single byte result
3. WHEN writing a chunk checksum THEN the System SHALL store the result at chunk_offset+11
4. WHEN processing Kronos OS 1.5/1.6 files THEN the System SHALL also update checksums in INI2 chunk at offset+54
5. WHEN processing Kronos OS 2.x/3.x files THEN the System SHALL update checksums in INI2 chunk at offset+22
6. WHEN locating INI2 checksum offsets THEN the System SHALL search for chunk name matches at 64-byte intervals starting at INI2+16
7. WHEN the INI3 marker is encountered THEN the System SHALL skip 16 bytes and continue searching
8. WHEN fixing checksums THEN the System SHALL process chunks PBK1, MBK1, CBK1, SBK1, GLB1, WBK1, DBK1

### Requirement 19: DIV1 Bank Presence Implementation

**User Story:** As a developer, I want to parse DIV1 to determine which banks exist, so that I can correctly handle partial PCG files.

#### Acceptance Criteria

1. WHEN parsing DIV1 THEN the System SHALL read the chunk at offset 0x1C from PCG1 start (Kronos/Oasys)
2. WHEN parsing DIV1 THEN the System SHALL read the chunk at offset 0x18 from PCG1 start (Triton)
3. WHEN reading program bank flags THEN the System SHALL interpret bit 0 as I-A present, bit 1 as I-B present, etc.
4. WHEN reading extended program bank flags THEN the System SHALL interpret bits for U-DD through U-GG
5. WHEN a bank flag is 0 THEN the System SHALL skip parsing that bank's chunk
6. WHEN creating a new bank THEN the System SHALL update the corresponding DIV1 flag to 1

### Requirement 20: Drum Kit Data Structure (DKT1/DBK1)

**User Story:** As a developer, I want to understand drum kit structure, so that I can display and potentially edit drum kit data.

#### Acceptance Criteria

1. WHEN parsing DKT1 THEN the System SHALL read the container chunk and iterate through DBK1 sub-chunks
2. WHEN parsing DBK1 THEN the System SHALL read the number of drum kits at offset +12 (4 bytes, big-endian)
3. WHEN parsing DBK1 THEN the System SHALL read the drum kit size at offset +16 (4 bytes, big-endian)
4. WHEN parsing DBK1 THEN the System SHALL read the bank ID at offset +20 (4 bytes, big-endian)
5. WHEN parsing DBK1 THEN the System SHALL read drum kit data starting at offset +24
6. WHEN decoding drum kit bank ID THEN the System SHALL map 0 to INT bank
7. WHEN decoding drum kit bank ID THEN the System SHALL map 0x20000+ to USER banks (U-A through U-GG)
8. WHEN parsing a Kronos drum kit THEN the System SHALL read the 24-byte name at offset +0

### Requirement 21: Wave Sequence Data Structure (WSQ1/WBK1)

**User Story:** As a developer, I want to understand wave sequence structure, so that I can display and potentially edit wave sequence data.

#### Acceptance Criteria

1. WHEN parsing WSQ1 THEN the System SHALL read the container chunk and iterate through WBK1 sub-chunks
2. WHEN parsing WBK1 THEN the System SHALL read the number of wave sequences at offset +12 (4 bytes, big-endian)
3. WHEN parsing WBK1 THEN the System SHALL read the wave sequence size at offset +16 (4 bytes, big-endian)
4. WHEN parsing WBK1 THEN the System SHALL read the bank ID at offset +20 (4 bytes, big-endian)
5. WHEN parsing WBK1 THEN the System SHALL read wave sequence data starting at offset +24
6. WHEN decoding wave sequence bank ID THEN the System SHALL map 0 to INT bank
7. WHEN decoding wave sequence bank ID THEN the System SHALL map 0x20000+ to USER banks (U-A through U-GG)
8. WHEN parsing a Kronos wave sequence THEN the System SHALL read the 24-byte name at offset +0

### Requirement 22: Global Category Names Structure

**User Story:** As a developer, I want to understand GLB1 category name storage, so that I can display user-defined category names.

#### Acceptance Criteria

1. WHEN parsing GLB1 THEN the System SHALL locate category names at offset 12912 from GLB1 data start (Kronos/Oasys)
2. WHEN parsing category names THEN the System SHALL read 18 main categories
3. WHEN parsing category names THEN the System SHALL read 8 sub-categories per main category
4. WHEN parsing category names THEN the System SHALL read 24 bytes per category name
5. WHEN calculating category name offset THEN the System SHALL use formula: GLB1_offset + 12912 + (category_index × 8 × 24) + (sub_category_index × 24)
6. WHEN a file lacks GLB1 THEN the System SHALL use default Korg category names

### Requirement 23: Extended Data Chunks (PRG2/CMB2/STL2) for Kronos OS 1.5+

**User Story:** As a developer, I want to understand extended data chunks, so that I can preserve Kronos OS 1.5+ specific data during editing.

#### Acceptance Criteria

1. WHEN parsing a Kronos OS 1.5+ file THEN the System SHALL detect INI3 chunk presence to identify OS version
2. WHEN parsing PRG2 THEN the System SHALL read extended program parameters for each program
3. WHEN parsing CMB2 THEN the System SHALL read extended combi parameters (16 timbres × N parameters)
4. WHEN parsing STL2 THEN the System SHALL read extended set list slot parameters (bank and patch bytes)
5. WHEN copying a program THEN the System SHALL also copy corresponding PRG2 data
6. WHEN copying a combi THEN the System SHALL also copy corresponding CMB2 data
7. WHEN copying a set list slot THEN the System SHALL also copy corresponding STL2 data
8. WHEN writing a modified file THEN the System SHALL preserve PRG2/CMB2/STL2 chunk structure

### Requirement 24: Multi-Model Support Offsets

**User Story:** As a developer, I want to understand model-specific offsets, so that I can support multiple Korg workstations.

#### Acceptance Criteria

1. WHEN parsing an Oasys file (product ID 0x70) THEN the System SHALL use DIV1 offset 0x1C
2. WHEN parsing a Triton file (product ID 0x50) THEN the System SHALL use DIV1 offset 0x18
3. WHEN parsing an M3 file (product ID 0x75) THEN the System SHALL use DIV1 offset 0x1C
4. WHEN parsing a Krome file (product ID 0x95) THEN the System SHALL use DIV1 offset 0x1C
5. WHEN parsing a Kross file (product ID 0x96) THEN the System SHALL use DIV1 offset 0x1C
6. WHEN parsing model-specific program data THEN the System SHALL use model-appropriate offsets for parameters
7. WHEN parsing model-specific combi data THEN the System SHALL use model-appropriate timbre offsets

