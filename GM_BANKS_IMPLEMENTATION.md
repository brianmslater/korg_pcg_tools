# GM and GM2 Banks Implementation

## Overview
This document describes the implementation of GM (General MIDI) and GM2 bank support in PCG Tools.

## Bank Types

### 1. GM Bank (Fully Implemented)
- **Bank ID**: `GM` (bank ID 6 in PCG file)
- **Content**: 128 General MIDI programs
- **Status**: ✅ Fully parsed and displayed
- **Examples**:
  - GM000: Acoustic Grand Piano
  - GM001: Bright Acoustic Piano
  - GM002: Electric Grand Piano
  - etc.

### 2. GM2 Banks (Read-Only Display)
These banks exist on Kronos hardware but are **not stored** in PCG files:

#### g(1) through g(9)
- **Content**: GM2 Main programs (additional GM sound variations)
- **Status**: ✅ Parsed and displayed (read-only)
- **Behavior**: Shows program names, not editable
- **Examples**:
  - g(1): Piano variations (Grand Piano KSP, Piano Strings, etc.)
  - g(2): Chromatic Percussion (Celesta, Glockenspiel, etc.)
  - g(3): Organ variations (Drawbar Organ, Rock Organ, etc.)
  - g(4): Guitar variations (Nylon Guitar, Jazz Guitar, etc.)
  - g(5): Bass variations (Acoustic Bass, Fingered Bass, etc.)
  - g(6): Strings/Orchestra (Violin, Viola, Cello, etc.)
  - g(7): Ensemble (String Ensemble, Choir Aahs, etc.)
  - g(8): Brass (Trumpet, Trombone, French Horn, etc.)
  - g(9): Reed/Pipe (Soprano Sax, Alto Sax, Oboe, etc.)

#### g(d)
- **Content**: GM2 Drum kits
- **Status**: ✅ Parsed and displayed (read-only)
- **Behavior**: Shows drum kit names, not editable
- **Examples**:
  - g(d)000: Standard Kit
  - g(d)001: Standard Kit 2
  - g(d)008: Room Kit
  - g(d)016: Power Kit
  - g(d)024: Electronic Kit
  - g(d)025: TR-808 Kit
  - g(d)032: Jazz Kit
  - g(d)040: Brush Kit
  - g(d)048: Orchestra Kit
  - g(d)056: SFX Kit
  - g(d)127: CM-64/CM-32L

## Implementation Details

The g(1)-g(9) and g(d) banks are:
1. **ROM banks** - Read-only, stored in Kronos firmware
2. **Not in PCG files** - These banks are not saved in PCG files
3. **Statically defined** - Program names are hardcoded based on GM2 specification
4. **Display only** - Can be viewed but not edited

The C# PCG Tools does not implement these banks (they are commented out in the source code).
Our implementation provides read-only display for better user experience.

## User Experience

### Bank Selector
Users see all banks in the bank selector:
```
All Banks
INT-A
INT-B
...
USER-GG
g(1)
g(2)
...
g(9)
g(d)
```

### Viewing GM2 Banks
When a user clicks on g(1)-g(9) or g(d), they see:
- A list of 128 programs with their names
- Programs are marked as read-only (cannot be edited)
- Known program names are displayed (e.g., "Grand Piano KSP", "Standard Kit")
- Unknown slots show default names (e.g., "g(1)008")
- Engine type shows as "GM2"
- Oscillator mode shows as "Single" or "Drums"

## Technical Implementation

### Bank Class
```python
@dataclass
class Bank:
    bank_id: str
    bank_type: str
    patches: List = field(default_factory=list)
    is_placeholder: bool = False  # Not used for GM2 banks
    is_read_only: bool = False  # True for GM2 banks
```

### GM2 Data Module
In `gm2_data.py`:
```python
# Define program names for each GM2 bank
GM2_G1_PROGRAMS = {
    0: "Grand Piano KSP",
    1: "Grand Piano",
    2: "Piano Strings",
    # ... etc
}

GM2_DRUM_KITS = {
    0: "Standard Kit",
    8: "Room Kit",
    16: "Power Kit",
    # ... etc
}

def get_gm2_program_name(bank_id: str, index: int) -> str:
    """Get the name of a GM2 program."""
    # Returns defined name or default name
```

### Creating GM2 Banks
In `reader.py`:
```python
def _add_placeholder_banks(self, pcg: PcgFile):
    from .gm2_data import get_gm2_program_name
    
    # g(1) through g(9): GM2 Main programs
    for i in range(1, 10):
        bank_id = f"g({i})"
        programs = []
        
        # Create 128 programs for this bank
        for index in range(128):
            prog = Program(
                bank=bank_id,
                index=index,
                name=get_gm2_program_name(bank_id, index),
                engine="GM2",
                osc_mode="Single"
            )
            programs.append(prog)
        
        bank = Bank(
            bank_id=bank_id,
            bank_type="Program",
            patches=programs,
            is_read_only=True
        )
        pcg.program_banks.append(bank)
    
    # Similar for g(d) drum kits
```

### GUI Handling
The GUI displays GM2 banks like any other bank, but:
- Programs are shown with their names
- Edit operations should check `bank.is_read_only` flag
- Copy operations are allowed (copy from GM2 banks)
- Paste operations are blocked (cannot paste to GM2 banks)

## Future Enhancements

Possible improvements for GM2 bank support:

1. **Complete program definitions**
   - Currently only first 8-11 programs per bank have names
   - Could add all 128 program names for each bank
   - Would require research or extraction from Kronos documentation

2. **Additional metadata**
   - Add category information for GM2 programs
   - Add engine type details
   - Add parameter information (if available)

3. **GUI enhancements**
   - Visual indicator for read-only banks
   - Tooltip showing "ROM bank - read only"
   - Disable edit buttons when GM2 bank is selected

## Testing

Run tests to verify implementation:
```bash
cd korg_pcg_tools
python3 test_bank_display.py
python3 test_placeholder_banks.py
```

## References

- GM (General MIDI) Level 1: 128 standard instrument sounds
- GM2 (General MIDI Level 2): Extended GM with additional variations
- Kronos supports both GM and GM2 standards
- C# PCG Tools source: `KronosProgramBanks.cs` (lines with g() banks are commented out)
