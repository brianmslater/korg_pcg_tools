#!/usr/bin/env python3
"""
Debug what the parser is reading from SLS1.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file

def debug_parser():
    """Check what parser reads."""
    
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"File not found: {test_file}")
        return
    
    print("=" * 80)
    print("PARSER DEBUG")
    print("=" * 80)
    
    pcg = read_pcg_file(str(test_file))
    
    print(f"\nParsed {len(pcg.set_lists)} setlists")
    
    for i, setlist in enumerate(pcg.set_lists[:5]):
        print(f"\nSetlist {i}:")
        print(f"  Name: '{setlist.name}'")
        print(f"  ID: {setlist.id}")
        print(f"  Slots: {len(setlist.slots)}")
        if setlist.slots:
            print(f"  First slot: '{setlist.slots[0].name}'")
    
    # Now check raw data
    print(f"\n{'=' * 80}")
    print("RAW DATA CHECK")
    print("=" * 80)
    
    with open(test_file, 'rb') as f:
        data = f.read()
    
    # Check SLS1 at offset 3744 (from our earlier analysis)
    print(f"\nSLS1 at offset 3744:")
    name = data[3744:3744+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"  Name: '{name}'")
    
    # Check SBK1 at offset 531920
    print(f"\nSBK1 at offset 531920:")
    name = data[531920:531920+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"  Name: '{name}'")

if __name__ == '__main__':
    debug_parser()
