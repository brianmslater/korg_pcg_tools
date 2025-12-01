#!/usr/bin/env python3
"""Test editing directly in pcg.raw_data instead of prog.raw_data."""

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
import os

input_file = 'test_files/soundcheck_BASE_FOR_TESTING.PCG'
output_file = 'test_files/soundcheck_DIRECT_EDIT_TEST.PCG'

print('Testing DIRECT edit in pcg.raw_data...')
print('=' * 80)

# Read
pcg = read_pcg_file(input_file)
print('1. Read file')

# Find first program
programs = pcg.get_all_programs()
test_program = None
for prog in programs:
    if prog.name and not prog.name.startswith('[Empty'):
        test_program = prog
        break

print(f'2. Found: {test_program.id} - {test_program.name}')
print(f'   Offset: {test_program._raw_offset}')

# Edit DIRECTLY in pcg.raw_data (not in prog.raw_data)
print('3. Editing DIRECTLY in pcg.raw_data...')
raw_data = bytearray(pcg.raw_data)
offset = test_program._raw_offset

# Update name at the offset
new_name = 'DIRECT EDIT'
name_bytes = new_name.encode('ascii', errors='replace')[:24]
name_bytes = name_bytes.ljust(24, b'\x00')
raw_data[offset:offset+24] = name_bytes

# Update pcg.raw_data
pcg.raw_data = bytes(raw_data)
print(f'   ✓ Updated name at offset {offset}')

# DON'T update prog.raw_data - let it stay as is
print('4. NOT updating prog.raw_data (leaving it unchanged)')

# Save
print(f'5. Saving to: {output_file}')
write_pcg_file(pcg, output_file)
print('   ✓ Saved')

# Compare
orig_size = os.path.getsize(input_file)
new_size = os.path.getsize(output_file)
print(f'6. File sizes: {orig_size:,} -> {new_size:,} (same: {orig_size == new_size})')

print('=' * 80)
print('✅ Test complete - copy to USB and test on hardware')
