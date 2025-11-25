#!/usr/bin/env python3
"""
Test writing to BOTH SLS1 and SBK1 chunks to fix the hardware rejection issue.
"""

import sys
import struct
from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def find_chunk(data, chunk_id):
    """Find a chunk and return (offset, size)."""
    offset = data.find(chunk_id)
    if offset < 0:
        return None, None
    size = struct.unpack('<I', data[offset+4:offset+8])[0]
    return offset, size

def update_sls1_name(raw_data, setlist_index, new_name):
    """Update setlist name in SLS1 chunk (new format)."""
    # Find SLS1 chunk
    sls1_offset, sls1_size = find_chunk(raw_data, b'SLS1')
    if not sls1_offset:
        print("  ❌ SLS1 chunk not found")
        return raw_data
    
    print(f"  ✓ Found SLS1 at offset {sls1_offset}, size {sls1_size}")
    
    sls1_data_start = sls1_offset + 8
    sls1_end = sls1_data_start + sls1_size
    
    # Find setlist by marker pattern
    marker = b'\x1e\x02\x00\x00'
    separator = b'\x28\x0f\x01\x00'
    
    positions = []
    pos = sls1_data_start
    while pos < sls1_end:
        pos = raw_data.find(marker, pos, sls1_end)
        if pos == -1:
            break
        
        # Name is 4 bytes after marker
        name_start = pos + 4
        # Separator should be 24 bytes after name
        sep_pos = name_start + 24
        
        if sep_pos + 4 <= sls1_end and raw_data[sep_pos:sep_pos+4] == separator:
            positions.append(name_start)
            # Read current name
            current_name = raw_data[name_start:name_start+24].rstrip(b'\x00').decode('ascii', errors='ignore')
            print(f"    Found setlist {len(positions)-1} at {name_start}: '{current_name}'")
        
        pos += 1
    
    if setlist_index >= len(positions):
        print(f"  ❌ Setlist {setlist_index} not found (only {len(positions)} setlists)")
        return raw_data
    
    # Update the name
    name_pos = positions[setlist_index]
    name_bytes = new_name.encode('ascii')[:24].ljust(24, b'\x00')
    
    print(f"  ✓ Updating SLS1 setlist {setlist_index} at offset {name_pos}")
    print(f"    Old: {raw_data[name_pos:name_pos+24]}")
    print(f"    New: {name_bytes}")
    
    raw_data = bytearray(raw_data)
    raw_data[name_pos:name_pos+24] = name_bytes
    
    return bytes(raw_data)

def update_sbk1_name(raw_data, setlist_index, new_name):
    """Update setlist name in SBK1 chunk (old format)."""
    # Find SBK1 chunk
    sbk1_offset, sbk1_size = find_chunk(raw_data, b'SBK1')
    if not sbk1_offset:
        print("  ❌ SBK1 chunk not found")
        return raw_data
    
    print(f"  ✓ Found SBK1 at offset {sbk1_offset}, size {sbk1_size}")
    
    sbk1_data_start = sbk1_offset + 8
    
    # Constants from analysis
    SETLIST_SPACING = 69416
    FIRST_SETLIST_OFFSET = 69432
    
    # Calculate position
    if setlist_index == 0:
        name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET
    else:
        name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET + (setlist_index * SETLIST_SPACING)
    
    if name_pos + 24 > len(raw_data):
        print(f"  ❌ Position {name_pos} out of bounds")
        return raw_data
    
    # Read current name
    current_name = raw_data[name_pos:name_pos+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"    Current name at {name_pos}: '{current_name}'")
    
    # Update the name
    name_bytes = new_name.encode('ascii')[:24].ljust(24, b'\x00')
    
    print(f"  ✓ Updating SBK1 setlist {setlist_index} at offset {name_pos}")
    print(f"    Old: {raw_data[name_pos:name_pos+24]}")
    print(f"    New: {name_bytes}")
    
    raw_data = bytearray(raw_data)
    raw_data[name_pos:name_pos+24] = name_bytes
    
    return bytes(raw_data)

def test_dual_format_write():
    """Test writing to both SLS1 and SBK1 formats."""
    
    # Find a test file
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    print(f"Loading: {test_file}")
    print("=" * 80)
    
    # Read the file
    pcg = read_pcg_file(str(test_file))
    print(f"Loaded {len(pcg.set_lists)} setlists")
    
    # Show first setlist
    if pcg.set_lists:
        setlist = pcg.set_lists[0]
        print(f"\nFirst setlist: '{setlist.name}'")
        print(f"  ID: {setlist.id}")
        print(f"  Description: {setlist.description}")
        print(f"  Slots: {len(setlist.slots)}")
    
    # Modify the first setlist name
    new_name = "DUAL FORMAT TEST"
    print(f"\n{'=' * 80}")
    print(f"Changing first setlist name to: '{new_name}'")
    print("=" * 80)
    
    # Update in memory
    pcg.set_lists[0].name = new_name
    
    # Get raw data
    raw_data = pcg.raw_data
    
    # Update BOTH formats
    print("\n1. Updating SLS1 (new format):")
    raw_data = update_sls1_name(raw_data, 0, new_name)
    
    print("\n2. Updating SBK1 (old format):")
    raw_data = update_sbk1_name(raw_data, 0, new_name)
    
    # Update the PCG object
    pcg.raw_data = raw_data
    
    # Write the file
    output_file = Path('test_files/dual_format_test.PCG')
    print(f"\n{'=' * 80}")
    print(f"Writing to: {output_file}")
    print("=" * 80)
    
    write_pcg_file(pcg, str(output_file))
    
    print(f"\n✓ File written successfully!")
    print(f"\nNext steps:")
    print(f"1. Copy {output_file} to USB drive")
    print(f"2. Load on Kronos hardware")
    print(f"3. Check if setlist name appears as '{new_name}'")
    print(f"4. Verify file is accepted (not rejected)")
    
    # Verify by reading back
    print(f"\n{'=' * 80}")
    print("Verifying written file...")
    print("=" * 80)
    
    pcg_verify = read_pcg_file(str(output_file))
    if pcg_verify.set_lists:
        verified_name = pcg_verify.set_lists[0].name
        print(f"First setlist name: '{verified_name}'")
        if verified_name == new_name:
            print("✓ Name matches!")
        else:
            print(f"❌ Name mismatch! Expected '{new_name}', got '{verified_name}'")
    
    # Check both locations in raw data
    print(f"\nChecking raw data locations:")
    with open(output_file, 'rb') as f:
        verify_data = f.read()
    
    # Check SLS1
    sls1_offset, _ = find_chunk(verify_data, b'SLS1')
    if sls1_offset:
        marker = b'\x1e\x02\x00\x00'
        pos = verify_data.find(marker, sls1_offset + 8)
        if pos > 0:
            name_pos = pos + 4
            sls1_name = verify_data[name_pos:name_pos+24].rstrip(b'\x00').decode('ascii', errors='ignore')
            print(f"  SLS1 name: '{sls1_name}' {'✓' if sls1_name == new_name else '❌'}")
    
    # Check SBK1
    sbk1_offset, _ = find_chunk(verify_data, b'SBK1')
    if sbk1_offset:
        name_pos = sbk1_offset + 8 + 69432
        sbk1_name = verify_data[name_pos:name_pos+24].rstrip(b'\x00').decode('ascii', errors='ignore')
        print(f"  SBK1 name: '{sbk1_name}' {'✓' if sbk1_name == new_name else '❌'}")

if __name__ == '__main__':
    test_dual_format_write()
