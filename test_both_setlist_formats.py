#!/usr/bin/env python3
"""Test both STL1 and SLS1 setlist formats."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_both_formats(filename):
    """Test parsing both STL1 and SLS1 formats."""
    print(f"Testing setlist parsing on: {filename}\n")
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Check which formats are present
    has_stl1 = b'STL1' in data
    has_sls1 = b'SLS1' in data
    
    print(f"Format detection:")
    print(f"  STL1 (single setlist export): {has_stl1}")
    print(f"  SLS1 (internal 16 setlists): {has_sls1}")
    print()
    
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
    
    # Try STL1 first
    if has_stl1:
        print("="*80)
        print("PARSING STL1 FORMAT (Single Setlist Export)")
        print("="*80)
        parser.parse_stl1_chunk(pcg)
        
        if pcg.set_lists:
            setlist = pcg.set_lists[0]
            print(f"\nSetlist: {setlist.name}")
            print(f"Slots: {len(setlist.slots)}")
            
            # Show first 10 non-empty slots
            print(f"\nFirst 10 slots:")
            shown = 0
            for slot in setlist.slots:
                if slot.name and len(slot.name) >= 2:
                    print(f"  [{slot.slot_index:3d}] {slot.name}")
                    print(f"        Color: {slot.color_name} ({slot.color})")
                    print(f"        Text Size: {slot.text_size_name} ({slot.text_size})")
                    print(f"        Patch: {slot.patch_type} {slot.patch_bank}-{slot.patch_index:03d}")
                    print(f"        Volume: {slot.volume}")
                    shown += 1
                    if shown >= 10:
                        break
        print()
    
    # Clear and try SLS1
    pcg.set_lists = []
    
    if has_sls1:
        print("="*80)
        print("PARSING SLS1 FORMAT (Internal 16 Setlists)")
        print("="*80)
        parser.parse_sls1_chunk(pcg)
        
        print(f"\nFound {len(pcg.set_lists)} setlists")
        
        # Show first 3 setlists
        for sl_idx, setlist in enumerate(pcg.set_lists[:3]):
            print(f"\n--- Setlist {sl_idx}: {setlist.name} ---")
            print(f"Slots: {len(setlist.slots)}")
            
            # Show first 5 non-empty slots
            shown = 0
            for slot in setlist.slots:
                if slot.name and len(slot.name) >= 2:
                    print(f"  [{slot.slot_index:3d}] {slot.name}")
                    print(f"        Patch: {slot.patch_type} index={slot.patch_index}")
                    shown += 1
                    if shown >= 5:
                        break
        
        print(f"\n... and {len(pcg.set_lists) - 3} more setlists")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"STL1 format: {'✓ Parsed' if has_stl1 else '✗ Not present'}")
    if has_stl1:
        print(f"  - Has color and text size metadata")
        print(f"  - Has patch references (bank, index, type)")
        print(f"  - Single setlist export format")
    
    print(f"\nSLS1 format: {'✓ Parsed' if has_sls1 else '✗ Not present'}")
    if has_sls1:
        print(f"  - Contains all 16 internal setlists")
        print(f"  - Slot names from SLS1 chunk")
        print(f"  - Full combi data in SLD1 chunk")
        print(f"  - Color/text size not available in this format")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    test_both_formats(filename)
