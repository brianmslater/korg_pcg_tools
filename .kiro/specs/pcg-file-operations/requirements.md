# Requirements Document

## Introduction

This document specifies requirements for enhancing PCG Tools with critical file operation features: cross-file copy/paste, missing bank creation, engine type validation, Save As functionality, and undo support. These features address gaps in the current Python implementation compared to the original C# PCG Tools application.

## Glossary

- **PCG File**: Korg's proprietary binary file format for storing synthesizer patch data (programs, combis, setlists)
- **Program**: A single synthesizer patch/sound
- **Combi**: A combination patch that layers or splits multiple programs
- **User Bank**: A writable bank for storing user-created patches (e.g., U-A through U-GG)
- **HD-1 Engine**: Korg's sample-based synthesis engine
- **EXi Engine**: Korg's expanded instrument engine with different synthesis types
- **Setlist**: An ordered collection of 128 slots referencing programs or combis for live performance
- **Clipboard**: In-memory storage for copied patch data during copy/paste operations

## Requirements

### Requirement 1: Cross-File Copy and Paste

**User Story:** As a musician, I want to copy programs and combis from one PCG file and paste them into another open PCG file, so that I can consolidate patches from multiple sources into a single working file.

#### Acceptance Criteria

1. WHEN a user has two PCG files open AND copies a program from the source file THEN the System SHALL store the program data in the clipboard with source file context
2. WHEN a user pastes a copied program into a destination file THEN the System SHALL insert the program data at the selected bank and slot location
3. WHEN a user copies a combi from the source file THEN the System SHALL store the combi data including all timbre references in the clipboard
4. WHEN a user pastes a copied combi into a destination file THEN the System SHALL insert the combi data and preserve internal timbre program references
5. WHEN a paste operation completes successfully THEN the System SHALL update the destination file's modified state to indicate unsaved changes

### Requirement 2: Missing User Bank Creation

**User Story:** As a sound designer, I want to paste programs into user banks that don't exist in my destination file, so that I can organize patches without being limited by the current bank structure.

#### Acceptance Criteria

1. WHEN a user attempts to paste into a user bank that does not exist in the destination file THEN the System SHALL prompt the user to create the missing bank
2. WHEN the user confirms bank creation THEN the System SHALL create the user bank with the correct chunk structure and size
3. WHEN a new user bank is created THEN the System SHALL initialize all slots to empty/default state
4. WHEN a new user bank is created THEN the System SHALL maintain valid PCG file structure with correct chunk headers and checksums

### Requirement 3: Engine Type Validation

**User Story:** As a Kronos user, I want the tool to prevent me from mixing HD-1 and EXi programs in the same bank, so that I avoid creating PCG files that cause load errors on my hardware.

#### Acceptance Criteria

1. WHEN a user attempts to paste a program into a bank THEN the System SHALL detect the engine type of the source program
2. WHEN the destination bank contains programs of a different engine type THEN the System SHALL block the paste operation
3. WHEN a paste operation is blocked due to engine type mismatch THEN the System SHALL display a clear error message explaining the incompatibility
4. WHEN a user pastes into an empty bank THEN the System SHALL allow the paste regardless of engine type

### Requirement 4: Save As Functionality

**User Story:** As a user, I want to save my PCG file with a new name, so that I can create backups or variations without overwriting my original file.

#### Acceptance Criteria

1. WHEN a user selects Save As THEN the System SHALL display a file dialog for selecting the destination path and filename
2. WHEN the user confirms the Save As dialog THEN the System SHALL write the complete PCG data to the new file path
3. WHEN Save As completes successfully THEN the System SHALL update the current working file reference to the new file path
4. WHEN Save As completes successfully THEN the System SHALL clear the modified state indicator
5. IF the user cancels the Save As dialog THEN the System SHALL maintain the current file state without changes

### Requirement 5: Undo Support

**User Story:** As a user, I want to undo my recent changes, so that I can experiment with edits safely and recover from mistakes without reloading the entire file.

#### Acceptance Criteria

1. WHEN a user performs an edit operation (paste, delete, rename, move) THEN the System SHALL store the previous state in an undo stack
2. WHEN a user triggers the undo command THEN the System SHALL restore the previous state from the undo stack
3. WHEN a user triggers undo after an undo THEN the System SHALL restore the next previous state (multiple undo levels)
4. WHEN the undo stack is empty THEN the System SHALL disable the undo command
5. WHEN a user performs a new edit after undoing THEN the System SHALL clear any redo history and add the new edit to the undo stack
