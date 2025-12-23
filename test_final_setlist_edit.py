#!/usr/bin/env python3
"""Final test: Edit setlist with SLS1 + STL1 updates + checksum fixing."""

import sys
sys.path.insert(0, '.')

import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.pcg_parser import PcgBinaryParser
import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.writer import write_pcg_file
import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_final():
    """Edit setlist name with full updates and checksum fixing."""
    input_file = 'files_2_test/nw.PCG'
    output_file = 'files_2_test/soundcheck_FINAL_TEST.PCG'
    
    print("="*80)
    print("FINAL SETLIST EDIT TEST")
    print("="*80)
    print("Updates: SLS1 + STL1 + Checksums")
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
    
    # Parse setlists
    parser = PcgBinaryParser(data)
    parser.parse_sls1_chunk(pcg)
    
    print(f"Parsed {len(pcg.set_lists)} setlists")
    
    # Edit first setlist
    for setlist in pcg.set_lists:
        if "NIGHTWISH" in setlist.name.upper():
            old_name = setlist.name
            setlist.name = "NIGHTWISH EDITED"
            print(f"\nEdited setlist:")
            print(f"  Old: '{old_name}'")
            print(f"  New: '{setlist.name}'")
            break
    
    # Write with full updates
    print("\nWriting file...")
    print("  - Updating SLS1 names")
    print("  - Updating STL1 names")
    print("  - Fixing checksums")
    write_pcg_file(pcg, output_file)
    
    print(f"\n✓ Wrote {output_file}")
    
    # Verify
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    diffs = sum(1 for i in range(len(data)) if data[i] != new_data[i])
    print(f"Bytes changed: {diffs}")
    print()
    print("="*80)
    print("READY FOR HARDWARE TEST")
    print("="*80)
    print("Expected result: File loads AND name changes to 'NIGHTWISH EDITED'")

if __name__ == '__main__':
    test_final()
