#!/usr/bin/env python3
"""Test program copy/paste functionality."""

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.clipboard import get_clipboard

def test_program_copy_paste():
    """Test copying and pasting programs."""
    
    # Read test file
    print("Reading test file...")
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    
    # Get first program bank
    bank = pcg.program_banks[0]
    print(f"\nBank: {bank.bank_id}")
    print(f"Programs: {len(bank.patches)}")
    
    if len(bank.patches) < 2:
        print("Not enough programs to test copy/paste")
        return
    
    # Get source and destination programs
    source_program = bank.patches[0]
    dest_program = bank.patches[10]
    
    print(f"\nSource program (index {0}):")
    print(f"  ID: {source_program.id}")
    print(f"  Name: {source_program.name}")
    print(f"  Category: {source_program.category}")
    print(f"  Favorite: {source_program.favorite}")
    print(f"  Engine: {source_program.engine}")
    print(f"  OSC Mode: {source_program.osc_mode}")
    
    print(f"\nDestination program (index {10}) BEFORE paste:")
    print(f"  ID: {dest_program.id}")
    print(f"  Name: {dest_program.name}")
    print(f"  Category: {dest_program.category}")
    
    # Copy the program
    clipboard = get_clipboard()
    clipboard.copy_program(source_program)
    print("\n✓ Copied program to clipboard")
    
    # Check clipboard
    assert clipboard.has_program(), "Clipboard should have a program"
    print("✓ Clipboard has program")
    
    # Paste the program
    clipboard.paste_program(dest_program)
    print("\n✓ Pasted program from clipboard")
    
    # Verify the paste
    print(f"\nDestination program (index {10}) AFTER paste:")
    print(f"  ID: {dest_program.id}")  # ID should NOT change
    print(f"  Name: {dest_program.name}")  # Name should match source
    print(f"  Category: {dest_program.category}")
    print(f"  Favorite: {dest_program.favorite}")
    print(f"  Engine: {dest_program.engine}")
    print(f"  OSC Mode: {dest_program.osc_mode}")
    
    # Verify properties match (except ID which should stay the same)
    assert dest_program.name == source_program.name, "Names should match"
    assert dest_program.favorite == source_program.favorite, "Favorite should match"
    assert dest_program.engine == source_program.engine, "Engine should match"
    assert dest_program.osc_mode == source_program.osc_mode, "OSC Mode should match"
    
    # Verify ID did NOT change
    assert dest_program.id == "I-A010", "ID should remain unchanged"
    
    print("\n✓ All properties match!")
    print("✓ Program ID preserved (not copied)")
    
    # Save the modified file
    output_file = "test_files/soundcheck_PROGRAM_COPY_PASTE_TEST.PCG"
    write_pcg_file(pcg, output_file)
    print(f"\n✓ Saved to {output_file}")
    
    # Read it back and verify
    print("\nVerifying saved file...")
    pcg2 = read_pcg_file(output_file)
    bank2 = pcg2.program_banks[0]
    pasted_program = bank2.patches[10]
    
    assert pasted_program.name == source_program.name, "Name should persist after save"
    assert pasted_program.id == "I-A010", "ID should remain I-A010"
    
    print("✓ Pasted program verified in saved file")
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_program_copy_paste()
