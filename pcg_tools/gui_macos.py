"""macOS-compatible GUI for PCG Tools using Listbox instead of Treeview."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from pathlib import Path
from .reader import read_pcg_file
from .writer import write_pcg_file
from .clipboard import get_clipboard
from .operations import PatchOperations
from .edit_dialog import EditPatchDialog, EditSetListDialog


class PcgWindow:
    """Individual PCG file window - macOS compatible version."""
    
    def __init__(self, parent, filepath=None):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("PCG File")
        self.window.geometry("900x600")
        
        self.pcg = None
        self.filepath = filepath
        self.is_dirty = False
        self.clipboard = get_clipboard()
        self.operations = None
        
        self._create_widgets()
        
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        if filepath:
            self.load_file(filepath)
    
    def _create_widgets(self):
        """Create window widgets - macOS compatible."""
        
        # Menu bar
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Cmd+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self._on_close, accelerator="Cmd+W")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit Patch", command=self._edit_selected, accelerator="Return")
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy", command=self._copy_selection, accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", command=self._paste_selection, accelerator="Cmd+V")
        edit_menu.add_command(label="Clear", command=self._clear_selection, accelerator="Delete")
        
        # Top section: View selector and status
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # View selector
        view_frame = ttk.Frame(top_frame)
        view_frame.pack(side=tk.LEFT)
        
        self.view_var = tk.StringVar(value="programs")
        ttk.Radiobutton(view_frame, text="Programs", variable=self.view_var, 
                       value="programs", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(view_frame, text="Combis", variable=self.view_var, 
                       value="combis", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(view_frame, text="Set Lists", variable=self.view_var, 
                       value="setlists", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        
        # Status
        status_frame = ttk.Frame(top_frame)
        status_frame.pack(side=tk.RIGHT)
        
        ttk.Label(status_frame, text="Patches:").pack(side=tk.LEFT, padx=5)
        self.patch_count_label = ttk.Label(status_frame, text="0", font=('Arial', 10, 'bold'))
        self.patch_count_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_frame, text="Selected:").pack(side=tk.LEFT, padx=5)
        self.selected_count_label = ttk.Label(status_frame, text="0", font=('Arial', 10, 'bold'))
        self.selected_count_label.pack(side=tk.LEFT, padx=5)
        
        # Main content area
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Programs view
        self.programs_frame = ttk.Frame(self.content_frame)
        self._create_listbox_view(self.programs_frame, "programs")
        
        # Combis view
        self.combis_frame = ttk.Frame(self.content_frame)
        self._create_listbox_view(self.combis_frame, "combis")
        
        # Setlists view
        self.setlists_frame = ttk.Frame(self.content_frame)
        try:
            self._create_setlist_view(self.setlists_frame)
        except Exception as e:
            print(f"Error creating setlist view: {e}")
            import traceback
            traceback.print_exc()
        
        # Show programs by default
        self.programs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(bottom_frame, text="Edit", command=self._edit_selected, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="Copy", command=self._copy_selection, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="Paste", command=self._paste_selection, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text="Clear", command=self._clear_selection, width=12).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(bottom_frame, text="Save", command=self.save_file, width=12).pack(side=tk.RIGHT, padx=2)
        
        # Keyboard shortcuts
        self.window.bind('<Command-s>', lambda e: self.save_file())
        self.window.bind('<Command-w>', lambda e: self._on_close())
        self.window.bind('<Command-c>', lambda e: self._copy_selection())
        self.window.bind('<Command-v>', lambda e: self._paste_selection())
        self.window.bind('<Return>', lambda e: self._edit_selected())
        self.window.bind('<Delete>', lambda e: self._clear_selection())
        self.window.bind('<BackSpace>', lambda e: self._clear_selection())
    
    def _create_listbox_view(self, parent, list_type):
        """Create a listbox view (works better on macOS than Treeview)."""
        
        # Header frame
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 2))
        
        # Column headers
        ttk.Label(header_frame, text="ID", width=9, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Name", width=24, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Engine", width=8, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Info", width=6, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Category", width=13, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Sub-Cat", width=13, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Fav", width=3, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Use monospace font for alignment
        mono_font = tkfont.Font(family='Monaco', size=11)
        
        listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            font=mono_font,
            activestyle='none',
            exportselection=False
        )
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to edit
        listbox.bind('<Double-Button-1>', lambda e: self._edit_selected())
        
        # Selection change
        listbox.bind('<<ListboxSelect>>', lambda e: self._update_counts())
        
        # Store reference
        if list_type == "programs":
            self.programs_listbox = listbox
            self.programs_data = []
        else:
            self.combis_listbox = listbox
            self.combis_data = []
    
    def _create_setlist_view(self, parent):
        """Create setlist view with note editing."""
        # Top: Setlist selector
        selector_frame = ttk.Frame(parent)
        selector_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(selector_frame, text="Set List:").pack(side=tk.LEFT, padx=5)
        self.setlist_var = tk.StringVar()
        self.setlist_combo = ttk.Combobox(selector_frame, textvariable=self.setlist_var, 
                                          state='readonly', width=30)
        self.setlist_combo.pack(side=tk.LEFT, padx=5)
        self.setlist_combo.bind('<<ComboboxSelected>>', lambda e: self._load_setlist_slots())
        
        # Edit setlist name button
        ttk.Button(selector_frame, text="Edit Name", command=self._edit_setlist_name, width=12).pack(side=tk.LEFT, padx=5)
        
        # New setlist button
        ttk.Button(selector_frame, text="New Setlist", command=self._create_new_setlist, width=12).pack(side=tk.LEFT, padx=5)
        
        # Middle: Slots list
        slots_frame = ttk.Frame(parent)
        slots_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Header
        header_frame = ttk.Frame(slots_frame)
        header_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(header_frame, text="Slot", width=5, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Name", width=24, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Patch", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Trans", width=5, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Vol", width=4, anchor=tk.W).pack(side=tk.LEFT, padx=2)
        
        # Listbox
        list_frame = ttk.Frame(slots_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        mono_font = tkfont.Font(family='Monaco', size=11)
        self.setlist_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=mono_font,
            activestyle='none',
            exportselection=False
        )
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.setlist_listbox.yview)
        self.setlist_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.setlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.setlist_listbox.bind('<<ListboxSelect>>', lambda e: self._load_slot_notes())
        
        self.setlist_data = []
        
        # Bottom: Notes editor
        notes_frame = ttk.LabelFrame(parent, text="Slot Notes", padding=5)
        notes_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        self.notes_text = tk.Text(notes_frame, height=6, wrap=tk.WORD)
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Save notes button
        save_notes_btn = ttk.Button(notes_frame, text="Save Notes", command=self._save_slot_notes)
        save_notes_btn.pack(side=tk.BOTTOM, pady=5)
        
        # Bind text changes
        self.notes_text.bind('<KeyRelease>', lambda e: self._mark_notes_dirty())
        self.notes_dirty = False
    
    def _switch_view(self):
        """Switch between views."""
        # Write to file for debugging
        with open('/tmp/pcg_debug.log', 'a') as f:
            f.write(f"_switch_view called\n")
        
        self.programs_frame.pack_forget()
        self.combis_frame.pack_forget()
        self.setlists_frame.pack_forget()
        
        view = self.view_var.get()
        with open('/tmp/pcg_debug.log', 'a') as f:
            f.write(f"Switching to view: {view}\n")
        
        if view == "programs":
            self.programs_frame.pack(fill=tk.BOTH, expand=True)
        elif view == "combis":
            self.combis_frame.pack(fill=tk.BOTH, expand=True)
        else:  # setlists
            with open('/tmp/pcg_debug.log', 'a') as f:
                f.write(f"Packing setlists frame\n")
            self.setlists_frame.pack(fill=tk.BOTH, expand=True)
            self._load_setlists()
        
        self._update_counts()
        
        # Force GUI update on macOS
        self.window.update_idletasks()
        self.window.update()
    
    def load_file(self, filepath):
        """Load a PCG file."""
        try:
            self.pcg = read_pcg_file(filepath)
            self.filepath = filepath
            self.operations = PatchOperations(self.pcg)
            self._update_display()
            self.window.title(f"PCG Tools - {Path(filepath).name}")
            # Force GUI update on macOS
            self.window.update_idletasks()
            self.window.update()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}", parent=self.window)
    
    def _update_display(self):
        """Update the display with current PCG data."""
        if not self.pcg:
            return
        
        # Update programs listbox
        self.programs_listbox.delete(0, tk.END)
        self.programs_data = []
        
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                cat = prog.category.name if prog.category else ""
                sub_cat = prog.category.sub_name if prog.category else ""
                fav = "✓" if prog.favorite else " "
                engine = prog.engine if hasattr(prog, 'engine') else ""
                # Determine info
                info = ""
                if prog.bank.startswith("I-") and len(prog.bank) > 3:
                    info = "EXi"
                elif prog.bank.startswith("U-"):
                    info = "User"
                
                # Format line with fixed widths for alignment
                line = f"{prog.id:<9} {prog.name:<24} {engine:<8} {info:<6} {cat:<13} {sub_cat:<13} {fav}"
                self.programs_listbox.insert(tk.END, line)
                self.programs_data.append(prog)
        
        # Update combis listbox
        self.combis_listbox.delete(0, tk.END)
        self.combis_data = []
        
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                cat = combi.category.name if combi.category else ""
                sub_cat = combi.category.sub_name if combi.category else ""
                fav = "✓" if combi.favorite else " "
                # Determine info
                info = ""
                if combi.bank.startswith("U-"):
                    info = "User"
                
                line = f"{combi.id:<9} {combi.name:<24} {'N/A':<8} {info:<6} {cat:<13} {sub_cat:<13} {fav}"
                self.combis_listbox.insert(tk.END, line)
                self.combis_data.append(combi)
        
        self._update_counts()
    
    def _load_setlists(self):
        """Load setlists into combo box."""
        print(f"DEBUG: _load_setlists called, pcg={self.pcg is not None}")
        if not self.pcg:
            print(f"DEBUG: No PCG loaded")
            self.setlist_combo['values'] = []
            return
        
        print(f"DEBUG: PCG has {len(self.pcg.set_lists) if self.pcg.set_lists else 0} setlists")
        if not self.pcg.set_lists:
            print(f"DEBUG: No setlists, showing message")
            self.setlist_combo['values'] = ["(No setlists - click 'New Setlist' to create)"]
            self.setlist_combo.current(0)
            self.setlist_listbox.delete(0, tk.END)
            self.notes_text.delete('1.0', tk.END)
            return
        
        setlist_names = [f"{sl.index}: {sl.name}" for sl in self.pcg.set_lists]
        print(f"DEBUG: Setlist names: {setlist_names}")
        self.setlist_combo['values'] = setlist_names
        if setlist_names:
            self.setlist_combo.current(0)
            self._load_setlist_slots()
    
    def _load_setlist_slots(self):
        """Load slots for selected setlist."""
        if not self.pcg or not self.pcg.set_lists:
            return
        
        selection = self.setlist_var.get()
        if not selection:
            return
        
        # Extract index from "0: Name" format
        sl_idx = int(selection.split(':')[0])
        if sl_idx >= len(self.pcg.set_lists):
            return
        
        setlist = self.pcg.set_lists[sl_idx]
        
        # Clear and populate listbox
        self.setlist_listbox.delete(0, tk.END)
        self.setlist_data = []
        
        # Create a map of slot_index -> slot for quick lookup
        slot_map = {slot.slot_index: slot for slot in setlist.slots}
        
        # Display all 128 slots like the Kronos does
        for slot_idx in range(128):
            if slot_idx in slot_map:
                slot = slot_map[slot_idx]
                
                # Get the actual patch/combi name (like Kronos displays)
                patch_name = self._get_patch_name(slot)
                
                # Format like Kronos: "0  STARGAZERS STRINGS INTRO  CMB I-A 057  +0  127"
                trans_str = f"{slot.transpose:+3d}" if slot.transpose != 0 else "  0"
                patch_type_short = "CMB" if slot.patch_type == "Combi" else "PRG"
                line = f"{slot_idx:3d}  {patch_name:<30} {patch_type_short} {slot.patch_bank}-{slot.patch_index:03d}  {trans_str} {slot.volume:3d}"
                self.setlist_listbox.insert(tk.END, line)
                self.setlist_data.append(slot)
            else:
                # Empty slot
                line = f"{slot_idx:3d}  (empty)"
                self.setlist_listbox.insert(tk.END, line)
                self.setlist_data.append(None)
        
        # Clear notes
        self.notes_text.delete('1.0', tk.END)
        self.notes_dirty = False
    
    def _get_patch_name(self, slot):
        """Get the actual patch/combi name for a slot (like Kronos displays)."""
        if not self.pcg:
            return slot.name
        
        # Try to find the referenced patch
        if slot.patch_type == "Combi":
            for bank in self.pcg.combi_banks:
                if bank.bank_id == slot.patch_bank:
                    if slot.patch_index < len(bank.patches):
                        return bank.patches[slot.patch_index].name
                    break
        elif slot.patch_type == "Program":
            for bank in self.pcg.program_banks:
                if bank.bank_id == slot.patch_bank:
                    if slot.patch_index < len(bank.patches):
                        return bank.patches[slot.patch_index].name
                    break
        
        # Fallback to slot name if patch not found
        return slot.name if slot.name else "(unknown)"
    
    def _load_slot_notes(self):
        """Load notes for selected slot."""
        if self.notes_dirty:
            response = messagebox.askyesno(
                "Unsaved Notes",
                "You have unsaved notes. Save them first?",
                parent=self.window
            )
            if response:
                self._save_slot_notes()
        
        selection = self.setlist_listbox.curselection()
        if not selection or not self.setlist_data:
            self.notes_text.delete('1.0', tk.END)
            return
        
        index = selection[0]
        if 0 <= index < len(self.setlist_data):
            slot = self.setlist_data[index]
            self.notes_text.delete('1.0', tk.END)
            if slot:  # Not an empty slot
                self.notes_text.insert('1.0', slot.notes)
            self.notes_dirty = False
    
    def _mark_notes_dirty(self):
        """Mark notes as modified."""
        self.notes_dirty = True
    
    def _save_slot_notes(self):
        """Save notes for current slot."""
        selection = self.setlist_listbox.curselection()
        if not selection or not self.setlist_data:
            return
        
        index = selection[0]
        if 0 <= index < len(self.setlist_data):
            slot = self.setlist_data[index]
            if slot:  # Not an empty slot
                notes = self.notes_text.get('1.0', tk.END).strip()
                slot.notes = notes
                self.notes_dirty = False
                self.is_dirty = True
                self._update_title()
                messagebox.showinfo("Saved", "Notes saved successfully", parent=self.window)
            else:
                messagebox.showwarning("Empty Slot", "Cannot save notes for an empty slot", parent=self.window)
    
    def _create_new_setlist(self):
        """Create a new setlist."""
        if not self.pcg:
            return
        
        from .models import SetList
        
        # Determine next index
        next_index = len(self.pcg.set_lists)
        if next_index >= 16:
            messagebox.showwarning(
                "Maximum Setlists",
                "Maximum of 16 setlists reached. Cannot create more.",
                parent=self.window
            )
            return
        
        # Create new setlist
        new_setlist = SetList(
            index=next_index,
            name=f"Set List {next_index + 1}",
            description="",
            color=0,
            slots=[]
        )
        
        # Add to PCG
        self.pcg.set_lists.append(new_setlist)
        self.pcg.has_set_lists = True
        
        # Mark as dirty
        self.is_dirty = True
        self._update_title()
        
        # Reload and select new setlist
        self._load_setlists()
        self.setlist_combo.current(next_index)
        self._load_setlist_slots()
        
        # Show confirmation
        self.parent.status_bar.config(
            text=f"✓ New setlist '{new_setlist.name}' created - Press Cmd+S to save to file",
            foreground='blue'
        )
    
    def _edit_setlist_name(self):
        """Edit the name of the currently selected setlist."""
        if not self.pcg or not self.pcg.set_lists:
            return
        
        selection = self.setlist_var.get()
        if not selection:
            return
        
        # Extract index from "0: Name" format
        sl_idx = int(selection.split(':')[0])
        if sl_idx >= len(self.pcg.set_lists):
            return
        
        setlist = self.pcg.set_lists[sl_idx]
        
        # Show edit dialog
        dialog = EditSetListDialog(self.window, setlist)
        if dialog.show():
            self.is_dirty = True
            self._update_title()
            # Reload setlist combo to show new name
            self._load_setlists()
            # Restore selection
            self.setlist_combo.current(sl_idx)
            self._load_setlist_slots()
            # Show confirmation in status bar
            self.parent.status_bar.config(
                text=f"✓ Set list '{setlist.name}' updated in memory - Press Cmd+S to save to file",
                foreground='blue'
            )
    
    def _update_counts(self):
        """Update patch and selection counts."""
        if not self.pcg:
            self.patch_count_label.config(text="0")
            self.selected_count_label.config(text="0")
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            total = len(self.programs_data)
            selected = len(self.programs_listbox.curselection())
        elif view == "combis":
            total = len(self.combis_data)
            selected = len(self.combis_listbox.curselection())
        else:  # setlists
            total = len(self.setlist_data)
            selected = len(self.setlist_listbox.curselection())
        
        self.patch_count_label.config(text=str(total))
        self.selected_count_label.config(text=str(selected))
    
    def _edit_selected(self):
        """Edit selected patch."""
        if not self.pcg:
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            listbox = self.programs_listbox
            data = self.programs_data
            patch_type = "program"
        else:
            listbox = self.combis_listbox
            data = self.combis_data
            patch_type = "combi"
        
        selection = listbox.curselection()
        if not selection:
            return
        
        # Edit first selected
        index = selection[0]
        if 0 <= index < len(data):
            patch = data[index]
            dialog = EditPatchDialog(self.window, patch, patch_type)
            if dialog.show():
                self.is_dirty = True
                self._update_display()
                self._update_title()
                # Show confirmation in status bar
                self.parent.status_bar.config(
                    text=f"✓ {patch_type.capitalize()} '{patch.name}' updated in memory - Press Cmd+S to save to file",
                    foreground='blue'
                )
    
    def _copy_selection(self):
        """Copy selected patches."""
        if not self.pcg:
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            listbox = self.programs_listbox
            data = self.programs_data
        else:
            listbox = self.combis_listbox
            data = self.combis_data
        
        selection = listbox.curselection()
        if not selection:
            return
        
        patches = [data[i] for i in selection if 0 <= i < len(data)]
        
        if patches:
            if view == "programs":
                self.clipboard.copy_programs(patches, self.filepath or "Untitled")
            else:
                self.clipboard.copy_combis(patches, self.filepath or "Untitled", self.pcg, include_programs=True)
            
            self.parent.status_bar.config(text=f"Copied {len(patches)} {view}")
    
    def _paste_selection(self):
        """Paste from clipboard."""
        if not self.pcg or not self.operations:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        if self.clipboard.is_empty():
            messagebox.showwarning("Warning", "Clipboard is empty", parent=self.window)
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            listbox = self.programs_listbox
            data = self.programs_data
        else:
            listbox = self.combis_listbox
            data = self.combis_data
        
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a destination slot", parent=self.window)
            return
        
        # Get destination
        index = selection[0]
        if 0 <= index < len(data):
            patch = data[index]
            
            try:
                if view == "programs":
                    count = self.operations.paste_programs(patch.bank, patch.index)
                else:
                    count = self.operations.paste_combis(patch.bank, patch.index)
                
                if count > 0:
                    self.is_dirty = True
                    self._update_display()
                    self._update_title()
                    self.parent.status_bar.config(text=f"Pasted {count} {view}")
                    messagebox.showinfo("Success", f"Pasted {count} {view}", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to paste:\n{e}", parent=self.window)
    
    def _clear_selection(self):
        """Clear selected patches."""
        if not self.pcg or not self.operations:
            return
        
        view = self.view_var.get()
        
        if view == "programs":
            listbox = self.programs_listbox
            data = self.programs_data
        else:
            listbox = self.combis_listbox
            data = self.combis_data
        
        selection = listbox.curselection()
        if not selection:
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            f"Clear {len(selection)} {view}?",
            parent=self.window
        )
        
        if not result:
            return
        
        for i in selection:
            if 0 <= i < len(data):
                patch = data[i]
                if view == "programs":
                    self.operations.clear_program(patch.bank, patch.index)
                else:
                    self.operations.clear_combi(patch.bank, patch.index)
        
        self.is_dirty = True
        self._update_display()
        self._update_title()
        self.parent.status_bar.config(text=f"Cleared {len(selection)} {view}")
    
    def save_file(self):
        """Save the current PCG file."""
        if not self.pcg or not self.filepath:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        try:
            write_pcg_file(self.pcg, self.filepath)
            self.is_dirty = False
            self._update_title()
            self.parent.status_bar.config(
                text=f"✓ File saved: {Path(self.filepath).name}",
                foreground='green'
            )
            messagebox.showinfo("Success", "File saved successfully", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=self.window)
    
    def save_as_file(self):
        """Save as new file."""
        if not self.pcg:
            messagebox.showwarning("Warning", "No file loaded", parent=self.window)
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save PCG File As",
            defaultextension=".PCG",
            filetypes=[("PCG Files", "*.PCG"), ("All Files", "*.*")],
            parent=self.window
        )
        
        if filename:
            try:
                write_pcg_file(self.pcg, filename)
                self.filepath = filename
                self.is_dirty = False
                self._update_title()
                self.parent.status_bar.config(
                    text=f"✓ File saved as: {Path(filename).name}",
                    foreground='green'
                )
                messagebox.showinfo("Success", "File saved successfully", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=self.window)
    
    def _update_title(self):
        """Update window title."""
        dirty_flag = "*" if self.is_dirty else ""
        filename = Path(self.filepath).name if self.filepath else "Untitled"
        self.window.title(f"PCG Tools - {filename}{dirty_flag}")
    
    def _on_close(self):
        """Handle window close."""
        if self.is_dirty:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Do you want to save changes before closing?",
                parent=self.window
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_file()
        
        self.window.destroy()
        if self in self.parent.windows:
            self.parent.windows.remove(self)


class PcgToolsGUI:
    """Main GUI application - macOS compatible."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PCG Tools")
        self.root.geometry("800x500")
        
        self.windows = []
        
        self._create_menu()
        self._create_widgets()
        
        # Force initial rendering on macOS
        self.root.update_idletasks()
        self.root.update()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # macOS-specific: Create application menu
        if self.root.tk.call('tk', 'windowingsystem') == 'aqua':
            app_menu = tk.Menu(menubar, name='apple')
            menubar.add_cascade(menu=app_menu)
            app_menu.add_command(label='About PCG Tools', command=self.show_about)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PCG...", command=self.open_file, accelerator="Cmd+O")
        file_menu.add_separator()
        file_menu.add_command(label="Close All", command=self.close_all)
        file_menu.add_command(label="Quit", command=self.root.quit, accelerator="Cmd+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Command-o>', lambda e: self.open_file())
        self.root.bind('<Command-q>', lambda e: self.root.quit())
    
    def _create_widgets(self):
        """Create main widgets."""
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(
            welcome_frame,
            text="PCG Tools - Korg PCG File Editor",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(
            welcome_frame,
            text="macOS Compatible Version",
            font=('Arial', 12)
        )
        subtitle_label.pack(pady=5)
        
        info_label = ttk.Label(
            welcome_frame,
            text="Open PCG files to edit patches",
            font=('Arial', 10)
        )
        info_label.pack(pady=10)
        
        open_button = ttk.Button(
            welcome_frame,
            text="Open PCG File",
            command=self.open_file,
            width=20
        )
        open_button.pack(pady=10)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W, padx=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Force immediate rendering on macOS
        self.root.update_idletasks()
        self.root.update()
        welcome_frame.update_idletasks()
        welcome_frame.update()
    
    def open_file(self, filename=None):
        """Open a PCG file."""
        if not filename:
            filename = filedialog.askopenfilename(
                title="Open PCG File",
                initialdir="/Volumes/KEYBOARD" if Path("/Volumes/KEYBOARD").exists() else None,
                filetypes=[("PCG Files", "*.PCG *.pcg"), ("All Files", "*.*")]
            )
        
        if filename:
            window = PcgWindow(self, filename)
            self.windows.append(window)
            self.status_bar.config(text=f"Loaded: {Path(filename).name}")
    
    def close_all(self):
        """Close all windows."""
        for window in self.windows[:]:
            window._on_close()
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About PCG Tools",
            "PCG Tools v2.0.0\n\n"
            "macOS Compatible Version\n"
            "Cross-platform Korg PCG file editor\n\n"
            "Python port of the original PCG Tools"
        )


def launch_gui():
    """Launch the GUI application."""
    import os
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    root = tk.Tk()
    app = PcgToolsGUI(root)
    root.mainloop()


if __name__ == '__main__':
    launch_gui()
