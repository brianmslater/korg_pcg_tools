# Requirements Document

## Introduction

This document specifies requirements for a comprehensive feature parity review between the original C# PCG Tools application and the Python port. The primary focus is on **Korg Kronos** support, with secondary support for other models. The goal is to ensure the Python version achieves complete functional parity with the original C# implementation for Kronos users.

## Glossary

- **PCG File**: Korg's proprietary binary file format for storing synthesizer patch data
- **Program**: A single synthesizer patch/sound (HD-1 or EXi engine type on Kronos)
- **Combi**: A combination patch that layers or splits multiple programs (up to 16 timbres)
- **Timbre**: A program slot within a combi (up to 16 per combi on Kronos)
- **Set List**: An ordered collection of 128 slots referencing programs or combis (16 set lists on Kronos)
- **Set List Slot**: A single entry in a set list with performance parameters (name, color, transpose, volume)
- **User Bank**: Writable banks for user patches (U-A through U-GG on Kronos OS 1.5+)
- **GM2 Bank**: Read-only General MIDI 2 banks (g(1)-g(9), g(d) on Kronos)
- **HD-1 Engine**: Korg's sample-based synthesis engine
- **EXi Engine**: Korg's expanded instrument engine with different synthesis types
- **Master File**: A reference PCG file used to provide category names for files without global chunks
- **Virtual Bank**: A logical bank that aggregates patches from multiple physical banks (Kronos only)
- **SNG File**: Korg song file format containing sequencer data and sample references
- **CRC**: Cyclic Redundancy Check value for patch comparison

## Supported Models Reference

### Primary Focus (HIGH PRIORITY)
- **Korg Kronos** (all versions: Kronos, Kronos X, Kronos 2) - OS 1.0 through 3.x

### Secondary Support (MEDIUM PRIORITY - Already Implemented)
- Korg Oasys
- Korg M3/M50
- Korg Triton (Classic/LE/Extreme/Studio/Rack/TR)
- Korg Karma
- Korg Krome/Krome EX
- Korg Kross/Kross 2
- Korg Trinity

### Legacy Models (LOW PRIORITY - Not Implemented)
- Korg microStation (PCG files)
- Korg microKORG/microKORG XL (.syx files)
- Korg MS2000 (.syx files)
- Korg M1/M1R (.syx files)
- Korg 01/W series (.syx files)
- Korg T1/T2/T3 series (.syx files)
- Korg Z1 (.syx files)
- Korg Wavestation (.syx files)

## Requirements

### Requirement 1: Kronos PCG File Support

**User Story:** As a Korg Kronos owner, I want PCG Tools to fully support all Kronos PCG file versions, so that I can manage my patch files regardless of which OS version I use.

#### Acceptance Criteria

1. WHEN a user opens a Kronos OS 1.0/1.1 PCG file THEN the System SHALL parse and display all programs, combis, and set lists correctly
2. WHEN a user opens a Kronos OS 1.5/1.6 PCG file THEN the System SHALL parse extended user banks (U-AA through U-GG) correctly
3. WHEN a user opens a Kronos OS 2.x PCG file THEN the System SHALL parse all data structures correctly
4. WHEN a user opens a Kronos OS 3.x PCG file THEN the System SHALL parse all data structures correctly
5. WHEN a user opens a Kronos X PCG file THEN the System SHALL handle the file identically to standard Kronos files
6. WHEN a user opens a Kronos 2 PCG file THEN the System SHALL handle the file identically to standard Kronos files
7. WHEN a user saves a Kronos PCG file THEN the System SHALL preserve the exact binary structure and checksums
8. WHEN a user modifies and saves a Kronos PCG file THEN the System SHALL produce a file loadable by Kronos hardware

### Requirement 2: Kronos Program Editing

**User Story:** As a Kronos sound designer, I want to edit program properties, so that I can organize and customize my patch library.

#### Acceptance Criteria

1. WHEN a user edits a program name THEN the System SHALL update the 24-character name in the PCG data structure
2. WHEN a user changes a program category THEN the System SHALL update the category value (0-15 for Kronos categories)
3. WHEN a user changes a program sub-category THEN the System SHALL update the sub-category value correctly
4. WHEN a user marks a program as favorite THEN the System SHALL set the favorite flag in the PCG data
5. WHEN a user clears a program THEN the System SHALL reset the program to default/init state
6. WHEN a user edits program OSC mode THEN the System SHALL update the oscillator mode parameter
7. WHEN a user views a GM2 program THEN the System SHALL display the program as read-only with [ROM] indicator
8. WHEN a user attempts to edit a GM2 program THEN the System SHALL prevent the edit and display an appropriate message
9. WHEN a user copies a GM2 program THEN the System SHALL allow copying to a user bank

### Requirement 3: Kronos Combi Editing

**User Story:** As a Kronos sound designer, I want to edit combi properties, so that I can organize and customize my layered sounds.

#### Acceptance Criteria

1. WHEN a user edits a combi name THEN the System SHALL update the 24-character name in the PCG data structure
2. WHEN a user changes a combi category THEN the System SHALL update the category value correctly
3. WHEN a user changes a combi sub-category THEN the System SHALL update the sub-category value correctly
4. WHEN a user marks a combi as favorite THEN the System SHALL set the favorite flag in the PCG data
5. WHEN a user clears a combi THEN the System SHALL reset the combi and all 16 timbres to default state
6. WHEN a user edits combi tempo THEN the System SHALL update the tempo parameter

### Requirement 4: Kronos Copy/Paste Operations

**User Story:** As a Kronos musician, I want to copy and paste patches between banks and files, so that I can organize my sound library efficiently.

#### Acceptance Criteria

1. WHEN a user copies a program THEN the System SHALL store the complete program data in the clipboard
2. WHEN a user pastes a program THEN the System SHALL insert the program at the selected location
3. WHEN a user copies a combi THEN the System SHALL store the combi data including all 16 timbre references
4. WHEN a user pastes a combi THEN the System SHALL insert the combi and optionally copy referenced programs
5. WHEN a user copies a set list slot THEN the System SHALL store the slot data including all Kronos-specific parameters
6. WHEN a user pastes a set list slot THEN the System SHALL insert the slot and optionally copy referenced patches
7. WHEN a user cuts a patch THEN the System SHALL copy the patch and clear the original location
8. WHEN a user pastes between different PCG files THEN the System SHALL handle program remapping correctly
9. WHEN a user pastes an HD-1 program into an EXi bank THEN the System SHALL block the operation and display an engine type mismatch error
10. WHEN a user pastes an EXi program into an HD-1 bank THEN the System SHALL block the operation and display an engine type mismatch error
11. WHEN a user pastes into a non-existent user bank THEN the System SHALL offer to create the missing bank
12. WHEN a user pastes from a GM2 bank THEN the System SHALL copy the program to the destination user bank

### Requirement 5: Kronos Batch Operations

**User Story:** As a Kronos power user, I want to perform batch operations on multiple patches, so that I can efficiently manage large patch libraries.

#### Acceptance Criteria

1. WHEN a user selects multiple patches and moves them up THEN the System SHALL move all selected patches up by one position
2. WHEN a user selects multiple patches and moves them down THEN the System SHALL move all selected patches down by one position
3. WHEN a user compacts a bank THEN the System SHALL move all empty slots to the end of the bank
4. WHEN a user sorts patches alphabetically THEN the System SHALL reorder patches by name with empty/init patches at the end
5. WHEN a user sorts patches by category THEN the System SHALL reorder patches by category then name
6. WHEN a user removes duplicates THEN the System SHALL identify and remove duplicate patches while updating combi and set list references
7. WHEN a user capitalizes names THEN the System SHALL convert patch names to title case
8. WHEN a user changes volumes for multiple combis THEN the System SHALL update the volume parameter for all selected combis
9. WHEN batch operations complete THEN the System SHALL update all affected combi and set list references automatically

### Requirement 6: Kronos Set List Editing

**User Story:** As a performing Kronos musician, I want to edit set lists and slots, so that I can prepare my performance configurations.

#### Acceptance Criteria

1. WHEN a user edits a set list name THEN the System SHALL update the 24-character set list name in the PCG data
2. WHEN a user edits a slot name THEN the System SHALL update the 24-character slot name parameter
3. WHEN a user edits a slot color THEN the System SHALL update the slot color parameter (0-16 color values)
4. WHEN a user edits a slot text size THEN the System SHALL update the font size parameter (XS/S/M/L/XL)
5. WHEN a user edits a slot transpose THEN the System SHALL update the transpose parameter (-24 to +24 semitones)
6. WHEN a user edits a slot volume THEN the System SHALL update the volume parameter (0-127)
7. WHEN a user edits a slot description THEN the System SHALL update the 512-character description/notes field
8. WHEN a user assigns a program or combi to a slot THEN the System SHALL update the slot reference type and ID
9. WHEN a user auto-fills slots THEN the System SHALL populate slots based on program/combi names
10. WHEN a user clears a slot THEN the System SHALL reset the slot to default state (reference to I-A000)
11. WHEN a user sorts slots THEN the System SHALL reorder slots by the selected criteria
12. WHEN a user views a slot without custom name THEN the System SHALL display the referenced patch name

### Requirement 7: Kronos Combi Timbre Editing

**User Story:** As a Kronos sound designer, I want to edit combi timbres, so that I can customize layered and split sounds.

#### Acceptance Criteria

1. WHEN a user views combi timbres THEN the System SHALL display all 16 timbres with their parameters and program names
2. WHEN a user edits timbre volume THEN the System SHALL update the volume parameter (0-127)
3. WHEN a user edits timbre MIDI channel THEN the System SHALL update the channel parameter (1-16 or Gch)
4. WHEN a user edits timbre transpose THEN the System SHALL update the transpose parameter (-24 to +24)
5. WHEN a user edits timbre detune THEN the System SHALL update the detune parameter
6. WHEN a user edits timbre status THEN the System SHALL update the status (INT/EXT/EX2/OFF)
7. WHEN a user edits timbre mute THEN the System SHALL update the mute flag
8. WHEN a user edits timbre key zones THEN the System SHALL update the top/bottom key parameters (C-1 to G9)
9. WHEN a user edits timbre velocity zones THEN the System SHALL update the top/bottom velocity parameters (1-127)
10. WHEN a user edits timbre priority THEN the System SHALL update the voice priority parameter
11. WHEN a user edits timbre portamento THEN the System SHALL update the portamento settings
12. WHEN a user moves a timbre up/down THEN the System SHALL swap timbre positions
13. WHEN a user clears a timbre THEN the System SHALL reset the timbre to default state
14. WHEN a user sorts timbres THEN the System SHALL reorder timbres by the selected criteria (channel/program/status)
15. WHEN a user clears unused timbres THEN the System SHALL reset all muted/OFF timbres

### Requirement 8: List Generation and Reports

**User Story:** As a Kronos user, I want to generate reports and lists from my PCG files, so that I can document and analyze my patch library.

#### Acceptance Criteria

1. WHEN a user generates a patch list THEN the System SHALL create a list of all programs and combis with their properties including favorites
2. WHEN a user generates a program usage list THEN the System SHALL show which combis and set lists use each program
3. WHEN a user generates a combi content list (short) THEN the System SHALL show the programs used in each combi
4. WHEN a user generates a combi content list (long) THEN the System SHALL show all timbre parameters for each combi
5. WHEN a user generates a differences list THEN the System SHALL compare two PCG files and show differences
6. WHEN a user generates a file content list THEN the System SHALL show bank usage summary with synthesis engine types
7. WHEN a user exports to CSV format THEN the System SHALL create a properly formatted CSV file with proper escaping
8. WHEN a user exports to TXT format THEN the System SHALL create a readable text file
9. WHEN a user exports to XML format THEN the System SHALL create a valid XML file with XSL stylesheet
10. WHEN a user exports to ASCII table format THEN the System SHALL create an aligned text table
11. WHEN a user generates a Cubase instrument definition THEN the System SHALL create a compatible definition file
12. WHEN a user requests CRC values THEN the System SHALL calculate and display CRC for patch comparison (including/excluding name)
13. WHEN a user filters by text THEN the System SHALL only include patches matching the search text
14. WHEN a user filters by favorite THEN the System SHALL only include patches marked as favorite

### Requirement 9: Master Files (Kronos)

**User Story:** As a Kronos user with partial PCG files, I want to use master files, so that I can see category names even when my file lacks a global chunk.

#### Acceptance Criteria

1. WHEN a user sets a master file THEN the System SHALL store the master file reference persistently
2. WHEN a user opens a PCG without global chunk THEN the System SHALL load category names from the master file
3. WHEN a user views timbres in a partial file THEN the System SHALL show program names from the master file
4. WHEN a user manages master files THEN the System SHALL allow opening, closing, and unassigning master files
5. WHEN a master file is already loaded THEN the System SHALL not reload it unnecessarily

### Requirement 10: Kronos SNG File Support

**User Story:** As a Kronos user, I want to view SNG file contents, so that I can see song names and sample usage.

#### Acceptance Criteria

1. WHEN a user opens a Kronos SNG file THEN the System SHALL display the song names
2. WHEN a user views SNG details THEN the System SHALL show the samples and sample files used
3. WHEN a user views SNG info THEN the System SHALL display the workstation model and sample count
4. WHEN a user views song timbres THEN the System SHALL display the timbres used in each song

### Requirement 11: Kronos Advanced Features

**User Story:** As a Kronos power user, I want access to advanced features, so that I can perform complex patch management tasks.

#### Acceptance Criteria

1. WHEN a user uses the program reference changer THEN the System SHALL update all combi and set list references to a program
2. WHEN a user enables virtual banks THEN the System SHALL display aggregated views of patches across all user banks
3. WHEN a user views reference counts THEN the System SHALL show how many combis/set lists reference each program
4. WHEN a user filters by text THEN the System SHALL show only patches matching the search text
5. WHEN a user filters by favorite THEN the System SHALL show only patches marked as favorite
6. WHEN a user filters by category THEN the System SHALL show only patches in the selected category
7. WHEN a user views drum kits THEN the System SHALL display drum kit banks with names
8. WHEN a user views wave sequences THEN the System SHALL display wave sequence banks with names

### Requirement 12: User Interface Features

**User Story:** As a user, I want a full-featured user interface, so that I can work efficiently with my PCG files.

#### Acceptance Criteria

1. WHEN a user opens multiple PCG files THEN the System SHALL display each in a separate window
2. WHEN a user uses keyboard shortcuts THEN the System SHALL execute the corresponding commands (Ctrl+C, Ctrl+V, Ctrl+Z, etc.)
3. WHEN a user right-clicks THEN the System SHALL display a context menu with relevant options
4. WHEN a user closes the application THEN the System SHALL remember window positions and sizes
5. WHEN a user has unsaved changes THEN the System SHALL warn before closing
6. WHEN a user accesses recent files THEN the System SHALL display a list of recently opened files
7. WHEN a user uses undo (Ctrl+Z) THEN the System SHALL restore the previous state
8. WHEN a user uses redo (Ctrl+Shift+Z) THEN the System SHALL restore the undone state
9. WHEN a user enables auto-backup THEN the System SHALL save backup copies at configurable intervals
10. WHEN a user uses Save As THEN the System SHALL allow saving to a new filename
11. WHEN a user uses Revert to Saved THEN the System SHALL reload the file from disk
12. WHEN a user double-clicks a patch THEN the System SHALL open the edit dialog
13. WHEN a user presses F6 THEN the System SHALL move to the next window
14. WHEN a user presses Ctrl+F4 THEN the System SHALL close the current window

### Requirement 13: Language Support

**User Story:** As a user, I want PCG Tools to display clear, consistent US English text, so that I can understand all features and options.

#### Acceptance Criteria

1. WHEN the System displays any UI text THEN the System SHALL use US English spelling and terminology
2. WHEN the System displays error messages THEN the System SHALL use clear, actionable language
3. WHEN the System displays tooltips THEN the System SHALL provide helpful context for each control

**Note:** The C# version supports 15+ languages (Dutch, French, German, Spanish, Portuguese, Italian, Polish, Czech, Greek, Turkish, Latin Serbian, Russian). Multi-language support is LOW PRIORITY for the Python version - focus on US English first.

### Requirement 14: Kronos-Specific Bank Support

**User Story:** As a Kronos user, I want full support for all Kronos bank types, so that I can manage my complete patch library.

#### Acceptance Criteria

1. WHEN a user views program banks THEN the System SHALL display all internal banks (I-A through I-F)
2. WHEN a user views program banks THEN the System SHALL display all user banks (U-A through U-G)
3. WHEN a user views program banks (OS 1.5+) THEN the System SHALL display extended user banks (U-AA through U-GG)
4. WHEN a user views program banks THEN the System SHALL display GM2 banks (g(1)-g(9), g(d)) as read-only
5. WHEN a user views combi banks THEN the System SHALL display all internal banks (I-A through I-F)
6. WHEN a user views combi banks THEN the System SHALL display all user banks (U-A through U-G)
7. WHEN a user views combi banks (OS 1.5+) THEN the System SHALL display extended user banks (U-AA through U-GG)
8. WHEN a user views set lists THEN the System SHALL display all 16 set lists with 128 slots each
9. WHEN a user views a bank THEN the System SHALL display the synthesis engine type (HD-1/EXi) in the bank list

