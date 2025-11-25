#!/usr/bin/env python3
"""Test SLS1/SLD1 parsing with the updated parser."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_sls1_parsing(filename):
    """Test parsing SLS1/SLD1 format."""
    print(f"Testing SLS1/SLD1 parsing on: {filename}\n")
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Create PCG file object
    header = PcgHeader(
        magic=b'KORG',
        product_id=0,
        file_type=0,
        major_version=1,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header, raw_data=data)
    
    # Parse with binary parser
    parser = PcgBinaryParser(data)
    parser.parse_sls1_chunk(pcg)
    
    # Display results
    print(f"Found {len(pcg.set_lists)} setlists\n")
    
    for sl_idx, setlist in enumerate(pcg.set_lists[:3]):  # Show first 3
        print(f"=== SETLIST {sl_idx}: {setlist.name} ===")
        print(f"Slots: {len(setlist.slots)}")
        
        # Show first 10 non-empty slots
        shown = 0
        for slot in setlist.slots:
            if slot.name and len(slot.name) >= 2:
                print(f"  [{slot.slot_index:3d}] {slot.name}")
                print(f"        Color: {slot.color_name} ({slot.color})")
                print(f"        Patch: {slot.patch_type} index={slot.patch_index}")
                if slot.description:
                    print(f"        Label: {slot.description}")
                shown += 1
                if shown >= 10:
                    break
        print()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    test_sls1_parsing(filename)
