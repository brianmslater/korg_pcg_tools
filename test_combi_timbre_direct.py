#!/usr/bin/env python3
"""Test direct combi timbre editing with correct offsets."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_combi_timbre_direct():
    """Edit combi timbre 8 directly with correct offsets."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_TIMBRE8_EDITED.PCG'
    
    print("="*80)
    print("COMBI TIMBRE 8 DIRECT EDIT TEST")
    print("="*80)
    print()
    
    # Read file
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())
    
    # Create PCG object
    header = PcgHeader(
        magic=b'KORG',
        product_id=0,
        file_type=0,
        major_version=1,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header, raw_data=bytes(data))
    
    # Parse combis to find combi 001
    parser = PcgBinaryParser(bytes(data))
    parser.parse_cmb1_chunk(pcg)
    
    # Find combi I-A001
    combi_001 = None
    for bank in pcg.combi_banks:
        for combi in bank.patches:
            if combi.id == "I-A001":
                combi_001 = combi
                break
        if combi_001:
            break
    
    if not combi_001:
        print("ERROR: Could not find combi I-A001")
        return
    
    print(f"Found combi: {combi_001.id} - {combi_001.name}")
    print(f"Combi offset: 0x{combi_001._raw_offset:08x}")
    print()
    
    # Calculate timbre 8 offset (index 7)
    # From C# KronosTimbres.cs: TimbresOffsetConstant => 4802
    # Each timbre is 188 bytes (from C# KronosTimbre.cs)
    timbre_base = combi_001._raw_offset + 4802
    timbre_8_offset = timbre_base + (7 * 188)
    
    print(f"Timbre base offset: 0x{timbre_base:08x}")
    print(f"Timbre 8 offset: 0x{timbre_8_offset:08x}")
    print()
    
    # Read current values
    # From C# Timbre.cs:
    # - Volume: TimbresOffset + 5, bits 7-0
    # - MIDI Channel: TimbresOffset + 2, bits 4-0
    # - Transpose: TimbresOffset + 7, bits 7-0 (signed)
    
    old_volume = data[timbre_8_offset + 5]
    old_midi_ch = data[timbre_8_offset + 2] & 0x1F
    old_transpose_byte = data[timbre_8_offset + 7]
    old_transpose = old_transpose_byte if old_transpose_byte < 128 else old_transpose_byte - 256
    
    print("Timbre 8 BEFORE:")
    print(f"  Volume: {old_volume}")
    print(f"  MIDI Channel: {old_midi_ch}")
    print(f"  Transpose: {old_transpose:+d}")
    print()
    
    # Edit values
    new_volume = 127
    new_midi_ch = 15
    new_transpose = 24
    
    # Write new values
    data[timbre_8_offset + 5] = new_volume
    
    # MIDI channel is in bits 4-0 of byte +2, preserve other bits
    midi_ch_byte = data[timbre_8_offset + 2]
    midi_ch_byte = (midi_ch_byte & 0xE0) | (new_midi_ch & 0x1F)
    data[timbre_8_offset + 2] = midi_ch_byte
    
    # Transpose is signed byte
    transpose_byte = new_transpose if new_transpose >= 0 else (256 + new_transpose)
    data[timbre_8_offset + 7] = transpose_byte
    
    print("Timbre 8 AFTER:")
    print(f"  Volume: {new_volume}")
    print(f"  MIDI Channel: {new_midi_ch}")
    print(f"  Transpose: {new_transpose:+d}")
    print()
    
    # Update PCG object with modified data
    pcg.raw_data = bytes(data)
    
    # Write with checksum fixing
    print("Writing file with checksum fix...")
    write_pcg_file(pcg, output_file)
    
    print(f"✓ Wrote {output_file}")
    print()
    
    # Verify the changes
    with open(output_file, 'rb') as f:
        verify_data = f.read()
    
    verify_volume = verify_data[timbre_8_offset + 5]
    verify_midi_ch = verify_data[timbre_8_offset + 2] & 0x1F
    verify_transpose_byte = verify_data[timbre_8_offset + 7]
    verify_transpose = verify_transpose_byte if verify_transpose_byte < 128 else verify_transpose_byte - 256
    
    print("Verification (reading back from file):")
    print(f"  Volume: {verify_volume} (expected {new_volume})")
    print(f"  MIDI Channel: {verify_midi_ch} (expected {new_midi_ch})")
    print(f"  Transpose: {verify_transpose:+d} (expected {new_transpose:+d})")
    print()
    
    if verify_volume == new_volume and verify_midi_ch == new_midi_ch and verify_transpose == new_transpose:
        print("✓ SUCCESS: All values match!")
    else:
        print("✗ FAILURE: Values don't match!")
    
    print()
    print("="*80)
    print("READY FOR HARDWARE TEST")
    print("="*80)
    print("Load the file on Kronos and check Combi I-A001, Timbre 8:")
    print(f"  Expected: Volume={new_volume}, MIDI Ch={new_midi_ch}, Transpose={new_transpose:+d}")

if __name__ == '__main__':
    test_combi_timbre_direct()
