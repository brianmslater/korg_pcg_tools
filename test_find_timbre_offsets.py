#!/usr/bin/env python3
"""Find actual timbre data offsets by examining binary data."""

import sys
sys.path.insert(0, '.')

from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

def test_find_offsets():
    """Examine binary data to find actual timbre offsets."""
    input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
    
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
    
    # Parse combis
    parser = PcgBinaryParser(data)
    parser.parse_cmb1_chunk(pcg)
    
    # Find combi I-A001
    target_combi = None
    for bank in pcg.combi_banks:
        for combi in bank.patches:
            if combi.id == "I-A001":
                target_combi = combi
                break
        if target_combi:
            break
    
    if not target_combi or not hasattr(target_combi, '_raw_offset'):
        print("Combi not found or no offset")
        return
    
    combi_offset = target_combi._raw_offset
    print(f"Combi I-A001: {target_combi.name}")
    print(f"Combi offset: 0x{combi_offset:08x}")
    print()
    
    # Show first 100 bytes of combi data
    print("First 100 bytes of combi:")
    for i in range(0, 100, 16):
        offset = combi_offset + i
        chunk = data[offset:offset+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f'{i:04x}: {hex_str}  {ascii_str}')
    
    print()
    print("="*80)
    print("TIMBRE DATA AREA (offset +1024)")
    print("="*80)
    
    # Show timbre data area
    timbre_base = combi_offset + 1024
    
    # Show first 3 timbres (each 188 bytes)
    for timbre_num in range(3):
        timbre_offset = timbre_base + (timbre_num * 188)
        print(f"\nTimbre {timbre_num + 1} at offset +{timbre_offset - combi_offset} (0x{timbre_offset:08x}):")
        
        # Show first 50 bytes
        for i in range(0, 50, 16):
            offset = timbre_offset + i
            chunk = data[offset:offset+16]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f'  +{i:02x}: {hex_str}  {ascii_str}')
        
        # Try to identify values
        print(f"\n  Byte analysis:")
        print(f"    +0: {data[timbre_offset]:3d} (0x{data[timbre_offset]:02x})")
        print(f"    +1: {data[timbre_offset+1]:3d} (0x{data[timbre_offset+1]:02x})")
        print(f"    +2: {data[timbre_offset+2]:3d} (0x{data[timbre_offset+2]:02x}) bits 4-0 = {data[timbre_offset+2] & 0x1F}")
        print(f"    +5: {data[timbre_offset+5]:3d} (0x{data[timbre_offset+5]:02x})")
        print(f"    +7: {data[timbre_offset+7]:3d} (0x{data[timbre_offset+7]:02x}) signed = {data[timbre_offset+7] if data[timbre_offset+7] < 128 else data[timbre_offset+7] - 256}")

if __name__ == '__main__':
    test_find_offsets()
