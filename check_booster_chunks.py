#!/usr/bin/env python3
with open('test_files/KRONOS BOOSTER PACK V3 Narfsounds/SETLISTS Open before loading!.PCG', 'rb') as f:
    data = f.read()

# Find chunks
chunks = []
for chunk_name in [b'SLS1', b'STL1', b'SBK1', b'SLD1']:
    pos = data.find(chunk_name)
    if pos >= 0:
        chunks.append((chunk_name.decode(), pos))

print('Chunks found:')
for name, pos in sorted(chunks, key=lambda x: x[1]):
    print(f'  {name} at 0x{pos:08X}')

# Check if STL1 exists
if b'STL1' in data:
    print('\nSTL1 chunk exists - should have patch references')
else:
    print('\nNo STL1 chunk - using older SLS1 format (no patch references)')
