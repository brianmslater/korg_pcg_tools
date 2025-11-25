#!/usr/bin/env python3
"""Parse SLS1/SLD1 format in detail."""

import struct

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def parse_sls1_setlists(filename):
    """Parse all setlists from SLS1/SLD1."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    if sld1_pos < 0:
        print("No SLD1 found")
        return
    
    print(f"SLD1 at 0x{sld1_pos:08X}\n")
    
    # Find all CBK1 markers (one per setlist)
    cbk1_positions = []
    search_pos = sld1_pos
    while True:
        cbk1_pos = data.find(b'CBK1', search_pos)
        if cbk1_pos < 0:
            break
        cbk1_positions.append(cbk1_pos)
        search_pos = cbk1_pos + 4
    
    print(f"Found {len(cbk1_positions)} setlists\n")
    
    SLOT_SIZE = 7810  # 0x1E82
    
    # Parse each setlist
    for sl_idx, cbk1_pos in enumerate(cbk1_positions):
        print(f"=== SETLIST {sl_idx} at 0x{cbk1_pos:08X} ===")
        
        # Setlist name is at CBK1 + 24
        setlist_name = get_string(data, cbk1_pos + 24, 24)
        print(f"Name: '{setlist_name}'")
        
        # Parse first 10 slots
        print(f"\nFirst 10 slots:")
        for slot_idx in range(10):
            slot_offset = cbk1_pos + (slot_idx * SLOT_SIZE)
            
            # Slot name at +24
            slot_name = get_string(data, slot_offset + 24, 24)
            
            if not slot_name:
                continue
            
            # Patch reference data after name
            patch_offset = slot_offset + 24 + 24  # name + 24 bytes
            
            if patch_offset + 10 < len(data):
                # Read patch reference bytes
                bank_byte = data[patch_offset]
                index_byte = data[patch_offset + 1]
                type_byte = data[patch_offset + 2]
                color_byte = data[patch_offset + 3]
                
                # Decode bank
                if bank_byte < 8:
                    bank = f"I-{chr(65 + bank_byte)}"
                elif bank_byte >= 0x20:
                    bank = f"U-{chr(65 + (bank_byte - 0x20))}"
                else:
                    bank = f"0x{bank_byte:02X}"
                
                # Decode type
                if type_byte == 0x30:
                    ptype = "Combi"
                elif type_byte == 0x20:
                    ptype = "Program"
                else:
                    ptype = f"0x{type_byte:02X}"
                
                print(f"  [{slot_idx:3d}] '{slot_name}'")
                print(f"        Patch: {ptype} {bank}-{index_byte:03d}, Color: {color_byte}")
        
        print()
        
        if sl_idx >= 2:  # Only show first 3 setlists
            print(f"... (showing first 3 setlists only)\n")
            break

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    parse_sls1_setlists(filename)
