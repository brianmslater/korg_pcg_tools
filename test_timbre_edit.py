#!/usr/bin/env python3
"""Test timbre editing within combis."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_timbre_edit():
    """Edit timbre properties with checksum fixing."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_TIMBRE_TEST.PCG'
    
    print("="*80)
    print("TIMBRE EDIT TEST")
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
    
    print(f"Parsed {len(pcg.combi_banks)} combi banks")
    
    # Edit first combi's first timbre
    if pcg.combi_banks and pcg.combi_banks[0].patches:
        combi = pcg.combi_banks[0].patches[0]
        print(f"\nCombi: {combi.name}")
        print(f"Timbres: {len(combi.timbres)}")
        
        if combi.timbres:
            timbre = combi.timbres[0]
            print(f"\nTimbre 1 (before):")
            print(f"  Status: {timbre.status}")
            print(f"  Program: {timbre.program_bank}{timbre.program_index:03d}")
            print(f"  MIDI Channel: {timbre.midi_channel}")
            print(f"  Volume: {timbre.volume}")
            print(f"  Pan: {timbre.pan}")
            print(f"  Transpose: {timbre.transpose}")
            print(f"  Detune: {timbre.detune}")
            
            # Edit timbre properties
            old_volume = timbre.volume
            old_pan = timbre.pan
            old_transpose = timbre.transpose
            
            timbre.volume = 100
            timbre.pan = 32  # Pan left
            timbre.transpose = 12  # Up one octave
            
            print(f"\nTimbre 1 (after):")
            print(f"  Volume: {old_volume} → {timbre.volume}")
            print(f"  Pan: {old_pan} → {timbre.pan}")
            print(f"  Transpose: {old_transpose} → {timbre.transpose}")
    
    # Write with checksum fixing
    print("\nWriting file with checksum fix...")
    write_pcg_file(pcg, output_file)
    
    print(f"✓ Wrote {output_file}")
    
    # Verify
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    diffs = sum(1 for i in range(len(data)) if data[i] != new_data[i])
    print(f"Bytes changed: {diffs}")
    print()
    print("="*80)
    print("READY FOR HARDWARE TEST")
    print("="*80)
    print("Expected results:")
    print("  - File loads successfully")
    print("  - Combi I-A000 timbre 1 has:")
    print("    * Volume = 100")
    print("    * Pan = 32 (left)")
    print("    * Transpose = +12 (one octave up)")

if __name__ == '__main__':
    test_timbre_edit()
