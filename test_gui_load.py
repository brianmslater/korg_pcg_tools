#!/usr/bin/env python3
"""Test GUI loading to debug display issues."""

import sys
from pcg_tools.reader import read_pcg_file

# Test file loading
test_file = "test_files/files/GLAM V3/GLAMV3.PCG"

print(f"Loading {test_file}...")
try:
    pcg = read_pcg_file(test_file)
    print(f"✓ File loaded successfully")
    print(f"  Model: {pcg.header.model}")
    print(f"  Program banks: {len(pcg.program_banks)}")
    print(f"  Combi banks: {len(pcg.combi_banks)}")
    
    if pcg.program_banks:
        bank = pcg.program_banks[0]
        print(f"\n  First program bank: {bank.bank_id}")
        print(f"  Patches in bank: {len(bank.patches)}")
        if bank.patches:
            prog = bank.patches[0]
            print(f"  First program: {prog.name} (ID: {prog.id})")
            print(f"    Category: {prog.category}")
            print(f"    Favorite: {prog.favorite}")
    
    if pcg.combi_banks:
        bank = pcg.combi_banks[0]
        print(f"\n  First combi bank: {bank.bank_id}")
        print(f"  Patches in bank: {len(bank.patches)}")
        if bank.patches:
            combi = bank.patches[0]
            print(f"  First combi: {combi.name} (ID: {combi.id})")
    
    print("\n✓ All data structures look good!")
    
except Exception as e:
    print(f"✗ Error loading file: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
