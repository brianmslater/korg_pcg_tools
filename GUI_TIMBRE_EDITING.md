# GUI Timbre Editing - Implementation Summary

## Overview
The GUI has been updated to support viewing and editing combi timbres with all hardware-verified parameters.

## Changes Made

### 1. Enhanced Combis Tab (`gui_qt.py`)
**Before:** Only showed combi list (ID, Name, Category, Sub-Category, Favorite)

**After:** 
- Shows combi list (top half)
- Shows timbre list for selected combi (bottom half)
- Timbre table displays 10 columns:
  - # (Timbre number 1-16)
  - Program (referenced program ID)
  - Status (Off/Int/Both/Ext/Ex2)
  - MIDI Ch (displayed as 1-16)
  - Volume (0-127)
  - Transpose (-128 to +127)
  - Mute (✓ if muted)
  - Key Zone (bottom-top)
  - Vel Zone (bottom-top)
  - Detune (cents)

### 2. New Timbre Edit Dialog (`qt_edit_dialog.py`)
Created `QtEditTimbreDialog` class with editable fields for all verified parameters:

**Editable Parameters:**
- Status (dropdown: Off, Int, Both, Ext, Ex2) ✓ Verified
- MIDI Channel (1-16) ✓ Verified
- Volume (0-127) ✓ Verified
- Transpose (-128 to +127) ✓ Verified
- Mute (checkbox) ✓ Verified
- Key Zone: Bottom Key (0-127) and Top Key (0-127) ✓ Verified
- Velocity Zone: Bottom Velocity (1-127) and Top Velocity (1-127) ✓ Verified

**Read-Only Display:**
- Program (shows which program the timbre uses)

### 3. New Methods Added

#### `load_combi_timbres()`
- Loads timbres for the selected combi
- Populates the timbres table with all 16 timbres
- Displays all key parameters

#### `edit_timbre()`
- Opens the timbre edit dialog when a timbre is double-clicked
- Passes the timbre and parent combi to the dialog
- Refreshes the display after editing

### 4. Raw Data Updates
The timbre edit dialog updates the combi's raw_data directly using verified offsets:

```python
# Timbre base offset: 4802 (from C# KronosTimbres.cs)
# Each timbre: 188 bytes (from C# KronosTimbre.cs)
timbre_offset = 4802 + (timbre_index * 188)

# Parameter offsets (all hardware verified):
# +2: Status (bits 7-5) and MIDI Channel (bits 4-0)
# +5: Volume
# +7: Transpose (signed byte)
# +34: Mute (bit 7)
# +37: Top Key
# +38: Bottom Key
# +40: Top Velocity
# +41: Bottom Velocity
```

## Usage

### Viewing Timbres
1. Open a PCG file
2. Go to the "Combis" tab
3. Click on any combi in the top table
4. The bottom table will show all 16 timbres for that combi

### Editing a Timbre
1. Select a combi (top table)
2. Double-click on any timbre in the bottom table
3. Edit the parameters in the dialog
4. Click OK to save changes
5. File will be marked as dirty (needs saving)

### Saving Changes
1. Use File → Save or Ctrl+S
2. Changes are written to the PCG file with automatic checksum fixing

## Parameters Not Yet in GUI

The following parameters are parsed but not yet editable in the GUI:
- **Detune** - Displayed in table but not editable yet
- **Priority** - Not displayed or editable
- **Portamento** - Not displayed or editable
- **Osc Mode** - Not displayed or editable
- **Osc Select** - Not displayed or editable

These can be added in future updates if needed.

## Testing

All editable parameters have been hardware-verified on Kronos:
- ✓ Volume
- ✓ MIDI Channel
- ✓ Transpose
- ✓ Status
- ✓ Mute
- ✓ Key Zones (Top/Bottom Key)
- ✓ Velocity Zones (Top/Bottom Velocity)

See `HARDWARE_TESTING.md` for detailed test results.

## Technical Notes

### MIDI Channel Display
- **File storage:** 0-15 (zero-indexed)
- **GUI display:** 1-16 (human-readable)
- **Conversion:** Display = File + 1

### Transpose Storage
- Stored as signed byte (-128 to +127)
- Negative values: 256 + value (e.g., -12 = 244)

### Status Values
- 0 = Off
- 1 = Int (Internal)
- 2 = Both
- 3 = Ext (External)
- 4 = Ex2

### Key/Velocity Zones
- Values outside the zone will not trigger the timbre
- Key range: 0-127 (C-1 to G9)
- Velocity range: 1-127

## Future Enhancements

Possible additions:
1. Add editing for Detune, Priority, Portamento, Osc Mode, Osc Select
2. Add bulk timbre operations (copy/paste timbres between combis)
3. Add timbre templates/presets
4. Add visual key/velocity zone editor
5. Add program selection dialog (change which program a timbre uses)
