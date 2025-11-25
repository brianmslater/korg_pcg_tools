#!/usr/bin/env python3
"""Analyze SLS1/SLD1 format structure to understand slot data layout."""

import struct

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def analyze_sls1_structure(filename):
    """Analyze SLS1/SLD1 structure."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"Size: {len(data)} bytes\n")
    
    # Find SLS1
    sls1_pos = data.find(b'SLS1')
    if sls1_pos < 0:
        print("No SLS1 chunk found")
        return
    
    sls1_size = struct.unpack('<I', data[sls1_pos+4:sls1_pos+8])[0]
    print(f"SLS1 at 0x{sls1_pos:08X}, size: 0x{sls1_size:08X} ({sls1_size} bytes)")
    
    # Find SLD1 within SLS1
    sld1_pos = data.find(b'SLD1', sls1_pos)
    if sld1_pos < 0:
        print("No SLD1 chunk found")
        return
    
    sld1_size = struct.unpack('<I', data[sld1_pos+4:sld1_pos+8])[0]
    print(f"SLD1 at 0x{sld1_pos:08X}, size: 0x{sld1_size:08X} ({sld1_size} bytes)")
    print(f"SLD1 data starts at 0x{sld1_pos+8:08X}\n")
    
    # Look for CBK1 markers in SLD1
    sld1_data_start = sld1_pos + 8
    sld1_data_end = sld1_data_start + sld1_size
    
    print("Looking for CBK1 markers in SLD1...")
    cbk1_positions = []
    search_pos = sld1_data_start
    while search_pos < sld1_data_end:
        cbk1_pos = data.find(b'CBK1', search_pos, sld1_data_end)
        if cbk1_pos < 0:
            break
        cbk1_positions.append(cbk1_pos)
        search_pos = cbk1_pos + 4
    
    print(f"Found {len(cbk1_positions)} CBK1 markers\n")
    
    if not cbk1_positions:
        print("No CBK1 markers found - trying different approach")
        # Try to find slot data by looking for readable names
        print("\nSearching for readable slot names...")
        for offset in range(sld1_data_start, min(sld1_data_start + 10000, len(data)), 100):
            name = get_string(data, offset, 24)
            if name and len(name) >= 5 and name.isprintable():
                print(f"  0x{offset:08X}: '{name}'")
        return
    
    # Analyze first few CBK1 entries
    print("Analyzing first 5 CBK1 entries:")
    for i, cbk1_pos in enumerate(cbk1_positions[:5]):
        print(f"\nCBK1 #{i} at 0x{cbk1_pos:08X}:")
        
        # CBK1 size
        cbk1_size = struct.unpack('<I', data[cbk1_pos+4:cbk1_pos+8])[0]
        print(f"  Size: 0x{cbk1_size:08X} ({cbk1_size} bytes)")
        
        # Try to read name at various offsets
        for name_offset in [8, 12, 16, 20, 24, 28, 32]:
            name = get_string(data, cbk1_pos + name_offset, 24)
            if name and len(name) >= 3:
                print(f"  Name at +{name_offset}: '{name}'")
        
        # Look for patch reference data
        # Typically: bank byte, index byte, type byte
        print(f"  Bytes at +32-40:")
        for j in range(32, min(40, cbk1_size)):
            byte_val = data[cbk1_pos + j]
            print(f"    +{j}: 0x{byte_val:02X} ({byte_val})")
    
    # Calculate spacing between CBK1 markers
    if len(cbk1_positions) > 1:
        print(f"\nSpacing between CBK1 markers:")
        for i in range(min(10, len(cbk1_positions) - 1)):
            spacing = cbk1_positions[i+1] - cbk1_positions[i]
            print(f"  CBK1 #{i} to #{i+1}: 0x{spacing:08X} ({spacing} bytes)")
    
    # Try to determine slot structure
    print(f"\nAttempting to parse slots...")
    SLOT_SIZE = 7810  # 0x1E82 - known Kronos slot size
    
    first_cbk1 = cbk1_positions[0]
    print(f"Starting from first CBK1 at 0x{first_cbk1:08X}")
    
    # Try different name offsets
    for name_offset in [24, 28, 32]:
        print(f"\nTrying name offset +{name_offset}:")
        for slot_idx in range(5):  # First 5 slots
            slot_pos = first_cbk1 + (slot_idx * SLOT_SIZE)
            name_pos = slot_pos + name_offset
            
            if name_pos + 24 > len(data):
                break
            
            name = get_string(data, name_pos, 24)
            if name and len(name) >= 3:
                print(f"  Slot {slot_idx} at 0x{slot_pos:08X}: '{name}'")
                
                # Try to read patch reference
                patch_offset = name_pos + 24
                if patch_offset + 8 <= len(data):
                    bank = data[patch_offset + 2]
                    index = data[patch_offset]
                    type_byte = data[patch_offset + 3]
                    print(f"    Patch: bank=0x{bank:02X}, index={index}, type=0x{type_byte:02X}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    analyze_sls1_structure(filename)
