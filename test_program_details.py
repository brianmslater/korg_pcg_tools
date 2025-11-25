#!/usr/bin/env python3
"""Test to extract detailed program information including engine."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"
# Fallback to local test file if KEYBOARD not mounted
import os
if not os.path.exists(TEST_FILE):
    TEST_FILE = "test_files/files/GLAM V3/GLAMV3.PCG"

print(f"\nAnalyzing: {TEST_FILE}\n")

pcg = read_pcg_file(TEST_FILE)

print(f"Program Banks: {len(pcg.program_banks)}")
for bank in pcg.program_banks:
    print(f"\nBank: {bank.bank_id}")
    print(f"  Patches: {len(bank.patches)}")
    
    # Show first 5 programs with raw data analysis
    for i, prog in enumerate(bank.patches[:5]):
        print(f"\n  Program {i}: {prog.id} - {prog.name}")
        print(f"    Bank: {prog.bank}")
        print(f"    Raw data length: {len(prog.raw_data)}")
        
        if len(prog.raw_data) >= 100:
            # Try to find engine information
            # In Kronos, engine type is typically at specific offsets
            # Let's examine the first 100 bytes
            print(f"    First 100 bytes (hex):")
            for j in range(0, min(100, len(prog.raw_data)), 16):
                hex_str = ' '.join(f'{b:02X}' for b in prog.raw_data[j:j+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in prog.raw_data[j:j+16])
                print(f"      {j:04X}: {hex_str:<48} {ascii_str}")
            
            # Check for engine indicators
            # Kronos engines: HD-1, AL-1, CX-3, STR-1, EP-1, etc.
            raw_str = prog.raw_data[:200].decode('ascii', errors='ignore')
            engines = ['HD-1', 'AL-1', 'CX-3', 'STR-1', 'EP-1', 'MS-20', 'PolysixEX', 'MOD-7']
            found_engines = [eng for eng in engines if eng in raw_str]
            if found_engines:
                print(f"    Possible engines found in raw data: {found_engines}")

print("\n" + "="*70)
