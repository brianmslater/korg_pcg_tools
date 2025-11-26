#!/usr/bin/env python3
"""
Simple Setlist Name Editor
A clean, focused GUI for editing PCG setlist names.
Uses the working writer code directly - no extra modifications.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

class SimpleSetlistEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Setlist Name Editor")
        self.root.geometry("600x500")
        
        self.pcg = None
        self.current_file = None
        
        self.setup_ui()
    
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
        
        # Setlist editor
        ttk.Label(main_frame, text="Setlists:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        # Setlist listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.setlist_listbox = tk.Listbox(list_frame, height=15)
        self.setlist_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.setlist_listbox.bind('<Double-Button-1>', self.edit_selected)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.setlist_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.setlist_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=2, sticky=(tk.N), padx=(10, 0))
        
        ttk.Button(button_frame, text="Edit Name", command=self.edit_selected).pack(pady=(0, 5), fill=tk.X)
        ttk.Button(button_frame, text="Save File", command=self.save_file).pack(pady=(0, 5), fill=tk.X)
        ttk.Button(button_frame, text="Save As...", command=self.save_as_file).pack(fill=tk.X)
        
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
        try:
            self.status_label.config(text="Loading file...", foreground="orange")
            self.root.update()
            
            self.pcg = read_pcg_file(filename)
            self.current_file = Path(filename)
            
            # Update UI
            self.file_label.config(text=self.current_file.name, foreground="black")
            self.update_setlist_display()
            
            self.status_label.config(text=f"Loaded {len(self.pcg.set_lists)} setlists from {self.current_file.name}", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_label.config(text="Error loading file", foreground="red")
    
    def update_setlist_display(self):
        """Update the setlist display."""
        self.setlist_listbox.delete(0, tk.END)
        
        if self.pcg and self.pcg.set_lists:
            for i, setlist in enumerate(self.pcg.set_lists):
                name = setlist.name if setlist.name else "(Empty)"
                self.setlist_listbox.insert(tk.END, f"{i+1:2d}. {name}")
    
    def edit_selected(self, event=None):
        """Edit the selected setlist name."""
        if not self.pcg:
            messagebox.showwarning("No File", "Please load a PCG file first.")
            return
        
        selection = self.setlist_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a setlist to edit.")
            return
        
        index = selection[0]
        setlist = self.pcg.set_lists[index]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Setlist {index + 1}")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Dialog content
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"Setlist {index + 1} Name:").pack(anchor=tk.W, pady=(0, 5))
        
        name_var = tk.StringVar(value=setlist.name or "")
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
            
            setlist.name = new_name
            self.update_setlist_display()
            self.status_label.config(text=f"Updated setlist {index + 1} name", foreground="blue")
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_name).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.RIGHT)
        
        # Bind Enter key
        entry.bind('<Return>', lambda e: save_name())
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
            self.file_label.config(text=self.current_file.name)
            self.status_label.config(text=f"Saved to {self.current_file.name}", foreground="green")
            
            messagebox.showinfo("Success", f"File saved successfully!\n\nFile: {filepath.name}\nLocation: {filepath.parent}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
            self.status_label.config(text="Error saving file", foreground="red")

def main():
    """Run the simple setlist editor."""
    root = tk.Tk()
    app = SimpleSetlistEditor(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
