#!/usr/bin/env python3
"""
Decode the SBK1 structure to find color and text size metadata.

Changes we know:
- Slot 0: Burgundy/M -> Indigo/XL
- Slot 1: Olive/M -> Burgundy/L
"""

import struct

def decode_sbk1():
    original = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    modified = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    with open(original, 'rb') as f:
        data1 = f.read()
    
    with open(modified, 'rb') as f:
        data2 = f.read()
    
    # Find SBK1
    sbk1_pos = data1.find(b'SBK1')
    sbk1_size = struct.unpack('>I', data1[sbk1_pos+4:sbk1_pos+8])[0]
    
    print(f"SBK1 at: 0x{sbk1_pos:08X}")
    print(f"SBK1 size: {sbk1_size:,} bytes\n")
    
    # SBK1 data starts at +8
    sbk1_data_start = sbk1_pos + 8
    
    # Show first 16 bytes
    print("First 16 bytes of SBK1 data:")
    first_16_orig = data1[sbk1_data_start:sbk1_data_start+16]
    first_16_mod = data2[sbk1_data_start:sbk1_data_start+16]
    
    print(f"  Original: {' '.join(f'{b:02X}' for b in first_16_orig)}")
    print(f"  Modified: {' '.join(f'{b:02X}' for b in first_16_mod)}")
    print()
    
    # Parse as structure
    print("Parsing first 16 bytes:")
    print(f"  Bytes 0-3:   0x{struct.unpack('>I', first_16_orig[0:4])[0]:08X} -> 0x{struct.unpack('>I', first_16_mod[0:4])[0]:08X}")
    print(f"  Bytes 4-7:   0x{struct.unpack('>I', first_16_orig[4:8])[0]:08X}")
    print(f"  Bytes 8-11:  0x{struct.unpack('>I', first_16_orig[8:12])[0]:08X}")
    print(f"  Bytes 12-15: 0x{struct.unpack('>I', first_16_orig[12:16])[0]:08X}")
    print()
    
    # The setlist name starts at +16
    setlist_name_offset = sbk1_data_start + 16
    setlist_name = data1[setlist_name_offset:setlist_name_offset+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Setlist name at +16: '{setlist_name}'\n")
    
    # After setlist name (24 bytes), look for slot data
    # Slot name "Ghostbusters" appears at +40
    slot0_name_offset = sbk1_data_start + 40
    slot0_name = data1[slot0_name_offset:slot0_name_offset+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Slot 0 name at +40: '{slot0_name}'\n")
    
    # Show 128 bytes starting from slot 0 name
    print("128 bytes starting from Slot 0 name:")
    for i in range(0, 128, 16):
        offset = slot0_name_offset + i
        
        orig_bytes = data1[offset:offset+16]
        mod_bytes = data2[offset:offset+16]
        
        orig_hex = ' '.join(f'{b:02X}' for b in orig_bytes)
        mod_hex = ' '.join(f'{b:02X}' for b in mod_bytes)
        
        marker = " <-- DIFF" if orig_bytes != mod_bytes else ""
        
        print(f"+{i:3d}: Orig: {orig_hex}")
        print(f"      Mod:  {mod_hex}{marker}")
        
        if marker:
            for j in range(16):
                if orig_bytes[j] != mod_bytes[j]:
                    print(f"        Byte +{i+j}: {orig_bytes[j]:3d} (0x{orig_bytes[j]:02X}) -> {mod_bytes[j]:3d} (0x{mod_bytes[j]:02X})")
        print()
    
    # The differences we found:
    # +36 (from slot name): 0x8C -> 0x20 (140 -> 32)
    # +41 (from slot name): 0x00 -> 0x10 (0 -> 16)
    
    print("="*80)
    print("METADATA ANALYSIS")
    print("="*80 + "\n")
    
    print("Slot 0 (Ghostbusters):")
    print(f"  Byte +36: {data1[slot0_name_offset+36]:3d} (0x{data1[slot0_name_offset+36]:02X}) -> {data2[slot0_name_offset+36]:3d} (0x{data2[slot0_name_offset+36]:02X})")
    print(f"    Change: Burgundy/M -> Indigo/XL")
    print(f"    Could be: Color? (140 -> 32)")
    
    print(f"\n  Byte +41: {data1[slot0_name_offset+41]:3d} (0x{data1[slot0_name_offset+41]:02X}) -> {data2[slot0_name_offset+41]:3d} (0x{data2[slot0_name_offset+41]:02X})")
    print(f"    Change: M -> XL")
    print(f"    Could be: Text size? (0 -> 16)")
    
    # Now find slot 1 and check its metadata
    # Need to find where slot 1 starts
    # Look for "Never Ending Story" after Ghostbusters
    
    search_start = slot0_name_offset + 100
    never_pos = data1.find(b'Never Ending Story', search_start, search_start + 10000)
    
    if never_pos > 0:
        print(f"\n\nSlot 1 'Never Ending Story' found at: 0x{never_pos:08X}")
        rel_to_slot0 = never_pos - slot0_name_offset
        print(f"  That's {rel_to_slot0} bytes after Slot 0 name\n")
        
        # Show metadata at same relative positions
        print("Slot 1 (Never Ending Story):")
        print(f"  Byte +36: {data1[never_pos+36]:3d} (0x{data1[never_pos+36]:02X}) -> {data2[never_pos+36]:3d} (0x{data2[never_pos+36]:02X})")
        print(f"    Change: Olive/M -> Burgundy/L")
        
        print(f"\n  Byte +41: {data1[never_pos+41]:3d} (0x{data1[never_pos+41]:02X}) -> {data2[never_pos+41]:3d} (0x{data2[never_pos+41]:02X})")
        print(f"    Change: M -> L")

if __name__ == '__main__':
    decode_sbk1()
