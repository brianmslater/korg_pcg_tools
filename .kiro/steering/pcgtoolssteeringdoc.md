# PCG Tools Steering

## Original C# Source
The original PCG Tools application (C#/.NET) is available at:
https://github.com/DaBlick/PCG-Tools

Local copy available at: `pcg-tools-csharp/`

Reference this repository when implementing features or verifying behavior parity.

## MANDATORY: Verification Before Implementation

**DO NOT make assumptions about PCG file structure or feature behavior.**

**C# IS THE SOURCE OF TRUTH. ALWAYS USE C# FIRST.**

Before implementing or modifying ANY feature, you MUST:

1. **Check C# Source Code First - EXHAUSTIVELY**
   - Search `pcg-tools-csharp/` for the relevant C# implementation
   - Read the actual C# code to understand exact offsets, bit fields, and algorithms
   - If you don't find it in one file, KEEP LOOKING in other C# files
   - Check parent classes, interfaces, and related files
   - Search for the parameter name, offset value, or feature name across ALL C# files
   - Key files to check:
     - `KronosProgram.cs` - Program structure and parameters
     - `KronosCombi.cs` - Combi structure and parameters
     - `KronosTimbre.cs` - Timbre structure (188 bytes each)
     - `KronosOasysTimbre.cs` - Base timbre parameters
     - `Timbre.cs` - Common timbre parameters (Volume, Transpose, etc.)
     - `KronosSetListSlot.cs` - Set list slot structure
     - `KronosPcgMemory.cs` - Checksum algorithm, INI2/INI3 handling
     - `PcgFileReader.cs` - Bank ID decoding, chunk parsing
   - **DO NOT give up searching C# until you have checked ALL relevant files**

2. **Check Korg Documentation**
   - Read `pcg-tools-csharp/Documentation/PCG Structure Kronos.txt`
   - Verify parameter ranges and data types against official specs
   - Cross-reference with Korg MIDI implementation guides if needed

3. **Only After C# is Exhausted, Check Python**
   - Python code should ONLY be consulted AFTER C# has been fully searched
   - Python is for verification, NOT as a source of truth
   - If Python differs from C#, C# is correct
   - Compare Python code against C# implementation line-by-line
   - Ensure offsets, bit masks, and algorithms are identical
   - Document any intentional differences with justification

**If you cannot find the answer in C# after exhaustive search, ASK before proceeding.**

## Problem Resolution Rules

**DO NOT move on when a solution is still pending.**

- If a test fails, fix it before proceeding to the next task
- If an implementation has issues, resolve them completely
- Do NOT defer problems or assume they can be addressed later
- Do NOT mark tasks as complete if there are known issues
- If you cannot fix a problem after multiple attempts, ASK the user:
  - Explain what you tried and why it failed
  - Ask if it's okay to move on or if you should keep trying
  - Never silently skip or defer issues
- Stay on the problem until it is fully resolved OR the user explicitly approves moving on

## Complete Implementation Rule

**ALL functions and features MUST be fully implemented - no minimization or shortcuts.**

- Implement ALL functionality from the C# source, not just the "important" parts
- Do NOT skip features because they seem complex or rarely used
- Do NOT suggest skipping tasks or deferring them to later
- Every task in the task list must be completed in order
- If a C# feature exists, it must be ported completely
- Do NOT ask "would you like me to skip this?" - just implement it
- Complete each phase fully before moving to the next phase

## Feature Parity Goal
This Python project must maintain feature parity with the original C# PCG Tools application. When implementing or modifying features, ensure they match the behavior and capabilities of the original C# version.

## Guidelines
- Before adding new features, verify they exist in the original C# PCG Tools
- When fixing bugs, consider how the original C# version handled the same scenario
- Maintain compatibility with PCG files created by the original tool
- UI workflows should feel familiar to users of the original C# application

## File Integrity
PCG file structure integrity is critical. Any changes to file reading/writing code must:
- Preserve the exact binary structure of PCG files
- Validate that modified files can be loaded back by Korg hardware
- Never corrupt chunk headers, checksums, or data boundaries
- Test roundtrip operations (read → modify → write → read) to ensure no data loss

## Korg Documentation
Always consult official Korg documentation when implementing or modifying features:
- Reference Korg MIDI implementation guides for SysEx and parameter details
- Verify PCG file format specifications against Korg technical documentation
- Use Korg's published parameter ranges and data types as the source of truth

## Testing Requirements
All new features and functions must include tests for validation:

### CLI Testing
- Create test scripts that exercise CLI commands with various inputs
- Verify command output matches expected results
- Test error handling for invalid inputs and edge cases
- Validate file operations produce correct PCG output

### GUI Testing
- Create test scripts that validate GUI logic and data handling
- Test dialog inputs and parameter validation
- Verify UI state changes reflect correct data model updates
- Document manual test procedures in `test_gui_manual.md` for visual verification

### General Testing Rules
- Tests should be placed in root directory as `test_*.py` files
- Every feature must have corresponding test coverage before completion
- Run `python test_complete.py` to validate all functionality
- Include roundtrip tests for any file modification features

## Tasks to Fix

### ✅ Save As and File Renaming (COMPLETED)
Implement "Save As" functionality to duplicate and rename files without overwriting the original PCG.
- Status: Already implemented in gui_qt.py (save_as_file method)

### ✅ Undo Support (COMPLETED)
Implement Undo command to allow safe experimentation without requiring full file reload after incorrect actions.
- Status: Implemented - UndoManager integrated into GUI with Ctrl+Z/Ctrl+Shift+Z shortcuts

### ✅ Copy and Paste Between Two PCG Files (COMPLETED)
Enable copying combis and programs from one PCG file into another when two different PCG files are open.
- Status: Implemented - "Paste from Other Window..." menu option added

### ✅ Engine Type Mismatch Validation (COMPLETED)
Prevent mixing HD-1 and EXi programs in the same bank. Add validation to block pasting an HD-1 program into an EXi bank (and vice versa) as this causes load errors on Kronos hardware.
- Status: Implemented - _validate_engine_compatibility() checks before paste operations

### ✅ Missing User Banks in Destination File (COMPLETED)
Allow pasting programs into user banks (e.g., U-GG, U-G) that don't exist in the destination file.
- Status: Fully implemented with bank creation capability
- Implementation:
  - `bank_creator.py` module creates PBK1 chunks with correct binary structure
  - `insert_bank_into_pcg()` adds new user banks to existing PCG files
  - GUI prompts user to create missing banks when pasting from another file
  - Tools → Create User Bank menu option for manual bank creation
  - Tested with roundtrip save/load verification

### ✅ Setlist Slot Display: Show Referenced Patch Name (COMPLETED)
Display the referenced program/combi name for setlist slots that don't have a custom slot name.

- Status: Implemented in `load_setlist_slots()` in gui_qt.py
- Implementation:
  - "Slot Name" column shows custom name if set, otherwise shows patch name in brackets with gray text
  - "Patch Name" column always shows the actual referenced program/combi name
  - Empty slots show empty in both columns

## Prompt Logging

All prompts provided during development sessions MUST be logged to `Prompts_Used.txt` in the project root.

- Log each prompt with a timestamp
- Include the context/task being worked on
- This creates a record of AI interactions for reference and reproducibility

## MANDATORY: C# Review Dimensions

When reviewing C# code for feature parity, check ALL of these dimensions - not just "does the function exist":

### 1. Architecture
- Data model patterns (eager vs lazy loading, pre-created collections)
- Object lifecycle (when are things created, initialized, disposed?)
- Parent-child relationships between classes
- How collections are populated and managed

### 2. Naming Conventions
- Exact property/method names (singular vs plural, camelCase vs snake_case mapping)
- Parameter names in function signatures
- Class and enum names
- Constants and magic values

### 3. Data Types & Constraints
- What type is each property? (string vs int, enum vs string)
- What are valid ranges for numeric values?
- Are there nullable types or optional values?
- What's the size/length of string fields?

### 4. Factory/Default Data
- Pre-defined constants (bank engine types, category lists, color mappings)
- Default values for new objects
- ROM/factory data that's baked into the application
- Lookup tables and mappings

### 5. Validation Rules
- Engine compatibility checks
- Bank type restrictions
- Range validation on parameters
- Cross-field validation (e.g., combi timbre references valid programs)

### 6. UI Workflows
- How does C# present empty/missing data?
- What happens on paste into non-existent bank?
- What dialogs appear and when?
- What's enabled/disabled based on state?

### 7. State Management
- What gets initialized when file is loaded?
- What's the lifecycle of clipboard contents?
- How is dirty/modified state tracked?
- What triggers UI refreshes?

### 8. Error Handling
- How does C# handle edge cases?
- What error messages are shown to users?
- What operations fail silently vs show errors?
- How are invalid files handled?

### Review Checklist Per Feature

Before implementing ANY feature, answer these questions from C# code:

- [ ] **Architecture**: How are the data structures organized?
- [ ] **Naming**: What are the exact property/method names?
- [ ] **Types**: What data types are used?
- [ ] **Defaults**: What factory/default data exists?
- [ ] **Validation**: What checks happen before operations?
- [ ] **UI Flow**: How does the UI present this feature?
- [ ] **State**: What state changes occur?
- [ ] **Errors**: How are errors handled?

### Examples of Missed Issues

| Issue | Dimension Missed | What C# Review Would Show |
|-------|-----------------|---------------------------|
| Empty banks not shown | Architecture | `CreateBanks()` pre-creates ALL banks |
| `has_programs()` vs `has_program()` | Naming | C# uses singular method names |
| `bank_index` vs `patch_bank` | Types | C# uses string bank ID, not int index |
| Wrong engine type on bank creation | Factory Data | `KronosProgramBanks.cs` has bank descriptions |

## MANDATORY: Architectural Review Before Major Changes

Before implementing UI features or data model changes, review C# architecture patterns:

### What to Review

1. **Data Model Initialization**
   - Check if C# pre-creates all possible banks/slots vs. lazy loading
   - Example: `KronosProgramBanks.CreateBanks()` creates ALL banks upfront
   - Example: `KronosCombiBanks.CreateBanks()` creates ALL combi banks upfront

2. **Method Naming Conventions**
   - C# uses singular/plural consistently - match in Python
   - Example: `has_program()` not `has_programs()`

3. **Property vs. Method Access**
   - Check if C# uses properties or methods for data access
   - Example: `set_lists` not `setlists`, `patch_bank` not `bank_index`

4. **Bank Type Designations**
   - Banks have factory-designated engine types (EXi vs HD-1)
   - Check `KronosProgramBanks.cs` for bank descriptions

### Known Architectural Differences

| Feature | C# Pattern | Python Must Match |
|---------|-----------|-------------------|
| Bank Lists | Pre-creates ALL possible banks | Show all banks, mark empty ones |
| Clipboard | Singular methods: `has_program()` | Use singular method names |
| SetList | `set_lists` property | Use `set_lists` not `setlists` |
| SetListSlot | `patch_bank` (string) | Use `patch_bank` not `bank_index` |
| Bank Engine | Factory presets define EXi/HD-1 | Use `bank_creator.is_exi_bank()` |

### Review Checklist

Before implementing ANY UI or data model feature:

- [ ] Search C# for the feature's data model classes
- [ ] Check how C# initializes collections (lazy vs. eager)
- [ ] Verify method/property naming matches C#
- [ ] Check if C# has validation or constraints
- [ ] Look for factory preset data (bank types, categories, etc.)

### Common Architectural Pitfalls

1. **Assuming lazy loading** - C# often pre-creates all possible items
2. **Wrong attribute names** - Always verify exact C# property names
3. **Missing validation** - C# may have engine type or bank compatibility checks
4. **Ignoring factory presets** - Banks have designated engine types

### Bank Engine Type Reference

Based on C# `KronosProgramBanks.cs`:

**EXi Banks (MBK1 chunks):**
- I-A: SGX-1, EP-1 and best of all other EXi
- U-B: AL-1
- U-C: AL-1 and CX-3
- U-D: STR-1
- U-E: MS-20EX & PolysixEX
- U-F: MOD-7

**HD-1 Banks (PBK1 chunks):**
- I-B through I-F: HD-1
- U-A: HD-1 including Ambient Drums and Sound Effects
- U-G: Initialized HD-1 Programs
- GM: GM2 Main programs (HD-1)
- U-AA through U-GG: Default to HD-1 (user-defined)
