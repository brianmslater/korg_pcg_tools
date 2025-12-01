#!/usr/bin/env python3
"""Test editing all 16 timbres in a combi."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_all_timbres():
    """Edit all 16 timbres in combi I-A001."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_ALL_TIMBRES.PCG'
    
    print("="*80)
    print("ALL TIMBRES EDIT TEST")
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
    
    # Calculate timbre base offset
    # From C# KronosTimbres.cs: TimbresOffsetConstant => 4802
    # Each timbre is 188 bytes (from C# KronosTimbre.cs)
    timbre_base = combi_001._raw_offset + 4802
    
    print("Editing all 16 timbres:")
    print("  Volume: 10 (all timbres)")
    print("  MIDI Channel: 6 (Korg display) = 5 (file value)")
    print("  Transpose: Timbre N gets +N semitones")
    print()
    
    # Target values
    target_volume = 10
    target_midi_ch_display = 6  # What Korg shows
    target_midi_ch_file = 5     # What we write (0-indexed)
    
    print("Timbre | Before (Vol/Ch/Trn) | After (Vol/Ch/Trn)")
    print("-------|---------------------|-------------------")
    
    # Edit all 16 timbres
    for timbre_idx in range(16):
        timbre_offset = timbre_base + (timbre_idx * 188)
        
        # Read current values
        old_volume = data[timbre_offset + 5]
        old_midi_ch = data[timbre_offset + 2] & 0x1F
        old_transpose_byte = data[timbre_offset + 7]
        old_transpose = old_transpose_byte if old_transpose_byte < 128 else old_transpose_byte - 256
        
        # Calculate new transpose (timbre 1 = +1, timbre 2 = +2, etc.)
        new_transpose = timbre_idx + 1
        
        # Write new values
        data[timbre_offset + 5] = target_volume
        
        # MIDI channel is in bits 4-0 of byte +2, preserve other bits
        midi_ch_byte = data[timbre_offset + 2]
        midi_ch_byte = (midi_ch_byte & 0xE0) | (target_midi_ch_file & 0x1F)
        data[timbre_offset + 2] = midi_ch_byte
        
        # Transpose is signed byte
        transpose_byte = new_transpose if new_transpose >= 0 else (256 + new_transpose)
        data[timbre_offset + 7] = transpose_byte
        
        # Display
        print(f"  {timbre_idx+1:2d}   | {old_volume:3d}/{old_midi_ch+1:2d}/{old_transpose:+3d}          | {target_volume:3d}/{target_midi_ch_display:2d}/{new_transpose:+3d}")
    
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
    
    print("Verification (reading back from file):")
    print("Timbre | Vol | MIDI Ch (display) | Transpose")
    print("-------|-----|-------------------|----------")
    
    all_correct = True
    for timbre_idx in range(16):
        timbre_offset = timbre_base + (timbre_idx * 188)
        
        verify_volume = verify_data[timbre_offset + 5]
        verify_midi_ch_file = verify_data[timbre_offset + 2] & 0x1F
        verify_midi_ch_display = verify_midi_ch_file + 1
        verify_transpose_byte = verify_data[timbre_offset + 7]
        verify_transpose = verify_transpose_byte if verify_transpose_byte < 128 else verify_transpose_byte - 256
        
        expected_transpose = timbre_idx + 1
        
        status = "✓" if (verify_volume == target_volume and 
                        verify_midi_ch_display == target_midi_ch_display and 
                        verify_transpose == expected_transpose) else "✗"
        
        if status == "✗":
            all_correct = False
        
        print(f"  {timbre_idx+1:2d}   | {verify_volume:3d} | {verify_midi_ch_display:17d} | {verify_transpose:+9d}  {status}")
    
    print()
    
    if all_correct:
        print("✓ SUCCESS: All 16 timbres verified correct!")
    else:
        print("✗ FAILURE: Some values don't match!")
    
    print()
    print("="*80)
    print("READY FOR HARDWARE TEST")
    print("="*80)
    print("Load the file on Kronos and check Combi I-A001:")
    print("  All 16 timbres should have:")
    print("    - Volume: 10")
    print("    - MIDI Channel: 6")
    print("    - Transpose: Timbre 1=+1, Timbre 2=+2, ... Timbre 16=+16")

if __name__ == '__main__':
    test_all_timbres()
