#!/usr/bin/env python3
"""Test program and combi editing with checksum fixing."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_program_combi_edit():
    """Edit program and combi names with checksum fixing."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_PROG_COMBI_TEST.PCG'
    
    print("="*80)
    print("PROGRAM & COMBI EDIT TEST")
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
    
    print(f"Parsed {len(pcg.program_banks)} program banks")
    print(f"Parsed {len(pcg.combi_banks)} combi banks")
    print()
    
    # Edit first program
    if pcg.program_banks and pcg.program_banks[0].patches:
        prog = pcg.program_banks[0].patches[0]
        old_name = prog.name
        prog.name = "EDITED PROGRAM"
        print(f"Edited program I-A000:")
        print(f"  Old: '{old_name}'")
        print(f"  New: '{prog.name}'")
        print()
    
    # Edit first combi
    if pcg.combi_banks and pcg.combi_banks[0].patches:
        combi = pcg.combi_banks[0].patches[0]
        old_name = combi.name
        combi.name = "EDITED COMBI"
        print(f"Edited combi I-A000:")
        print(f"  Old: '{old_name}'")
        print(f"  New: '{combi.name}'")
        print()
    
    # Write with checksum fixing
    print("Writing file with checksum fix...")
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
    print("  - Program I-A000 shows 'EDITED PROGRAM'")
    print("  - Combi I-A000 shows 'EDITED COMBI'")

if __name__ == '__main__':
    test_program_combi_edit()
