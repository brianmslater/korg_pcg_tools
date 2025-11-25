#!/usr/bin/env python3
"""Test engine display in programs."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"
if not os.path.exists(TEST_FILE):
    TEST_FILE = "test_files/files/GLAM V3/GLAMV3.PCG"

print(f"\nTesting engine display in: {TEST_FILE}\n")

pcg = read_pcg_file(TEST_FILE)

print("Checking first 10 programs:")
for bank in pcg.program_banks:
    for i, prog in enumerate(bank.patches[:10]):
        has_engine = hasattr(prog, 'engine')
        engine_value = prog.engine if has_engine else "NO ATTRIBUTE"
        print(f"{prog.id}: {prog.name:<30} has_engine={has_engine}, engine='{engine_value}'")

print("\n" + "="*70)
print("If engine is empty or 'NO ATTRIBUTE', there's a problem with parsing")
