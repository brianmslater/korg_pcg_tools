#!/usr/bin/env python3
"""Test editing ONLY setlist names (not programs/combis) to isolate the issue."""

import sys
import shutil
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_setlist_only_edit():
    """Edit only setlist names, not touching programs or combis."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    output_file = 'test_files/soundcheck_SETLIST_ONLY_EDIT.PCG'
    
    print("="*80)
    print("SETLIST-ONLY EDIT TEST")
    print("="*80)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Read file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
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
    
    # Parse setlists
    parser = PcgBinaryParser(data)
    parser.parse_sls1_chunk(pcg)
    
    print(f"Parsed {len(pcg.set_lists)} setlists")
    print()
    
    # Find and edit a setlist
    edited_count = 0
    for setlist in pcg.set_lists:
        if "NIGHTWISH" in setlist.name.upper():
            old_name = setlist.name
            setlist.name = "NIGHTWISH EDITED"
            print(f"Edited setlist {setlist.index}:")
            print(f"  Old: '{old_name}'")
            print(f"  New: '{setlist.name}'")
            edited_count += 1
            break
    
    if edited_count == 0:
        # Edit first non-default setlist
        for setlist in pcg.set_lists:
            if not setlist.name.startswith("Set List"):
                old_name = setlist.name
                setlist.name = "EDITED SETLIST"
                print(f"Edited setlist {setlist.index}:")
                print(f"  Old: '{old_name}'")
                print(f"  New: '{setlist.name}'")
                edited_count += 1
                break
    
    if edited_count == 0:
        print("ERROR: No setlists found to edit")
        return False
    
    print()
    print("Writing edited file...")
    
    # Write file
    write_pcg_file(pcg, output_file)
    
    # Verify
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    print(f"Output file size: {len(new_data)} bytes")
    
    # Compare sizes
    if len(data) != len(new_data):
        print(f"ERROR: File size changed! {len(data)} -> {len(new_data)}")
        return False
    
    # Count differences
    diffs = sum(1 for i in range(len(data)) if data[i] != new_data[i])
    print(f"Bytes changed: {diffs} ({diffs*100//len(data)}%)")
    
    print()
    print("✓ Setlist-only edit completed successfully!")
    print()
    print("NEXT STEPS:")
    print("1. Copy this file to USB drive")
    print("2. Test on Kronos hardware")
    print("3. If this works, the issue is specific to program/combi editing")
    print("4. If this fails, the issue is in our file writing logic")
    
    return True

if __name__ == '__main__':
    success = test_setlist_only_edit()
    sys.exit(0 if success else 1)
