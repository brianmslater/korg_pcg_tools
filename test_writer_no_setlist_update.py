#!/usr/bin/env python3
"""
Test writer WITHOUT calling setlist update methods.
This will tell us if the setlist updates are the problem.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.models import PcgFile

def write_without_setlist_updates(pcg: PcgFile, filepath: str):
    """Write file WITHOUT updating setlist chunks."""
    
    if not pcg.raw_data:
        raise ValueError("No raw data to write")
    
    # Write raw_data directly without any modifications
    with open(filepath, 'wb') as f:
        f.write(pcg.raw_data)

def test_no_setlist_update():
    """Test writing without setlist updates."""
    
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    print("=" * 80)
    print("TEST: Write WITHOUT Setlist Updates")
    print("=" * 80)
    
    # Read file
    print(f"\n1. Reading: {test_file}")
    pcg = read_pcg_file(str(test_file))
    print(f"   ✓ Loaded")
    
    # Write WITHOUT calling any update methods
    output_file = Path('test_files/no_setlist_update.PCG')
    print(f"\n2. Writing (NO setlist updates): {output_file}")
    write_without_setlist_updates(pcg, str(output_file))
    print(f"   ✓ Written")
    
    # Compare sizes
    original_size = test_file.stat().st_size
    output_size = output_file.stat().st_size
    
    print(f"\n3. File size:")
    print(f"   Original: {original_size:,} bytes")
    print(f"   Output:   {output_size:,} bytes")
    
    if original_size == output_size:
        print(f"   ✓ Sizes match")
    else:
        print(f"   ❌ Size difference: {output_size - original_size:+,} bytes")
    
    print(f"\n{'=' * 80}")
    print("NEXT STEP:")
    print("Copy test_files/no_setlist_update.PCG to USB drive")
    print()
    print("If this file LOADS successfully:")
    print("  → The setlist update methods are corrupting the file")
    print("  → Need to fix _update_sls1_names() and/or _update_sbk1_names()")
    print()
    print("If this file FAILS to load:")
    print("  → Something else is wrong (not related to our updates)")
    print("  → May be a parser issue or file format issue")
    print("=" * 80)

if __name__ == '__main__':
    test_no_setlist_update()
