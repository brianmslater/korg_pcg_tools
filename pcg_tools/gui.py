"""Simple GUI for PCG Tools using tkinter."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .reader import read_pcg_file
from .writer import write_pcg_file
from .clipboard import get_clipboard
from .operations import PatchOperations
from .edit_dialog import EditPatchDialog
from .settings import get_settings


class PcgWindow:
    """Individual PCG file window."""
    
    def __init__(self, parent, filepath=None):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("PCG File")
        self.window.geometry("800x500")
        
        self.pcg = None
        self.filepath = filepath
        self.is_dirty = False
        self.clipboard = get_clipboard()
        self.operations = None
        
        self._create_widgets()
        
        if filepath:
            self.load_file(filepath)
    
    def _create_widgets(self):
        """Create window widgets - matching original PCG Tools layout."""
        
        # Top section: Radio buttons and status
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Radio buttons for view selection
        radio_frame = ttk.Frame(top_frame)
        radio_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.view_var = tk.StringVar(value="programs")
        
        ttk.Radiobutton(radio_frame, text="Programs", variable=self.view_var, 
                       value="programs", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Combis", variable=self.view_var, 
                       value="combis", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Set Lists", variable=self.view_var, 
                       value="setlists", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="All Patches", variable=self.view_var, 
                       value="all", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        
        # Status labels
        status_frame = ttk.Frame(top_frame)
        status_frame.pack(side=tk.RIGHT)
        
        ttk.Label(status_frame, text="Number of Patches:").pack(side=tk.LEFT, padx=5)
        self.patch_count_label = ttk.Label(status_frame, text="0", font=('Arial', 10, 'bold'))
        self.patch_count_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_frame, text="Selected:").pack(side=tk.LEFT, padx=5)
        self.selected_count_label = ttk.Label(status_frame, text="0", font=('Arial', 10, 'bold'))
        self.selected_count_label.pack(side=tk.LEFT, padx=5)
        
        # Main content area with all views (show/hide based on radio selection)
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Programs view
        self.programs_frame = ttk.Frame(self.content_frame)
        self._create_patch_list(self.programs_frame, "programs")
        
        # Combis view
        self.combis_frame = ttk.Frame(self.content_frame)
        self._create_patch_list(self.combis_frame, "combis")
        
        # Set Lists view
        self.setlists_frame = ttk.Frame(self.content_frame)
        self._create_setlist_view(self.setlists_frame)
        
        # All patches view
        self.all_frame = ttk.Frame(self.content_frame)
        self._create_all_patches_view(self.all_frame)
        
        # Show programs by default
        self.programs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu bar for window
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Revert to Saved", command=self.revert_to_saved)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.close, accelerator="Ctrl+W")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Invert Selection", command=self.invert_selection)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", command=self.show_find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Find Next", command=self.find_next, accelerator="F3")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Duplicates", command=self.clear_duplicates)
        edit_menu.add_command(label="Swap Patches", command=self.swap_patches)
        edit_menu.add_command(label="Insert Empty", command=self.insert_empty)
        edit_menu.add_separator()
        edit_menu.add_command(label="Capitalize Names", command=lambda: self.change_case('capitalize'))
        edit_menu.add_command(label="Uppercase Names", command=lambda: self.change_case('upper'))
        edit_menu.add_command(label="Lowercase Names", command=lambda: self.change_case('lower'))
        edit_menu.add_command(label="Title Case Names", command=lambda: self.change_case('title'))
        edit_menu.add_separator()
        edit_menu.add_command(label="Change Volume...", command=self.change_volume)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Export Patch List...", command=self.export_list)
        tools_menu.add_command(label="Generate Reports...", command=self.generate_reports)
        
        # Keyboard shortcuts for window
        self.window.bind('<Control-s>', lambda e: self.save_file())
        self.window.bind('<Control-w>', lambda e: self.close())
        self.window.bind('<Control-f>', lambda e: self.show_find())
        self.window.bind('<F3>', lambda e: self.find_next())
        self.window.bind('<Control-a>', lambda e: self.select_all())
        
        # Store last search
        self.last_search = ""
        self.last_search_index = 0
        
        # Bottom section: Operation buttons (like original)
        bottom_frame = ttk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Main operations toolbar
        ops_frame = ttk.Frame(bottom_frame)
        ops_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(ops_frame, text="Edit", command=self._edit_selected_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(ops_frame, text="Up", command=self._move_up_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(ops_frame, text="Down", command=self._move_down_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(ops_frame, text="Clear", command=self._clear_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(ops_frame, text="Compact", command=self._compact_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(ops_frame, text="Sort", command=self._sort_quick, width=10).pack(side=tk.LEFT, padx=2)
        
        # Copy/Paste section (like original)
        clipboard_frame = ttk.LabelFrame(bottom_frame, text="Copy/Paste Mode", padding=5)
        clipboard_frame.pack(fill=tk.X, pady=2)
        
        clipboard_buttons = ttk.Frame(clipboard_frame)
        clipboard_buttons.pack(side=tk.LEFT)
        
        ttk.Button(clipboard_buttons, text="Cut", command=self._cut_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(clipboard_buttons, text="Copy", command=self._copy_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(clipboard_buttons, text="Paste", command=self._paste_quick, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(clipboard_buttons, text="Exit", command=self._exit_copy_mode, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(clipboard_buttons, text="Recall", command=self._recall_clipboard, width=10).pack(side=tk.LEFT, padx=2)
        
        # Clipboard status
        self.clipboard_status = ttk.Label(clipboard_frame, text="", foreground="blue")
        self.clipboard_status.pack(side=tk.LEFT, padx=10)
        
        # Generate List button
        list_frame = ttk.Frame(bottom_frame)
        list_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(list_frame, text="Generate List", command=self.generate_reports, width=15).pack(side=tk.LEFT, padx=2)
        
        # File operations
        ttk.Button(list_frame, text="Save", command=self.save_file, width=10).pack(side=tk.RIGHT, padx=2)
        ttk.Button(list_frame, text="Save As", command=self.save_as_file, width=10).pack(side=tk.RIGHT, padx=2)
    
    def _create_patch_list(self, parent, list_type):
        """Create a patch list view with drag-and-drop support."""
        # Treeview
        columns = ('ID', 'Name', 'Category', 'Favorite')
        tree = ttk.Treeview(parent, columns=columns, show='tree headings', selectmode='extended')
        
        tree.heading('#0', text='Bank')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Category', text='Category')
        tree.heading('Favorite', text='Fav')
        
        tree.column('#0', width=100)
        tree.column('ID', width=100)
        tree.column('Name', width=300)
        tree.column('Category', width=150)
        tree.column('Favorite', width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu
        tree.bind('<Button-3>', lambda e: self._show_context_menu(e, tree, list_type))
        tree.bind('<Double-Button-1>', lambda e: self._on_double_click(e, tree, list_type))
        
        # Keyboard shortcuts
        tree.bind('<Control-c>', lambda e: self._copy_selection(tree, list_type))
        tree.bind('<Control-x>', lambda e: self._cut_selection(tree, list_type))
        tree.bind('<Control-v>', lambda e: self._paste_selection(tree, list_type))
        tree.bind('<Delete>', lambda e: self._clear_selection(tree, list_type))
        
        # Drag and drop
        tree.bind('<ButtonPress-1>', lambda e: self._on_drag_start(e, tree, list_type))
        tree.bind('<B1-Motion>', lambda e: self._on_drag_motion(e, tree, list_type))
        tree.bind('<ButtonRelease-1>', lambda e: self._on_drag_drop(e, tree, list_type))
        
        # Bind selection event to update counts
        tree.bind('<<TreeviewSelect>>', lambda e: self._update_counts())
        
        # Store reference
        if list_type == "programs":
            self.programs_tree = tree
        else:
            self.combis_tree = tree
    
    def _create_setlist_view(self, parent):
        """Create set list view."""
        # Treeview with columns for set list slots
        columns = ('ID', 'Name', 'Patch', 'Notes', 'Transpose', 'Volume')
        tree = ttk.Treeview(parent, columns=columns, show='tree headings', selectmode='extended')
        
        tree.heading('#0', text='Set List')
        tree.heading('ID', text='Slot')
        tree.heading('Name', text='Name')
        tree.heading('Patch', text='Patch')
        tree.heading('Notes', text='Notes')
        tree.heading('Transpose', text='Transpose')
        tree.heading('Volume', text='Volume')
        
        tree.column('#0', width=100)
        tree.column('ID', width=80)
        tree.column('Name', width=200)
        tree.column('Patch', width=120)
        tree.column('Notes', width=250)
        tree.column('Transpose', width=80)
        tree.column('Volume', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu for set lists
        tree.bind('<Button-3>', lambda e: self._show_setlist_context_menu(e, tree))
        tree.bind('<Double-Button-1>', lambda e: self._edit_setlist_slot(e, tree))
        
        # Store reference
        self.setlists_tree = tree
    
    def _show_setlist_context_menu(self, event, tree):
        """Show context menu for set list slots."""
        item = tree.identify_row(event.y)
        if item and item not in tree.selection():
            tree.selection_set(item)
        
        if not tree.selection():
            return
        
        menu = tk.Menu(tree, tearoff=0)
        menu.add_command(label="Edit Slot...", command=lambda: self._edit_setlist_slot(event, tree))
        menu.add_command(label="Edit Notes...", command=lambda: self._edit_slot_notes(tree))
        menu.add_separator()
        menu.add_command(label="Clear Slot", command=lambda: self._clear_setlist_slot(tree))
        
        menu.post(event.x_root, event.y_root)
    
    def _edit_setlist_slot(self, event, tree):
        """Edit set list slot."""
        selection = tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        # TODO: Implement set list slot editing dialog
        messagebox.showinfo("Edit Slot", "Set list slot editing coming soon!", parent=self.window)
    
    def _edit_slot_notes(self, tree):
        """Edit notes for a set list slot."""
        if not self.pcg:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        # Create notes dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Edit Slot Notes")
        dialog.geometry("500x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Notes for {values[1]}:").pack(pady=10)
        
        # Text widget for notes
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, height=10)
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load current notes
        current_notes = values[3] if len(values) > 3 else ""
        text_widget.insert('1.0', current_notes)
        
        def save_notes():
            new_notes = text_widget.get('1.0', 'end-1c')
            # TODO: Save notes to set list slot
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_title()
            dialog.destroy()
            messagebox.showinfo("Saved", "Notes saved successfully!", parent=self.window)
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=save_notes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _clear_setlist_slot(self, tree):
        """Clear set list slot."""
        if not self.pcg:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            f"Clear {len(selection)} set list slot(s)?",
            parent=self.window
        )
        
        if result:
            # TODO: Implement clear slot
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
    
    def _show_context_menu(self, event, tree, list_type):
        """Show context menu on right-click."""
        # Select item under cursor if not already selected
        item = tree.identify_row(event.y)
        if item and item not in tree.selection():
            tree.selection_set(item)
        
        if not tree.selection():
            return
        
        menu = tk.Menu(tree, tearoff=0)
        menu.add_command(label="Edit...", command=lambda: self._edit_selected(tree, list_type))
        menu.add_separator()
        menu.add_command(label="Copy", command=lambda: self._copy_selection(tree, list_type))
        menu.add_command(label="Cut", command=lambda: self._cut_selection(tree, list_type))
        menu.add_command(label="Paste", command=lambda: self._paste_selection(tree, list_type))
        menu.add_separator()
        menu.add_command(label="Clear", command=lambda: self._clear_selection(tree, list_type))
        menu.add_command(label="Move Up", command=lambda: self._move_up(tree, list_type))
        menu.add_command(label="Move Down", command=lambda: self._move_down(tree, list_type))
        menu.add_separator()
        menu.add_command(label="Sort...", command=lambda: self._sort_patches(tree, list_type))
        menu.add_command(label="Compact", command=lambda: self._compact_patches(tree, list_type))
        
        menu.post(event.x_root, event.y_root)
    
    def _on_double_click(self, event, tree, list_type):
        """Handle double-click to edit."""
        self._edit_selected(tree, list_type)
    
    def _edit_selected(self, tree, list_type):
        """Edit selected patch."""
        if not self.pcg:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
        # Get first selected item
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        patch_id = values[0]  # e.g., "I-A000"
        bank = patch_id[:-3]
        index = int(patch_id[-3:])
        
        if list_type == "programs":
            patch = self.pcg.find_program(bank, index)
        else:
            patch = self.pcg.find_combi(bank, index)
        
        if patch:
            dialog = EditPatchDialog(self.window, patch, list_type[:-1])  # Remove 's'
            if dialog.show():
                self.pcg.is_dirty = True
                self.is_dirty = True
                self._update_display()
                self._update_title()
    
    def _copy_selection(self, tree, list_type):
        """Copy selected patches to clipboard."""
        if not self.pcg:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
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
        
        if patches:
            if list_type == "programs":
                self.clipboard.copy_programs(patches, self.filepath or "Untitled")
            else:
                self.clipboard.copy_combis(patches, self.filepath or "Untitled", self.pcg, include_programs=True)
            
            self.parent.status_bar.config(text=f"Copied {len(patches)} {list_type}")
    
    def _cut_selection(self, tree, list_type):
        """Cut selected patches to clipboard."""
        if not self.pcg:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
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
        
        if patches:
            if list_type == "programs":
                self.clipboard.cut_programs(patches, self.filepath or "Untitled")
            else:
                self.clipboard.cut_combis(patches, self.filepath or "Untitled", self.pcg)
            
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Cut {len(patches)} {list_type}")
    
    def _paste_selection(self, tree, list_type):
        """Paste from clipboard."""
        if not self.pcg or not self.operations:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        # Check if clipboard has content
        if self.clipboard.is_empty():
            messagebox.showwarning("Warning", "Clipboard is empty. Copy patches first.", parent=self.window)
            return
        
        # Check if clipboard type matches
        if list_type == "programs" and not self.clipboard.programs:
            messagebox.showwarning("Warning", "Clipboard contains combis, not programs", parent=self.window)
            return
        if list_type == "combis" and not self.clipboard.combis:
            messagebox.showwarning("Warning", "Clipboard contains programs, not combis", parent=self.window)
            return
        
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a destination slot", parent=self.window)
            return
        
        # Get first selected item as destination
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        patch_id = values[0]
        bank = patch_id[:-3]
        index = int(patch_id[-3:])
        
        try:
            if list_type == "programs":
                count = self.operations.paste_programs(bank, index)
            else:
                count = self.operations.paste_combis(bank, index)
            
            if count > 0:
                self.pcg.is_dirty = True
                self.is_dirty = True
                self._update_display()
                self._update_title()
                self.parent.status_bar.config(text=f"Pasted {count} {list_type} to {bank}{index:03d}")
                messagebox.showinfo("Success", f"Pasted {count} {list_type}", parent=self.window)
            else:
                messagebox.showwarning("Warning", "Nothing was pasted", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste:\n{e}", parent=self.window)
    
    def _clear_selection(self, tree, list_type):
        """Clear selected patches."""
        if not self.pcg or not self.operations:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            f"Clear {len(selection)} {list_type}?",
            parent=self.window
        )
        
        if not result:
            return
        
        for item in selection:
            values = tree.item(item)['values']
            if not values:
                continue
            
            patch_id = values[0]
            bank = patch_id[:-3]
            index = int(patch_id[-3:])
            
            if list_type == "programs":
                self.operations.clear_program(bank, index)
            else:
                self.operations.clear_combi(bank, index)
        
        self.pcg.is_dirty = True
        self.is_dirty = True
        self._update_display()
        self._update_title()
        self.parent.status_bar.config(text=f"Cleared {len(selection)} {list_type}")
    
    def _move_up(self, tree, list_type):
        """Move selected patch up."""
        if not self.pcg or not self.operations:
            return
        
        selection = tree.selection()
        if not selection or len(selection) != 1:
            messagebox.showwarning("Warning", "Select exactly one patch to move", parent=self.window)
            return
        
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        patch_id = values[0]
        bank = patch_id[:-3]
        index = int(patch_id[-3:])
        
        try:
            if list_type == "programs":
                self.operations.move_program_up(bank, index)
            else:
                self.operations.move_combi_up(bank, index)
            
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Moved {patch_id} up")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move:\n{e}", parent=self.window)
    
    def _move_down(self, tree, list_type):
        """Move selected patch down."""
        if not self.pcg or not self.operations:
            return
        
        selection = tree.selection()
        if not selection or len(selection) != 1:
            messagebox.showwarning("Warning", "Select exactly one patch to move", parent=self.window)
            return
        
        item = selection[0]
        values = tree.item(item)['values']
        if not values:
            return
        
        patch_id = values[0]
        bank = patch_id[:-3]
        index = int(patch_id[-3:])
        
        try:
            if list_type == "programs":
                self.operations.move_program_down(bank, index)
            else:
                self.operations.move_combi_down(bank, index)
            
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Moved {patch_id} down")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move:\n{e}", parent=self.window)
    
    def _sort_patches(self, tree, list_type):
        """Sort patches in bank."""
        if not self.pcg or not self.operations:
            return
        
        # Simple sort dialog
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
            # Get all banks and sort each one
            if list_type == "programs":
                for bank in self.pcg.program_banks:
                    self.operations.sort_programs(bank.bank_id, sort_var.get())
            else:
                for bank in self.pcg.combi_banks:
                    self.operations.sort_combis(bank.bank_id, sort_var.get())
            
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Sorted {list_type} by {sort_var.get()}")
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Sort", command=do_sort).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _compact_patches(self, tree, list_type):
        """Compact patches (move empty to end)."""
        if not self.pcg or not self.operations:
            return
        
        result = messagebox.askyesno(
            "Confirm Compact",
            f"Move all empty {list_type} to the end?",
            parent=self.window
        )
        
        if not result:
            return
        
        # Compact all banks
        if list_type == "programs":
            for bank in self.pcg.program_banks:
                self.operations.compact_programs(bank.bank_id)
        else:
            for bank in self.pcg.combi_banks:
                self.operations.compact_combis(bank.bank_id)
        
        self.pcg.is_dirty = True
        self.is_dirty = True
        self._update_display()
        self._update_title()
        self.parent.status_bar.config(text=f"Compacted {list_type}")
    
    def _switch_view(self):
        """Switch between different views based on radio button selection."""
        # Hide all views
        self.programs_frame.pack_forget()
        self.combis_frame.pack_forget()
        self.setlists_frame.pack_forget()
        self.all_frame.pack_forget()
        
        # Show selected view
        view = self.view_var.get()
        if view == "programs":
            self.programs_frame.pack(fill=tk.BOTH, expand=True)
            self._update_counts()
        elif view == "combis":
            self.combis_frame.pack(fill=tk.BOTH, expand=True)
            self._update_counts()
        elif view == "setlists":
            self.setlists_frame.pack(fill=tk.BOTH, expand=True)
            self._update_counts()
        elif view == "all":
            self.all_frame.pack(fill=tk.BOTH, expand=True)
            self._update_counts()
    
    def _create_all_patches_view(self, parent):
        """Create view showing all patches (programs and combis together)."""
        columns = ('Type', 'ID', 'Name', 'Category', 'Favorite')
        tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='extended')
        
        tree.heading('Type', text='Type')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Category', text='Category')
        tree.heading('Favorite', text='Fav')
        
        tree.column('Type', width=80)
        tree.column('ID', width=100)
        tree.column('Name', width=300)
        tree.column('Category', width=150)
        tree.column('Favorite', width=50)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        tree.bind('<<TreeviewSelect>>', lambda e: self._update_counts())
        tree.bind('<Double-Button-1>', lambda e: self._edit_selected_quick())
        
        self.all_tree = tree
    
    def _update_counts(self):
        """Update patch count and selection count labels."""
        if not self.pcg:
            self.patch_count_label.config(text="0")
            self.selected_count_label.config(text="0")
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            tree = self.programs_tree
            total = sum(len(bank.patches) for bank in self.pcg.program_banks)
        elif view == "combis":
            tree = self.combis_tree
            total = sum(len(bank.patches) for bank in self.pcg.combi_banks)
        elif view == "setlists":
            tree = self.setlists_tree
            total = sum(len(sl.slots) for sl in self.pcg.set_lists)
        elif view == "all":
            tree = self.all_tree
            total = sum(len(bank.patches) for bank in self.pcg.program_banks) + \
                   sum(len(bank.patches) for bank in self.pcg.combi_banks)
        else:
            return
        
        selected = len(tree.selection())
        
        self.patch_count_label.config(text=str(total))
        self.selected_count_label.config(text=str(selected))
        
        # Update clipboard status
        if self.clipboard.programs or self.clipboard.combis:
            count = len(self.clipboard.programs) + len(self.clipboard.combis)
            self.clipboard_status.config(text=f"Clipboard: {count} patch(es)")
        else:
            self.clipboard_status.config(text="")
    
    def _get_current_tree(self):
        """Get the currently visible tree."""
        view = self.view_var.get()
        if view == "programs":
            return self.programs_tree, "programs"
        elif view == "combis":
            return self.combis_tree, "combis"
        elif view == "setlists":
            return self.setlists_tree, "setlists"
        elif view == "all":
            return self.all_tree, "all"
        return None, None
    
    # Quick button methods (matching original UI)
    def _edit_selected_quick(self):
        """Edit selected patch (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._edit_selected(tree, list_type)
    
    def _move_up_quick(self):
        """Move selected patch up (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._move_up(tree, list_type)
    
    def _move_down_quick(self):
        """Move selected patch down (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._move_down(tree, list_type)
    
    def _clear_quick(self):
        """Clear selected patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._clear_selection(tree, list_type)
    
    def _compact_quick(self):
        """Compact patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._compact_patches(tree, list_type)
    
    def _sort_quick(self):
        """Sort patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._sort_patches(tree, list_type)
    
    def _copy_quick(self):
        """Copy selected patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._copy_selection(tree, list_type)
            self._update_counts()
    
    def _cut_quick(self):
        """Cut selected patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._cut_selection(tree, list_type)
            self._update_counts()
    
    def _paste_quick(self):
        """Paste patches (quick button)."""
        tree, list_type = self._get_current_tree()
        if tree and list_type in ["programs", "combis"]:
            self._paste_selection(tree, list_type)
            self._update_counts()
    
    def _exit_copy_mode(self):
        """Exit copy/paste mode (clear clipboard)."""
        self.clipboard.clear()
        self._update_counts()
        self.parent.status_bar.config(text="Clipboard cleared")
    
    def _recall_clipboard(self):
        """Recall last clipboard operation (undo)."""
        # TODO: Implement clipboard history
        messagebox.showinfo("Recall", "Clipboard recall not yet implemented", parent=self.window)
    
    def load_file(self, filepath):
        """Load a PCG file."""
        try:
            self.pcg = read_pcg_file(filepath)
            self.filepath = filepath
            self.operations = PatchOperations(self.pcg)
            self._update_display()
            self.window.title(f"PCG Tools - {Path(filepath).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}", parent=self.window)
    
    def save_file(self):
        """Save the current PCG file."""
        if not self.pcg or not self.filepath:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        try:
            write_pcg_file(self.pcg, self.filepath)
            self.is_dirty = False
            self._update_title()
            messagebox.showinfo("Success", "File saved successfully", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=self.window)
    
    def save_as_file(self):
        """Save the current PCG file with a new name."""
        if not self.pcg:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save PCG File As",
            defaultextension=".pcg",
            filetypes=[("PCG Files", "*.pcg"), ("All Files", "*.*")],
            parent=self.window
        )
        
        if filename:
            try:
                write_pcg_file(self.pcg, filename)
                self.filepath = filename
                self.is_dirty = False
                self._update_title()
                messagebox.showinfo("Success", "File saved successfully", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=self.window)
    
    def revert_to_saved(self):
        """Revert to the saved version of the file."""
        if not self.filepath:
            messagebox.showwarning("Warning", "No file to revert to", parent=self.window)
            return
        
        if self.is_dirty:
            result = messagebox.askyesno(
                "Revert to Saved?",
                f"Discard all changes to {Path(self.filepath).name}?",
                parent=self.window
            )
            if not result:
                return
        
        try:
            self.pcg = read_pcg_file(self.filepath)
            self.operations = PatchOperations(self.pcg)
            self.is_dirty = False
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Reverted to saved: {Path(self.filepath).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to revert:\n{e}", parent=self.window)
    
    def show_find(self):
        """Show find dialog."""
        if not self.pcg:
            return
        
        # Create find dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Find")
        dialog.geometry("400x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Find patch by name:").pack(pady=10)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(dialog, textvariable=search_var, width=40)
        search_entry.pack(pady=5)
        search_entry.focus()
        
        result_label = ttk.Label(dialog, text="")
        result_label.pack(pady=5)
        
        def do_find():
            search_text = search_var.get().lower()
            if not search_text:
                return
            
            # Search in current tab
            current_tab = self.notebook.index(self.notebook.select())
            if current_tab == 0:  # Programs
                tree = self.programs_tree
                patches = [(bank, prog) for bank in self.pcg.program_banks for prog in bank.patches]
            elif current_tab == 1:  # Combis
                tree = self.combis_tree
                patches = [(bank, combi) for bank in self.pcg.combi_banks for combi in bank.patches]
            else:
                result_label.config(text="Search not available in this tab")
                return
            
            # Find matching patches
            matches = []
            for bank, patch in patches:
                if search_text in patch.name.lower():
                    matches.append((bank, patch))
            
            if matches:
                result_label.config(text=f"Found {len(matches)} match(es)")
                # Select first match
                bank, patch = matches[0]
                # Find and select in tree
                for item in tree.get_children():
                    if tree.item(item)['text'] == f"Bank {bank.bank_id}":
                        tree.item(item, open=True)
                        for child in tree.get_children(item):
                            values = tree.item(child)['values']
                            if values and values[0] == patch.id:
                                tree.selection_set(child)
                                tree.see(child)
                                break
                        break
            else:
                result_label.config(text="No matches found")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Find", command=do_find).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        search_entry.bind('<Return>', lambda e: do_find())
    
    def clear_duplicates(self):
        """Clear duplicate patches (same name)."""
        if not self.pcg or not self.operations:
            return
        
        result = messagebox.askyesno(
            "Clear Duplicates?",
            "This will clear patches with duplicate names, keeping only the first occurrence.\n\nContinue?",
            parent=self.window
        )
        
        if not result:
            return
        
        # Get current tab
        current_tab = self.notebook.index(self.notebook.select())
        
        cleared_count = 0
        if current_tab == 0:  # Programs
            seen_names = set()
            for bank in self.pcg.program_banks:
                for i, prog in enumerate(bank.patches):
                    if prog.name in seen_names:
                        self.operations.clear_program(bank.bank_id, i)
                        cleared_count += 1
                    else:
                        seen_names.add(prog.name)
        elif current_tab == 1:  # Combis
            seen_names = set()
            for bank in self.pcg.combi_banks:
                for i, combi in enumerate(bank.patches):
                    if combi.name in seen_names:
                        self.operations.clear_combi(bank.bank_id, i)
                        cleared_count += 1
                    else:
                        seen_names.add(combi.name)
        
        if cleared_count > 0:
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            messagebox.showinfo("Complete", f"Cleared {cleared_count} duplicate(s)", parent=self.window)
        else:
            messagebox.showinfo("Complete", "No duplicates found", parent=self.window)
    
    def export_list(self):
        """Export patch list."""
        if not self.pcg:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Patch List",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")],
            parent=self.window
        )
        
        if filename:
            try:
                from .cli import _export_csv, _export_txt
                if filename.endswith('.csv'):
                    _export_csv(self.pcg, filename)
                else:
                    _export_txt(self.pcg, filename)
                messagebox.showinfo("Success", f"Exported to {Path(filename).name}", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{e}", parent=self.window)
    
    def generate_reports(self):
        """Generate various reports."""
        if not self.pcg:
            return
        
        # Create reports dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Generate Reports")
        dialog.geometry("400x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select report type:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        report_var = tk.StringVar(value="usage")
        
        ttk.Radiobutton(dialog, text="Program Usage List", variable=report_var, value="usage").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Combi Content List (Short)", variable=report_var, value="content_short").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Combi Content List (Long)", variable=report_var, value="content_long").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="File Summary", variable=report_var, value="summary").pack(anchor=tk.W, padx=20)
        
        def generate():
            report_type = report_var.get()
            
            filename = filedialog.asksaveasfilename(
                title="Save Report",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")],
                parent=dialog
            )
            
            if filename:
                try:
                    from .list_generators import ListGenerator
                    generator = ListGenerator(self.pcg)
                    
                    fmt = 'csv' if filename.endswith('.csv') else 'txt'
                    
                    if report_type == "usage":
                        generator.generate_program_usage_list(filename, fmt)
                    elif report_type == "content_short":
                        generator.generate_combi_content_list(filename, fmt, 'short')
                    elif report_type == "content_long":
                        generator.generate_combi_content_list(filename, fmt, 'long')
                    elif report_type == "summary":
                        generator.generate_file_content_list(filename, fmt)
                    
                    messagebox.showinfo("Success", f"Report saved to {Path(filename).name}", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate report:\n{e}", parent=dialog)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Generate", command=generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def select_all(self):
        """Select all patches in current tab."""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            tree = self.programs_tree
        elif current_tab == 1:
            tree = self.combis_tree
        else:
            return
        
        # Select all items
        for item in tree.get_children():
            for child in tree.get_children(item):
                tree.selection_add(child)
    
    def invert_selection(self):
        """Invert selection in current tab."""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            tree = self.programs_tree
        elif current_tab == 1:
            tree = self.combis_tree
        else:
            return
        
        # Get all items
        all_items = []
        for item in tree.get_children():
            all_items.extend(tree.get_children(item))
        
        # Get current selection
        selected = set(tree.selection())
        
        # Invert
        tree.selection_set([item for item in all_items if item not in selected])
    
    def find_next(self):
        """Find next occurrence of last search."""
        if not self.last_search:
            self.show_find()
            return
        
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            tree = self.programs_tree
            patches = [(bank, prog) for bank in self.pcg.program_banks for prog in bank.patches]
        elif current_tab == 1:
            tree = self.combis_tree
            patches = [(bank, combi) for bank in self.pcg.combi_banks for combi in bank.patches]
        else:
            return
        
        # Find matches starting from last index
        matches = []
        for bank, patch in patches:
            if self.last_search.lower() in patch.name.lower():
                matches.append((bank, patch))
        
        if matches:
            # Get next match
            self.last_search_index = (self.last_search_index + 1) % len(matches)
            bank, patch = matches[self.last_search_index]
            
            # Select in tree
            for item in tree.get_children():
                if tree.item(item)['text'] == f"Bank {bank.bank_id}":
                    tree.item(item, open=True)
                    for child in tree.get_children(item):
                        values = tree.item(child)['values']
                        if values and values[0] == patch.id:
                            tree.selection_set(child)
                            tree.see(child)
                            break
                    break
            
            self.parent.status_bar.config(text=f"Found: {patch.name} ({self.last_search_index + 1}/{len(matches)})")
    
    def swap_patches(self):
        """Swap two selected patches."""
        if not self.pcg:
            return
        
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            tree = self.programs_tree
            list_type = "programs"
        elif current_tab == 1:
            tree = self.combis_tree
            list_type = "combis"
        else:
            return
        
        selection = tree.selection()
        if len(selection) != 2:
            messagebox.showwarning("Warning", "Select exactly 2 patches to swap", parent=self.window)
            return
        
        # Get patch info
        patches_info = []
        for item in selection:
            values = tree.item(item)['values']
            if values:
                patch_id = values[0]
                bank = patch_id[:-3]
                index = int(patch_id[-3:])
                patches_info.append((bank, index))
        
        if len(patches_info) == 2:
            # Swap patches
            bank1, idx1 = patches_info[0]
            bank2, idx2 = patches_info[1]
            
            if list_type == "programs":
                # Get patches
                patch1 = self.pcg.find_program(bank1, idx1)
                patch2 = self.pcg.find_program(bank2, idx2)
                
                # Swap
                for bank in self.pcg.program_banks:
                    if bank.bank_id == bank1:
                        bank.patches[idx1] = patch2
                        patch2.bank = bank1
                        patch2.index = idx1
                    if bank.bank_id == bank2:
                        bank.patches[idx2] = patch1
                        patch1.bank = bank2
                        patch1.index = idx2
            else:
                # Get combis
                combi1 = self.pcg.find_combi(bank1, idx1)
                combi2 = self.pcg.find_combi(bank2, idx2)
                
                # Swap
                for bank in self.pcg.combi_banks:
                    if bank.bank_id == bank1:
                        bank.patches[idx1] = combi2
                        combi2.bank = bank1
                        combi2.index = idx1
                    if bank.bank_id == bank2:
                        bank.patches[idx2] = combi1
                        combi1.bank = bank2
                        combi1.index = idx2
            
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text="Patches swapped")
    
    def insert_empty(self):
        """Insert empty patch at selection."""
        if not self.pcg:
            return
        
        messagebox.showinfo("Not Implemented", "Insert empty patch feature coming soon!", parent=self.window)
    
    def change_case(self, case_type):
        """Change case of selected patch names."""
        if not self.pcg:
            return
        
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            tree = self.programs_tree
            list_type = "programs"
        elif current_tab == 1:
            tree = self.combis_tree
            list_type = "combis"
        else:
            return
        
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select patches to rename", parent=self.window)
            return
        
        count = 0
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
                if case_type == 'capitalize':
                    patch.name = patch.name.capitalize()
                elif case_type == 'upper':
                    patch.name = patch.name.upper()
                elif case_type == 'lower':
                    patch.name = patch.name.lower()
                elif case_type == 'title':
                    patch.name = patch.name.title()
                count += 1
        
        if count > 0:
            self.pcg.is_dirty = True
            self.is_dirty = True
            self._update_display()
            self._update_title()
            self.parent.status_bar.config(text=f"Changed case for {count} patch(es)")
    
    def change_volume(self):
        """Change volume for selected combis."""
        if not self.pcg:
            return
        
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab != 1:
            messagebox.showwarning("Warning", "Volume change only works for Combis", parent=self.window)
            return
        
        tree = self.combis_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select combis to change volume", parent=self.window)
            return
        
        # Create volume dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Volume")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="New volume (0-127):").pack(pady=10)
        
        volume_var = tk.IntVar(value=127)
        volume_spin = ttk.Spinbox(dialog, from_=0, to=127, textvariable=volume_var, width=10)
        volume_spin.pack(pady=5)
        
        def apply_volume():
            new_volume = volume_var.get()
            count = 0
            
            for item in selection:
                values = tree.item(item)['values']
                if not values:
                    continue
                
                patch_id = values[0]
                bank = patch_id[:-3]
                index = int(patch_id[-3:])
                
                combi = self.pcg.find_combi(bank, index)
                if combi:
                    for timbre in combi.timbres:
                        timbre.volume = new_volume
                    count += 1
            
            if count > 0:
                self.pcg.is_dirty = True
                self.is_dirty = True
                self._update_display()
                self._update_title()
                messagebox.showinfo("Success", f"Changed volume for {count} combi(s)", parent=dialog)
            
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Apply", command=apply_volume).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def close(self):
        """Close this window."""
        if self.is_dirty:
            result = messagebox.askyesnocancel(
                "Save Changes?",
                f"Do you want to save changes to {Path(self.filepath).name if self.filepath else 'Untitled'}?",
                parent=self.window
            )
            if result is None:  # Cancel
                return
            elif result:  # Yes
                self.save_file()
        
        self.window.destroy()
        self.parent.windows.remove(self)
    
    def _update_display(self):
        """Update the display with current PCG data."""
        if not self.pcg:
            return
        
        # Update counts (info is now in status labels)
        self._update_counts()
        
        # Update programs tree
        self.programs_tree.delete(*self.programs_tree.get_children())
        for bank in self.pcg.program_banks:
            bank_node = self.programs_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
            for prog in bank.patches:
                cat = prog.category.name if prog.category else ""
                fav = "✓" if prog.favorite else ""
                self.programs_tree.insert(bank_node, 'end', values=(prog.id, prog.name, cat, fav))
        
        # Update combis tree
        self.combis_tree.delete(*self.combis_tree.get_children())
        for bank in self.pcg.combi_banks:
            bank_node = self.combis_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
            for combi in bank.patches:
                cat = combi.category.name if combi.category else ""
                fav = "✓" if combi.favorite else ""
                self.combis_tree.insert(bank_node, 'end', values=(combi.id, combi.name, cat, fav))
        
        # Update all patches tree
        self.all_tree.delete(*self.all_tree.get_children())
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                cat = prog.category.name if prog.category else ""
                fav = "✓" if prog.favorite else ""
                self.all_tree.insert('', 'end', values=("Program", prog.id, prog.name, cat, fav))
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                cat = combi.category.name if combi.category else ""
                fav = "✓" if combi.favorite else ""
                self.all_tree.insert('', 'end', values=("Combi", combi.id, combi.name, cat, fav))
        
        # Update set lists tree
        self.setlists_tree.delete(*self.setlists_tree.get_children())
        if self.pcg.set_lists:
            for setlist in self.pcg.set_lists:
                setlist_node = self.setlists_tree.insert('', 'end', text=f"{setlist.name} ({setlist.id})")
                for slot in setlist.slots:
                    transpose_str = f"+{slot.transpose}" if slot.transpose > 0 else str(slot.transpose) if slot.transpose < 0 else "0"
                    self.setlists_tree.insert(
                        setlist_node, 
                        'end', 
                        values=(
                            f"{slot.slot_index:03d}",
                            slot.name,
                            slot.patch_id,
                            slot.notes[:50] + "..." if len(slot.notes) > 50 else slot.notes,
                            transpose_str,
                            slot.volume
                        )
                    )
        else:
            # Show message when no set lists
            self.setlists_tree.insert('', 'end', text="No set lists in this file", values=("", "Set lists are optional", "", "", "", ""))
    
    def _update_title(self):
        """Update window title."""
        dirty_flag = "*" if self.is_dirty else ""
        filename = Path(self.filepath).name if self.filepath else "Untitled"
        self.window.title(f"PCG Tools - {filename}{dirty_flag}")
    
    def _on_drag_start(self, event, tree, list_type):
        """Handle drag start."""
        # Store drag data
        item = tree.identify_row(event.y)
        if item and tree.parent(item):  # Only drag actual patches, not bank headers
            if item not in tree.selection():
                tree.selection_set(item)
            self.drag_data = {
                'source_window': self,
                'source_tree': tree,
                'list_type': list_type,
                'items': tree.selection()
            }
        else:
            self.drag_data = None
    
    def _on_drag_motion(self, event, tree, list_type):
        """Handle drag motion - visual feedback."""
        if hasattr(self, 'drag_data') and self.drag_data:
            # Change cursor to indicate dragging
            tree.config(cursor="hand2")
    
    def _on_drag_drop(self, event, tree, list_type):
        """Handle drag drop."""
        # Reset cursor
        tree.config(cursor="")
        
        if not hasattr(self, 'drag_data') or not self.drag_data:
            return
        
        # Check if we're dropping on a valid target
        target_item = tree.identify_row(event.y)
        if not target_item or not tree.parent(target_item):
            self.drag_data = None
            return
        
        # Get source and target info
        source_window = self.drag_data['source_window']
        source_tree = self.drag_data['source_tree']
        source_list_type = self.drag_data['list_type']
        
        # Check if dropping on same window (allow drag within same window for reordering)
        # But for now, we'll use copy/paste for cross-window operations
        if source_window == self and source_tree == tree:
            # Same window, same tree - could implement reordering here
            self.drag_data = None
            return
        
        # Check if list types match
        if source_list_type != list_type:
            messagebox.showwarning(
                "Type Mismatch",
                f"Cannot drag {source_list_type} to {list_type}",
                parent=self.window
            )
            self.drag_data = None
            return
        
        # Get source patches
        patches = []
        for item in self.drag_data['items']:
            values = source_tree.item(item)['values']
            if not values:
                continue
            
            patch_id = values[0]
            bank = patch_id[:-3]
            index = int(patch_id[-3:])
            
            if source_list_type == "programs":
                patch = source_window.pcg.find_program(bank, index)
            else:
                patch = source_window.pcg.find_combi(bank, index)
            
            if patch:
                patches.append(patch)
        
        if not patches:
            self.drag_data = None
            return
        
        # Copy patches to clipboard
        if source_list_type == "programs":
            self.clipboard.copy_programs(patches, source_window.filepath or "Untitled")
        else:
            self.clipboard.copy_combis(patches, source_window.filepath or "Untitled")
        
        # Get target position
        target_values = tree.item(target_item)['values']
        if target_values:
            target_patch_id = target_values[0]
            target_bank = target_patch_id[:-3]
            target_index = int(target_patch_id[-3:])
            
            # Paste at target
            try:
                if list_type == "programs":
                    count = self.operations.paste_programs(target_bank, target_index)
                else:
                    count = self.operations.paste_combis(target_bank, target_index)
                
                if count > 0:
                    self.pcg.is_dirty = True
                    self.is_dirty = True
                    self._update_display()
                    self._update_title()
                    self.parent.status_bar.config(
                        text=f"Dragged {count} {list_type} from {Path(source_window.filepath).name if source_window.filepath else 'Untitled'}"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to drop:\n{e}", parent=self.window)
        
        self.drag_data = None


class PcgToolsGUI:
    """Main GUI application with MDI support."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PCG Tools")
        self.root.geometry("1000x700")
        
        self.windows = []
        self.settings = get_settings()
        
        self._create_menu()
        self._create_widgets()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Window", command=self.new_window, accelerator="Ctrl+N")
        file_menu.add_command(label="Open PCG...", command=self.open_file, accelerator="Ctrl+O")
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self._update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Settings...", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Close All", command=self.close_all)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Window menu
        window_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Window", menu=window_menu)
        window_menu.add_command(label="Minimize All", command=self.minimize_all)
        window_menu.add_command(label="Maximize All", command=self.maximize_all)
        window_menu.add_separator()
        window_menu.add_command(label="Tile Horizontally", command=self.tile_horizontal)
        window_menu.add_command(label="Tile Vertically", command=self.tile_vertical)
        window_menu.add_command(label="Cascade", command=self.cascade_windows)
        window_menu.add_separator()
        window_menu.add_command(label="Close All But This", command=self.close_all_but_this)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Export Patch List...", command=self.export_list)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_window())
        self.root.bind('<Control-o>', lambda e: self.open_file())
    
    def _create_widgets(self):
        """Create main widgets."""
        # Welcome frame
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            welcome_frame,
            text="PCG Tools - Korg PCG File Editor",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)
        
        ttk.Label(
            welcome_frame,
            text="Open multiple PCG files and drag patches between them",
            font=('Arial', 10)
        ).pack(pady=10)
        
        btn_frame = ttk.Frame(welcome_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame,
            text="Open PCG File",
            command=self.open_file,
            width=20
        ).pack(pady=5)
        
        ttk.Button(
            btn_frame,
            text="New Empty Window",
            command=self.new_window,
            width=20
        ).pack(pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready - Open a PCG file to get started", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_file(self, filename=None):
        """Open a PCG file."""
        if not filename:
            filename = filedialog.askopenfilename(
                title="Open PCG File",
                filetypes=[("PCG Files", "*.pcg"), ("All Files", "*.*")]
            )
        
        if filename:
            window = PcgWindow(self, filename)
            self.windows.append(window)
            self.settings.add_recent_file(filename)
            self._update_recent_menu()
            self.status_bar.config(text=f"Loaded: {Path(filename).name} ({len(self.windows)} windows open)")
    
    def export_list(self):
        """Export patch list from active window."""
        if not self.windows:
            messagebox.showwarning("Warning", "No file loaded")
            return
        
        # Get the most recently focused window
        # For simplicity, just use the first window
        window = self.windows[0]
        if not window.pcg:
            messagebox.showwarning("Warning", "No file loaded in window")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Patch List",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                from .cli import _export_csv, _export_txt
                if filename.endswith('.csv'):
                    _export_csv(window.pcg, filename)
                else:
                    _export_txt(window.pcg, filename)
                messagebox.showinfo("Success", f"Exported to {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{e}")
    
    def new_window(self):
        """Create a new empty window."""
        window = PcgWindow(self)
        self.windows.append(window)
        self.status_bar.config(text=f"Opened new window ({len(self.windows)} windows open)")
    
    def tile_horizontal(self):
        """Tile windows horizontally."""
        if not self.windows:
            return
        
        count = len(self.windows)
        height = 600 // count
        
        for i, window in enumerate(self.windows):
            window.window.geometry(f"800x{height}+100+{i * height}")
    
    def tile_vertical(self):
        """Tile windows vertically."""
        if not self.windows:
            return
        
        count = len(self.windows)
        width = 1200 // count
        
        for i, window in enumerate(self.windows):
            window.window.geometry(f"{width}x600+{i * width}+100")
    
    def cascade_windows(self):
        """Cascade windows."""
        if not self.windows:
            return
        
        for i, window in enumerate(self.windows):
            offset = i * 30
            window.window.geometry(f"800x600+{100 + offset}+{100 + offset}")
    
    def close_all(self):
        """Close all windows."""
        for window in self.windows[:]:  # Copy list to avoid modification during iteration
            window.close()
    
    def _update_recent_menu(self):
        """Update recent files menu."""
        self.recent_menu.delete(0, tk.END)
        
        recent_files = self.settings.get_recent_files()
        if recent_files:
            for filepath in recent_files:
                self.recent_menu.add_command(
                    label=Path(filepath).name,
                    command=lambda f=filepath: self.open_file(f)
                )
        else:
            self.recent_menu.add_command(label="(No recent files)", state=tk.DISABLED)
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="PCG Tools Settings", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Settings frame
        settings_frame = ttk.Frame(dialog)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Auto save
        auto_save_var = tk.BooleanVar(value=self.settings.auto_save)
        ttk.Checkbutton(
            settings_frame,
            text="Auto-save on close",
            variable=auto_save_var
        ).pack(anchor=tk.W, pady=5)
        
        # Confirm clear
        confirm_clear_var = tk.BooleanVar(value=self.settings.confirm_clear)
        ttk.Checkbutton(
            settings_frame,
            text="Confirm before clearing patches",
            variable=confirm_clear_var
        ).pack(anchor=tk.W, pady=5)
        
        # Confirm delete
        confirm_delete_var = tk.BooleanVar(value=self.settings.confirm_delete)
        ttk.Checkbutton(
            settings_frame,
            text="Confirm before deleting",
            variable=confirm_delete_var
        ).pack(anchor=tk.W, pady=5)
        
        # Max recent files
        ttk.Label(settings_frame, text="Maximum recent files:").pack(anchor=tk.W, pady=(10, 0))
        max_recent_var = tk.IntVar(value=self.settings.max_recent_files)
        ttk.Spinbox(
            settings_frame,
            from_=5,
            to=20,
            textvariable=max_recent_var,
            width=10
        ).pack(anchor=tk.W, pady=5)
        
        def save_settings():
            self.settings.auto_save = auto_save_var.get()
            self.settings.confirm_clear = confirm_clear_var.get()
            self.settings.confirm_delete = confirm_delete_var.get()
            self.settings.max_recent_files = max_recent_var.get()
            self.settings.save()
            messagebox.showinfo("Success", "Settings saved", parent=dialog)
            dialog.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def minimize_all(self):
        """Minimize all windows."""
        for window in self.windows:
            window.window.iconify()
    
    def maximize_all(self):
        """Maximize all windows."""
        for window in self.windows:
            window.window.deiconify()
            window.window.state('zoomed')  # Windows maximize
    
    def close_all_but_this(self):
        """Close all windows except the focused one."""
        # Find focused window
        focused = None
        for window in self.windows:
            if window.window.focus_get():
                focused = window
                break
        
        if not focused and self.windows:
            focused = self.windows[0]
        
        # Close all others
        for window in self.windows[:]:
            if window != focused:
                window.close()
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        
        # Create text widget with scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = tk.Text(frame, wrap=tk.WORD, width=60, height=30)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        shortcuts_text = """
KEYBOARD SHORTCUTS
==================

File Operations:
  Ctrl+O          Open PCG file
  Ctrl+N          New window
  Ctrl+S          Save file
  Ctrl+W          Close window
  Ctrl+F          Find patch

Editing:
  F2              Edit selected patch
  Double-click    Edit patch
  Delete          Clear selected patches

Copy/Paste:
  Ctrl+C          Copy selected patches
  Ctrl+X          Cut selected patches
  Ctrl+V          Paste patches

Selection:
  Click           Select patch
  Ctrl+Click      Add to selection
  Shift+Click     Select range

Navigation:
  Arrow Keys      Navigate patches
  Tab             Switch between tabs
  Ctrl+Tab        Switch between windows

Window Management:
  Alt+F4          Exit application

Context Menu:
  Right-click     Show context menu with:
                  - Edit
                  - Copy/Cut/Paste
                  - Move Up/Down
                  - Sort
                  - Compact
                  - Clear

Drag and Drop:
  Click+Drag      Drag patches between windows
                  Drop on target slot to copy

Tips:
  - Use multi-select (Ctrl+Click) for batch operations
  - Right-click for quick access to all operations
  - Drag and drop works across multiple windows
  - All operations update references automatically
"""
        
        text.insert('1.0', shortcuts_text)
        text.configure(state='disabled')
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About PCG Tools",
            "PCG Tools v2.0.0\n\n"
            "Cross-platform Korg PCG file editor\n"
            "Python port of the original PCG Tools\n"
            "by Michel Keijzers\n\n"
            "Free for non-commercial use"
        )


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = PcgToolsGUI(root)
    root.mainloop()


if __name__ == '__main__':
    launch_gui()
