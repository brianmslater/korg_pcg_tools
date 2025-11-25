#!/usr/bin/env python3
"""Test GUI display functionality."""

import tkinter as tk
from tkinter import ttk
from pcg_tools.reader import read_pcg_file
from pathlib import Path

# Test file
test_file = "test_files/files/GLAM V3/GLAMV3.PCG"

print(f"Loading {test_file}...")
pcg = read_pcg_file(test_file)
print(f"✓ File loaded: {len(pcg.program_banks)} program banks, {len(pcg.combi_banks)} combi banks")

# Create a simple test window
root = tk.Tk()
root.title("PCG Display Test")
root.geometry("800x600")

# Create notebook
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Programs tab
programs_frame = ttk.Frame(notebook)
notebook.add(programs_frame, text="Programs")

# Create treeview for programs
columns = ('ID', 'Name', 'Category', 'Favorite')
programs_tree = ttk.Treeview(programs_frame, columns=columns, show='tree headings', selectmode='extended')

programs_tree.heading('#0', text='Bank')
programs_tree.heading('ID', text='ID')
programs_tree.heading('Name', text='Name')
programs_tree.heading('Category', text='Category')
programs_tree.heading('Favorite', text='Fav')

programs_tree.column('#0', width=100)
programs_tree.column('ID', width=100)
programs_tree.column('Name', width=300)
programs_tree.column('Category', width=150)
programs_tree.column('Favorite', width=50)

scrollbar = ttk.Scrollbar(programs_frame, orient=tk.VERTICAL, command=programs_tree.yview)
programs_tree.configure(yscrollcommand=scrollbar.set)

programs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Populate programs tree
print("\nPopulating programs tree...")
for bank in pcg.program_banks:
    print(f"  Adding bank {bank.bank_id} with {len(bank.patches)} patches")
    bank_node = programs_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
    for prog in bank.patches:
        cat = prog.category.name if prog.category else ""
        fav = "✓" if prog.favorite else ""
        programs_tree.insert(bank_node, 'end', values=(prog.id, prog.name, cat, fav))
        
print(f"✓ Added {len(pcg.program_banks)} program banks to tree")

# Combis tab
combis_frame = ttk.Frame(notebook)
notebook.add(combis_frame, text="Combis")

# Create treeview for combis
combis_tree = ttk.Treeview(combis_frame, columns=columns, show='tree headings', selectmode='extended')

combis_tree.heading('#0', text='Bank')
combis_tree.heading('ID', text='ID')
combis_tree.heading('Name', text='Name')
combis_tree.heading('Category', text='Category')
combis_tree.heading('Favorite', text='Fav')

combis_tree.column('#0', width=100)
combis_tree.column('ID', width=100)
combis_tree.column('Name', width=300)
combis_tree.column('Category', width=150)
combis_tree.column('Favorite', width=50)

scrollbar2 = ttk.Scrollbar(combis_frame, orient=tk.VERTICAL, command=combis_tree.yview)
combis_tree.configure(yscrollcommand=scrollbar2.set)

combis_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

# Populate combis tree
print("\nPopulating combis tree...")
for bank in pcg.combi_banks:
    print(f"  Adding bank {bank.bank_id} with {len(bank.patches)} patches")
    bank_node = combis_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
    for combi in bank.patches:
        cat = combi.category.name if combi.category else ""
        fav = "✓" if combi.favorite else ""
        combis_tree.insert(bank_node, 'end', values=(combi.id, combi.name, cat, fav))

print(f"✓ Added {len(pcg.combi_banks)} combi banks to tree")

# Status label
status = ttk.Label(root, text=f"Loaded: {Path(test_file).name} - {len(pcg.get_all_programs())} programs, {len(pcg.get_all_combis())} combis")
status.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

print("\n✓ GUI test window created successfully!")
print("If you can see patches in the tree, the display is working.")
print("If the tree is empty, there's a display issue.\n")

root.mainloop()
