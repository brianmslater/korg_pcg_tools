#!/usr/bin/env python3
"""Test that GM and GM2 banks are marked as read-only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file


def test_readonly_banks(pcg_path: str):
    """Test that ROM banks are marked as read-only.
    
    Args:
        pcg_path: Path to PCG file
    """
    print("=" * 80)
    print(f"Testing Read-Only Banks: {pcg_path}")
    print("=" * 80)
    print()
    
    pcg = read_pcg_file(pcg_path)
    
    # Check all program banks
    print("Program Banks:")
    print("-" * 80)
    
    for bank in pcg.program_banks:
        rom_indicator = " [ROM]" if bank.is_read_only else ""
        print(f"  {bank.bank_id:8s} - {len(bank.patches):3d} programs{rom_indicator}")
    
    print()
    
    # Find ROM banks
    rom_banks = [bank for bank in pcg.program_banks if bank.is_read_only]
    
    print(f"Found {len(rom_banks)} ROM (read-only) banks:")
    for bank in rom_banks:
        print(f"  - {bank.bank_id}: {len(bank.patches)} programs")
    
    print()
    
    # Verify expected ROM banks
    # Note: GM bank is only present if it was in the original PCG file
    # GM2 banks (g(1)-g(9), g(d)) are always added by the reader
    expected_rom = ["GM", "g(1)", "g(2)", "g(3)", "g(4)", "g(5)", 
                    "g(6)", "g(7)", "g(8)", "g(9)", "g(d)"]
    
    rom_bank_ids = [bank.bank_id for bank in rom_banks]
    
    print("Expected ROM banks:")
    for bank_id in expected_rom:
        if bank_id in rom_bank_ids:
            print(f"  ✓ {bank_id}")
        elif bank_id == "GM":
            print(f"  - {bank_id} (not in this PCG file - ROM bank)")
        else:
            print(f"  ✗ {bank_id} (MISSING)")
    
    print()
    
    # Check if any unexpected banks are marked as ROM
    unexpected_rom = [bid for bid in rom_bank_ids if bid not in expected_rom]
    if unexpected_rom:
        print(f"WARNING: Unexpected ROM banks: {unexpected_rom}")
    else:
        print("✓ All ROM banks correctly identified")
    
    print()
    
    # Summary
    gm2_banks = [bid for bid in rom_bank_ids if bid.startswith("g(")]
    if len(gm2_banks) == 10:
        print("✓ All 10 GM2 banks present and marked as read-only")
    else:
        print(f"✗ Expected 10 GM2 banks, found {len(gm2_banks)}")
    
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_readonly_banks(sys.argv[1])
    else:
        print("Usage: python3 test_gm_readonly.py <path_to_pcg_file>")
