#!/usr/bin/env python3
"""Debug bank ID issue."""

from pcg_tools.reader import read_pcg_file

# Load file
pcg = read_pcg_file('test_files/files/GLAM V3/GLAMV3.PCG')

# Check program banks
print("Program Banks:")
for bank in pcg.program_banks:
    print(f"  Bank ID: '{bank.bank_id}' (type: {type(bank.bank_id)})")
    print(f"  First 3 programs:")
    for i, prog in enumerate(bank.patches[:3]):
        print(f"    {i}: bank='{prog.bank}', index={prog.index}, id='{prog.id}'")

# Check combi banks
print("\nCombi Banks:")
for bank in pcg.combi_banks:
    print(f"  Bank ID: '{bank.bank_id}'")
    print(f"  First 3 combis:")
    for i, combi in enumerate(bank.patches[:3]):
        print(f"    {i}: bank='{combi.bank}', index={combi.index}, id='{combi.id}'")
        if combi.timbres:
            print(f"       Timbres: {len(combi.timbres)}")
            for j, timbre in enumerate(combi.timbres[:3]):
                if timbre.status != "OFF":
                    print(f"         Timbre {j}: status={timbre.status}, prog_bank='{timbre.program_bank}', prog_index={timbre.program_index}, prog_id='{timbre.program_id}'")
