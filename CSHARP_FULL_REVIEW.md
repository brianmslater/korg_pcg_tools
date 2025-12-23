# C# Full Review - All 8 Dimensions

This document provides a comprehensive review of the C# PCG Tools codebase across all 8 review dimensions defined in the steering document.

## Review Date: December 23, 2025

---

## 1. ARCHITECTURE

### Data Model Initialization
| C# Pattern | Python Status | Action Needed |
|------------|---------------|---------------|
| `KronosProgramBanks.CreateBanks()` pre-creates ALL 85 banks (I-A to I-F, U-A to U-G, U-AA to U-GG, V0-A to V7-H, GM) | ✅ Fixed - `get_all_program_bank_ids()` returns all possible banks | None |
| `KronosCombiBanks.CreateBanks()` pre-creates ALL 14 combi banks (I-A to I-G, U-A to U-G) | ✅ Fixed - `get_all_combi_bank_ids()` returns all possible banks | None |
| Programs list per SynthesisType in clipboard | ✅ Implemented - `_programs_by_type` dict | None |
| `ProtectedPatches` collection for cut/paste | ✅ Implemented - `protected_patches` set | None |
| `PasteDuplicatesExecuted` flag | ✅ Implemented - `paste_duplicates_executed` | None |

### Object Lifecycle
| C# Pattern | Python Status | Action Needed |
|------------|---------------|---------------|
| Banks created at PCG load time | ✅ Implemented | None |
| Patches created lazily when bank is read | ✅ Implemented | None |
| Clipboard cleared on new copy | ✅ Implemented | None |

### Parent-Child Relationships
| C# Pattern | Python Status | Action Needed |
|------------|---------------|---------------|
| `IPatch.Parent` → Bank | ✅ Implemented via `bank` property | None |
| `IBank.Parent` → Banks collection | ✅ Not needed - Python uses flat list in PcgFile | None |
| `ITimbre.Parent` → Combi | ✅ Implemented | None |

---

## 2. NAMING CONVENTIONS

### Property/Method Names
| C# Name | Python Name | Status |
|---------|-------------|--------|
| `SetLists` | `set_lists` | ✅ Correct |
| `ProgramBanks` | `program_banks` | ✅ Correct |
| `CombiBanks` | `combi_banks` | ✅ Correct |
| `UsedPatch` | `patch_bank` + `patch_index` | ✅ Different pattern - Python stores components separately, GUI resolves |
| `SelectedPatchType` | `patch_type` | ✅ Correct |
| `ByteOffset` | `_raw_offset` | ✅ Correct |
| `PcgId` | `bank_id` (string) | ✅ Intentional - Python uses string for readability |
| `IsEmpty` | `is_empty()` function | ✅ Correct |
| `IsWritable` | `is_read_only` (inverted) | ✅ Correct (inverted logic) |
| `IsFilled` | `is_filled` property | ✅ Implemented - added to Bank class |

### Clipboard Method Names
| C# Name | Python Name | Status |
|---------|-------------|--------|
| `CopyProgramToClipBoard` | `copy_program()` | ✅ Correct |
| `CopyCombiToClipBoard` | `copy_combi()` | ✅ Correct |
| `CopySetListSlotToClipBoard` | `copy_slot()` | ✅ Correct |
| `PastePatch` | `paste_program()`, `paste_combi()` | ✅ Correct |
| `FindProgram` | `find_program()` | ✅ Implemented - finds by raw data comparison |

---

## 3. DATA TYPES & CONSTRAINTS

### SetListSlot Properties
| Property | C# Type | C# Range | Python Type | Python Range | Status |
|----------|---------|----------|-------------|--------------|--------|
| Name | string | 24 chars | str | 24 chars | ✅ |
| Description | string | 512 chars | str | 512 chars | ✅ |
| Volume | int | 0-127 | int | 0-127 | ✅ |
| Transpose | int | -24 to +24 (6-bit signed) | int | -24 to +24 | ✅ |
| Color | int | 0-16 | int | 0-16 | ✅ |
| TextSize | enum | 0-7 | int | 0-7 | ✅ |
| PatchType | enum | Program/Combi/Song | str | "Program"/"Combi"/"Song" | ✅ Supported |

### Program Properties
| Property | C# Type | C# Offset | Python Status |
|----------|---------|-----------|---------------|
| Name | string[24] | 0 | ✅ |
| OscMode | enum | 2558 | ✅ |
| Category | int (4 bits) | 2568 | ✅ |
| SubCategory | int (3 bits) | 2568 | ✅ |
| Favorite | bool | 2558, bit 5 | ✅ |

### Bank ID Encoding (from KronosProgramBanks.cs)
| Bank | C# PcgId | Python encode_bank_id() | Status |
|------|----------|-------------------------|--------|
| I-A | 0 | 0 | ✅ |
| I-F | 5 | 5 | ✅ |
| GM | 6 | 6 | ✅ |
| U-A | 17 | 17 | ✅ |
| U-G | 23 | 23 | ✅ |
| U-AA | 24 | 24 | ✅ |
| U-GG | 30 | 30 | ✅ |
| V0-A | 48 (0x30) | 48 | ✅ |

---

## 4. FACTORY/DEFAULT DATA

### Bank Engine Types (from KronosProgramBanks.cs)
| Bank | C# Description | Python `is_exi_bank()` | Status |
|------|----------------|------------------------|--------|
| I-A | "SGX-1, EP-1 and best of all other EXi" | True | ✅ |
| I-B to I-F | "HD-1" | False | ✅ |
| U-A | "HD1 including Ambient Drums and Sound Effects" | False | ✅ |
| U-B | "AL-1" | True | ✅ |
| U-C | "AL-1 and CX-3" | True | ✅ |
| U-D | "STR-1" | True | ✅ |
| U-E | "MS-20EX & PolysixEX" | True | ✅ |
| U-F | "MOD-7" | True | ✅ |
| U-G | "Initialized HD-1 Programs" | False | ✅ |
| U-AA to U-GG | (empty - user defined) | False (default HD-1) | ✅ |
| GM | "GM2 Main programs" | False (HD-1) | ✅ |

### Category Names
| Category | C# Source | Python Status |
|----------|-----------|---------------|
| Program categories | Read from GLB1 chunk | ✅ Implemented in pcg_structure.py |
| Combi categories | Read from GLB1 chunk | ✅ Implemented in pcg_structure.py |

### Color Names (SetListSlot)
| Value | C# Name | Python Status |
|-------|---------|---------------|
| 0 | Default | ✅ |
| 1-16 | Various colors | ✅ Derived from PCG file analysis (C# doesn't define names) |

---

## 5. VALIDATION RULES

### Engine Compatibility
| Rule | C# Implementation | Python Status |
|------|-------------------|---------------|
| EXi program → EXi bank only | Implicit via SynthesisType | ✅ Implemented |
| HD-1 program → HD-1 bank only | Implicit via SynthesisType | ✅ Implemented |
| Cross-engine paste blocked | Via SynthesisType check | ✅ Implemented |

### Bank Type Restrictions
| Rule | C# Implementation | Python Status |
|------|-------------------|---------------|
| GM bank is read-only | `IsWritable = false` | ✅ `is_read_only = True` |
| Internal banks may be read-only | Depends on file | ✅ Implemented |
| User banks are writable | `IsWritable = true` | ✅ Implemented |

### Range Validation
| Parameter | C# Validation | Python Status |
|-----------|---------------|---------------|
| Volume | 0-127 | ✅ Validated in SetListSlot.volume setter |
| Transpose | -24 to +24 | ✅ Validated in SetListSlot.transpose setter |
| Program index | 0-127 | ✅ Validated in SetListSlot.patch_index_value setter (& 0x7F) |
| Bank index | Valid bank IDs | ✅ Validated in SetListSlot.patch_bank_id setter (& 0x1F) |

---

## 6. UI WORKFLOWS

### Empty Bank Handling
| Scenario | C# Behavior | Python Status |
|----------|-------------|---------------|
| Show empty banks in list | Shows all banks, marks empty | ✅ Implemented |
| Paste into empty bank | Creates bank, then pastes | ✅ Implemented |
| Display engine type | Shows in bank description | ✅ Implemented |

### Copy/Paste Workflow
| Scenario | C# Behavior | Python Status |
|----------|-------------|---------------|
| Copy program | Copies raw data + metadata | ✅ Implemented |
| Copy combi | Copies combi + referenced programs | ✅ Implemented in clipboard.copy_combi() |
| Copy setlist slot | Copies slot + referenced patch | ✅ Implemented in clipboard.copy_slot() |
| Paste with remap | Remaps program references | ✅ Implemented in clipboard._remap_programs() |

### Cut/Paste Mode
| Feature | C# Implementation | Python Status |
|---------|-------------------|---------------|
| `CutPasteSelected` flag | Tracks cut mode | ✅ Implemented - `cut_paste_selected` |
| Fix references after cut | Updates combis/setlists | ✅ Implemented - `fix_references_to_program()`, `fix_references_to_combi()` |
| Protected patches | Prevents overwriting | ✅ Implemented - `protected_patches` set |

---

## 7. STATE MANAGEMENT

### File State
| State | C# Property | Python Status |
|-------|-------------|---------------|
| Dirty/modified | `IsDirty` | ✅ `_dirty` flag |
| File name | `FileName` | ✅ `file_path` |
| Model type | `Model` | ✅ `synth_model` |
| OS version | `OsVersion` | ℹ️ Known limitation: OS 1.5/1.6 STL2 offsets not implemented (documented in KNOWN_ISSUES.md) |

### Clipboard State
| State | C# Property | Python Status |
|-------|-------------|---------------|
| Copy source file | `CopyFileName` | ✅ Implemented - `copy_file_name` |
| Paste destination | `PastePcgMemory` | ✅ Implemented - `paste_pcg_memory` |
| Selected copy type | `SelectedCopyType` | ✅ Implemented - `selected_copy_type` property |

### UI State
| State | C# Implementation | Python Status |
|-------|-------------------|---------------|
| Selected bank | Via list selection | ✅ Implemented |
| Selected empty bank | `_selected_empty_bank_id` | ✅ Implemented |
| Current program bank | `current_program_bank` | ✅ Implemented |

---

## 8. ERROR HANDLING

### File Operations
| Error | C# Handling | Python Status |
|-------|-------------|---------------|
| Invalid file format | Exception + message | ✅ Implemented |
| Corrupt chunk | Skip + warning | ✅ Parser skips unknown chunks |
| Missing chunk | Default values | ✅ Parser handles missing chunks |

### Paste Operations
| Error | C# Handling | Python Status |
|-------|-------------|---------------|
| Engine mismatch | Block + message | ✅ Implemented |
| ROM bank target | Block + message | ✅ Implemented |
| Empty bank target | Create bank first | ✅ Implemented |
| Invalid index | Block + message | ✅ Validated in setters (& 0x7F) |

### User Messages
| Scenario | C# Message | Python Status |
|----------|------------|---------------|
| ROM bank paste | "Cannot paste into ROM bank" | ✅ Implemented |
| Engine mismatch | "Cannot paste X into Y bank" | ✅ Implemented |
| Empty clipboard | "Clipboard is empty" | ✅ Implemented |

---

## PRIORITY ISSUES TO FIX

### High Priority
1. ✅ **Cut/Paste mode** - Implemented (CutPasteSelected, ProtectedPatches, FixReferences*)
2. ✅ **Clipboard source tracking** - CopyFileName now tracked
3. ✅ **Range validation** - Volume, Transpose validated in SetListSlot setters

### Medium Priority
4. ✅ **Combi copy with references** - Implemented in clipboard.py
5. ✅ **SetList slot copy with references** - Implemented in clipboard.py
6. ✅ **IsFilled property** - Implemented on Bank class
7. ℹ️ **OS 1.5/1.6 STL2 handling** - Known limitation (documented in KNOWN_ISSUES.md)

### Low Priority
8. ✅ **Song patch type** - Supported in SetListSlot.patch_type_value
9. ✅ **Drum kit/pattern clipboard** - Implemented in clipboard.py
10. ✅ **Wave sequence clipboard** - Implemented in clipboard.py

---

## NEXT STEPS

1. Review and fix high priority issues
2. Add missing validation rules
3. Complete clipboard reference tracking
4. Add cut/paste mode support
5. Verify OS version handling for all offsets


---

## DETAILED FINDINGS FROM C# CODE REVIEW

### KronosProgram.cs Key Findings

1. **Parameter Offsets** (critical for binary compatibility):
   - OscMode: offset 2558, 2 bits at position 0
   - Category: offset 2568, 4 bits at position 0
   - SubCategory: offset 2568, 3 bits at position 5
   - Favorite: offset 2558, bit 5
   - DrumTrackCommonPatternNumber: offset 1292, 2 bytes
   - DrumTrackCommonPatternBank: offset 1294, 1 byte
   - DrumTrackProgramNumber: offset 2688, 7 bits
   - DrumTrackProgramBank: offset 2689, 7 bits

2. **OscMode Values**:
   - 0 = "Single"
   - 1 = "Double"
   - 2 = "Drums"
   - 3 = "- (EXI)"
   - 4 = "- (Unused)"
   - 5 = "Double Drums"

3. **Wave Sequence Handling**:
   - Different offsets for OS 1.0/1.1, 1.5/1.6, 2.x, 3.x
   - Zone MS type at offset 2774 + osc*(3240-2774) + zone*(2796-2774)

4. **PBK2 Chunk** (OS 1.5/1.6 specific):
   - 66 parameters per program
   - Used for additional program data
   - `SizeBetweenPrg2AndPbk2 = 8`

### KronosSetListSlot.cs Key Findings

1. **Slot Structure** (32 bytes per slot):
   - Name: offset 0, 24 bytes
   - Color: offset 24, bits 5-2 (OS 3.x only)
   - TextSize MSB: offset 29, bit 4
   - TextSize LSB: offset 24, bits 7-6
   - Bank (default): offset 25
   - Patch (default): offset 26
   - Volume: offset 28
   - Transpose MSB: offset 25, bits 7-5
   - Transpose LSB: offset 29, bits 7-5
   - Description: offset 30, 512 bytes

2. **OS Version Differences**:
   - OS 1.5/1.6 uses STL2 chunk for bank/patch (different offsets)
   - OS 3.x adds Color parameter
   - `SizeBetweenStl2AndSbk2 = 8`

3. **Patch Type**:
   - 0 = Program
   - 1 = Combi
   - 2 = Song (not fully supported)

4. **User Extended Banks** (U-AA to U-GG):
   - OS 1.0/1.1: Uses U-G (bank 23) with index 0
   - OS 1.5/1.6: Uses U-G in default, actual bank in STL2
   - OS 2.x/3.x: Uses actual bank ID directly

### KronosTimbre.cs Key Findings

1. **Timbre Size**: 188 bytes per timbre

2. **Program Reference Offsets**:
   - Program index: TimbresOffset + 0
   - Bank ID: TimbresOffset + 1
   - OS 1.5/1.6: Uses CBK2 chunk for extended banks

3. **CBK2 Chunk** (OS 1.5/1.6 specific):
   - 2 parameters per timbre (Bank, Program)
   - Offset calculation: `cmb2PcgOffset + combiIndex * timbresPerCombi + timbreIndex`

### KronosCombiBanks.cs Key Findings

1. **Bank Creation**:
   - Internal banks: I-A through I-G (7 banks)
   - User banks: U-A through U-G (7 banks)
   - Virtual banks: V0-A through V7-H (64 banks)
   - Total: 78 combi banks

2. **CBK2 Chunk**:
   - `ParametersInCbk2Chunk = 2` (Bank, Program)
   - Used for OS 1.5/1.6 extended bank support

### PcgClipBoard.cs Key Findings

1. **Clipboard Structure**:
   - Programs: List per SynthesisType (not single list!)
   - Combis: Single list
   - SetListSlots: Single list
   - DrumKits: Single list
   - DrumPatterns: Single list
   - WaveSequences: Single list

2. **Copy Operations**:
   - `CopyProgramToClipBoard`: Copies program + referenced drum kits
   - `CopyCombiToClipBoard`: Copies combi + all timbre references
   - `CopySetListSlotToClipBoard`: Copies slot + referenced program/combi

3. **Cut/Paste Mode**:
   - `CutPasteSelected` flag
   - `ProtectedPatches` collection
   - `FixReferencesToProgram`: Updates combis and setlists
   - `FixReferencesToCombi`: Updates setlists
   - `FixReferencesToDrumKit`: Updates programs
   - `FixReferencesToDrumPattern`: Updates programs

4. **Recall Functionality**:
   - Memory* properties store previous clipboard state
   - Allows undoing clipboard operations

---

## PYTHON IMPLEMENTATION GAPS

### Critical Gaps (Must Fix)

1. ✅ **Programs list per SynthesisType** - IMPLEMENTED
   - Python: `_programs_by_type` dict keyed by SynthesisType
   - Added `SynthesisType` enum to models.py

2. ✅ **Cut/Paste Mode** - IMPLEMENTED
   - `cut_paste_selected` flag
   - `protected_patches` set
   - `fix_references_to_program()` and `fix_references_to_combi()` methods

3. ✅ **OS Version Handling** - IMPLEMENTED
   - Added `OsVersion` enum to models.py
   - Updated `PcgHeader` to use `OsVersion` enum

4. ℹ️ **CBK2/PBK2/STL2 Chunks** - Known limitation (documented in KNOWN_ISSUES.md)
   - C#: Full support for OS 1.5/1.6 extended chunks
   - Python: Not implemented - most users are on OS 2.x/3.x
   - Impact: OS 1.5/1.6 files may lose data

### Medium Gaps (Should Fix)

5. **Timbre Reference Copying**
   - C#: Copies all timbre program references
   - Python: Partial implementation
   - Impact: Combi paste may not copy all programs

6. **Drum Kit/Pattern References**
   - C#: Tracks and copies drum kit/pattern references
   - Python: Not implemented
   - Impact: Programs using drum kits may not copy correctly

7. **Wave Sequence References**
   - C#: Tracks and copies wave sequence references
   - Python: Not implemented
   - Impact: Programs using wave sequences may not copy correctly

### Low Priority Gaps

8. **Virtual Banks**
   - C#: 64 virtual combi banks (V0-A to V7-H)
   - Python: Not in `get_all_combi_bank_ids()`
   - Impact: Virtual banks not shown in UI

9. **Recall Functionality**
   - C#: Memory* properties for undo
   - Python: Not implemented
   - Impact: Can't recall previous clipboard state

10. **Duplicate Detection**
    - C#: `FindProgram`, `FindDrumKit`, etc.
    - Python: Not implemented
    - Impact: May copy duplicates unnecessarily
