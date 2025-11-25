#!/usr/bin/env python3
"""Test SLS1 parsing on soundcheck file with detailed output."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_soundcheck_sls1():
    """Test SLS1 parsing on soundcheck file."""
    filename = 'test_files/soundcheck9_25_25_combined2.PCG'
    
    print("="*80)
    print("SOUNDCHECK FILE - SLS1/SLD1 PARSING TEST")
    print("="*80)
    print()
    
    # Read file
    with open(filename, 'rb') as f:
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
    
    # Parse SLS1
    parser = PcgBinaryParser(data)
    parser.parse_sls1_chunk(pcg)
    
    print(f"Parsed {len(pcg.set_lists)} setlists\n")
    
    # Show custom-named setlists
    print("Custom-Named Setlists:")
    print("-" * 80)
    for setlist in pcg.set_lists:
        if not setlist.name.startswith("Set List"):
            non_empty = sum(1 for s in setlist.slots if s.name and len(s.name) >= 2)
            print(f"[{setlist.index:2d}] {setlist.name}")
            print(f"     {non_empty} non-empty slots")
            
            # Show first 5 slots
            shown = 0
            for slot in setlist.slots:
                if slot.name and len(slot.name) >= 2:
                    print(f"       [{slot.slot_index:3d}] {slot.name}")
                    shown += 1
                    if shown >= 5:
                        break
            print()
    
    # Show NIGHTWISH LEGACY setlist in detail
    print("="*80)
    print("NIGHTWISH LEGACY SETLIST (Detailed)")
    print("="*80)
    
    nightwish = None
    for sl in pcg.set_lists:
        if "NIGHTWISH" in sl.name.upper():
            nightwish = sl
            break
    
    if nightwish:
        print(f"\nSetlist: {nightwish.name}")
        print(f"Index: {nightwish.index}")
        print(f"Total slots: {len(nightwish.slots)}")
        
        non_empty = [s for s in nightwish.slots if s.name and len(s.name) >= 2]
        print(f"Non-empty slots: {len(non_empty)}")
        
        print(f"\nFirst 20 slots:")
        for i, slot in enumerate(non_empty[:20]):
            print(f"  [{slot.slot_index:3d}] {slot.name}")
    
    # Statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    
    total_slots = sum(len(sl.slots) for sl in pcg.set_lists)
    non_empty_total = sum(1 for sl in pcg.set_lists for s in sl.slots if s.name and len(s.name) >= 2)
    
    print(f"\nTotal setlists: {len(pcg.set_lists)}")
    print(f"Total slots: {total_slots}")
    print(f"Non-empty slots: {non_empty_total}")
    print(f"Empty slots: {total_slots - non_empty_total}")
    print(f"Fill rate: {non_empty_total * 100 // total_slots}%")
    
    # Custom named setlists
    custom_named = [sl for sl in pcg.set_lists if not sl.name.startswith("Set List")]
    print(f"\nCustom-named setlists: {len(custom_named)}")
    for sl in custom_named:
        print(f"  - {sl.name}")
    
    print("\n✓ Test completed successfully!")

if __name__ == '__main__':
    test_soundcheck_sls1()
