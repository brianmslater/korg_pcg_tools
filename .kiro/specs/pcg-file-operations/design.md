# Design Document: PCG File Operations

## Overview

This design document specifies the architecture and implementation details for enhancing PCG Tools with critical file operation features: cross-file copy/paste, missing bank creation, engine type validation, Save As functionality, and undo support. These features bring the Python implementation to feature parity with the original C# PCG Tools application.

## Architecture

The implementation follows a layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    GUI Layer (gui_qt.py)                │
│  - User interactions, dialogs, menu actions             │
├─────────────────────────────────────────────────────────┤
│                  Operations Layer                        │
│  - clipboard.py: Copy/paste operations                  │
│  - undo.py: Undo/redo management                        │
│  - bank_creator.py: Bank creation logic                 │
├─────────────────────────────────────────────────────────┤
│                    Model Layer                           │
│  - models.py: PcgFile, Program, Combi, Bank             │
│  - pcg_parser.py: Engine type detection                 │
├─────────────────────────────────────────────────────────┤
│                    I/O Layer                             │
│  - reader.py: PCG file reading                          │
│  - writer.py: PCG file writing                          │
└─────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Cross-File Copy/Paste System

**Component: PcgMainWindow (gui_qt.py)**

The GUI maintains a class-level list of all open windows to enable cross-file operations:

```python
class PcgMainWindow(QMainWindow):
    _open_windows = []  # Class variable tracking all open windows
    
    def paste_from_other_window(self):
        """Show dialog to select source window and patches to paste."""
        pass
    
    def _paste_patches_from_source(self, source_pcg, patch_ids):
        """Perform the actual paste from source PCG."""
        pass
```

**Component: Clipboard (clipboard.py)**

Based on C# `PcgClipBoard.cs`, the clipboard separates programs by synthesis type:

```python
class Clipboard:
    def __init__(self):
        # Programs separated by synthesis type (matches C# Programs[] array)
        # Index corresponds to SynthesisType enum value
        self.programs_by_type = {}  # Dict[str, List[Program]] keyed by engine type
        self.combis = []            # List of copied Combi objects
        self.setlist_slots = []     # List of copied SetListSlot objects
        self.source_file = None     # Source file path for context
        self.copy_filename = None   # CopyFileName from C#
    
    def copy_program(self, program: Program) -> None:
        """Copy a program to clipboard with deep copy.
        
        C# stores programs in Programs[BankSynthesisType] array.
        """
        pass
    
    def copy_combi(self, combi: Combi) -> None:
        """Copy a combi including timbre references.
        
        C# also copies timbre program references via CopyTimbreOfCombiToClipboard.
        """
        pass
    
    def paste_program(self, target: Program) -> None:
        """Paste program data to target slot."""
        pass
```

### 2. Missing Bank Creation System

**Component: BankCreator (bank_creator.py)**

```python
def get_missing_banks(pcg: PcgFile, required_bank_ids: List[str]) -> List[str]:
    """Return list of bank IDs that don't exist in the PCG file."""
    pass

def insert_bank_into_pcg(pcg: PcgFile, bank_id: str) -> bool:
    """Create and insert a new user bank into the PCG file.
    
    Creates proper PBK1 chunk with:
    - Correct chunk header (4-byte type, 4-byte size)
    - Bank ID encoding
    - 128 empty program slots (KRONOS_PROGRAM_SIZE bytes each)
    """
    pass

def create_pbk1_chunk(bank_id: str) -> bytes:
    """Create a complete PBK1 chunk for a user bank."""
    pass
```

### 3. Engine Type Validation System

**Component: Engine Validator (gui_qt.py)**

```python
def _validate_engine_compatibility(self, source_programs, target_program) -> Optional[str]:
    """Validate engine type compatibility for paste operation.
    
    Returns error message if incompatible, None if OK.
    HD-1 and EXi programs cannot be mixed in the same bank.
    """
    pass

def _get_bank_engine_type(self, bank) -> Optional[str]:
    """Determine the engine type of a bank ('HD-1', 'EXi', or None)."""
    pass

def _classify_engine(self, engine_name: str) -> Optional[str]:
    """Classify an engine name as 'HD-1' or 'EXi'."""
    pass
```

**Component: Engine Detection (pcg_parser.py)**

```python
def detect_program_engine(program_data: bytes) -> str:
    """Detect engine type from program raw data.
    
    Based on C# KronosProgram.cs:
    - OSC Mode at offset 2558, bits 0-2
    - Value 3 = EXi engine
    - Other values (0,1,2,5) = HD-1 engine
    """
    pass
```

### 4. Save As System

**Component: PcgMainWindow (gui_qt.py)**

```python
def save_as_file(self):
    """Save file with new name.
    
    1. Display file dialog
    2. Write PCG data to new path
    3. Update filepath reference
    4. Clear dirty flag
    """
    pass
```

### 5. Undo/Redo System (Python Enhancement - Not in C#)

**Note:** The original C# PCG Tools does NOT have undo/redo functionality. This is a Python-only enhancement that improves user experience but is not required for C# feature parity.

**Component: UndoManager (undo.py)**

```python
@dataclass
class Action:
    description: str
    undo_func: Callable
    redo_func: Callable
    undo_data: Any = None
    redo_data: Any = None

class UndoManager:
    def __init__(self, max_history: int = 50):
        self.undo_stack: List[Action] = []
        self.redo_stack: List[Action] = []
        self.callbacks: List[Callable] = []
    
    def add_action(self, action: Action) -> None:
        """Add action to undo stack, clear redo stack."""
        pass
    
    def undo(self) -> bool:
        """Execute undo, move action to redo stack."""
        pass
    
    def redo(self) -> bool:
        """Execute redo, move action back to undo stack."""
        pass
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        pass
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        pass
```

**Component: UndoableEdit (undo.py)**

Factory methods for creating undoable actions:

```python
class UndoableEdit:
    @staticmethod
    def create_paste_action(bank, start_index, patches, old_patches) -> Action:
        """Create undoable paste action."""
        pass
    
    @staticmethod
    def create_patch_edit(patch, old_state, new_state) -> Action:
        """Create undoable patch edit action."""
        pass
    
    @staticmethod
    def create_move_action(bank, from_index, to_index) -> Action:
        """Create undoable move action."""
        pass
```

## Data Models

### Engine Type Classification

Based on C# `ProgramBank.SynthesisType` enum and `Program.IsModeled()`:

| SynthesisType | Classification | Description |
|---------------|----------------|-------------|
| Ai, Ai2, Access, Hi, Eds, Edsi, Edsx, Hd1 | Sampled | Sample-based engines |
| AnalogModeling, Mmt, MossZ1, Radias, Exi | Modeled | Modeled/EXi engines |

The C# code uses `FirstModeledSynthesisType = SynthesisType.AnalogModeling` to determine if a bank is modeled.

For Kronos specifically:
- HD-1 (Hd1) = Sample-based engine
- EXi = All modeled engines (AL-1, CX-3, STR-1, EP-1, MS-20, PolySix, MOD-7, SGX-1, SGX-2)

### Bank ID Encoding

User banks follow the pattern:
- U-A through U-G: Standard user banks (PCG IDs 7-13)
- U-AA through U-GG: Extended user banks (PCG IDs 25-31)

### Undo Action Structure

```python
Action(
    description="Paste 3 program(s)",
    undo_func=restore_old_patches,
    redo_func=apply_new_patches,
    undo_data={'start_index': 0, 'old_patches': [...]},
    redo_data={'start_index': 0, 'new_patches': [...]}
)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Program Copy/Paste Round Trip

*For any* valid program in a source PCG file, copying it to the clipboard and pasting it to a destination slot should result in the destination containing equivalent program data (name, category, favorite, engine type, raw data).

**Validates: Requirements 1.1, 1.2**

### Property 2: Combi Copy/Paste Preserves Timbre References

*For any* valid combi with timbre references, copying and pasting should preserve all timbre program bank and index references in the destination combi.

**Validates: Requirements 1.3, 1.4**

### Property 3: Paste Sets Dirty Flag

*For any* successful paste operation (program or combi), the destination file's modified state (is_dirty) should be True after the operation.

**Validates: Requirements 1.5**

### Property 4: Bank Creation Integrity

*For any* valid user bank ID, creating a new bank should result in:
- A valid PBK1 chunk with correct header
- 128 initialized empty slots
- A PCG file that can be saved and reloaded without data loss

**Validates: Requirements 2.2, 2.3, 2.4**

### Property 5: Engine Type Detection Consistency

*For any* program with raw data, the engine type detection should consistently return either "HD-1" or "EXi" based on the OSC Mode value at offset 2558.

**Validates: Requirements 3.1**

### Property 6: Engine Mismatch Blocks Paste

*For any* source program with engine type E1 and destination bank containing programs with engine type E2 where E1 ≠ E2, the paste validation should return an error message.

**Validates: Requirements 3.2, 3.3**

### Property 7: Empty Bank Accepts Any Engine

*For any* source program and empty destination bank, the paste validation should return None (no error), regardless of the source program's engine type.

**Validates: Requirements 3.4**

### Property 8: Save As Round Trip

*For any* PCG file, performing Save As to a new path should result in:
- A new file at the specified path with identical data
- The filepath reference updated to the new path
- The dirty flag cleared (is_dirty = False)

**Validates: Requirements 4.2, 4.3, 4.4**

### Property 9: Undo Stack Behavior

*For any* sequence of N edit operations, the undo stack should contain N entries (up to max_history), and calling undo N times should restore the original state.

**Validates: Requirements 5.1, 5.2, 5.3**

### Property 10: Undo Availability

*For any* UndoManager with empty undo stack, can_undo() should return False. After adding an action, can_undo() should return True.

**Validates: Requirements 5.4**

### Property 11: Redo Cleared on New Edit

*For any* sequence of edits followed by undo operations, performing a new edit should clear the redo stack (can_redo() returns False).

**Validates: Requirements 5.5**

## Error Handling

### Cross-File Paste Errors
- No other windows open: Display informational message
- No patches selected: Display warning
- Source patches not found: Display warning

### C# Feature Notes

The C# implementation has additional features not yet implemented in Python:
- **Duplicate Detection**: C# checks for bytewise duplicates and name-based duplicates before pasting
- **Protected Patches**: C# tracks patches that shouldn't be overwritten during paste
- **Overwrite Settings**: C# has user settings for whether to overwrite filled patches
- **Auto-extend Selection**: C# can automatically extend paste to subsequent slots

These are advanced features that could be added in future iterations.

### Bank Creation Errors
- Invalid bank ID format: Return False, log error
- Bank already exists: Return False (no-op)
- File structure corruption: Raise exception

### Engine Validation Errors
- Engine mismatch: Return descriptive error message
- Unknown engine type: Allow paste (fail-open for unknown types)

### Save As Errors
- Write permission denied: Display error dialog
- Disk full: Display error dialog
- Invalid path: Display error dialog

### Undo Errors
- Undo on empty stack: Return False (no-op)
- Undo function raises exception: Re-add action to stack, re-raise

## Testing Strategy

### Unit Tests
- Test engine classification for known engine names
- Test bank ID encoding/decoding
- Test clipboard copy/paste for individual patches
- Test UndoManager stack operations

### Property-Based Tests
- Use `hypothesis` library for Python property-based testing
- Minimum 100 iterations per property test
- Generate random programs, combis, and bank IDs
- Test round-trip properties for copy/paste and save operations

### Integration Tests
- Test cross-file paste with real PCG files
- Test bank creation and file save/reload
- Test undo/redo with multiple operation types

### Test Configuration
```python
from hypothesis import given, settings
from hypothesis import strategies as st

@settings(max_examples=100)
@given(st.text(min_size=1, max_size=24))
def test_program_name_roundtrip(name):
    # Property test implementation
    pass
```
