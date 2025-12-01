#!/usr/bin/env python3
"""Detailed timbre editing test with clear identification."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_timbre_detailed():
    """Edit timbre with detailed output showing exactly what's being changed."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_TIMBRE_DETAILED.PCG'
    
    print("="*80)
    print("DETAILED TIMBRE EDIT TEST")
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
    
    # Parse programs and combis
    parser = PcgBinaryParser(data)
    parser.parse_prg1_chunk(pcg)
    parser.parse_cmb1_chunk(pcg)
    
    # Find a combi with active timbres
    target_combi = None
    for bank in pcg.combi_banks:
        for combi in bank.patches:
            # Look for a combi with at least one INT timbre
            active_timbres = [t for t in combi.timbres if t.status == "INT"]
            if active_timbres:
                target_combi = combi
                break
        if target_combi:
            break
    
    if not target_combi:
        print("No combi with active timbres found!")
        return
    
    print(f"TARGET COMBI: {target_combi.id} - {target_combi.name}")
    print("="*80)
    print()
    
    # Show all active timbres
    print("ACTIVE TIMBRES IN THIS COMBI:")
    print("-"*80)
    for i, timbre in enumerate(target_combi.timbres, 1):
        if timbre.status == "INT":
            # Find the program name
            prog_name = "Unknown"
            for prog_bank in pcg.program_banks:
                for prog in prog_bank.patches:
                    if prog.bank == timbre.program_bank and prog.index == timbre.program_index:
                        prog_name = prog.name
                        break
            
            print(f"Timbre {i}:")
            print(f"  Status: {timbre.status}")
            print(f"  Program: {timbre.program_bank}{timbre.program_index:03d} - {prog_name}")
            print(f"  MIDI Ch: {timbre.midi_channel}")
            print(f"  Volume: {timbre.volume}")
            print(f"  Pan: {timbre.pan}")
            print(f"  Transpose: {timbre.transpose:+d}")
            print()
    
    # Edit the first active timbre
    active_timbres = [t for t in target_combi.timbres if t.status == "INT"]
    if active_timbres:
        timbre = active_timbres[0]
        timbre_num = target_combi.timbres.index(timbre) + 1
        
        # Find program name
        prog_name = "Unknown"
        for prog_bank in pcg.program_banks:
            for prog in prog_bank.patches:
                if prog.bank == timbre.program_bank and prog.index == timbre.program_index:
                    prog_name = prog.name
                    break
        
        print("="*80)
        print(f"EDITING TIMBRE {timbre_num}")
        print("="*80)
        print(f"Program: {timbre.program_bank}{timbre.program_index:03d} - {prog_name}")
        print()
        
        # Make dramatic changes
        old_volume = timbre.volume
        old_pan = timbre.pan
        old_transpose = timbre.transpose
        old_midi_ch = timbre.midi_channel
        
        timbre.volume = 127  # Max volume
        timbre.pan = 0  # Full left
        timbre.transpose = 24  # Up 2 octaves
        timbre.midi_channel = 15  # Change MIDI channel
        
        print("CHANGES:")
        print(f"  Volume:     {old_volume:3d} → {timbre.volume:3d}")
        print(f"  Pan:        {old_pan:3d} → {timbre.pan:3d} (0=full left, 64=center, 127=full right)")
        print(f"  Transpose:  {old_transpose:+3d} → {timbre.transpose:+3d} semitones")
        print(f"  MIDI Ch:    {old_midi_ch:3d} → {timbre.midi_channel:3d}")
        print()
    
    # Write with checksum fixing
    print("Writing file with checksum fix...")
    write_pcg_file(pcg, output_file)
    
    print(f"✓ Wrote {output_file}")
    print()
    print("="*80)
    print("HARDWARE TEST INSTRUCTIONS")
    print("="*80)
    print(f"1. Load combi: {target_combi.id} - {target_combi.name}")
    print(f"2. Go to COMBI EDIT mode")
    print(f"3. Select Timbre {timbre_num}")
    print(f"4. Check these values:")
    print(f"   - Volume = 127 (max)")
    print(f"   - Pan = 0 (full left)")
    print(f"   - Transpose = +24 (2 octaves up)")
    print(f"   - MIDI Channel = 15")
    print()
    print(f"5. Play the combi - Timbre {timbre_num} should be:")
    print(f"   - Very loud")
    print(f"   - Panned hard left")
    print(f"   - Pitched 2 octaves higher")

if __name__ == '__main__':
    test_timbre_detailed()
