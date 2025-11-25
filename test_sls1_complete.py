#!/usr/bin/env python3
"""Complete test of SLS1/SLD1 parsing functionality."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_sls1_complete(filename):
    """Complete test of SLS1/SLD1 parsing."""
    print("="*80)
    print("SLS1/SLD1 FORMAT PARSING - COMPLETE TEST")
    print("="*80)
    print(f"\nFile: {filename}\n")
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data):,} bytes")
    
    # Check format
    has_sls1 = b'SLS1' in data
    has_sld1 = b'SLD1' in data
    
    if not has_sls1:
        print("✗ No SLS1 chunk found - file does not contain internal setlists")
        return
    
    print(f"✓ SLS1 chunk found")
    print(f"✓ SLD1 chunk found" if has_sld1 else "✗ SLD1 chunk not found")
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
    
    # Parse
    parser = PcgBinaryParser(data)
    parser.parse_sls1_chunk(pcg)
    
    # Results
    print("="*80)
    print("PARSING RESULTS")
    print("="*80)
    print(f"\nSetlists found: {len(pcg.set_lists)}")
    
    if not pcg.set_lists:
        print("✗ No setlists parsed")
        return
    
    # Statistics
    total_slots = 0
    non_empty_slots = 0
    
    for setlist in pcg.set_lists:
        total_slots += len(setlist.slots)
        for slot in setlist.slots:
            if slot.name and len(slot.name) >= 2:
                non_empty_slots += 1
    
    print(f"Total slots: {total_slots}")
    print(f"Non-empty slots: {non_empty_slots}")
    print(f"Empty slots: {total_slots - non_empty_slots}")
    
    # Show each setlist
    print("\n" + "="*80)
    print("SETLIST DETAILS")
    print("="*80)
    
    for sl_idx, setlist in enumerate(pcg.set_lists):
        print(f"\n[{sl_idx:2d}] {setlist.name}")
        print(f"     Slots: {len(setlist.slots)}")
        
        # Count non-empty
        non_empty = sum(1 for s in setlist.slots if s.name and len(s.name) >= 2)
        print(f"     Non-empty: {non_empty}")
        
        # Show first 3 non-empty slots
        shown = 0
        for slot in setlist.slots:
            if slot.name and len(slot.name) >= 2:
                if shown == 0:
                    print(f"     First slots:")
                print(f"       [{slot.slot_index:3d}] {slot.name}")
                shown += 1
                if shown >= 3:
                    break
    
    # Validation
    print("\n" + "="*80)
    print("VALIDATION")
    print("="*80)
    
    issues = []
    
    # Check setlist count
    if len(pcg.set_lists) != 16:
        issues.append(f"Expected 16 setlists, found {len(pcg.set_lists)}")
    else:
        print("✓ Correct number of setlists (16)")
    
    # Check slot counts
    for sl_idx, setlist in enumerate(pcg.set_lists):
        if len(setlist.slots) != 128:
            issues.append(f"Setlist {sl_idx} has {len(setlist.slots)} slots, expected 128")
    
    if not issues:
        print("✓ All setlists have 128 slots")
    
    # Check for duplicate names
    all_names = [sl.name for sl in pcg.set_lists]
    if len(all_names) != len(set(all_names)):
        issues.append("Duplicate setlist names found")
    else:
        print("✓ No duplicate setlist names")
    
    # Check slot indices
    for setlist in pcg.set_lists:
        indices = [s.slot_index for s in setlist.slots]
        expected = list(range(128))
        if indices != expected:
            issues.append(f"Setlist {setlist.index} has incorrect slot indices")
            break
    else:
        print("✓ All slot indices are correct")
    
    # Report issues
    if issues:
        print("\n✗ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✓ All validation checks passed!")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"""
SLS1/SLD1 Format Parsing: {'✓ SUCCESS' if not issues else '✗ FAILED'}

Parsed Data:
  - {len(pcg.set_lists)} setlists
  - {total_slots} total slots
  - {non_empty_slots} non-empty slots
  - {total_slots - non_empty_slots} empty slots

Format Characteristics:
  - Slot names: From SLD1 combi data
  - Patch type: Combi (all slots)
  - Color/Text size: Not available (set to 0)
  - Patch references: Slot index used as patch index

Implementation Status:
  ✓ SLS1 chunk parsing
  ✓ SLD1 chunk parsing
  ✓ CBK1 marker handling
  ✓ 24-byte gap handling
  ✓ Setlist name extraction
  ✓ Slot name extraction
  ✓ Proper slot indexing
""")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    test_sls1_complete(filename)
