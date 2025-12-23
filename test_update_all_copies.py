#!/usr/bin/env python3
"""Test updating ALL copies of a setlist name."""

def test_update_all_copies():
    """Update all 4 copies of NIGHTWISH LEGACY."""
    input_file = 'files_2_test/nw.PCG'
    output_file = 'files_2_test/soundcheck_ALL_COPIES_UPDATED.PCG'
    
    print("="*80)
    print("UPDATE ALL COPIES TEST")
    print("="*80)
    
    # Read file
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())
    
    # Find all occurrences
    search = b'NIGHTWISH LEGACY'
    positions = []
    pos = 0
    while True:
        pos = data.find(search, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1
    
    print(f"Found {len(positions)} occurrences of 'NIGHTWISH LEGACY'")
    
    # Update ALL of them
    new_name = b'NIGHTWISH EDITED'
    for pos in positions:
        old_name = data[pos:pos+24]
        data[pos:pos+len(new_name)] = new_name
        # Pad with zeros
        for i in range(len(new_name), 24):
            data[pos+i] = 0
        print(f"  Updated at 0x{pos:08x}")
    
    # Write
    with open(output_file, 'wb') as f:
        f.write(data)
    
    print(f"\n✓ Wrote {output_file}")
    print(f"File size: {len(data)} bytes")
    
    # Verify changes
    with open(output_file, 'rb') as f:
        new_data = f.read()
    
    diffs = sum(1 for i in range(len(data)) if data[i] != new_data[i])
    print(f"Bytes changed: {diffs}")

if __name__ == '__main__':
    test_update_all_copies()
