#!/usr/bin/env python3
"""
Diagnose what should be displayed in the GUI for nw.PCG
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

pcg = read_pcg_file('/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG')

print("=" * 80)
print("NW.PCG FILE DIAGNOSIS")
print("=" * 80)

print("\n📋 SETLISTS IN DROPDOWN:")
print("-" * 80)
for sl in pcg.set_lists:
    print(f"  {sl.index}: {sl.name}")

print("\n" + "=" * 80)
print("SETLIST 0: Preload Set List")
print("=" * 80)
setlist0 = pcg.set_lists[0]
print(f"Total slots: {len(setlist0.slots)}")
print(f"\nFirst 10 slots:")
print(f"{'Slot':<6} {'Name':<30} {'Patch':<15} {'Trans':<7} {'Vol':<5} {'Color':<15} {'Size'}")
print("-" * 80)
for i, slot in enumerate(setlist0.slots[:10]):
    patch_ref = ""
    if slot.patch_bank and slot.patch_type:
        patch_ref = f"{slot.patch_type[0]}-{slot.patch_bank}{slot.patch_index:03d}"
    print(f"{slot.slot_index:<6} {slot.name:<30} {patch_ref:<15} {slot.transpose:<7} {slot.volume:<5} {slot.color_name:<15} {slot.text_size_name}")

print("\n" + "=" * 80)
print("SETLIST 1: NIGHTWISH LEGACY 2")
print("=" * 80)
setlist1 = pcg.set_lists[1]
print(f"Total slots: {len(setlist1.slots)}")
print(f"\nAll non-empty slots:")
print(f"{'Slot':<6} {'Name':<30} {'Patch':<15} {'Trans':<7} {'Vol':<5} {'Color':<15} {'Size'}")
print("-" * 80)
for slot in setlist1.slots:
    if slot.name and slot.name.strip():
        patch_ref = ""
        if slot.patch_bank and slot.patch_type:
            patch_ref = f"{slot.patch_type[0]}-{slot.patch_bank}{slot.patch_index:03d}"
        print(f"{slot.slot_index:<6} {slot.name:<30} {patch_ref:<15} {slot.transpose:<7} {slot.volume:<5} {slot.color_name:<15} {slot.text_size_name}")

print("\n" + "=" * 80)
print("EXPECTED GUI BEHAVIOR:")
print("=" * 80)
print("1. Setlist dropdown should show:")
print("   - 0: Preload Set List")
print("   - 1: NIGHTWISH LEGACY 2")
print("   - 2-15: Set List 003 through Set List 016")
print()
print("2. When 'Preload Set List' is selected:")
print("   - Should show 32 slots (0-31)")
print("   - Slot names: SGX-2, HD-1, EP-1, etc.")
print()
print("3. When 'NIGHTWISH LEGACY 2' is selected:")
print("   - Should show 128 slots (0-127)")
print("   - Only slots 0, 4, 7, 11 have names ('STARGAZERS')")
print("   - Other slots should be empty/blank")
print()
print("=" * 80)
