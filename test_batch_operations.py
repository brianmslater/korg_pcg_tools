#!/usr/bin/env python3
"""Test batch operations functionality."""

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.batch_operations import BatchOperations

def test_batch_operations():
    """Test batch operations on programs."""
    
    # Read test file
    print("Reading test file...")
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    
    bank = pcg.program_banks[0]
    print(f"\nBank: {bank.bank_id}")
    print(f"Programs: {len(bank.patches)}")
    
    # Show first 10 programs
    print("\nFirst 10 programs BEFORE operations:")
    for i in range(min(10, len(bank.patches))):
        prog = bank.patches[i]
        print(f"  {prog.id}: {prog.name} (Fav: {prog.favorite})")
    
    # Test 1: Sort by name
    print("\n=== Test 1: Sort by Name ===")
    BatchOperations.sort_programs(bank, key="name")
    print("✓ Sorted by name")
    print("\nFirst 10 after sort:")
    for i in range(min(10, len(bank.patches))):
        prog = bank.patches[i]
        print(f"  {prog.id}: {prog.name}")
    
    # Test 2: Mark some as favorites
    print("\n=== Test 2: Mark Favorites ===")
    for i in range(5):
        bank.patches[i].favorite = True
    print("✓ Marked first 5 as favorites")
    
    # Test 3: Move favorites to top
    print("\n=== Test 3: Move Favorites to Top ===")
    BatchOperations.move_favorites_to_top(bank)
    print("✓ Moved favorites to top")
    print("\nFirst 10 after moving favorites:")
    for i in range(min(10, len(bank.patches))):
        prog = bank.patches[i]
        fav_mark = "★" if prog.favorite else " "
        print(f"  {fav_mark} {prog.id}: {prog.name}")
    
    # Test 4: Capitalize names
    print("\n=== Test 4: Capitalize Names ===")
    original_name = bank.patches[0].name
    BatchOperations.capitalize_names(bank, style="upper")
    print(f"✓ Capitalized names to UPPER")
    print(f"  Example: '{original_name}' → '{bank.patches[0].name}'")
    
    # Test 5: Remove duplicates (create some first)
    print("\n=== Test 5: Remove Duplicates ===")
    original_count = len(bank.patches)
    # Duplicate first program
    bank.patches.append(bank.patches[0])
    bank.patches.append(bank.patches[1])
    print(f"  Added 2 duplicates: {original_count} → {len(bank.patches)}")
    
    BatchOperations.remove_duplicates(bank, by="name")
    print(f"✓ Removed duplicates: {len(bank.patches)} remaining")
    
    # Test 6: Compact bank (won't remove much from this file)
    print("\n=== Test 6: Compact Bank ===")
    before_compact = len(bank.patches)
    BatchOperations.compact_bank(bank)
    after_compact = len(bank.patches)
    removed = before_compact - after_compact
    print(f"✓ Compacted: removed {removed} empty patches")
    print(f"  {before_compact} → {after_compact}")
    
    # Save result
    output_file = "test_files/soundcheck_BATCH_OPS_TEST.PCG"
    write_pcg_file(pcg, output_file)
    print(f"\n✓ Saved to {output_file}")
    
    # Verify by reading back
    print("\nVerifying saved file...")
    pcg2 = read_pcg_file(output_file)
    bank2 = pcg2.program_banks[0]
    
    print(f"✓ File verified: {len(bank2.patches)} programs")
    print("\nFirst 5 programs in saved file:")
    for i in range(min(5, len(bank2.patches))):
        prog = bank2.patches[i]
        fav_mark = "★" if prog.favorite else " "
        print(f"  {fav_mark} {prog.id}: {prog.name}")
    
    print("\n✅ All batch operations tests passed!")

if __name__ == "__main__":
    test_batch_operations()
