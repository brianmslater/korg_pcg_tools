#!/usr/bin/env python3
"""Find all unknown engine bytes and their program examples."""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

# Test with multiple files
test_files = [
    "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG",
    "/Volumes/KEYBOARD/Narf Sounds Movie TV Themes/Narf Sounds Movie TV Themes.PCG",
    "/Volumes/KEYBOARD/KORGSOUNDS/KRONOS BOOSTER PACK V3 Narfsounds/SETLISTS Open before loading!.PCG",
    "test_files/files/GLAM V3/GLAMV3.PCG",
]

unknown_engines = defaultdict(list)

for test_file in test_files:
    if not os.path.exists(test_file):
        continue
    
    print(f"\nAnalyzing: {test_file}")
    
    try:
        pcg = read_pcg_file(test_file)
        
        for bank in pcg.program_banks:
            for prog in bank.patches:
                engine = getattr(prog, 'engine', '')
                # Check if engine starts with "0x" (unknown)
                if engine.startswith("0x"):
                    if len(unknown_engines[engine]) < 5:  # Keep up to 5 examples
                        unknown_engines[engine].append(f"{prog.id}: {prog.name}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*70)
print("UNKNOWN ENGINE BYTES FOUND")
print("="*70)

if unknown_engines:
    for engine_hex, examples in sorted(unknown_engines.items()):
        print(f"\n{engine_hex}:")
        for example in examples:
            print(f"  {example}")
else:
    print("\nNo unknown engines found! All engines are properly mapped.")

print("\n" + "="*70)
print("SUGGESTED ADDITIONS TO ENGINE MAP")
print("="*70)
print("""
Based on program names, try to identify the engine:
- Piano/Grand/EP names -> SGX-1 or SGX-2
- Organ names -> CX-3
- Analog/Synth names -> AL-1 or HD-1
- String names -> STR-1
- Modular/FM names -> MOD-7
- MS-20/Polysix names -> MS-20EX or PolysixEX

Add these to the engine_map in pcg_parser.py _extract_engine method.
""")
