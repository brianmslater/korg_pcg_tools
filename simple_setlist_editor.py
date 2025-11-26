#!/usr/bin/env python3
"""
Simple Setlist Editor
A clean, reliable GUI for editing PCG setlists and slots.
Uses the working writer code directly - no extra modifications.
Hardware tested and confirmed working on Korg Kronos.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import SLOT_COLOR_VALUES, SlotTextSize

# Configuration file location
CONFIG_FILE = Path.home() / '.pcg_tools_simple_editor.json'
MAX_RECENT_FILES = 10

class SimpleSetlistEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Setlist Editor")
        
        self.pcg = None
        self.current_file = None
        self.current_setlist = None
        self.modified = False
        self.recent_files = []
        
        # Load configuration
        self.load_config()
        
        # Set window geometry from config or default
        geometry = self.config.get('window_geometry', '900x700')
        self.root.geometry(geometry)
        
        self.setup_ui()
        self.setup_menu()
        self.setup_keyboard_shortcuts()
        
        # Track window position changes
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        """Load configuration from file."""
        self.config = {}
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
                self.recent_files = self.config.get('recent_files', [])
            except Exception:
                pass
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Get current window geometry
            self.config['window_geometry'] = self.root.geometry()
            self.config['recent_files'] = self.recent_files[:MAX_RECENT_FILES]
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def add_recent_file(self, filepath):
        """Add a file to the recent files list."""
        filepath_str = str(filepath)
        if filepath_str in self.recent_files:
            self.recent_files.remove(filepath_str)
        self.recent_files.insert(0, filepath_str)
        self.recent_files = self.recent_files[:MAX_RECENT_FILES]
        self.update_recent_files_menu()
    
    def setup_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.browse_file, accelerator="Ctrl+O")
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self.update_recent_files_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def update_recent_files_menu(self):
        """Update the recent files menu."""
        self.recent_menu.delete(0, tk.END)
        
        if not self.recent_files:
            self.recent_menu.add_command(label="(No recent files)", state='disabled')
            return
        
        for filepath in self.recent_files:
            path = Path(filepath)
            if path.exists():
                self.recent_menu.add_command(
                    label=path.name,
                    command=lambda f=filepath: self.load_file(f)
                )
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-o>', lambda e: self.browse_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Simple Setlist Editor",
            "Simple Setlist Editor v1.1\n\n"
            "A clean, reliable GUI for editing PCG setlists.\n"
            "Hardware tested on Korg Kronos.\n\n"
            "Features:\n"
            "• Edit setlist and slot names\n"
            "• Change colors and text sizes\n"
            "• Adjust transpose and volume\n"
            "• Add notes to slots\n"
            "• Recent files list\n"
            "• Window position memory\n\n"
            "Part of PCG Tools Python\n"
            "https://github.com/yourusername/pcg-tools"
        )
    
    def setup_context_menu(self):
        """Setup context menu for slots."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Slot", command=self.edit_slot)
        self.context_menu.add_command(label="Clear Slot", command=self.clear_slot)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy Slot Name", command=self.copy_slot_name)
        
        self.slots_tree.bind('<Button-3>', self.show_context_menu)  # Right-click
        if self.root.tk.call('tk', 'windowingsystem') == 'aqua':  # macOS
            self.slots_tree.bind('<Button-2>', self.show_context_menu)
            self.slots_tree.bind('<Control-Button-1>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu at cursor position."""
        # Select the item under cursor
        item = self.slots_tree.identify_row(event.y)
        if item:
            self.slots_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def clear_slot(self):
        """Clear the selected slot."""
        if not self.current_setlist:
            return
        
        selection = self.slots_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a slot to clear.")
            return
        
        # Get slot index
        item = selection[0]
        tags = self.slots_tree.item(item, 'tags')
        if not tags:
            return
        
        slot_idx = int(tags[0])
        slot = self.current_setlist.slots[slot_idx]
        
        # Confirm
        if not messagebox.askyesno("Clear Slot", f"Clear slot {slot_idx + 1}?\n\nThis will reset the slot to default values."):
            return
        
        # Clear slot
        slot.name = ""
        slot.color = 0  # Default color
        slot.text_size = SlotTextSize.M
        slot.transpose = 0
        slot.volume = 127
        slot.notes = ""
        
        self.mark_modified()
        self.update_slots_display()
        self.status_label.config(text=f"Cleared slot {slot_idx + 1}", foreground="blue")
    
    def copy_slot_name(self):
        """Copy the selected slot name to clipboard."""
        if not self.current_setlist:
            return
        
        selection = self.slots_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        tags = self.slots_tree.item(item, 'tags')
        if not tags:
            return
        
        slot_idx = int(tags[0])
        slot = self.current_setlist.slots[slot_idx]
        
        if slot.name:
            self.root.clipboard_clear()
            self.root.clipboard_append(slot.name)
            self.status_label.config(text=f"Copied '{slot.name}' to clipboard", foreground="blue")
    
    def setup_ui(self):
        """Create the user interface."""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="PCG File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=0, column=1, padx=(10, 0))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Setlist selector
        ttk.Label(main_frame, text="Setlist:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        setlist_select_frame = ttk.Frame(main_frame)
        setlist_select_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        setlist_select_frame.columnconfigure(0, weight=1)
        
        self.setlist_combo = ttk.Combobox(setlist_select_frame, state='readonly')
        self.setlist_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.setlist_combo.bind('<<ComboboxSelected>>', self.on_setlist_selected)
        
        ttk.Button(setlist_select_frame, text="Edit Setlist Name", command=self.edit_setlist_name).grid(row=0, column=1)
        
        # Slots table
        ttk.Label(main_frame, text="Slots:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        
        # Create table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for slots
        columns = ('slot', 'name', 'color', 'size', 'transpose', 'volume')
        self.slots_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        self.slots_tree.heading('slot', text='#')
        self.slots_tree.heading('name', text='Slot Name')
        self.slots_tree.heading('color', text='Color')
        self.slots_tree.heading('size', text='Size')
        self.slots_tree.heading('transpose', text='Transpose')
        self.slots_tree.heading('volume', text='Volume')
        
        self.slots_tree.column('slot', width=40, anchor=tk.CENTER)
        self.slots_tree.column('name', width=300, anchor=tk.W)
        self.slots_tree.column('color', width=100, anchor=tk.CENTER)
        self.slots_tree.column('size', width=60, anchor=tk.CENTER)
        self.slots_tree.column('transpose', width=80, anchor=tk.CENTER)
        self.slots_tree.column('volume', width=80, anchor=tk.CENTER)
        
        self.slots_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.slots_tree.bind('<Double-Button-1>', self.edit_slot)
        self.slots_tree.bind('<Return>', self.edit_slot)
        
        # Context menu for slots
        self.setup_context_menu()
        
        # Scrollbar for table
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.slots_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.slots_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=1, columnspan=2, sticky=(tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Edit Slot", command=self.edit_slot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save File", command=self.save_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save As...", command=self.save_as_file).pack(side=tk.LEFT)
        
        # Status bar
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        
        self.status_label = ttk.Label(main_frame, text="Ready - Load a PCG file to start editing", foreground="blue")
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W)
    
    def browse_file(self):
        """Browse for a PCG file."""
        filename = filedialog.askopenfilename(
            title="Select PCG File",
            filetypes=[("PCG Files", "*.PCG"), ("All Files", "*.*")]
        )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, filename):
        """Load a PCG file."""
        # Check for unsaved changes
        if self.modified and not self.confirm_discard_changes():
            return
        
        try:
            self.status_label.config(text="Loading file...", foreground="orange")
            self.root.update()
            
            self.pcg = read_pcg_file(filename)
            self.current_file = Path(filename)
            self.modified = False
            self.update_title()
            
            # Add to recent files
            self.add_recent_file(self.current_file)
            
            # Update UI
            self.file_label.config(text=self.current_file.name, foreground="black")
            self.update_setlist_display()
            
            self.status_label.config(text=f"Loaded {len(self.pcg.set_lists)} setlists from {self.current_file.name}", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_label.config(text="Error loading file", foreground="red")
    
    def mark_modified(self):
        """Mark the file as modified."""
        if not self.modified:
            self.modified = True
            self.update_title()
    
    def update_title(self):
        """Update the window title."""
        title = "Simple Setlist Editor"
        if self.current_file:
            title += f" - {self.current_file.name}"
            if self.modified:
                title += " *"
        self.root.title(title)
    
    def confirm_discard_changes(self):
        """Ask user to confirm discarding unsaved changes."""
        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save them?",
            icon='warning'
        )
        
        if result is None:  # Cancel
            return False
        elif result:  # Yes - save
            self.save_file()
            return not self.modified  # Only proceed if save succeeded
        else:  # No - discard
            return True
    
    def update_setlist_display(self):
        """Update the setlist combo box."""
        self.setlist_combo['values'] = []
        
        if self.pcg and self.pcg.set_lists:
            setlist_names = [f"{i+1}. {sl.name or '(Empty)'}" for i, sl in enumerate(self.pcg.set_lists)]
            self.setlist_combo['values'] = setlist_names
            if setlist_names:
                self.setlist_combo.current(0)
                self.on_setlist_selected()
    
    def on_setlist_selected(self, event=None):
        """Handle setlist selection change."""
        if not self.pcg or not self.pcg.set_lists:
            return
        
        idx = self.setlist_combo.current()
        if idx >= 0:
            self.current_setlist = self.pcg.set_lists[idx]
            self.update_slots_display()
    
    def update_slots_display(self):
        """Update the slots table."""
        # Clear existing items
        for item in self.slots_tree.get_children():
            self.slots_tree.delete(item)
        
        if not self.current_setlist or not self.current_setlist.slots:
            return
        
        # Count used slots
        used_slots = sum(1 for slot in self.current_setlist.slots if slot.name and slot.name.strip())
        total_slots = len(self.current_setlist.slots)
        
        # Add slots to table
        for slot in self.current_setlist.slots:
            values = (
                str(slot.slot_index + 1),
                slot.name or "(Empty)",
                slot.color_name,
                slot.text_size_name,
                f"{slot.transpose:+d}" if slot.transpose != 0 else "0",
                str(slot.volume)
            )
            self.slots_tree.insert('', tk.END, values=values, tags=(str(slot.slot_index),))
        
        # Update status with slot count
        if hasattr(self, 'status_label'):
            self.status_label.config(
                text=f"Setlist: {self.current_setlist.name or '(Unnamed)'} - {used_slots}/{total_slots} slots used",
                foreground="blue"
            )
    
    def edit_setlist_name(self):
        """Edit the current setlist name."""
        if not self.current_setlist:
            messagebox.showwarning("No Setlist", "Please select a setlist first.")
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Setlist Name")
        dialog.geometry("400x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 250, self.root.winfo_rooty() + 200))
        
        # Dialog content
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Setlist Name:").pack(anchor=tk.W, pady=(0, 5))
        
        name_var = tk.StringVar(value=self.current_setlist.name or "")
        entry = ttk.Entry(frame, textvariable=name_var, width=40)
        entry.pack(fill=tk.X, pady=(0, 10))
        entry.focus()
        entry.select_range(0, tk.END)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        def save_name():
            new_name = name_var.get().strip()
            if len(new_name) > 24:
                messagebox.showwarning("Name Too Long", "Setlist names must be 24 characters or less.")
                return
            
            self.current_setlist.name = new_name
            self.mark_modified()
            self.update_setlist_display()
            self.status_label.config(text=f"Updated setlist name", foreground="blue")
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_name).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.RIGHT)
        
        # Bind keys
        entry.bind('<Return>', lambda e: save_name())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def edit_slot(self, event=None):
        """Edit the selected slot."""
        if not self.current_setlist:
            messagebox.showwarning("No Setlist", "Please select a setlist first.")
            return
        
        selection = self.slots_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a slot to edit.")
            return
        
        # Get slot index from tags
        item = selection[0]
        tags = self.slots_tree.item(item, 'tags')
        if not tags:
            return
        
        slot_idx = int(tags[0])
        slot = self.current_setlist.slots[slot_idx]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Slot {slot_idx + 1}")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 225, self.root.winfo_rooty() + 175))
        
        # Dialog content
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Slot name
        ttk.Label(frame, text="Slot Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        name_var = tk.StringVar(value=slot.name or "")
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        name_entry.focus()
        
        # Color
        ttk.Label(frame, text="Color:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        color_var = tk.StringVar(value=slot.color_name)
        color_combo = ttk.Combobox(frame, textvariable=color_var, state='readonly', width=37)
        color_combo['values'] = sorted(SLOT_COLOR_VALUES.keys())
        color_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Text Size
        ttk.Label(frame, text="Text Size:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        size_var = tk.StringVar(value=slot.text_size_name)
        size_combo = ttk.Combobox(frame, textvariable=size_var, state='readonly', width=37)
        size_combo['values'] = ['XS', 'S', 'M', 'L', 'XL']
        size_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Transpose
        ttk.Label(frame, text="Transpose:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        transpose_var = tk.IntVar(value=slot.transpose)
        transpose_spin = ttk.Spinbox(frame, from_=-24, to=24, textvariable=transpose_var, width=38)
        transpose_spin.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Volume
        ttk.Label(frame, text="Volume:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        volume_var = tk.IntVar(value=slot.volume)
        volume_spin = ttk.Spinbox(frame, from_=0, to=127, textvariable=volume_var, width=38)
        volume_spin.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Notes
        ttk.Label(frame, text="Notes:").grid(row=5, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        notes_text = tk.Text(frame, height=5, width=40)
        notes_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=(10, 10))
        notes_text.insert('1.0', slot.notes or "")
        
        frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.E), pady=(10, 0))
        
        def save_slot():
            # Validate name length
            new_name = name_var.get().strip()
            if len(new_name) > 24:
                messagebox.showwarning("Name Too Long", "Slot names must be 24 characters or less.")
                return
            
            # Update slot
            slot.name = new_name
            slot.color = SLOT_COLOR_VALUES[color_var.get()]
            slot.text_size = SlotTextSize[size_var.get()]
            slot.transpose = transpose_var.get()
            slot.volume = volume_var.get()
            slot.notes = notes_text.get('1.0', tk.END).strip()
            
            self.mark_modified()
            self.update_slots_display()
            self.status_label.config(text=f"Updated slot {slot_idx + 1}", foreground="blue")
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_slot).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.RIGHT)
        
        # Bind Escape key
        dialog.bind('<Escape>', lambda e: cancel())
    
    def save_file(self):
        """Save the current file."""
        if not self.pcg or not self.current_file:
            messagebox.showwarning("No File", "No file to save.")
            return
        
        self.save_to_file(self.current_file)
    
    def save_as_file(self):
        """Save as a new file."""
        if not self.pcg:
            messagebox.showwarning("No File", "No file to save.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save PCG File As",
            defaultextension=".PCG",
            filetypes=[("PCG Files", "*.PCG"), ("All Files", "*.*")]
        )
        
        if filename:
            self.save_to_file(Path(filename))
    
    def save_to_file(self, filepath):
        """Save to the specified file."""
        try:
            self.status_label.config(text="Saving file...", foreground="orange")
            self.root.update()
            
            # Use our working writer code directly
            write_pcg_file(self.pcg, str(filepath))
            
            self.current_file = filepath
            self.modified = False
            self.update_title()
            self.add_recent_file(filepath)
            self.file_label.config(text=self.current_file.name)
            self.status_label.config(text=f"Saved to {self.current_file.name}", foreground="green")
            
            messagebox.showinfo("Success", f"File saved successfully!\n\nFile: {filepath.name}\nLocation: {filepath.parent}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
            self.status_label.config(text="Error saving file", foreground="red")
    
    def on_closing(self):
        """Handle window closing."""
        if self.modified and not self.confirm_discard_changes():
            return
        
        # Save configuration
        self.save_config()
        
        self.root.quit()
        self.root.destroy()

def main():
    """Run the simple setlist editor."""
    root = tk.Tk()
    app = SimpleSetlistEditor(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()

if __name__ == '__main__':
    main()
