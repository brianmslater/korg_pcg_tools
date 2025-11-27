"""Qt-based GUI for PCG Tools - Modern, native-looking interface."""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget,
    QFileDialog, QMessageBox, QComboBox, QTextEdit, QHeaderView,
    QMenuBar, QMenu, QStatusBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

from .reader import read_pcg_file
from .writer import write_pcg_file


class PcgMainWindow(QMainWindow):
    """Main PCG Tools window."""
    
    def __init__(self):
        super().__init__()
        self.pcg = None
        self.filepath = None
        self.is_dirty = False
        
        self.setWindowTitle("PCG Tools - Korg PCG File Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        self._create_menu()
        self._create_ui()
        self._create_statusbar()
        
    def _create_menu(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open PCG...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _create_ui(self):
        """Create main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Welcome screen (shown when no file is loaded)
        self.welcome_widget = self._create_welcome_screen()
        layout.addWidget(self.welcome_widget)
        
        # Main content (shown when file is loaded)
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_programs_tab(), "Programs")
        self.tabs.addTab(self._create_combis_tab(), "Combis")
        self.tabs.addTab(self._create_setlists_tab(), "Set Lists")
        
        content_layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_selected)
        button_layout.addWidget(self.edit_button)
        
        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_selected)
        button_layout.addWidget(self.copy_button)
        
        self.paste_button = QPushButton("Paste")
        self.paste_button.clicked.connect(self.paste_selected)
        button_layout.addWidget(self.paste_button)
        
        button_layout.addStretch()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_button)
        
        content_layout.addLayout(button_layout)
        
        layout.addWidget(self.content_widget)
        self.content_widget.hide()
    
    def _create_welcome_screen(self):
        """Create welcome screen."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("PCG Tools - Korg PCG File Editor")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Qt Version - Native macOS Interface")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        info = QLabel("Open a PCG file to view and edit patches")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        layout.addSpacing(20)
        
        open_button = QPushButton("Open PCG File")
        open_button.setMinimumWidth(200)
        open_button.setMinimumHeight(40)
        open_button.clicked.connect(self.open_file)
        layout.addWidget(open_button, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        return widget
    
    def _create_programs_tab(self):
        """Create programs tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.programs_table = QTableWidget()
        self.programs_table.setColumnCount(6)
        self.programs_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Engine", "Fav"])
        self.programs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.programs_table.doubleClicked.connect(self.edit_selected)
        
        layout.addWidget(self.programs_table)
        
        return widget
    
    def _create_combis_tab(self):
        """Create combis tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.combis_table = QTableWidget()
        self.combis_table.setColumnCount(5)
        self.combis_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Fav"])
        self.combis_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.combis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.combis_table.doubleClicked.connect(self.edit_selected)
        
        layout.addWidget(self.combis_table)
        
        return widget
    
    def _create_setlists_tab(self):
        """Create setlists tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Setlist selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Setlist:"))
        
        self.setlist_combo = QComboBox()
        self.setlist_combo.currentIndexChanged.connect(self.load_setlist_slots)
        selector_layout.addWidget(self.setlist_combo)
        
        self.new_setlist_button = QPushButton("New Setlist")
        self.new_setlist_button.clicked.connect(self.create_new_setlist)
        selector_layout.addWidget(self.new_setlist_button)
        
        self.edit_setlist_button = QPushButton("Edit Setlist Name")
        self.edit_setlist_button.clicked.connect(self.edit_setlist_name)
        selector_layout.addWidget(self.edit_setlist_button)
        
        self.color_button = QPushButton("Set Color")
        self.color_button.clicked.connect(self.set_setlist_color)
        selector_layout.addWidget(self.color_button)
        
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Slots table
        self.slots_table = QTableWidget()
        self.slots_table.setColumnCount(7)
        self.slots_table.setHorizontalHeaderLabels(["Slot", "Slot Name", "Patch Name", "Transpose", "Volume", "Color", "Size"])
        self.slots_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.slots_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.slots_table.doubleClicked.connect(self.edit_selected)
        self.slots_table.itemChanged.connect(self.on_slot_item_changed)
        
        layout.addWidget(self.slots_table)
        
        # Comments section
        notes_layout = QVBoxLayout()
        
        # Comments header with font size selector
        comments_header = QHBoxLayout()
        comments_header.addWidget(QLabel("Comments:"))
        comments_header.addStretch()
        comments_header.addWidget(QLabel("Font Size:"))
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["XS", "S", "M", "L", "XL"])
        self.font_size_combo.setCurrentText("M")
        self.font_size_combo.currentTextChanged.connect(self.on_font_size_changed)
        comments_header.addWidget(self.font_size_combo)
        
        notes_layout.addLayout(comments_header)
        
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(100)
        self.notes_text.setPlaceholderText("Select a slot to view/edit comments...")
        self.notes_text.textChanged.connect(self.on_notes_changed)
        notes_layout.addWidget(self.notes_text)
        
        layout.addLayout(notes_layout)
        
        # Connect slot selection to notes display
        self.slots_table.itemSelectionChanged.connect(self.on_slot_selection_changed)
        
        return widget
    
    def _create_statusbar(self):
        """Create status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
    
    def open_file(self):
        """Open a PCG file."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open PCG File",
            "",
            "PCG Files (*.PCG *.pcg);;All Files (*)"
        )
        
        if filename:
            try:
                self.pcg = read_pcg_file(filename)
                self.filepath = filename
                self.is_dirty = False
                
                self.welcome_widget.hide()
                self.content_widget.show()
                
                self.load_programs()
                self.load_combis()
                self.load_setlists()
                
                self.setWindowTitle(f"PCG Tools - {Path(filename).name}")
                self.statusbar.showMessage(f"Loaded: {Path(filename).name}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")
    
    def load_programs(self):
        """Load programs into table."""
        self.programs_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        program_count = 0
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                row = self.programs_table.rowCount()
                self.programs_table.insertRow(row)
                
                self.programs_table.setItem(row, 0, QTableWidgetItem(prog.id))
                self.programs_table.setItem(row, 1, QTableWidgetItem(prog.name))
                self.programs_table.setItem(row, 2, QTableWidgetItem(str(prog.category.main_category) if prog.category else ""))
                self.programs_table.setItem(row, 3, QTableWidgetItem(str(prog.category.sub_category) if prog.category else ""))
                self.programs_table.setItem(row, 4, QTableWidgetItem(prog.engine if hasattr(prog, 'engine') else ""))
                self.programs_table.setItem(row, 5, QTableWidgetItem("✓" if prog.favorite else ""))
                program_count += 1
        
        # Update status bar with count
        if program_count == 0:
            self.statusbar.showMessage(f"No programs found in file (found {len(self.pcg.program_banks)} program banks)")
        else:
            self.statusbar.showMessage(f"Loaded {program_count} programs from {len(self.pcg.program_banks)} banks")
    
    def load_combis(self):
        """Load combis into table."""
        self.combis_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        combi_count = 0
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                row = self.combis_table.rowCount()
                self.combis_table.insertRow(row)
                
                self.combis_table.setItem(row, 0, QTableWidgetItem(combi.id))
                self.combis_table.setItem(row, 1, QTableWidgetItem(combi.name))
                self.combis_table.setItem(row, 2, QTableWidgetItem(str(combi.category.main_category) if combi.category else ""))
                self.combis_table.setItem(row, 3, QTableWidgetItem(str(combi.category.sub_category) if combi.category else ""))
                self.combis_table.setItem(row, 4, QTableWidgetItem("✓" if combi.favorite else ""))
                combi_count += 1
        
        # Update status bar with count
        if combi_count > 0:
            self.statusbar.showMessage(f"Loaded {combi_count} combis from {len(self.pcg.combi_banks)} banks")
    
    def load_setlists(self):
        """Load setlists into combo box."""
        self.setlist_combo.clear()
        
        if not self.pcg or not self.pcg.set_lists:
            return
        
        for setlist in self.pcg.set_lists:
            self.setlist_combo.addItem(f"{setlist.index}: {setlist.name}", setlist)
        
        if self.setlist_combo.count() > 0:
            self.setlist_combo.setCurrentIndex(0)
    
    def load_setlist_slots(self):
        """Load slots for selected setlist."""
        # Block signals while loading to avoid triggering itemChanged
        self.slots_table.blockSignals(True)
        self.slots_table.setRowCount(0)
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            self.slots_table.blockSignals(False)
            return
        
        # Slots are already in order (0-127)
        for slot in setlist.slots:
            row = self.slots_table.rowCount()
            self.slots_table.insertRow(row)
            
            # Slot number (read-only)
            slot_item = QTableWidgetItem(str(slot.slot_index))
            slot_item.setFlags(slot_item.flags() & ~Qt.ItemIsEditable)
            self.slots_table.setItem(row, 0, slot_item)
            
            # Slot Name (editable custom name)
            name_item = QTableWidgetItem(slot.name if slot.name else "")
            self.slots_table.setItem(row, 1, name_item)
            
            # Patch Name (read-only - shows actual patch name)
            patch_name = ""
            if slot.patch_bank and slot.patch_type and self.pcg:
                # Look up the actual patch name
                if slot.patch_type == "Program":
                    prog = self.pcg.find_program(slot.patch_bank, slot.patch_index)
                    if prog:
                        patch_name = prog.name
                elif slot.patch_type == "Combi":
                    combi = self.pcg.find_combi(slot.patch_bank, slot.patch_index)
                    if combi:
                        patch_name = combi.name
            patch_item = QTableWidgetItem(patch_name)
            patch_item.setFlags(patch_item.flags() & ~Qt.ItemIsEditable)
            self.slots_table.setItem(row, 2, patch_item)
            
            # Transpose - editable
            transpose_item = QTableWidgetItem(str(slot.transpose))
            self.slots_table.setItem(row, 3, transpose_item)
            
            # Volume - editable
            volume_item = QTableWidgetItem(str(slot.volume))
            self.slots_table.setItem(row, 4, volume_item)
            
            # Color - read-only (edit via dialog) with visual indicator
            color_item = QTableWidgetItem(slot.color_name)
            color_item.setFlags(color_item.flags() & ~Qt.ItemIsEditable)
            
            # Add color background based on slot color value
            from PySide6.QtGui import QColor
            bg_color = self._get_display_color(slot.color)
            if bg_color:
                color_item.setBackground(bg_color)
                # Use white text for dark backgrounds
                if bg_color.lightness() < 128:
                    color_item.setForeground(QColor(255, 255, 255))
            
            self.slots_table.setItem(row, 5, color_item)
            
            # Text Size - read-only (edit via dialog)
            size_item = QTableWidgetItem(slot.text_size_name)
            size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
            self.slots_table.setItem(row, 6, size_item)
        
        self.slots_table.blockSignals(False)
    
    def _get_display_color(self, color_value):
        """Get QColor for display based on slot color value."""
        from PySide6.QtGui import QColor
        
        # Map color values to RGB colors for display (all 16 official Kronos colors)
        color_map = {
            0: None,  # Default - no background color
            136: QColor(178, 34, 34),      # Brick - dark red
            140: QColor(128, 0, 32),       # Burgundy - deep red
            144: QColor(34, 139, 34),      # Ivy - forest green
            148: QColor(128, 128, 0),      # Olive - yellow-green
            152: QColor(255, 215, 0),      # Gold - bright yellow
            156: QColor(139, 69, 19),      # Cacao - brown
            160: QColor(75, 0, 130),       # Indigo - blue-purple
            164: QColor(0, 0, 128),        # Navy - dark blue
            168: QColor(255, 182, 193),    # Rose - pink
            172: QColor(230, 230, 250),    # Lavender - light purple
            176: QColor(135, 206, 250),    # Azure - light blue
            180: QColor(21, 96, 189),      # Denim - medium blue
            184: QColor(192, 192, 192),    # Silver - light gray
            188: QColor(112, 128, 144),    # Slate - blue-gray
            196: QColor(54, 69, 79),       # Charcoal - dark gray
        }
        
        return color_map.get(color_value, QColor(200, 200, 200))  # Light gray for unknown
    
    def on_slot_item_changed(self, item):
        """Handle slot table item changes."""
        if not self.pcg:
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        row = item.row()
        col = item.column()
        
        if row >= len(setlist.slots):
            return
        
        slot = setlist.slots[row]
        
        try:
            # Column 1: Slot Name
            if col == 1:
                new_name = item.text()
                if len(new_name) > 24:
                    QMessageBox.warning(self, "Warning", "Slot name too long. Maximum 24 characters.")
                    item.setText(slot.name if slot.name else "")
                    return
                slot.name = new_name
                self.mark_dirty()
            
            # Column 3: Transpose
            elif col == 3:
                new_transpose = int(item.text())
                if new_transpose < -24 or new_transpose > 24:
                    QMessageBox.warning(self, "Warning", "Transpose must be between -24 and +24.")
                    item.setText(str(slot.transpose))
                    return
                slot.transpose = new_transpose
                self.mark_dirty()
            
            # Column 4: Volume
            elif col == 4:
                new_volume = int(item.text())
                if new_volume < 0 or new_volume > 127:
                    QMessageBox.warning(self, "Warning", "Volume must be between 0 and 127.")
                    item.setText(str(slot.volume))
                    return
                slot.volume = new_volume
                self.mark_dirty()
        
        except ValueError:
            # Invalid number entered, revert
            if col == 3:
                item.setText(str(slot.transpose))
            elif col == 4:
                item.setText(str(slot.volume))
    
    def edit_selected(self):
        """Edit selected item."""
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            row = self.programs_table.currentRow()
            if row >= 0:
                # Get the program from the PCG file
                program = self._get_program_at_row(row)
                if program:
                    self.edit_program(program)
        
        elif current_tab == 1:  # Combis
            row = self.combis_table.currentRow()
            if row >= 0:
                # Get the combi from the PCG file
                combi = self._get_combi_at_row(row)
                if combi:
                    self.edit_combi(combi)
        
        elif current_tab == 2:  # Setlists
            row = self.slots_table.currentRow()
            if row >= 0 and row < 128:
                setlist = self.setlist_combo.currentData()
                if setlist:
                    # Find the slot by index
                    slot = None
                    for s in setlist.slots:
                        if s.slot_index == row:
                            slot = s
                            break
                    
                    if slot:
                        self.edit_slot_name(slot)
                    else:
                        # Create new slot
                        from .models import SetListSlot
                        slot = SetListSlot(
                            set_list_index=setlist.index,
                            slot_index=row,
                            name="",
                            notes="",
                            patch_type="",
                            patch_bank="",
                            patch_index=0,
                            transpose=0,
                            volume=127
                        )
                        setlist.slots.append(slot)
                        self.edit_slot_name(slot)
    
    def _get_program_at_row(self, row):
        """Get program at specified table row."""
        if not self.pcg:
            return None
        
        current_row = 0
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                if current_row == row:
                    return prog
                current_row += 1
        return None
    
    def _get_combi_at_row(self, row):
        """Get combi at specified table row."""
        if not self.pcg:
            return None
        
        current_row = 0
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if current_row == row:
                    return combi
                current_row += 1
        return None
    
    def edit_program(self, program):
        """Edit a program using the Qt edit dialog."""
        # CRITICAL: Program editing is DISABLED due to file corruption
        # Editing programs breaks hardware validation (checksum issue)
        QMessageBox.warning(
            self,
            "Program Editing Disabled",
            f"Program editing is currently disabled due to a critical bug.\n\n"
            f"Program: {program.id} - {program.name}\n"
            f"Category: {program.category.main_category if program.category else 'N/A'}\n"
            f"Favorite: {program.favorite}\n"
            f"Engine: {program.engine}\n\n"
            f"Issue: Editing programs corrupts the file (Kronos shows 'File Unavailable').\n"
            f"Cause: Programs have internal checksums that we don't know how to update.\n\n"
            f"Workaround: Use the C# PCG Tools for program editing.\n"
            f"Status: Being investigated for future release."
        )
    
    def edit_combi(self, combi):
        """Edit a combi using the Qt edit dialog."""
        # CRITICAL: Combi editing is DISABLED due to file corruption
        # Editing combis breaks hardware validation (checksum issue)
        QMessageBox.warning(
            self,
            "Combi Editing Disabled",
            f"Combi editing is currently disabled due to a critical bug.\n\n"
            f"Combi: {combi.id} - {combi.name}\n"
            f"Category: {combi.category.main_category if combi.category else 'N/A'}\n"
            f"Favorite: {combi.favorite}\n"
            f"Tempo: {combi.tempo} BPM\n\n"
            f"Issue: Editing combis corrupts the file (Kronos shows 'File Unavailable').\n"
            f"Cause: Combis have internal checksums that we don't know how to update.\n\n"
            f"Workaround: Use the C# PCG Tools for combi editing.\n"
            f"Status: Being investigated for future release."
        )
    
    def edit_slot_name(self, slot):
        """Edit slot name, color, and text size."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFormLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Slot")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # Name field
        name_edit = QLineEdit(slot.name)
        name_edit.setMaxLength(24)
        form.addRow("Name:", name_edit)
        
        # Color selector - use expanded color mapping
        from .models import SLOT_COLOR_VALUES
        
        color_combo = QComboBox()
        # Sort colors by value for consistent ordering
        sorted_colors = sorted(SLOT_COLOR_VALUES.items(), key=lambda x: x[1])
        
        for color_name, color_value in sorted_colors:
            color_combo.addItem(color_name, color_value)
        
        # Set current color
        current_index = 0
        for i in range(color_combo.count()):
            if color_combo.itemData(i) == slot.color:
                current_index = i
                break
        color_combo.setCurrentIndex(current_index)
        form.addRow("Color:", color_combo)
        
        # Text size selector
        size_combo = QComboBox()
        size_options = [
            ("XS (Extra Small)", 0),  # Placeholder
            ("S (Small)", 0),  # Placeholder
            ("M (Medium)", 0),
            ("L (Large)", 0),  # Placeholder
            ("XL (Extra Large)", 16),
        ]
        for size_name, size_value in size_options:
            size_combo.addItem(size_name, size_value)
        
        # Set current size
        current_index = 2  # Default to M
        if slot.text_size == 16:
            current_index = 4  # XL
        elif slot.text_size == 0:
            current_index = 2  # M
        size_combo.setCurrentIndex(current_index)
        form.addRow("Text Size:", size_combo)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            new_name = name_edit.text()
            if len(new_name) > 24:
                QMessageBox.warning(self, "Warning", "Name too long. Maximum 24 characters.")
                return
            
            slot.name = new_name
            slot.color = color_combo.currentData()
            slot.text_size = size_combo.currentData()
            
            self.mark_dirty()
            self.load_setlist_slots()
    
    def create_new_setlist(self):
        """Create a new setlist."""
        from PySide6.QtWidgets import QInputDialog
        
        if not self.pcg:
            QMessageBox.warning(self, "Warning", "No PCG file loaded.")
            return
        
        # Get setlist name
        name, ok = QInputDialog.getText(
            self,
            "New Setlist",
            "Setlist Name (max 24 characters):",
            text="New Setlist"
        )
        
        if not ok or not name:
            return
        
        if len(name) > 24:
            QMessageBox.warning(self, "Warning", "Name too long. Maximum 24 characters.")
            return
        
        # Find next available setlist index
        existing_indices = [sl.index for sl in self.pcg.set_lists]
        next_index = 0
        while next_index in existing_indices and next_index < 128:
            next_index += 1
        
        if next_index >= 128:
            QMessageBox.warning(self, "Warning", "Maximum number of setlists (128) reached.")
            return
        
        # Create new setlist
        from .models import SetList, SetListSlot
        new_setlist = SetList(
            index=next_index,
            name=name,
            description="",
            color=0,
            slots=[]
        )
        
        # Create 128 empty slots
        for i in range(128):
            slot = SetListSlot(
                set_list_index=next_index,
                slot_index=i,
                name=f"Slot {i}",
                description="",
                notes="",
                patch_type="",
                patch_bank="",
                patch_index=0,
                transpose=0,
                volume=127,
                hold=False,
                color=0,
                text_size=0
            )
            new_setlist.slots.append(slot)
        
        self.pcg.set_lists.append(new_setlist)
        self.pcg.has_set_lists = True
        self.mark_dirty()
        self.load_setlists()
        
        # Select the new setlist
        for i in range(self.setlist_combo.count()):
            if self.setlist_combo.itemData(i) == new_setlist:
                self.setlist_combo.setCurrentIndex(i)
                break
        
        QMessageBox.information(self, "Success", f"Created new setlist: {name}")
    
    def edit_setlist_name(self):
        """Edit setlist name."""
        from PySide6.QtWidgets import QInputDialog
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Setlist Name",
            "Setlist Name (max 24 characters):",
            text=setlist.name
        )
        
        if ok and new_name:
            if len(new_name) > 24:
                QMessageBox.warning(self, "Warning", "Name too long. Maximum 24 characters.")
                return
            
            setlist.name = new_name
            self.mark_dirty()
            self.load_setlists()
    
    def set_setlist_color(self):
        """Set setlist color."""
        from PySide6.QtWidgets import QInputDialog
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        # Kronos color palette
        colors = [
            ("Blue", 0),
            ("Indigo", 1),
            ("Navy", 2),
            ("Olive", 3),
            ("Charcoal", 4),
            ("Sky", 5),
            ("Violet", 6),
            ("Brick", 7),
            ("Slate", 8),
            ("Lavender", 9),
            ("Cocoa", 10),
            ("Burgundy", 11)
        ]
        
        color_names = [name for name, _ in colors]
        current_color_name = color_names[setlist.color] if setlist.color < len(color_names) else color_names[0]
        
        color_name, ok = QInputDialog.getItem(
            self,
            "Set Setlist Color",
            "Choose a color:",
            color_names,
            color_names.index(current_color_name),
            False
        )
        
        if ok:
            # Find the color value
            for name, value in colors:
                if name == color_name:
                    setlist.color = value
                    self.mark_dirty()
                    QMessageBox.information(self, "Success", f"Setlist color set to {color_name}")
                    break
    
    def copy_selected(self):
        """Copy selected item."""
        QMessageBox.information(self, "Info", "Copy functionality coming soon")
    
    def paste_selected(self):
        """Paste item."""
        QMessageBox.information(self, "Info", "Paste functionality coming soon")
    
    def on_slot_selection_changed(self):
        """Handle slot selection change."""
        if not self.pcg:
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        selected_rows = self.slots_table.selectionModel().selectedRows()
        if not selected_rows:
            self.notes_text.blockSignals(True)
            self.notes_text.clear()
            self.notes_text.blockSignals(False)
            self.font_size_combo.blockSignals(True)
            self.font_size_combo.setCurrentText("M")
            self.font_size_combo.blockSignals(False)
            return
        
        row = selected_rows[0].row()
        if row < len(setlist.slots):
            slot = setlist.slots[row]
            
            # Update notes text
            self.notes_text.blockSignals(True)
            self.notes_text.setPlainText(slot.notes if slot.notes else "")
            self.notes_text.blockSignals(False)
            
            # Update font size combo to match slot's text_size
            self.font_size_combo.blockSignals(True)
            self.font_size_combo.setCurrentText(slot.text_size_name)
            self.font_size_combo.blockSignals(False)
    
    def on_notes_changed(self):
        """Handle notes text change."""
        if not self.pcg:
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        selected_rows = self.slots_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if row < len(setlist.slots):
            slot = setlist.slots[row]
            slot.notes = self.notes_text.toPlainText()
            self.mark_dirty()
    
    def on_font_size_changed(self, size_text):
        """Handle font size change for slot text size."""
        if not self.pcg:
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        selected_rows = self.slots_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if row < len(setlist.slots):
            slot = setlist.slots[row]
            
            # Map size labels to SlotTextSize enum
            from .models import SlotTextSize
            size_map = {
                "S": SlotTextSize.S,
                "XS": SlotTextSize.XS,
                "M": SlotTextSize.M,
                "L": SlotTextSize.L,
                "XL": SlotTextSize.XL
            }
            
            if size_text in size_map:
                slot.text_size = size_map[size_text]
                self.mark_dirty()
                
                # Update the table display
                if self.slots_table.item(row, 6):
                    self.slots_table.item(row, 6).setText(size_text)
    
    def mark_dirty(self):
        """Mark file as modified."""
        if not self.is_dirty:
            self.is_dirty = True
            if self.filepath:
                self.setWindowTitle(f"PCG Tools - {Path(self.filepath).name} *")
    
    def save_file(self):
        """Save current file."""
        if not self.pcg or not self.filepath:
            return
        
        try:
            write_pcg_file(self.pcg, self.filepath)
            self.is_dirty = False
            self.setWindowTitle(f"PCG Tools - {Path(self.filepath).name}")
            self.statusbar.showMessage("File saved successfully")
            QMessageBox.information(self, "Success", "File saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
    
    def save_as_file(self):
        """Save file as new name."""
        if not self.pcg:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save PCG File As",
            "",
            "PCG Files (*.PCG);;All Files (*)"
        )
        
        if filename:
            try:
                write_pcg_file(self.pcg, filename)
                self.filepath = filename
                self.is_dirty = False
                self.setWindowTitle(f"PCG Tools - {Path(filename).name}")
                self.statusbar.showMessage("File saved successfully")
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About PCG Tools",
            "PCG Tools - Korg PCG File Editor\n\n"
            "Qt Version with native macOS interface\n\n"
            "Edit programs, combis, and setlists for Korg Kronos"
        )
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.is_dirty:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Launch Qt GUI."""
    app = QApplication(sys.argv)
    app.setApplicationName("PCG Tools")
    app.setOrganizationName("PCG Tools")
    
    window = PcgMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
