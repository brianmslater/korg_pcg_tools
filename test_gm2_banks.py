#!/usr/bin/env python3
"""Test script to parse and display GM2 banks g(1-9) and g(d).

These banks are ROM banks on the Kronos hardware and are not stored in PCG files.
This script tests the GM2 bank parsing functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.gm2_data import is_gm2_bank


def test_gm2_banks_from_file(pcg_path: str):
    """Test GM2 banks loaded from a PCG file.
    
    Args:
        pcg_path: Path to PCG file
    """
    print("=" * 80)
    print(f"Testing GM2 Banks from: {pcg_path}")
    print("=" * 80)
    print()
    
    pcg = read_pcg_file(pcg_path)
    
    # Find GM2 banks
    gm2_banks = [bank for bank in pcg.program_banks if is_gm2_bank(bank.bank_id)]
    
    print(f"Found {len(gm2_banks)} GM2 banks")
    print()
    
    for bank in gm2_banks:
        print(f"Bank: {bank.bank_id}")
        print(f"Type: {bank.bank_type}")
        print(f"Placeholder: {bank.is_placeholder}")
        print(f"Read-Only: {bank.is_read_only}")
        print(f"Programs: {len(bank.patches)}")
        
        if bank.patches:
            print("\nFirst 10 programs:")
            for prog in bank.patches[:10]:
                print(f"  {prog.id}: {prog.name} (Engine: {prog.engine}, Mode: {prog.osc_mode})")
            
            # Show some specific interesting programs
            if bank.bank_id == "g(d)":
                print("\nKnown drum kits:")
                interesting = [0, 1, 8, 16, 24, 25, 32, 40, 48, 56, 127]
                for idx in interesting:
                    if idx < len(bank.patches):
                        prog = bank.patches[idx]
                        if not prog.name.startswith("g(d)"):  # Only show named kits
                            print(f"  {prog.id}: {prog.name}")
            
            if len(bank.patches) > 10:
                print(f"\n  ... and {len(bank.patches) - 10} more")
        
        print()
        print("-" * 80)
        print()


def test_gm2_data_module():
    """Test the GM2 data module directly."""
    from pcg_tools.gm2_data import get_gm2_program_name, GM2_BANK_PROGRAMS
    
    print("=" * 80)
    print("GM2 Data Module Test")
    print("=" * 80)
    print()
    
    for bank_id in ["g(1)", "g(2)", "g(3)", "g(4)", "g(5)", 
                    "g(6)", "g(7)", "g(8)", "g(9)", "g(d)"]:
        print(f"\nBank {bank_id}:")
        if bank_id in GM2_BANK_PROGRAMS:
            programs = GM2_BANK_PROGRAMS[bank_id]
            print(f"  Defined programs: {len(programs)}")
            for idx in sorted(programs.keys())[:5]:
                print(f"    {idx:03d}: {programs[idx]}")
        else:
            print("  No programs defined")
    
    print()


if __name__ == "__main__":
    # Test the data module
    test_gm2_data_module()
    
    # Test with a PCG file if provided
    if len(sys.argv) > 1:
        test_gm2_banks_from_file(sys.argv[1])
    else:
        print("\nTo test with a PCG file, run:")
        print("  python3 test_gm2_banks.py <path_to_pcg_file>")
        print()
