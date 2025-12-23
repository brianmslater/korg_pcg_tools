#!/usr/bin/env python3
"""Test reading and writing a file with NO changes - pure roundtrip test."""

import sys
sys.path.insert(0, '.')

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

def test_roundtrip_unchanged():
    """Read a file and write it back with NO changes."""
    input_file = 'files_2_test/nw.PCG'
    output_file = 'files_2_test/soundcheck_UNCHANGED_ROUNDTRIP.PCG'
    
    print("="*80)
    print("UNCHANGED ROUNDTRIP TEST")
    print("="*80)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Read file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Create PCG object with raw data but DON'T parse anything
    header = PcgHeader(
        magic=b'KORG',
        product_id=0,
        file_type=0,
        major_version=1,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header, raw_data=data)
    
    # Write it back immediately with NO changes
    print("Writing file back unchanged...")
    write_pcg_file(pcg, output_file)
    
    # Verify
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    print(f"Output file size: {len(new_data)} bytes")
    
    # Compare
    if data == new_data:
        print("✓ Files are IDENTICAL - writer is working correctly")
        return True
    else:
        diffs = sum(1 for i in range(min(len(data), len(new_data))) if data[i] != new_data[i])
        print(f"✗ Files differ: {diffs} bytes changed")
        
        # Show first few differences
        print("\nFirst 10 differences:")
        count = 0
        for i in range(min(len(data), len(new_data))):
            if data[i] != new_data[i]:
                print(f"  0x{i:08x}: {data[i]:02x} -> {new_data[i]:02x}")
                count += 1
                if count >= 10:
                    break
        return False

if __name__ == '__main__':
    success = test_roundtrip_unchanged()
    sys.exit(0 if success else 1)
