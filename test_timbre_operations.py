#!/usr/bin/env python3
"""Test script for timbre operations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.batch_operations import BatchOperations


def test_timbre_operations(pcg_path: str):
    """Test timbre operations on a PCG file.
    
    Args:
        pcg_path: Path to PCG file
    """
    print("=" * 80)
    print(f"Testing Timbre Operations: {pcg_path}")
    print("=" * 80)
    print()
    
    pcg = read_pcg_file(pcg_path)
    
    # Find a combi with timbres
    test_combi = None
    for bank in pcg.combi_banks:
        for combi in bank.patches:
            if len(combi.timbres) > 2:
                test_combi = combi
                break
        if test_combi:
            break
    
    if not test_combi:
        print("No combis with timbres found!")
        return
    
    print(f"Testing with combi: {test_combi.id} - {test_combi.name}")
    print(f"Timbres: {len(test_combi.timbres)}")
    print()
    
    # Test 1: Display timbres
    print("Test 1: Display Timbres")
    print("-" * 80)
    for i, timbre in enumerate(test_combi.timbres[:5]):
        print(f"  Timbre {i}: {timbre.program_id} - Ch {timbre.midi_channel} - {timbre.status}")
    print()
    
    # Test 2: Move timbre up
    print("Test 2: Move Timbre Up")
    print("-" * 80)
    if len(test_combi.timbres) > 1:
        print(f"  Before: Timbre 1 = {test_combi.timbres[1].program_id}")
        result = BatchOperations.move_timbre_up(test_combi, 1)
        print(f"  Move up result: {result}")
        print(f"  After: Timbre 0 = {test_combi.timbres[0].program_id}")
        print(f"  ✓ Move up works!" if result else "  ✗ Move up failed")
        # Move back
        BatchOperations.move_timbre_down(test_combi, 0)
    print()
    
    # Test 3: Move timbre down
    print("Test 3: Move Timbre Down")
    print("-" * 80)
    if len(test_combi.timbres) > 1:
        print(f"  Before: Timbre 0 = {test_combi.timbres[0].program_id}")
        result = BatchOperations.move_timbre_down(test_combi, 0)
        print(f"  Move down result: {result}")
        print(f"  After: Timbre 1 = {test_combi.timbres[1].program_id}")
        print(f"  ✓ Move down works!" if result else "  ✗ Move down failed")
        # Move back
        BatchOperations.move_timbre_up(test_combi, 1)
    print()
    
    # Test 4: Sort timbres
    print("Test 4: Sort Timbres by MIDI Channel")
    print("-" * 80)
    print("  Before sort:")
    for i, timbre in enumerate(test_combi.timbres[:5]):
        print(f"    Timbre {i}: Ch {timbre.midi_channel}")
    
    BatchOperations.sort_timbres(test_combi, "channel")
    
    print("  After sort:")
    for i, timbre in enumerate(test_combi.timbres[:5]):
        print(f"    Timbre {i}: Ch {timbre.midi_channel}")
    print("  ✓ Sort works!")
    print()
    
    # Test 5: Clear timbre
    print("Test 5: Clear Timbre")
    print("-" * 80)
    if len(test_combi.timbres) > 0:
        print(f"  Before: Timbre 0 = {test_combi.timbres[0].program_id}")
        result = BatchOperations.clear_timbre(test_combi, 0)
        print(f"  Clear result: {result}")
        print(f"  After: Timbre 0 = {test_combi.timbres[0].program_id}")
        print(f"  ✓ Clear works!" if result else "  ✗ Clear failed")
    print()
    
    # Test 6: Clear unused timbres
    print("Test 6: Clear Unused Timbres")
    print("-" * 80)
    # Count muted/OFF timbres
    unused_count = sum(1 for t in test_combi.timbres if t.mute or t.status == "OFF")
    print(f"  Unused timbres (muted or OFF): {unused_count}")
    
    cleared = BatchOperations.clear_unused_timbres(test_combi)
    print(f"  Cleared: {cleared}")
    print(f"  ✓ Clear unused works!")
    print()
    
    print("=" * 80)
    print("All Timbre Operations Tests Complete!")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_timbre_operations(sys.argv[1])
    else:
        print("Usage: python3 test_timbre_operations.py <path_to_pcg_file>")
        print()
        print("Example:")
        print("  python3 test_timbre_operations.py test_files/soundcheck11242025.PCG")
