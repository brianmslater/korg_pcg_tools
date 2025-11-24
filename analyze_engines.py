#!/usr/bin/env python3
"""Analyze engine bytes in PCG files to improve engine detection."""

import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

# Test with a file from KEYBOARD
TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"
if not os.path.exists(TEST_FILE):
    TEST_FILE = "test_files/files/GLAM V3/GLAMV3.PCG"

print(f"\nAnalyzing engine bytes in: {TEST_FILE}\n")

pcg = read_pcg_file(TEST_FILE)

# Collect engine byte statistics
engine_bytes = Counter()
engine_examples = {}

for bank in pcg.program_banks:
    print(f"\nBank: {bank.bank_id}")
    for i, prog in enumerate(bank.patches[:20]):  # First 20 programs
        if len(prog.raw_data) > 0x58:
            engine_byte = prog.raw_data[0x58]
            engine_bytes[engine_byte] += 1
            
            # Store example for each engine byte
            if engine_byte not in engine_examples:
                engine_examples[engine_byte] = []
            if len(engine_examples[engine_byte]) < 3:
                engine_examples[engine_byte].append(prog.name)
            
            # Show current detection
            print(f"  {prog.id}: {prog.name:<30} Engine byte: 0x{engine_byte:02X} -> {prog.engine}")

print("\n" + "="*70)
print("ENGINE BYTE STATISTICS")
print("="*70)

for byte_val, count in sorted(engine_bytes.items()):
    examples = ", ".join(engine_examples[byte_val][:3])
    print(f"0x{byte_val:02X}: {count:3d} programs - Examples: {examples}")

print("\n" + "="*70)
print("SUGGESTED ENGINE MAPPING")
print("="*70)
print("""
Based on the analysis above, update the engine_map in pcg_parser.py:

engine_map = {
    0x28: "HD-1",      # HD-1 Synthesizer
    0x29: "AL-1",      # AL-1 Analog Synthesizer  
    0x0B: "CX-3",      # CX-3 Tonewheel Organ
    0x2A: "STR-1",     # STR-1 String Synthesizer
    0x2B: "EP-1",      # EP-1 Electric Piano
    0x0C: "MS-20EX",   # MS-20EX
    0x0D: "PolysixEX", # PolysixEX
    0x2C: "MOD-7",     # MOD-7 Waveshaping VPM
    # Add more mappings based on the statistics above
}
""")

print("\nLook at the examples for each byte value and determine which engine they represent.")
print("Common Kronos engines: HD-1, AL-1, CX-3, STR-1, EP-1, MS-20EX, PolysixEX, MOD-7")
print("Also: SGX-1 (piano), SGX-2 (EP), Korg Wavestation, Korg M1, etc.")
