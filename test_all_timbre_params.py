#!/usr/bin/env python3
"""Test parsing all timbre parameters."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_all_timbre_params():
    """Display all parsed timbre parameters."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    
    print("="*80)
    print("ALL TIMBRE PARAMETERS PARSING TEST")
    print("="*80)
    print()
    
    # Read file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Create PCG object
    header = PcgHeader(
        magic=b'KORG',
        product_id=0,
        file_type=0,
        major_version=1,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header, raw_data=data)
    
    # Parse combis
    parser = PcgBinaryParser(data)
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
    
    print(f"Combi: {combi_001.id} - {combi_001.name}")
    print(f"Number of timbres: {len(combi_001.timbres)}")
    print()
    
    # Display all parameters for each timbre
    for i, timbre in enumerate(combi_001.timbres, 1):
        print(f"Timbre {i}:")
        print(f"  Program: {timbre.program_id}")
        print(f"  Status: {timbre.status}")
        print(f"  MIDI Channel: {timbre.midi_channel + 1} (file: {timbre.midi_channel})")
        print(f"  Volume: {timbre.volume}")
        print(f"  Transpose: {timbre.transpose:+d}")
        print(f"  Detune: {timbre.detune}")
        print(f"  Mute: {timbre.mute}")
        print(f"  Priority: {timbre.priority}")
        print(f"  Osc Mode: {timbre.osc_mode}")
        print(f"  Osc Select: {timbre.osc_select}")
        print(f"  Portamento: {timbre.portamento}")
        print(f"  Key Zone: {timbre.bottom_key} - {timbre.top_key}")
        print(f"  Velocity Zone: {timbre.bottom_velocity} - {timbre.top_velocity}")
        print()
    
    print("="*80)
    print("PARAMETER SUMMARY")
    print("="*80)
    print()
    print("Parameters now parsed from C# code:")
    print("  ✓ Program Bank/Index")
    print("  ✓ Status (Off/Int/Both/Ext/Ex2)")
    print("  ✓ MIDI Channel")
    print("  ✓ Volume")
    print("  ✓ Transpose")
    print("  ✓ Detune")
    print("  ✓ Mute")
    print("  ✓ Priority")
    print("  ✓ Osc Mode (Prg/Poly/Mono/Legato)")
    print("  ✓ Osc Select (Both/Osc1/Osc2)")
    print("  ✓ Portamento")
    print("  ✓ Key Zones (Bottom/Top Key)")
    print("  ✓ Velocity Zones (Bottom/Top Velocity)")
    print()
    print("Note: Pan is a program parameter, not a timbre parameter")

if __name__ == '__main__':
    test_all_timbre_params()
