#!/usr/bin/env python3
"""Test setlist editing WITH checksum fixing."""

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

def test_with_checksum():
    """Edit setlist name with checksum fixing."""
    input_file = 'files_2_test/nw.PCG'
    output_file = 'files_2_test/soundcheck_WITH_CHECKSUM.PCG'
    
    print("="*80)
    print("SETLIST EDIT WITH CHECKSUM FIX")
    print("="*80)
    
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
    
    # Edit first setlist
    for setlist in pcg.set_lists:
        if "NIGHTWISH" in setlist.name.upper():
            old_name = setlist.name
            setlist.name = "NIGHTWISH EDITED"
            print(f"Edited: '{old_name}' -> '{setlist.name}'")
            break
    
    # Write with checksum fixing
    print("\nWriting file with checksum fix...")
    write_pcg_file(pcg, output_file)
    
    print(f"✓ Wrote {output_file}")
    
    # Verify
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    diffs = sum(1 for i in range(len(data)) if data[i] != new_data[i])
    print(f"Bytes changed: {diffs}")

if __name__ == '__main__':
    test_with_checksum()
