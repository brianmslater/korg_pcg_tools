#!/usr/bin/env python3
from pcg_tools.reader import read_pcg_file

pcg = read_pcg_file('test_files/KRONOS BOOSTER PACK V3 Narfsounds/SETLISTS Open before loading!.PCG')

print(f'Setlists: {len(pcg.set_lists)}')
for sl in pcg.set_lists[:3]:
    print(f'\nSetlist {sl.index}: {sl.name}')
    non_empty = [s for s in sl.slots if s.name and s.name.strip()]
    print(f'  Non-empty slots: {len(non_empty)}')
    
    # Show first 3 slots with details
    for slot in non_empty[:3]:
        print(f'    Slot {slot.slot_index}: name={slot.name}')
        print(f'      patch: {slot.patch_type} {slot.patch_bank}{slot.patch_index:03d}')
        print(f'      color: {slot.color} = {slot.color_name}')
        print(f'      size: {slot.text_size} = {slot.text_size_name}')
        if slot.notes:
            print(f'      notes: {slot.notes[:50]}...')
