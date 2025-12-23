#!/usr/bin/env python3
"""Comprehensive test of all editable timbre parameters."""

import sys
sys.path.insert(0, '.')

import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.pcg_parser import PcgBinaryParser
import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.writer import write_pcg_file
import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_comprehensive_timbre():
    """Edit multiple parameters on Timbre 1 to test all offsets."""
    input_file = 'files_2_test/nw.PCG'
    output_file = 'test_files/soundcheck_COMPREHENSIVE.PCG'
    
    print("="*80)
    print("COMPREHENSIVE TIMBRE PARAMETER TEST")
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
    
    # Calculate timbre 1 offset
    timbre_base = combi_001._raw_offset + 4802
    timbre_1_offset = timbre_base
    
    print(f"Timbre 1 offset: 0x{timbre_1_offset:08x}")
    print()
    
    # Read current values
    print("Timbre 1 BEFORE:")
    old_volume = data[timbre_1_offset + 5]
    old_midi_ch = data[timbre_1_offset + 2] & 0x1F
    old_transpose = data[timbre_1_offset + 7]
    old_transpose_signed = old_transpose if old_transpose < 128 else old_transpose - 256
    old_status = (data[timbre_1_offset + 2] >> 5) & 0x07
    old_mute = bool(data[timbre_1_offset + 34] & 0x80)
    old_top_key = data[timbre_1_offset + 37]
    old_bottom_key = data[timbre_1_offset + 38]
    old_top_vel = data[timbre_1_offset + 40]
    old_bottom_vel = data[timbre_1_offset + 41]
    
    print(f"  Volume: {old_volume}")
    print(f"  MIDI Channel: {old_midi_ch + 1}")
    print(f"  Transpose: {old_transpose_signed:+d}")
    print(f"  Status: {old_status} (0=Off, 1=Int)")
    print(f"  Mute: {old_mute}")
    print(f"  Key Zone: {old_bottom_key} - {old_top_key}")
    print(f"  Velocity Zone: {old_bottom_vel} - {old_top_vel}")
    print()
    
    # Set new values - make them distinctive for easy verification
    new_volume = 99
    new_midi_ch = 7  # Display as 8
    new_transpose = 5
    new_status = 1  # Int
    new_mute = False
    new_top_key = 96  # C7
    new_bottom_key = 36  # C2
    new_top_vel = 120
    new_bottom_vel = 10
    
    # Write new values
    # Volume (offset +5)
    data[timbre_1_offset + 5] = new_volume
    
    # MIDI channel and Status (offset +2)
    # Bits 7-5: Status, Bits 4-0: MIDI Channel
    byte_2 = (new_status << 5) | (new_midi_ch & 0x1F)
    data[timbre_1_offset + 2] = byte_2
    
    # Transpose (offset +7, signed)
    transpose_byte = new_transpose if new_transpose >= 0 else (256 + new_transpose)
    data[timbre_1_offset + 7] = transpose_byte
    
    # Mute (offset +34, bit 7)
    if new_mute:
        data[timbre_1_offset + 34] |= 0x80
    else:
        data[timbre_1_offset + 34] &= 0x7F
    
    # Key zones (offset +37/+38)
    data[timbre_1_offset + 37] = new_top_key
    data[timbre_1_offset + 38] = new_bottom_key
    
    # Velocity zones (offset +40/+41)
    data[timbre_1_offset + 40] = new_top_vel
    data[timbre_1_offset + 41] = new_bottom_vel
    
    print("Timbre 1 AFTER:")
    print(f"  Volume: {new_volume}")
    print(f"  MIDI Channel: {new_midi_ch + 1} (file: {new_midi_ch})")
    print(f"  Transpose: {new_transpose:+d}")
    print(f"  Status: {new_status} (Int)")
    print(f"  Mute: {new_mute}")
    print(f"  Key Zone: {new_bottom_key} (C2) - {new_top_key} (C7)")
    print(f"  Velocity Zone: {new_bottom_vel} - {new_top_vel}")
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
    
    verify_volume = verify_data[timbre_1_offset + 5]
    verify_midi_ch = verify_data[timbre_1_offset + 2] & 0x1F
    verify_transpose_byte = verify_data[timbre_1_offset + 7]
    verify_transpose = verify_transpose_byte if verify_transpose_byte < 128 else verify_transpose_byte - 256
    verify_status = (verify_data[timbre_1_offset + 2] >> 5) & 0x07
    verify_mute = bool(verify_data[timbre_1_offset + 34] & 0x80)
    verify_top_key = verify_data[timbre_1_offset + 37]
    verify_bottom_key = verify_data[timbre_1_offset + 38]
    verify_top_vel = verify_data[timbre_1_offset + 40]
    verify_bottom_vel = verify_data[timbre_1_offset + 41]
    
    print("Verification (reading back from file):")
    print(f"  Volume: {verify_volume} (expected {new_volume})")
    print(f"  MIDI Channel: {verify_midi_ch + 1} (expected {new_midi_ch + 1})")
    print(f"  Transpose: {verify_transpose:+d} (expected {new_transpose:+d})")
    print(f"  Status: {verify_status} (expected {new_status})")
    print(f"  Mute: {verify_mute} (expected {new_mute})")
    print(f"  Key Zone: {verify_bottom_key} - {verify_top_key} (expected {new_bottom_key} - {new_top_key})")
    print(f"  Velocity Zone: {verify_bottom_vel} - {verify_top_vel} (expected {new_bottom_vel} - {new_top_vel})")
    print()
    
    all_match = (
        verify_volume == new_volume and
        verify_midi_ch == new_midi_ch and
        verify_transpose == new_transpose and
        verify_status == new_status and
        verify_mute == new_mute and
        verify_top_key == new_top_key and
        verify_bottom_key == new_bottom_key and
        verify_top_vel == new_top_vel and
        verify_bottom_vel == new_bottom_vel
    )
    
    if all_match:
        print("✓ SUCCESS: All values match!")
    else:
        print("✗ FAILURE: Some values don't match!")
    
    print()
    print("="*80)
    print("READY FOR HARDWARE TEST")
    print("="*80)
    print("Load the file on Kronos and check Combi I-A001, Timbre 1:")
    print(f"  Volume: {new_volume}")
    print(f"  MIDI Channel: {new_midi_ch + 1}")
    print(f"  Transpose: {new_transpose:+d}")
    print(f"  Status: Int")
    print(f"  Mute: {new_mute}")
    print(f"  Key Zone: {new_bottom_key} (C2) to {new_top_key} (C7)")
    print(f"  Velocity Zone: {new_bottom_vel} to {new_top_vel}")
    print()
    print("Test by playing different keys and velocities:")
    print("  - Keys below C2 (36) should NOT trigger this timbre")
    print("  - Keys C2-C7 (36-96) SHOULD trigger this timbre")
    print("  - Keys above C7 (96) should NOT trigger this timbre")
    print("  - Velocities below 10 should NOT trigger this timbre")
    print("  - Velocities 10-120 SHOULD trigger this timbre")
    print("  - Velocities above 120 should NOT trigger this timbre")

if __name__ == '__main__':
    test_comprehensive_timbre()
