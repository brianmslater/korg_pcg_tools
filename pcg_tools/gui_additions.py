"""
Additional methods to add to PcgWindow class in gui.py

Copy these methods into the PcgWindow class to complete the implementation.
"""

# Add these imports at the top of gui.py:
# from .clipboard import get_clipboard
# from .operations import PatchOperations  
# from .edit_dialog import EditPatchDialog

# Add to __init__ after self.is_dirty = False:
# self.clipboard = get_clipboard()
# self.operations = None

# Add to load_file after self.filepath = filepath:
# self.operations = PatchOperations(self.pcg)

# Then add all these methods to PcgWindow class:

def _show_context_menu(self, event, tree, list_type):
    """Show context menu on right-click."""
    # Select item under cursor
    item = tree.identify_row(event.y)
    if item:
        tree.selection_set(item)
    
    menu = tk.Menu(tree, tearoff=0)
    menu.add_command(label="Edit...", command=lambda: self._edit_selected(tree, list_type))
    menu.add_separator()
    menu.add_command(label="Copy (Ctrl+C)", command=lambda: self._copy_selection(tree, list_type))
    menu.add_command(label="Cut (Ctrl+X)", command=lambda: self._cut_selection(tree, list_type))
    menu.add_command(label="Paste (Ctrl+V)", command=lambda: self._paste_selection(tree, list_type))
    menu.add_separator()
    menu.add_command(label="Move Up", command=lambda: self._move_up(tree, list_type))
    menu.add_command(label="Move Down", command=lambda: self._move_down(tree, list_type))
    menu.add_separator()
    menu.add_command(label="Sort...", command=lambda: self._sort_patches(tree, list_type))
    menu.add_command(label="Compact", command=lambda: self._compact_patches(tree, list_type))
    menu.add_command(label="Clear (Del)", command=lambda: self._clear_selection(tree, list_type))
    
    try:
        menu.post(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def _on_double_click(self, event, tree, list_type):
    """Handle double-click to edit."""
    item = tree.identify_row(event.y)
    if not item:
        return
    
    # Check if it's a patch (not a bank header)
    values = tree.item(item)['values']
    if not values:
        return
    
    self._edit_item(item, tree, list_type)

def _edit_selected(self, tree, list_type):
    """Edit selected patch."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a patch to edit", parent=self.window)
        return
    
    self._edit_item(selection[0], tree, list_type)

def _edit_item(self, item, tree, list_type):
    """Edit a specific item."""
    values = tree.item(item)['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    index = int(patch_id[-3:])
    
    if list_type == "programs":
        patch = self.pcg.find_program(bank, index)
        patch_type = "program"
    else:
        patch = self.pcg.find_combi(bank, index)
        patch_type = "combi"
    
    if patch:
        from .edit_dialog import EditPatchDialog
        dialog = EditPatchDialog(self.window, patch, patch_type)
        if dialog.show():
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()

def _copy_selection(self, tree, list_type):
    """Copy selected patches to clipboard."""
    patches = self._get_selected_patches(tree, list_type)
    if not patches:
        return
    
    if list_type == "programs":
        self.clipboard.copy_programs(patches, self.filepath or "Untitled")
    else:
        self.clipboard.copy_combis(patches, self.filepath or "Untitled")
    
    self.parent.status_bar.config(text=self.clipboard.get_summary())

def _cut_selection(self, tree, list_type):
    """Cut selected patches to clipboard."""
    patches = self._get_selected_patches(tree, list_type)
    if not patches:
        return
    
    if list_type == "programs":
        self.clipboard.cut_programs(patches, self.filepath or "Untitled")
    else:
        self.clipboard.cut_combis(patches, self.filepath or "Untitled")
    
    self.parent.status_bar.config(text=self.clipboard.get_summary())

def _paste_selection(self, tree, list_type):
    """Paste from clipboard."""
    if self.clipboard.is_empty():
        messagebox.showinfo("Clipboard Empty", "Nothing to paste", parent=self.window)
        return
    
    if not self.operations:
        return
    
    # Get target location
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Target", "Please select where to paste", parent=self.window)
        return
    
    values = tree.item(selection[0])['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    index = int(patch_id[-3:])
    
    # Paste
    if list_type == "programs" and self.clipboard.programs:
        count = self.operations.paste_programs(self.clipboard.programs, bank, index)
        messagebox.showinfo("Paste Complete", f"Pasted {count} program(s)", parent=self.window)
    elif list_type == "combis" and self.clipboard.combis:
        count = self.operations.paste_combis(self.clipboard.combis, bank, index)
        messagebox.showinfo("Paste Complete", f"Pasted {count} combi(s)", parent=self.window)
    
    self.pcg.is_dirty = True
    self.is_dirty = True
    self._update_display()
    self._update_title()

def _clear_selection(self, tree, list_type):
    """Clear selected patches."""
    patches = self._get_selected_patches(tree, list_type)
    if not patches:
        return
    
    if not messagebox.askyesno("Confirm Clear", 
                               f"Clear {len(patches)} patch(es)?", 
                               parent=self.window):
        return
    
    for patch in patches:
        if list_type == "programs":
            self.operations.clear_program(patch.bank, patch.index)
        else:
            self.operations.clear_combi(patch.bank, patch.index)
    
    self.pcg.is_dirty = True
    self.is_dirty = True
    self._update_display()
    self._update_title()

def _move_up(self, tree, list_type):
    """Move selected patch up."""
    selection = tree.selection()
    if not selection or len(selection) != 1:
        messagebox.showwarning("Selection", "Please select exactly one patch", parent=self.window)
        return
    
    values = tree.item(selection[0])['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    index = int(patch_id[-3:])
    
    if list_type == "programs":
        success = self.operations.move_program_up(bank, index)
    else:
        success = self.operations.move_combi_up(bank, index)
    
    if success:
        self.pcg.is_dirty = True
        self.is_dirty = True
        self._update_display()
        self._update_title()

def _move_down(self, tree, list_type):
    """Move selected patch down."""
    selection = tree.selection()
    if not selection or len(selection) != 1:
        messagebox.showwarning("Selection", "Please select exactly one patch", parent=self.window)
        return
    
    values = tree.item(selection[0])['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    index = int(patch_id[-3:])
    
    if list_type == "programs":
        success = self.operations.move_program_down(bank, index)
    else:
        success = self.operations.move_combi_down(bank, index)
    
    if success:
        self.pcg.is_dirty = True
        self.is_dirty = True
        self._update_display()
        self._update_title()

def _sort_patches(self, tree, list_type):
    """Sort patches in bank."""
    # Get selected bank
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a bank or patch", parent=self.window)
        return
    
    values = tree.item(selection[0])['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    
    # Show sort dialog
    dialog = tk.Toplevel(self.window)
    dialog.title("Sort Patches")
    dialog.geometry("300x150")
    dialog.transient(self.window)
    dialog.grab_set()
    
    ttk.Label(dialog, text="Sort by:").pack(pady=10)
    
    sort_var = tk.StringVar(value="name")
    ttk.Radiobutton(dialog, text="Name", variable=sort_var, value="name").pack()
    ttk.Radiobutton(dialog, text="Category", variable=sort_var, value="category").pack()
    
    def do_sort():
        if sort_var.get() == "name":
            key = lambda p: p.name
        else:
            key = lambda p: (p.category.name if p.category else "")
        
        if list_type == "programs":
            self.operations.sort_programs(bank, key=key)
        else:
            self.operations.sort_combis(bank, key=key)
        
        self.pcg.is_dirty = True
        self.is_dirty = True
        self._update_display()
        self._update_title()
        dialog.destroy()
    
    ttk.Button(dialog, text="Sort", command=do_sort).pack(pady=10)

def _compact_patches(self, tree, list_type):
    """Compact patches (move empty to end)."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a bank or patch", parent=self.window)
        return
    
    values = tree.item(selection[0])['values']
    if not values:
        return
    
    patch_id = values[0]
    bank = patch_id[:-3]
    
    if not messagebox.askyesno("Confirm Compact", 
                               f"Compact bank {bank}? This will move empty patches to the end.", 
                               parent=self.window):
        return
    
    if list_type == "programs":
        self.operations.compact_programs(bank)
    else:
        self.operations.compact_combis(bank)
    
    self.pcg.is_dirty = True
    self.is_dirty = True
    self._update_display()
    self._update_title()
    messagebox.showinfo("Complete", f"Bank {bank} compacted", parent=self.window)

def _get_selected_patches(self, tree, list_type):
    """Get list of selected patches."""
    selection = tree.selection()
    if not selection:
        return []
    
    patches = []
    for item in selection:
        values = tree.item(item)['values']
        if not values:
            continue
        
        patch_id = values[0]
        bank = patch_id[:-3]
        index = int(patch_id[-3:])
        
        if list_type == "programs":
            patch = self.pcg.find_program(bank, index)
        else:
            patch = self.pcg.find_combi(bank, index)
        
        if patch:
            patches.append(patch)
    
    return patches
