"""Create a minimal blank PCG file for Korg Kronos."""

import struct
from pathlib import Path

def create_blank_pcg(output_path: str):
    """Create a minimal blank PCG file with empty banks."""
    
    # PCG Header (16 bytes)
    header = bytearray()
    header += b'KORG'  # Magic
    header += bytes([0x68])  # Product ID (Kronos)
    header += bytes([0x00])  # File type
    header += bytes([0x02, 0x02])  # Version 2.2
    header += bytes([0x01, 0x00, 0x00, 0x00])  # Unknown
    header += bytes([0x00, 0x00, 0x00, 0x00])  # Padding
    
    # Create PRG1 container chunk
    prg1_data = bytearray()
    prg1_data += bytes([0x00] * 4)  # Gap after PRG1 header
    
    # Add PBK1 bank
    pbk1_data = create_empty_program_bank()
    prg1_data += pbk1_data
    
    # Wrap in PRG1 chunk
    prg1_chunk = b'PRG1' + struct.pack('<I', len(prg1_data)) + prg1_data
    
    # Create CMB1 container chunk
    cmb1_data = bytearray()
    cmb1_data += bytes([0x00] * 4)  # Gap after CMB1 header
    
    # Add CBK1 bank
    cbk1_data = create_empty_combi_bank()
    cmb1_data += cbk1_data
    
    # Wrap in CMB1 chunk
    cmb1_chunk = b'CMB1' + struct.pack('<I', len(cmb1_data)) + cmb1_data
    
    # Create SLS1 chunk (Set lists)
    sls1_data = create_empty_setlist()
    sls1_chunk = b'SLS1' + struct.pack('<I', len(sls1_data)) + sls1_data
    
    # Create PCG1 container
    pcg1_data = bytearray()
    pcg1_data += prg1_chunk
    pcg1_data += cmb1_chunk
    pcg1_data += sls1_chunk
    
    # Wrap in PCG1 chunk
    pcg1_chunk = b'PCG1' + struct.pack('<I', len(pcg1_data)) + pcg1_data
    
    # Combine header and PCG1
    pcg_file = header + pcg1_chunk
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(pcg_file)
    
    print(f"Created blank PCG file: {output_path}")
    print(f"File size: {len(pcg_file)} bytes")
    return pcg_file

def create_empty_program_bank():
    """Create an empty program bank (I-A with 128 init programs)."""
    bank_data = bytearray()
    
    # PBK1 sub-chunk header (matches real files)
    bank_data += bytes([0x00, 0x00, 0x00, 0x00])  # Gap/padding
    bank_data += struct.pack('<I', 128)  # Number of programs
    bank_data += struct.pack('<I', 4960)  # Program size (Kronos)
    bank_data += struct.pack('<I', 0x00000000)  # Bank ID (I-A = 0x00000000)
    
    # Create 128 init programs
    for i in range(128):
        program = create_init_program(i)
        bank_data += program
    
    # Wrap in PBK1 chunk
    pbk1_data = b'PBK1' + struct.pack('<I', len(bank_data)) + bank_data
    
    # Add padding after PBK1 (12 bytes as seen in real files)
    pbk1_data += bytes([0x00] * 12)
    
    return pbk1_data

def create_init_program(index: int):
    """Create an init program."""
    program = bytearray(4960)  # Kronos program size
    
    # Program name at offset 0 (24 bytes)
    name = f"Init Program {index:03d}".ljust(24, '\x00')
    program[0:24] = name.encode('ascii')
    
    # Category at offset 24 (2 bytes)
    program[24] = 0x00  # Main category
    program[25] = 0x00  # Sub category
    
    # Favorite flag at offset 26 (1 byte)
    program[26] = 0x00  # Not favorite
    
    # Rest is zeros (default init state)
    return bytes(program)

def create_empty_combi_bank():
    """Create an empty combi bank (I-A with 128 init combis)."""
    # CBK1 structure matches MBK1 - combis start at offset 24
    bank_data = bytearray()
    
    # CBK1 header (24 bytes) - similar to MBK1
    bank_data += bytes([0x00] * 12)  # Initial padding
    bank_data += struct.pack('<I', 128)  # Number of combis (not used by parser but good to have)
    bank_data += struct.pack('<I', 7810)  # Combi size
    bank_data += struct.pack('<I', 0x00000000)  # Bank ID (I-A)
    
    # Create 128 init combis
    for i in range(128):
        combi = create_init_combi(i)
        bank_data += combi
    
    # Wrap in CBK1 chunk
    cbk1_data = b'CBK1' + struct.pack('<I', len(bank_data)) + bank_data
    
    # Add padding after CBK1 (12 bytes)
    cbk1_data += bytes([0x00] * 12)
    
    return cbk1_data

def create_init_combi(index: int):
    """Create an init combi."""
    combi = bytearray(7810)  # Kronos combi size
    
    # Combi name at offset 0 (24 bytes) - simple approach
    name = f"Init Combi {index:03d}".ljust(24, '\x00')
    combi[0:24] = name.encode('ascii')
    
    # Category at offset 24 (2 bytes)
    combi[24] = 0x00  # Main category
    combi[25] = 0x00  # Sub category
    
    # Favorite flag at offset 26 (1 byte)
    combi[26] = 0x00  # Not favorite
    
    # Timbres (16 timbres, each ~400 bytes starting at offset 100)
    # For init, all timbres are muted/disabled
    
    # Rest is zeros (default init state)
    return bytes(combi)

def create_empty_setlist():
    """Create empty set lists."""
    setlist_data = bytearray()
    
    # Number of set lists
    setlist_data += struct.pack('<I', 0)  # No set lists
    
    return bytes(setlist_data)

if __name__ == '__main__':
    output_file = 'test_output/blank_kronos.pcg'
    Path('test_output').mkdir(exist_ok=True)
    
    pcg_data = create_blank_pcg(output_file)
    
    # Verify by reading it back
    print("\nVerifying created file...")
    from pcg_tools.reader import read_pcg_file
    try:
        pcg = read_pcg_file(output_file)
        print("SUCCESS: File is valid!")
        print(f"   Program banks: {len(pcg.program_banks)}")
        print(f"   Combi banks: {len(pcg.combi_banks)}")
        if pcg.program_banks:
            print(f"   Programs in first bank: {len(pcg.program_banks[0].patches)}")
        if pcg.combi_banks:
            print(f"   Combis in first bank: {len(pcg.combi_banks[0].patches)}")
    except Exception as e:
        print(f"ERROR: Error reading file: {e}")
