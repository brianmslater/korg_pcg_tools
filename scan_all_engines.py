#!/usr/bin/env python3
"""Scan ALL PCG files on KEYBOARD device for unknown engines."""

import sys
import os
from collections import defaultdict
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

# Find all PCG files
pcg_files = []
if os.path.exists("/Volumes/KEYBOARD"):
    pcg_files = glob.glob("/Volumes/KEYBOARD/**/*.PCG", recursive=True)
    # Filter out ._ files
    pcg_files = [f for f in pcg_files if not os.path.basename(f).startswith("._")]

print(f"Found {len(pcg_files)} PCG files to scan\n")

unknown_engines = defaultdict(list)
total_programs = 0

for test_file in pcg_files:
    try:
        pcg = read_pcg_file(test_file)
        
        for bank in pcg.program_banks:
            for prog in bank.patches:
                total_programs += 1
                engine = getattr(prog, 'engine', '')
                # Check if engine starts with "0x" (unknown)
                if engine.startswith("0x"):
                    if len(unknown_engines[engine]) < 10:  # Keep up to 10 examples
                        file_short = os.path.basename(test_file)
                        unknown_engines[engine].append(f"{file_short} - {prog.id}: {prog.name}")
    except Exception as e:
        pass  # Skip files that can't be read

print(f"Scanned {total_programs} programs total\n")
print("="*70)
print("UNKNOWN ENGINE BYTES FOUND")
print("="*70)

if unknown_engines:
    for engine_hex, examples in sorted(unknown_engines.items()):
        byte_val = int(engine_hex[2:], 16)
        print(f"\n{engine_hex} (decimal {byte_val}):")
        for example in examples[:5]:  # Show first 5
            print(f"  {example}")
        if len(examples) > 5:
            print(f"  ... and {len(examples) - 5} more")
else:
    print("\nNo unknown engines found! All engines are properly mapped.")
