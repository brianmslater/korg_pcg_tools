#!/usr/bin/env python3
"""Test basic Listbox functionality on macOS."""

import tkinter as tk
from tkinter import ttk
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'

print("\n" + "="*70)
print("LISTBOX TEST - Testing basic Listbox rendering on macOS")
print("="*70)

root = tk.Tk()
root.title("Listbox Test")
root.geometry("600x400")

# Create a simple listbox
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Simple Listbox Test", font=('Arial', 14, 'bold')).pack(pady=10)
ttk.Label(frame, text="If you can see items below, Listbox works on your system").pack(pady=5)

# Listbox with scrollbar
list_frame = ttk.Frame(frame)
list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

listbox = tk.Listbox(list_frame, font=('Monaco', 12))
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)

listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add test items
print("\nAdding test items to listbox...")
test_items = [
    "Item 1: Test",
    "Item 2: Hello World",
    "Item 3: PCG Tools",
    "Item 4: Korg Kronos",
    "Item 5: Programs",
    "Item 6: Combis",
    "Item 7: Set Lists",
    "Item 8: Patches",
    "Item 9: Categories",
    "Item 10: Favorites"
]

for i, item in enumerate(test_items):
    listbox.insert(tk.END, item)
    print(f"  Added: {item}")

print(f"\nTotal items added: {listbox.size()}")

# Status
status = ttk.Label(root, text=f"Listbox contains {listbox.size()} items", relief=tk.SUNKEN)
status.pack(side=tk.BOTTOM, fill=tk.X)

print("\n" + "="*70)
print("WINDOW OPENED")
print("Can you see the 10 test items in the listbox?")
print("="*70 + "\n")

root.mainloop()
