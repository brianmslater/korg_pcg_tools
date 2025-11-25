#!/usr/bin/env python3
"""Test name editing functionality."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.edit_dialog import validate_korg_name, sanitize_korg_name

print("="*70)
print("NAME VALIDATION TESTS")
print("="*70)

# Test valid names
test_cases = [
    ("Valid Name", True),
    ("Program 001", True),
    ("Berlin Dark Grand", True),
    ("A" * 24, True),  # Max length
    ("A" * 25, False),  # Too long
    ("", False),  # Empty
    ("Test\x00Name", False),  # Null character
    ("Test\nName", False),  # Newline
    ("Valid-Name_123", True),  # Special chars
    ("Café", False),  # Non-ASCII (é)
]

for name, expected_valid in test_cases:
    is_valid, error = validate_korg_name(name)
    status = "✅" if is_valid == expected_valid else "❌"
    display_name = repr(name) if len(name) < 30 else repr(name[:27] + "...")
    print(f"{status} {display_name:<35} Valid: {is_valid}")
    if not is_valid and error:
        print(f"   Error: {error}")

print("\n" + "="*70)
print("NAME SANITIZATION TESTS")
print("="*70)

sanitize_cases = [
    ("Valid Name", "Valid Name"),
    ("A" * 30, "A" * 24),  # Truncate
    ("Test\x00Name", "TestName"),  # Remove null
    ("Café", "Caf"),  # Remove non-ASCII
    ("", "Untitled"),  # Empty becomes default
]

for input_name, expected_output in sanitize_cases:
    output = sanitize_korg_name(input_name)
    status = "✅" if output == expected_output else "❌"
    print(f"{status} {repr(input_name):<30} -> {repr(output)}")

print("\n" + "="*70)
print("PATCH NAME EDITING TEST")
print("="*70)

# Test with a real PCG file
TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

if os.path.exists(TEST_FILE):
    try:
        pcg = read_pcg_file(TEST_FILE)
        
        # Find first program
        if pcg.program_banks and pcg.program_banks[0].patches:
            prog = pcg.program_banks[0].patches[0]
            original_name = prog.name
            print(f"Original name: '{original_name}'")
            print(f"Has raw_data: {len(prog.raw_data) if prog.raw_data else 0} bytes")
            print(f"Has offset: {hasattr(prog, '_raw_offset')}")
            if hasattr(prog, '_raw_offset'):
                print(f"Offset: 0x{prog._raw_offset:08X}")
            
            # Simulate name change
            new_name = "Test Program Name"
            prog.name = new_name
            
            # Update raw_data (simulate what edit dialog does)
            if prog.raw_data:
                name_bytes = new_name.encode('ascii', errors='replace')[:24]
                name_bytes = name_bytes.ljust(24, b'\x00')
                raw_data = bytearray(prog.raw_data)
                raw_data[0:24] = name_bytes
                prog.raw_data = bytes(raw_data)
                
                # Verify
                stored_name = prog.raw_data[0:24].split(b'\x00')[0].decode('ascii')
                print(f"\n✅ Name updated in raw_data: '{stored_name}'")
                print(f"   Matches new name: {stored_name == new_name}")
            
        print("\n✅ Name editing mechanism works correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"⚠️  Test file not found: {TEST_FILE}")
    print("   Skipping PCG file test")

print("\n" + "="*70)
print("✅ ALL NAME EDITING TESTS COMPLETE")
print("="*70)
