#!/usr/bin/env python3
"""Quick check for unknown engines in currently open file."""

import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

# Check a few key files
test_files = [
    "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG",
    "/Volumes/KEYBOARD/KORGSOUNDS/KRONOS BOOSTER PACK V3 Narfsounds/KRONOS BOOSTER PACK V3.PCG",
]

all_engines = Counter()
unknown_examples = {}

for test_file in test_files:
    if not os.path.exists(test_file):
        continue
    
    print(f"Checking: {os.path.basename(test_file)}")
    
    try:
        pcg = read_pcg_file(test_file)
        
        for bank in pcg.program_banks:
            for prog in bank.patches:
                engine = getattr(prog, 'engine', 'MISSING')
                all_engines[engine] += 1
                
                # Track unknown engines
                if engine.startswith("0x"):
                    if engine not in unknown_examples:
                        unknown_examples[engine] = []
                    if len(unknown_examples[engine]) < 3:
                        unknown_examples[engine].append(f"{prog.id}: {prog.name}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*70)
print("ENGINE DISTRIBUTION")
print("="*70)

for engine, count in sorted(all_engines.items(), key=lambda x: -x[1]):
    status = "❌ UNKNOWN" if engine.startswith("0x") else "✓"
    print(f"{status} {engine:<15} {count:4d} programs")

if unknown_examples:
    print("\n" + "="*70)
    print("UNKNOWN ENGINE EXAMPLES")
    print("="*70)
    for engine_hex, examples in sorted(unknown_examples.items()):
        print(f"\n{engine_hex}:")
        for ex in examples:
            print(f"  {ex}")
else:
    print("\n✓ All engines properly mapped!")
