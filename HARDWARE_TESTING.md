# Hardware Testing Guide for Kronos PCG Files

## Testing Workflow

When testing PCG files on the Kronos hardware, follow this workflow:

### 1. Generate Test File
Run the appropriate test script to generate a modified PCG file:
```bash
python3 test_combi_timbre_direct.py
```

### 2. Copy to KEYBOARD Volume
All test PCG files must be copied to the `/Volumes/KEYBOARD/` mount point when the SD card/USB drive is connected:
```bash
# First, check if KEYBOARD volume is mounted
ls /Volumes/

# If KEYBOARD is mounted, copy the file
cp test_files/soundcheck_TIMBRE8_EDITED.PCG /Volumes/KEYBOARD/

# If KEYBOARD is not mounted, insert the SD card/USB drive first
```

**Important**: The KEYBOARD volume is the SD card or USB drive that the Kronos reads from. Always copy test files here before hardware testing.

**Current Status**: Test file is ready at `test_files/soundcheck_TIMBRE8_EDITED.PCG` - copy to KEYBOARD volume when SD card is inserted.

### 3. Load on Kronos
1. On the Kronos, go to the DISK mode
2. Navigate to the file on the SD card/USB drive
3. Load the PCG file
4. Navigate to the specific patch to verify changes

### 4. Verify Changes
Check that the modifications are correctly applied:
- For combi timbre edits: Check the timbre parameters in the combi
- For setlist edits: Check the setlist names and slot names
- For program edits: Check the program parameters

## Current Test Files

### soundcheck_TIMBRE8_EDITED.PCG
**Purpose**: Test single timbre parameter editing with correct offsets

**What to verify**:
- Load the file on Kronos
- Navigate to Combi I-A001 "Stradivarius Goes POP"
- Check Timbre 8 parameters:
  - Volume: Should be 127 (was 87) ✓
  - MIDI Channel: Should be 16 (was 4) - Note: file value 15 displays as 16 ✓
  - Transpose: Should be +24 (was 0) ✓

**Test Result**: ✓ PASSED - All values verified correct on hardware!

**Test script**: `test_combi_timbre_direct.py`

---

### soundcheck_ALL_TIMBRES.PCG
**Purpose**: Test editing all 16 timbres in a combi simultaneously

**What to verify**:
- Load the file on Kronos
- Navigate to Combi I-A001 "Stradivarius Goes POP"
- Check ALL 16 timbres:
  - Volume: Should be 10 (all timbres) ✓
  - MIDI Channel: Should be 6 (all timbres) ✓
  - Transpose: Should increment - Timbre 1=+1, Timbre 2=+2, ... Timbre 16=+16 ✓

**Test Result**: ✓ PASSED - All 16 timbres verified correct on hardware!

**Test script**: `test_all_timbres.py`

---

### soundcheck_COMPREHENSIVE.PCG
**Purpose**: Test all editable timbre parameters on a single timbre

**What to verify**:
- Load the file on Kronos
- Navigate to Combi I-A001 "Stradivarius Goes POP", Timbre 1
- Check parameters:
  - Volume: 99 ✓
  - MIDI Channel: 8 ✓
  - Transpose: +5 ✓
  - Status: Int ✓
  - Mute: False ✓
  - Key Zone: C2 (36) to C7 (96) ✓
  - Velocity Zone: 10 to 120 ✓
- Test key zones by playing keys outside/inside range
- Test velocity zones by playing soft/hard

**Test Result**: ✓ PASSED - All parameters verified correct on hardware!

**Test script**: `test_comprehensive_timbre.py`

**Test script**: `test_combi_timbre_direct.py`

## Important Notes

### Timbre Offset Fix (2024-11-27)
The timbre data offset was corrected from 1024 to 4802 bytes from the combi start. This is based on the C# reference implementation:
- `KronosTimbres.cs`: `TimbresOffsetConstant => 4802`
- `KronosTimbre.cs`: `TimbresSizeConstant => 188`

### Timbre Parameter Offsets (All Hardware Verified ✓)
From the C# `Timbre.cs` and `KronosOasysTimbre.cs` implementation:

**Basic Parameters:**
- **Volume**: TimbresOffset + 5, bits 7-0 (0-127) ✓ Tested
- **MIDI Channel**: TimbresOffset + 2, bits 4-0 (0-15 in file, displayed as 1-16 on Kronos) ✓ Tested
- **Transpose**: TimbresOffset + 7, bits 7-0 (signed byte, -128 to +127) ✓ Tested
- **Status**: TimbresOffset + 2, bits 7-5 (0=Off, 1=Int, 2=Both, 3=Ext, 4=Ex2) ✓ Tested
- **Detune**: TimbresOffset + 8, 2 bytes (signed, little-endian) ✓ Parsed

**Control Parameters:**
- **Mute**: TimbresOffset + 34, bit 7 ✓ Tested
- **Priority**: TimbresOffset + 35, bit 4 ✓ Parsed
- **Portamento**: TimbresOffset + 36, bits 7-0 (signed) ✓ Parsed

**Oscillator Parameters:**
- **Osc Mode**: TimbresOffset + 35, bits 1-0 (0=Prg, 1=Poly, 2=Mono, 3=Legato) ✓ Parsed
- **Osc Select**: TimbresOffset + 35, bits 3-2 (0=Both, 1=Osc1, 2=Osc2) ✓ Parsed

**Zone Parameters:**
- **Top Key**: TimbresOffset + 37, bits 7-0 (0-127) ✓ Tested
- **Bottom Key**: TimbresOffset + 38, bits 7-0 (0-127) ✓ Tested
- **Top Velocity**: TimbresOffset + 40, bits 7-0 (1-127) ✓ Tested
- **Bottom Velocity**: TimbresOffset + 41, bits 7-0 (1-127) ✓ Tested

**Important Notes**:
- MIDI channels are stored as 0-15 in the file but displayed as 1-16 on the Kronos hardware. When you write channel 15 to the file, it will display as channel 16 on the Kronos.
- **Pan is NOT a timbre parameter** - it's stored in the program that the timbre references. To change pan, you need to edit the program itself, not the timbre.
- Key and velocity zones control which keys/velocities trigger the timbre. Values outside the zone will not sound.

### Parameters Not Yet Tested on Hardware
The following parameters are parsed but haven't been modified and tested on hardware yet:
- **Detune**: Parsed correctly, needs write/test
- **Priority**: Parsed correctly, needs write/test
- **Portamento**: Parsed correctly, needs write/test
- **Osc Mode**: Parsed correctly, needs write/test
- **Osc Select**: Parsed correctly, needs write/test
- **Program Pan**: Stored in the program data (not timbre level) - needs testing

### Checksum
All PCG file modifications automatically recalculate the checksum using the `write_pcg_file()` function. The checksum is critical for the Kronos to accept the file.

## Troubleshooting

### File Won't Load
- Check that the checksum was recalculated
- Verify the file size matches the original
- Check for corruption during copy

### Changes Don't Appear
- Verify you're looking at the correct patch (bank/index)
- Check that the offset calculations are correct
- Compare byte-level changes with hex editor

### Kronos Shows Error
- The file structure may be corrupted
- Checksum may be incorrect
- Try loading the original base file first to verify hardware is working
