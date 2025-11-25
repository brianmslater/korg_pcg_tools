#!/usr/bin/env python3
"""Test with flat list instead of tree - macOS compatibility test."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"

print(f"\n{'='*70}")
print(f"FLAT LIST TEST - No tree hierarchy")
print(f"{'='*70}")
print(f"Loading: {TEST_FILE}")

try:
    pcg = read_pcg_file(TEST_FILE)
    print(f"✓ File loaded: {len(pcg.program_banks)} program banks, {len(pcg.combi_banks)} combi banks")
    
    root = tk.Tk()
    root.title(f"Flat List Test - {Path(TEST_FILE).name}")
    root.geometry("900x600")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Programs tab - FLAT LIST (no tree)
    programs_frame = ttk.Frame(notebook)
    notebook.add(programs_frame, text="Programs")
    
    columns = ('Bank', 'ID', 'Name', 'Category', 'Favorite')
    programs_tree = ttk.Treeview(programs_frame, columns=columns, show='headings', selectmode='extended')
    
    programs_tree.heading('Bank', text='Bank')
    programs_tree.heading('ID', text='ID')
    programs_tree.heading('Name', text='Name')
    programs_tree.heading('Category', text='Category')
    programs_tree.heading('Favorite', text='Fav')
    
    programs_tree.column('Bank', width=80)
    programs_tree.column('ID', width=100)
    programs_tree.column('Name', width=400)
    programs_tree.column('Category', width=150)
    programs_tree.column('Favorite', width=50)
    
    scrollbar = ttk.Scrollbar(programs_frame, orient=tk.VERTICAL, command=programs_tree.yview)
    programs_tree.configure(yscrollcommand=scrollbar.set)
    
    programs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate programs - FLAT (no hierarchy)
    print(f"\nPopulating programs (flat list)...")
    count = 0
    for bank in pcg.program_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        for i, prog in enumerate(bank.patches):
            cat = prog.category.name if prog.category else ""
            fav = "✓" if prog.favorite else ""
            programs_tree.insert('', 'end', values=(bank.bank_id, prog.id, prog.name, cat, fav))
            count += 1
            if i < 3:
                print(f"    [{i}] {prog.id}: {prog.name}")
    
    print(f"  Total: {count} programs inserted")
    
    # Combis tab - FLAT LIST
    combis_frame = ttk.Frame(notebook)
    notebook.add(combis_frame, text="Combis")
    
    combis_tree = ttk.Treeview(combis_frame, columns=columns, show='headings', selectmode='extended')
    
    combis_tree.heading('Bank', text='Bank')
    combis_tree.heading('ID', text='ID')
    combis_tree.heading('Name', text='Name')
    combis_tree.heading('Category', text='Category')
    combis_tree.heading('Favorite', text='Fav')
    
    combis_tree.column('Bank', width=80)
    combis_tree.column('ID', width=100)
    combis_tree.column('Name', width=400)
    combis_tree.column('Category', width=150)
    combis_tree.column('Favorite', width=50)
    
    scrollbar2 = ttk.Scrollbar(combis_frame, orient=tk.VERTICAL, command=combis_tree.yview)
    combis_tree.configure(yscrollcommand=scrollbar2.set)
    
    combis_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate combis - FLAT
    print(f"\nPopulating combis (flat list)...")
    count = 0
    for bank in pcg.combi_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        for i, combi in enumerate(bank.patches):
            cat = combi.category.name if combi.category else ""
            fav = "✓" if combi.favorite else ""
            combis_tree.insert('', 'end', values=(bank.bank_id, combi.id, combi.name, cat, fav))
            count += 1
            if i < 3:
                print(f"    [{i}] {combi.id}: {combi.name}")
    
    print(f"  Total: {count} combis inserted")
    
    # Status
    status = ttk.Label(root, text=f"Loaded: {Path(TEST_FILE).name} - Flat list view (no tree hierarchy)", relief=tk.SUNKEN)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    
    print(f"\n{'='*70}")
    print(f"✓ FLAT LIST GUI CREATED")
    print(f"  If you can see patches now, the issue is with tree hierarchy on macOS")
    print(f"  If you still can't see anything, there's a deeper tkinter issue")
    print(f"{'='*70}\n")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
