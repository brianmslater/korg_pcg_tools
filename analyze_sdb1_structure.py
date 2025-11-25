#!/usr/bin/env python3
"""Analyze SDB1 chunk structure to find setlist color data."""

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def analyze_sdb1(filename):
    """Analyze SDB1 structure."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find SDB1
    sdb1_pos = data.find(b'SDB1')
    if sdb1_pos < 0:
        print("SDB1 not found")
        return
    
    sdb1_size = int.from_bytes(data[sdb1_pos+4:sdb1_pos+8], 'little')
    print(f"SDB1 at 0x{sdb1_pos:08X}, size: {sdb1_size:,} bytes\n")
    
    # Expected colors for SC 10/4 (setlist index 4):
    # Slot 0: Navy (164/165)
    # Slot 1: Indigo (160)
    # Slots 2,3,4: Gold (152/153)
    
    print("Searching for SC 10/4 color pattern...")
    print("Expected: Navy(164/165), Indigo(160), Gold(152/153), Gold, Gold")
    print()
    
    # Search for sequences that might be the color data
    # Try to find: 164/165 followed by 160 within a reasonable distance
    sdb1_end = sdb1_pos + 8 + sdb1_size
    
    for navy in [164, 165]:
        for i in range(sdb1_pos, min(sdb1_end - 100, len(data))):
            if data[i] == navy:
                # Check next 20 bytes for indigo
                for j in range(i+1, min(i+20, len(data))):
                    if data[j] == 160:  # Indigo
                        # Check next 20 bytes for gold
                        for k in range(j+1, min(j+20, len(data))):
                            if data[k] in [152, 153]:  # Gold
                                # Check if next 2 bytes are also gold
                                if k+2 < len(data):
                                    if data[k+1] in [152, 153] and data[k+2] in [152, 153]:
                                        print(f"Found potential match at 0x{i:08X}:")
                                        print(f"  Navy at +0")
                                        print(f"  Indigo at +{j-i}")
                                        print(f"  Gold at +{k-i}, +{k-i+1}, +{k-i+2}")
                                        
                                        # Show context
                                        print(f"\n  Context (32 bytes before to 32 after):")
                                        start = max(sdb1_pos, i-32)
                                        end = min(len(data), i+64)
                                        for m in range(start, end, 16):
                                            hex_str = ' '.join(f'{data[m+n]:02X}' for n in range(min(16, end-m)))
                                            print(f"    {m:08X}: {hex_str}")
                                        print()
                                        
                                        # Only show first few matches
                                        return

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test_files/soundcheck9_25_25_combined2.PCG'
    
    analyze_sdb1(filename)
