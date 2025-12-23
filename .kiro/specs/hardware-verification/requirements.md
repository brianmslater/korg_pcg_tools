# Requirements Document

## Introduction

Hardware verification testing for PCG Tools v1.4.x on Korg Kronos hardware. This validates that all file editing features produce PCG files that load correctly and display the expected changes on actual Kronos hardware.

## Glossary

- **PCG_File**: Korg's binary file format for storing programs, combis, and setlists
- **Kronos**: Korg Kronos synthesizer workstation
- **Program**: A single sound patch
- **Combi**: A combination of up to 16 programs (timbres)
- **Timbre**: One of 16 program slots within a combi
- **Setlist**: A performance list containing 128 slots
- **Slot**: A setlist entry referencing a program or combi

## Requirements

### Requirement 1: File Round-Trip Integrity

**User Story:** As a user, I want PCG files saved by PCG Tools to load on my Kronos without errors.

#### Acceptance Criteria

1. WHEN a PCG file is opened and saved without modifications, THE Kronos SHALL load the file without errors
2. WHEN a PCG file is loaded on Kronos, THE programs and combis SHALL be accessible and playable

### Requirement 2: Program Editing

**User Story:** As a user, I want program edits made in PCG Tools to appear correctly on my Kronos.

#### Acceptance Criteria

1. WHEN a program name is changed, THE Kronos SHALL display the new name
2. WHEN a program category is changed, THE Kronos SHALL show the new category
3. WHEN a program favorite flag is toggled, THE Kronos SHALL display the favorite indicator

### Requirement 3: Combi Editing

**User Story:** As a user, I want combi edits made in PCG Tools to appear correctly on my Kronos.

#### Acceptance Criteria

1. WHEN a combi name is changed, THE Kronos SHALL display the new name
2. WHEN a combi category is changed, THE Kronos SHALL show the new category

### Requirement 4: Timbre Parameter Editing

**User Story:** As a user, I want timbre parameter changes to work correctly on my Kronos.

#### Acceptance Criteria

1. WHEN a timbre volume is changed, THE Kronos SHALL show the new volume value
2. WHEN a timbre MIDI channel is changed, THE Kronos SHALL assign the timbre to the new channel
3. WHEN a timbre transpose is changed, THE Kronos SHALL transpose the timbre by the specified amount
4. WHEN a timbre key zone is changed, THE Kronos SHALL only trigger the timbre within the specified key range

### Requirement 5: Setlist Editing

**User Story:** As a user, I want setlist edits made in PCG Tools to appear correctly on my Kronos.

#### Acceptance Criteria

1. WHEN a setlist name is changed, THE Kronos SHALL display the new name
2. WHEN a slot name is changed, THE Kronos SHALL display the new slot name
3. WHEN a slot color is changed, THE Kronos SHALL display the slot with the new color
4. WHEN a slot volume is changed, THE Kronos SHALL apply the new volume
5. WHEN a slot transpose is changed, THE Kronos SHALL transpose by the specified amount
6. WHEN a slot description is changed, THE Kronos SHALL display the new description

### Requirement 6: Copy/Paste Operations

**User Story:** As a user, I want copy/paste operations to produce valid patches on my Kronos.

#### Acceptance Criteria

1. WHEN a program is copied and pasted, THE Kronos SHALL load the pasted program correctly
2. WHEN a combi is copied and pasted, THE Kronos SHALL load the pasted combi with all timbres intact

### Requirement 7: Batch Operations

**User Story:** As a user, I want batch operations to not corrupt my PCG file.

#### Acceptance Criteria

1. WHEN programs are sorted, THE Kronos SHALL load all sorted programs correctly
2. WHEN undo is performed, THE previous state SHALL be restored correctly
