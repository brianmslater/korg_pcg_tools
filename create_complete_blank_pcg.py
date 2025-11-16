"""Create a complete blank PCG file with all standard banks."""

import struct
from pathlib import Path

def create_complete_blank_pcg(output_path: str, include_exi: bool = False):
    """Create a complete blank PCG file with all standard Kronos banks.
    
    Args:
        output_path: Path to save the blank PCG file
        include_exi: Whether to include EXi banks (default False)
    
    Returns:
        File size in bytes
    """
    
    # PCG Header (16 bytes)
    header = bytearray()
    header += b'KORG'  # Magic
    header += bytes([0x68])  # Product ID (Kronos)
    header += bytes([0x00])  # File type
    header += bytes([0x02, 0x02])  # Version 2.2
    header += bytes([0x01, 0x00, 0x00, 0x00])  # Unknown
    header += bytes([0x00, 0x00, 0x00, 0x00])  # Padding
    
    # Create PRG1 container with all program banks
    prg1_data = bytearray()
    prg1_data += bytes([0x00] * 4)  # Gap after PRG1 header
    
    # Create 7 standard internal program banks (I-A through I-G)
    for bank_idx in range(7):
        bank_id = 0x00000000 + (bank_idx << 16)  # I-A=0x00000000, I-B=0x00010000, etc.
        bank_letter = chr(65 + bank_idx)
        pbk1_data = create_program_bank(bank_id, f"I-{bank_letter}")
        prg1_data += pbk1_data
    
    # Optionally add EXi banks
    if include_exi:
        # Add 5 EXi banks (I-AA through I-AE as example)
        for exi_idx in range(5):
            bank_id = 0x0C000200 + (exi_idx << 8)  # I-AA=0x0C000200, I-AB=0x0C010200, etc.
            bank_letter = f"A{chr(65 + exi_idx)}"
            mbk1_data = create_exi_bank(bank_id, f"I-{bank_letter}")
            prg1_data += mbk1_data
    
    # Wrap in PRG1 chunk
    prg1_chunk = b'PRG1' + struct.pack('<I', len(prg1_data)) + prg1_data
    
    # Create CMB1 container with all combi banks
    cmb1_data = bytearray()
    cmb1_data += bytes([0x00] * 4)  # Gap after CMB1 header
    
    # Create 7 standard combi banks (I-A through I-G)
    for bank_idx in range(7):
        bank_id = 0x00000000 + (bank_idx << 16)
        bank_letter = chr(65 + bank_idx)
        cbk1_data = create_combi_bank(bank_id, f"I-{bank_letter}")
        cmb1_data += cbk1_data
    
    # Wrap in CMB1 chunk
    cmb1_chunk = b'CMB1' + struct.pack('<I', len(cmb1_data)) + cmb1_data
    
    # Create SLS1 chunk (empty set lists)
    sls1_data = struct.pack('<I', 0)  # 0 set lists
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
    
    print(f"Created complete blank PCG file: {output_path}")
    print(f"File size: {len(pcg_file):,} bytes ({len(pcg_file)/1024/1024:.2f} MB)")
    print(f"Program banks: {7 + (5 if include_exi else 0)}")
    print(f"Combi banks: 7")
    print(f"Total programs: {(7 + (5 if include_exi else 0)) * 128}")
    print(f"Total combis: {7 * 128}")
    
    return len(pcg_file)

def create_program_bank(bank_id: int, bank_name: str):
    """Create a PBK1 program bank."""
    bank_data = bytearray()
    
    # PBK1 header
    bank_data += bytes([0x00, 0x00, 0x00, 0x00])  # Gap/padding
    bank_data += struct.pack('<I', 128)  # Number of programs
    bank_data += struct.pack('<I', 4960)  # Program size (Kronos)
    bank_data += struct.pack('<I', bank_id)  # Bank ID
    
    # Create 128 init programs
    for i in range(128):
        program = create_init_program(i, bank_name)
        bank_data += program
    
    # Wrap in PBK1 chunk
    pbk1_data = b'PBK1' + struct.pack('<I', len(bank_data)) + bank_data
    
    # Add padding after PBK1 (12 bytes)
    pbk1_data += bytes([0x00] * 12)
    
    return pbk1_data

def create_exi_bank(bank_id: int, bank_name: str):
    """Create an MBK1 EXi bank."""
    bank_data = bytearray()
    
    # MBK1 header (24 bytes)
    bank_data += bytes([0x00] * 12)  # Initial padding
    bank_data += struct.pack('<I', 128)  # Number of programs
    bank_data += struct.pack('<I', 4960)  # Program size
    bank_data += struct.pack('<I', bank_id)  # Bank ID
    
    # Create 128 init programs
    for i in range(128):
        program = create_init_program(i, bank_name)
        bank_data += program
    
    # Wrap in MBK1 chunk
    mbk1_data = b'MBK1' + struct.pack('<I', len(bank_data)) + bank_data
    
    # Add padding after MBK1 (12 bytes)
    mbk1_data += bytes([0x00] * 12)
    
    return mbk1_data

def create_combi_bank(bank_id: int, bank_name: str):
    """Create a CBK1 combi bank."""
    bank_data = bytearray()
    
    # CBK1 header (32 bytes total before combis)
    bank_data += bytes([0x00] * 12)  # Initial padding
    bank_data += struct.pack('<I', 128)  # Number of combis
    bank_data += struct.pack('<I', 7810)  # Combi size
    bank_data += struct.pack('<I', bank_id)  # Bank ID
    bank_data += bytes([0x00] * 8)  # Additional padding (total 32 bytes)
    
    # Create 128 init combis
    for i in range(128):
        combi = create_init_combi(i, bank_name)
        bank_data += combi
    
    # Wrap in CBK1 chunk
    cbk1_data = b'CBK1' + struct.pack('<I', len(bank_data)) + bank_data
    
    # Add padding after CBK1 (12 bytes)
    cbk1_data += bytes([0x00] * 12)
    
    return cbk1_data

def create_init_program(index: int, bank_name: str):
    """Create an init program."""
    program = bytearray(4960)  # Kronos program size
    
    # Program name at offset 0 (24 bytes)
    name = f"Init {bank_name}-{index:03d}".ljust(24, '\x00')
    program[0:24] = name.encode('ascii')
    
    # Category at offset 24 (2 bytes)
    program[24] = 0x00  # Main category
    program[25] = 0x00  # Sub category
    
    # Favorite flag at offset 26 (1 byte)
    program[26] = 0x00  # Not favorite
    
    # Rest is zeros (default init state)
    return bytes(program)

def create_init_combi(index: int, bank_name: str):
    """Create an init combi."""
    combi = bytearray(7810)  # Kronos combi size
    
    # Combi name at offset 0 (24 bytes)
    name = f"Init {bank_name}-{index:03d}".ljust(24, '\x00')
    combi[0:24] = name.encode('ascii')
    
    # Category at offset 24 (2 bytes)
    combi[24] = 0x00  # Main category
    combi[25] = 0x00  # Sub category
    
    # Favorite flag at offset 26 (1 byte)
    combi[26] = 0x00  # Not favorite
    
    # Rest is zeros (default init state)
    return bytes(combi)

if __name__ == '__main__':
    import sys
    
    Path('test_output').mkdir(exist_ok=True)
    
    # Create standard blank file (7 program banks, 7 combi banks)
    print("Creating STANDARD blank PCG file...")
    print("="*60)
    create_complete_blank_pcg('test_output/blank_kronos_standard.pcg', include_exi=False)
    
    print("\n" + "="*60)
    print("Creating FULL blank PCG file (with EXi banks)...")
    print("="*60)
    create_complete_blank_pcg('test_output/blank_kronos_full.pcg', include_exi=True)
    
    # Verify by reading them back
    print("\n" + "="*60)
    print("Verifying created files...")
    print("="*60)
    
    from pcg_tools.reader import read_pcg_file
    
    for filename in ['blank_kronos_standard.pcg', 'blank_kronos_full.pcg']:
        filepath = f'test_output/{filename}'
        try:
            pcg = read_pcg_file(filepath)
            print(f"\n{filename}:")
            print(f"  Program banks: {len(pcg.program_banks)}")
            for bank in pcg.program_banks:
                print(f"    {bank.bank_id}: {len(bank.patches)} programs")
            print(f"  Combi banks: {len(pcg.combi_banks)}")
            for bank in pcg.combi_banks:
                print(f"    {bank.bank_id}: {len(bank.patches)} combis")
        except Exception as e:
            print(f"  ERROR: {e}")
