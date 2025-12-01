"""Qt-based GUI for PCG Tools - Modern, native-looking interface."""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget,
    QFileDialog, QMessageBox, QComboBox, QTextEdit, QHeaderView,
    QMenuBar, QMenu, QStatusBar, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

from .reader import read_pcg_file
from .writer import write_pcg_file


class PcgMainWindow(QMainWindow):
    """Main PCG Tools window."""
    
    # Class variable to track all open windows
    _open_windows = []
    
    def __init__(self):
        super().__init__()
        self.pcg = None
        self.filepath = None
        self.is_dirty = False
        
        self.setWindowTitle("PCG Tools - Korg PCG File Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Add this window to the list of open windows
        PcgMainWindow._open_windows.append(self)
        
        self._create_menu()
        self._create_ui()
        self._create_statusbar()
        
    def _create_menu(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_window_action = QAction("&New Window", self)
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        
        file_menu.addSeparator()
        
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
        
        revert_action = QAction("&Revert to Saved", self)
        revert_action.triggered.connect(self.revert_to_saved)
        file_menu.addAction(revert_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("&Close Window", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)
        
        quit_action = QAction("&Quit All", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit_all)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_selected)
        edit_menu.addAction(paste_action)
        
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut_selected)
        edit_menu.addAction(cut_action)
        
        edit_menu.addSeparator()
        
        move_up_action = QAction("Move &Up", self)
        move_up_action.setShortcut("Ctrl+Up")
        move_up_action.triggered.connect(self.move_up)
        edit_menu.addAction(move_up_action)
        
        move_down_action = QAction("Move &Down", self)
        move_down_action.setShortcut("Ctrl+Down")
        move_down_action.triggered.connect(self.move_down)
        edit_menu.addAction(move_down_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        sort_action = QAction("&Sort Bank...", self)
        sort_action.triggered.connect(self.sort_bank)
        tools_menu.addAction(sort_action)
        
        compact_action = QAction("&Compact Bank", self)
        compact_action.triggered.connect(self.compact_bank)
        tools_menu.addAction(compact_action)
        
        remove_dupes_action = QAction("Remove &Duplicates", self)
        remove_dupes_action.triggered.connect(self.remove_duplicates)
        tools_menu.addAction(remove_dupes_action)
        
        tools_menu.addSeparator()
        
        capitalize_action = QAction("Capitalize &Names...", self)
        capitalize_action.triggered.connect(self.capitalize_names)
        tools_menu.addAction(capitalize_action)
        
        favorites_action = QAction("Move &Favorites to Top", self)
        favorites_action.triggered.connect(self.move_favorites_to_top)
        tools_menu.addAction(favorites_action)
        
        tools_menu.addSeparator()
        
        clear_action = QAction("Clear/&Initialize Selected", self)
        clear_action.triggered.connect(self.clear_selected)
        tools_menu.addAction(clear_action)
        
        auto_fill_action = QAction("Auto-&Fill Setlist Slots", self)
        auto_fill_action.triggered.connect(self.auto_fill_slots)
        tools_menu.addAction(auto_fill_action)
        
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
        main_layout = QHBoxLayout(widget)
        
        # Left side: Bank selector
        bank_widget = QWidget()
        bank_layout = QVBoxLayout(bank_widget)
        bank_layout.addWidget(QLabel("Banks:"))
        
        from PySide6.QtWidgets import QListWidget
        self.program_bank_list = QListWidget()
        self.program_bank_list.currentRowChanged.connect(self.on_program_bank_changed)
        bank_layout.addWidget(self.program_bank_list)
        
        bank_widget.setMaximumWidth(150)
        main_layout.addWidget(bank_widget)
        
        # Right side: Programs
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Filter bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        
        self.program_filter = QLineEdit()
        self.program_filter.setPlaceholderText("Type to filter by name...")
        self.program_filter.textChanged.connect(self.filter_programs)
        filter_layout.addWidget(self.program_filter)
        
        self.program_fav_filter = QCheckBox("Favorites Only")
        self.program_fav_filter.stateChanged.connect(self.filter_programs)
        filter_layout.addWidget(self.program_fav_filter)
        
        clear_filter_btn = QPushButton("Clear")
        clear_filter_btn.clicked.connect(self.clear_program_filter)
        filter_layout.addWidget(clear_filter_btn)
        
        layout.addLayout(filter_layout)
        
        self.programs_table = QTableWidget()
        self.programs_table.setColumnCount(6)
        self.programs_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Engine", "Fav"])
        self.programs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.programs_table.doubleClicked.connect(self.edit_selected)
        self.programs_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.programs_table.customContextMenuRequested.connect(self.show_program_context_menu)
        
        layout.addWidget(self.programs_table)
        
        main_layout.addWidget(right_widget)
        
        return widget
    
    def _create_combis_tab(self):
        """Create combis tab with timbre view."""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)
        
        # Left side: Bank selector
        bank_widget = QWidget()
        bank_layout = QVBoxLayout(bank_widget)
        bank_layout.addWidget(QLabel("Banks:"))
        
        from PySide6.QtWidgets import QListWidget
        self.combi_bank_list = QListWidget()
        self.combi_bank_list.currentRowChanged.connect(self.on_combi_bank_changed)
        bank_layout.addWidget(self.combi_bank_list)
        
        bank_widget.setMaximumWidth(150)
        main_layout.addWidget(bank_widget)
        
        # Right side: Combis and timbres
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Combis table
        self.combis_table = QTableWidget()
        self.combis_table.setColumnCount(5)
        self.combis_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Fav"])
        self.combis_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.combis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.combis_table.doubleClicked.connect(self.edit_selected)
        self.combis_table.itemSelectionChanged.connect(self.load_combi_timbres)
        self.combis_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.combis_table.customContextMenuRequested.connect(self.show_combi_context_menu)
        
        layout.addWidget(self.combis_table, stretch=1)
        
        # Timbres section
        timbres_label = QLabel("Timbres (select a combi above to view):")
        timbres_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(timbres_label)
        
        self.timbres_table = QTableWidget()
        self.timbres_table.setColumnCount(11)
        self.timbres_table.setHorizontalHeaderLabels([
            "#", "Program", "Program Name", "Status", "MIDI Ch", "Volume", "Transpose", 
            "Mute", "Key Zone", "Vel Zone", "Detune"
        ])
        self.timbres_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Stretch Program Name column
        self.timbres_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.timbres_table.doubleClicked.connect(self.edit_timbre)
        
        layout.addWidget(self.timbres_table, stretch=1)
        
        main_layout.addWidget(right_widget)
        
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
        self.slots_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.slots_table.customContextMenuRequested.connect(self.show_slot_context_menu)
        
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
                
                self.populate_bank_lists()
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
        
        # Get selected bank (0 = "All Banks")
        selected_bank_index = self.program_bank_list.currentRow() if hasattr(self, 'program_bank_list') else 0
        selected_bank_name = None
        if selected_bank_index > 0 and hasattr(self, 'program_bank_list'):
            selected_bank_name = self.program_bank_list.currentItem().text()
        
        program_count = 0
        for bank in self.pcg.program_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_name and bank.bank_id != selected_bank_name:
                continue
                
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
        bank_info = f" from bank {selected_bank_name}" if selected_bank_name else f" from {len(self.pcg.program_banks)} banks"
        if program_count == 0:
            self.statusbar.showMessage(f"No programs found{bank_info}")
        else:
            self.statusbar.showMessage(f"Loaded {program_count} programs{bank_info}")
    
    def load_combis(self):
        """Load combis into table."""
        self.combis_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        # Get selected bank (0 = "All Banks")
        selected_bank_index = self.combi_bank_list.currentRow() if hasattr(self, 'combi_bank_list') else 0
        selected_bank_name = None
        if selected_bank_index > 0 and hasattr(self, 'combi_bank_list'):
            selected_bank_name = self.combi_bank_list.currentItem().text()
        
        combi_count = 0
        for bank in self.pcg.combi_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_name and bank.bank_id != selected_bank_name:
                continue
                
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
        bank_info = f" from bank {selected_bank_name}" if selected_bank_name else f" from {len(self.pcg.combi_banks)} banks"
        if combi_count > 0:
            self.statusbar.showMessage(f"Loaded {combi_count} combis{bank_info}")
    
    def load_combi_timbres(self):
        """Load timbres for selected combi."""
        self.timbres_table.setRowCount(0)
        
        selected_rows = self.combis_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        combi = self._get_combi_at_row(row)
        
        if not combi or not combi.timbres:
            return
        
        # Build a program lookup dictionary for faster access
        program_lookup = {}
        if self.pcg and self.pcg.program_banks:
            for bank in self.pcg.program_banks:
                for prog in bank.patches:
                    program_lookup[prog.id] = prog.name
            
            # Debug: Print first few programs to verify lookup is working
            if len(program_lookup) > 0:
                print(f"DEBUG: Built program lookup with {len(program_lookup)} programs")
                # Print first 3 for debugging
                for i, (prog_id, prog_name) in enumerate(list(program_lookup.items())[:3]):
                    print(f"  {prog_id}: {prog_name}")
        
        for i, timbre in enumerate(combi.timbres, 1):
            timbre_row = self.timbres_table.rowCount()
            self.timbres_table.insertRow(timbre_row)
            
            # Look up program name from dictionary
            program_name = program_lookup.get(timbre.program_id, "")
            
            # Debug: Print if program not found
            if not program_name and timbre.status != "Off":
                print(f"DEBUG: Timbre {i} references '{timbre.program_id}' but program not found in lookup")
            
            self.timbres_table.setItem(timbre_row, 0, QTableWidgetItem(str(i)))
            self.timbres_table.setItem(timbre_row, 1, QTableWidgetItem(timbre.program_id))
            self.timbres_table.setItem(timbre_row, 2, QTableWidgetItem(program_name))
            self.timbres_table.setItem(timbre_row, 3, QTableWidgetItem(timbre.status))
            self.timbres_table.setItem(timbre_row, 4, QTableWidgetItem(str(timbre.midi_channel + 1)))
            self.timbres_table.setItem(timbre_row, 5, QTableWidgetItem(str(timbre.volume)))
            self.timbres_table.setItem(timbre_row, 6, QTableWidgetItem(f"{timbre.transpose:+d}"))
            self.timbres_table.setItem(timbre_row, 7, QTableWidgetItem("✓" if timbre.mute else ""))
            self.timbres_table.setItem(timbre_row, 8, QTableWidgetItem(f"{timbre.bottom_key}-{timbre.top_key}"))
            self.timbres_table.setItem(timbre_row, 9, QTableWidgetItem(f"{timbre.bottom_velocity}-{timbre.top_velocity}"))
            self.timbres_table.setItem(timbre_row, 10, QTableWidgetItem(str(timbre.detune)))
    
    def edit_timbre(self):
        """Edit selected timbre."""
        selected_rows = self.timbres_table.selectedItems()
        if not selected_rows:
            return
        
        timbre_row = selected_rows[0].row()
        
        # Get the selected combi
        combi_rows = self.combis_table.selectedItems()
        if not combi_rows:
            return
        
        combi_row = combi_rows[0].row()
        combi = self._get_combi_at_row(combi_row)
        
        if not combi or timbre_row >= len(combi.timbres):
            return
        
        timbre = combi.timbres[timbre_row]
        
        # Import and show timbre edit dialog
        from .qt_edit_dialog import QtEditTimbreDialog
        dialog = QtEditTimbreDialog(self, timbre, combi)
        if dialog.exec() and dialog.result:
            self.mark_dirty()
            self.load_combi_timbres()  # Refresh timbre display
    
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
    
    def populate_bank_lists(self):
        """Populate bank selector lists for programs, combis, and setlists."""
        if not self.pcg:
            return
        
        # Populate program banks
        self.program_bank_list.clear()
        self.program_bank_list.addItem("All Banks")
        for bank in self.pcg.program_banks:
            self.program_bank_list.addItem(bank.bank_id)
        self.program_bank_list.setCurrentRow(0)
        
        # Populate combi banks
        self.combi_bank_list.clear()
        self.combi_bank_list.addItem("All Banks")
        for bank in self.pcg.combi_banks:
            self.combi_bank_list.addItem(bank.bank_id)
        self.combi_bank_list.setCurrentRow(0)
    
    def on_program_bank_changed(self, index):
        """Handle program bank selection change."""
        self.load_programs()
    
    def on_combi_bank_changed(self, index):
        """Handle combi bank selection change."""
        self.load_combis()
    
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
        """Edit slot name, color, text size, and patch assignment."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFormLayout, QGroupBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Slot")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_form = QFormLayout()
        
        # Name field
        name_edit = QLineEdit(slot.name)
        name_edit.setMaxLength(24)
        basic_form.addRow("Name:", name_edit)
        
        # Color selector
        from .models import SLOT_COLOR_VALUES
        
        color_combo = QComboBox()
        sorted_colors = sorted(SLOT_COLOR_VALUES.items(), key=lambda x: x[1])
        
        for color_name, color_value in sorted_colors:
            color_combo.addItem(color_name, color_value)
        
        current_index = 0
        for i in range(color_combo.count()):
            if color_combo.itemData(i) == slot.color:
                current_index = i
                break
        color_combo.setCurrentIndex(current_index)
        basic_form.addRow("Color:", color_combo)
        
        # Text size selector
        size_combo = QComboBox()
        size_options = [
            ("XS (Extra Small)", 0),
            ("S (Small)", 0),
            ("M (Medium)", 0),
            ("L (Large)", 0),
            ("XL (Extra Large)", 16),
        ]
        for size_name, size_value in size_options:
            size_combo.addItem(size_name, size_value)
        
        current_index = 2  # Default to M
        if slot.text_size == 16:
            current_index = 4
        elif slot.text_size == 0:
            current_index = 2
        size_combo.setCurrentIndex(current_index)
        basic_form.addRow("Text Size:", size_combo)
        
        basic_group.setLayout(basic_form)
        layout.addWidget(basic_group)
        
        # Patch assignment group
        patch_group = QGroupBox("Patch Assignment")
        patch_form = QFormLayout()
        
        # Patch type selector
        type_combo = QComboBox()
        type_combo.addItem("(None)", "")
        type_combo.addItem("Program", "Program")
        type_combo.addItem("Combi", "Combi")
        
        # Set current type
        if slot.patch_type:
            type_combo.setCurrentText(slot.patch_type)
        patch_form.addRow("Patch Type:", type_combo)
        
        # Patch selector
        patch_combo = QComboBox()
        patch_combo.setEnabled(False)
        
        def update_patch_list():
            """Update patch list based on selected type."""
            patch_combo.clear()
            patch_type = type_combo.currentData()
            
            if not patch_type:
                patch_combo.setEnabled(False)
                return
            
            patch_combo.setEnabled(True)
            
            if patch_type == "Program":
                for bank in self.pcg.program_banks:
                    for program in bank.patches:
                        patch_combo.addItem(f"{program.id}: {program.name}", program.id)
            elif patch_type == "Combi":
                for bank in self.pcg.combi_banks:
                    for combi in bank.patches:
                        patch_combo.addItem(f"{combi.id}: {combi.name}", combi.id)
            
            # Set current patch if it exists
            if slot.patch_bank and slot.patch_type == patch_type:
                current_id = f"{slot.patch_bank}{slot.patch_index:03d}"
                for i in range(patch_combo.count()):
                    if patch_combo.itemData(i) == current_id:
                        patch_combo.setCurrentIndex(i)
                        break
        
        type_combo.currentIndexChanged.connect(update_patch_list)
        update_patch_list()  # Initial population
        
        patch_form.addRow("Patch:", patch_combo)
        
        patch_group.setLayout(patch_form)
        layout.addWidget(patch_group)
        
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
            
            # Update patch assignment
            patch_type = type_combo.currentData()
            if patch_type:
                slot.patch_type = patch_type
                patch_id = patch_combo.currentData()
                if patch_id:
                    # Parse patch ID (e.g., "I-A042" -> bank="I-A", index=42)
                    slot.patch_bank = patch_id[:-3]
                    slot.patch_index = int(patch_id[-3:])
            else:
                slot.patch_type = ""
                slot.patch_bank = ""
                slot.patch_index = 0
            
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
                notes="",
                patch_type="",
                patch_bank="",
                patch_index=0,
                hold=False,
                color=0
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
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs tab
            selected_rows = self.programs_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a program to copy")
                return
            
            row = selected_rows[0].row()
            program = self._get_program_at_row(row)
            
            if program:
                from .clipboard import get_clipboard
                clipboard = get_clipboard()
                clipboard.copy_program(program)
                
                QMessageBox.information(
                    self,
                    "Copied",
                    f"Copied program '{program.name}' ({program.id})"
                )
        
        elif current_tab == 1:  # Combis tab
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a combi to copy")
                return
            
            row = selected_rows[0].row()
            combi = self._get_combi_at_row(row)
            
            if combi:
                from .clipboard import get_clipboard
                clipboard = get_clipboard()
                clipboard.copy_combi(combi, self.pcg)
                
                # Count referenced programs
                num_programs = len(clipboard.programs)
                QMessageBox.information(
                    self, 
                    "Copied", 
                    f"Copied combi '{combi.name}' with {num_programs} referenced program(s)"
                )
        
        elif current_tab == 2:  # Setlists tab
            selected_rows = self.slots_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a slot to copy")
                return
            
            row = selected_rows[0].row()
            setlist = self.setlist_combo.currentData()
            
            if setlist:
                # Find the slot by index
                slot = None
                for s in setlist.slots:
                    if s.slot_index == row:
                        slot = s
                        break
                
                if slot:
                    from .clipboard import get_clipboard
                    clipboard = get_clipboard()
                    clipboard.copy_slot(slot)
                    
                    QMessageBox.information(
                        self,
                        "Copied",
                        f"Copied slot '{slot.name}' ({slot.patch_id})"
                    )
                else:
                    QMessageBox.warning(self, "Empty Slot", "Cannot copy an empty slot")
        
        else:
            QMessageBox.information(self, "Info", "Copy works for programs, combis, and setlist slots")
    
    def paste_selected(self):
        """Paste item with program remapping."""
        if not self.pcg:
            return
        
        from .clipboard import get_clipboard
        clipboard = get_clipboard()
        
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs tab
            if not clipboard.has_program():
                QMessageBox.warning(self, "Nothing to Paste", "Clipboard is empty. Copy a program first.")
                return
            
            selected_rows = self.programs_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a destination program")
                return
            
            row = selected_rows[0].row()
            target_program = self._get_program_at_row(row)
            
            if not target_program:
                return
            
            # Confirm paste
            reply = QMessageBox.question(
                self,
                "Paste Program",
                f"Paste '{clipboard.program.name}' to '{target_program.id}'?\n\n"
                f"This will overwrite the current program.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
            
            # Paste the program
            clipboard.paste_program(target_program)
            
            QMessageBox.information(
                self,
                "Pasted",
                f"Pasted program to '{target_program.id}'\n"
                f"Name: {target_program.name}"
            )
            
            # Mark as dirty and refresh
            self.mark_dirty()
            self.load_programs()
        
        elif current_tab == 1:  # Combis tab
            if not clipboard.has_combi():
                QMessageBox.warning(self, "Nothing to Paste", "Clipboard is empty. Copy a combi first.")
                return
            
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a destination combi")
                return
            
            row = selected_rows[0].row()
            target_combi = self._get_combi_at_row(row)
            
            if not target_combi:
                return
            
            # Ask user about program remapping
            reply = QMessageBox.question(
                self,
                "Paste Options",
                f"Paste '{clipboard.combi.name}' to '{target_combi.id}'?\n\n"
                f"This will copy {len(clipboard.programs)} referenced program(s).\n\n"
                "Do you want to remap programs to avoid conflicts?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Cancel:
                return
            
            remap_programs = (reply == QMessageBox.Yes)
            
            # Paste the combi
            program_remap = clipboard.paste_combi(target_combi, self.pcg, remap_programs)
            
            # Show results
            if program_remap:
                remap_msg = "\n".join([f"  {old} → {new}" for old, new in program_remap.items()])
                QMessageBox.information(
                    self,
                    "Pasted",
                    f"Pasted combi to '{target_combi.id}'\n\n"
                    f"Program remapping:\n{remap_msg}"
                )
            else:
                QMessageBox.information(
                    self,
                    "Pasted",
                    f"Pasted combi to '{target_combi.id}'"
                )
            
            # Mark as dirty and refresh
            self.mark_dirty()
            self.load_combis()
            self.load_programs()  # Refresh programs if they were copied
        
        elif current_tab == 2:  # Setlists tab
            if not clipboard.has_slot():
                QMessageBox.warning(self, "Nothing to Paste", "Clipboard is empty. Copy a slot first.")
                return
            
            selected_rows = self.slots_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select a destination slot")
                return
            
            row = selected_rows[0].row()
            setlist = self.setlist_combo.currentData()
            
            if not setlist:
                return
            
            # Find or create the target slot
            target_slot = None
            for s in setlist.slots:
                if s.slot_index == row:
                    target_slot = s
                    break
            
            if not target_slot:
                # Create new slot at this position
                from .models import SetListSlot
                target_slot = SetListSlot(
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
                setlist.slots.append(target_slot)
            
            # Paste the slot
            clipboard.paste_slot(target_slot)
            
            QMessageBox.information(
                self,
                "Pasted",
                f"Pasted slot to position {row}\n"
                f"Name: {target_slot.name}\n"
                f"Patch: {target_slot.patch_id}"
            )
            
            # Mark as dirty and refresh
            self.mark_dirty()
            self.load_setlist_slots()
        
        else:
            QMessageBox.information(self, "Info", "Paste works for programs, combis, and setlist slots")
    
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
    
    def show_program_context_menu(self, position):
        """Show context menu for programs table."""
        menu = QMenu()
        
        edit_action = menu.addAction("Edit Program")
        edit_action.triggered.connect(self.edit_selected)
        
        menu.addSeparator()
        
        copy_action = menu.addAction("Copy Program")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected)
        
        paste_action = menu.addAction("Paste Program")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_selected)
        
        menu.addSeparator()
        
        move_up_action = menu.addAction("Move Up")
        move_up_action.setShortcut("Ctrl+Up")
        move_up_action.triggered.connect(self.move_up)
        
        move_down_action = menu.addAction("Move Down")
        move_down_action.setShortcut("Ctrl+Down")
        move_down_action.triggered.connect(self.move_down)
        
        menu.exec_(self.programs_table.viewport().mapToGlobal(position))
    
    def show_combi_context_menu(self, position):
        """Show context menu for combis table."""
        menu = QMenu()
        
        edit_action = menu.addAction("Edit Combi")
        edit_action.triggered.connect(self.edit_selected)
        
        menu.addSeparator()
        
        copy_action = menu.addAction("Copy Combi (with programs)")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected)
        
        paste_action = menu.addAction("Paste Combi")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_selected)
        
        menu.addSeparator()
        
        move_up_action = menu.addAction("Move Up")
        move_up_action.setShortcut("Ctrl+Up")
        move_up_action.triggered.connect(self.move_up)
        
        move_down_action = menu.addAction("Move Down")
        move_down_action.setShortcut("Ctrl+Down")
        move_down_action.triggered.connect(self.move_down)
        
        menu.exec_(self.combis_table.viewport().mapToGlobal(position))
    
    def show_slot_context_menu(self, position):
        """Show context menu for slots table."""
        menu = QMenu()
        
        edit_action = menu.addAction("Edit Slot")
        edit_action.triggered.connect(self.edit_selected)
        
        menu.addSeparator()
        
        copy_action = menu.addAction("Copy Slot")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected)
        
        paste_action = menu.addAction("Paste Slot")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_selected)
        
        menu.addSeparator()
        
        move_up_action = menu.addAction("Move Up")
        move_up_action.setShortcut("Ctrl+Up")
        move_up_action.triggered.connect(self.move_up)
        
        move_down_action = menu.addAction("Move Down")
        move_down_action.setShortcut("Ctrl+Down")
        move_down_action.triggered.connect(self.move_down)
        
        menu.addSeparator()
        
        clear_action = menu.addAction("Clear Slot")
        clear_action.triggered.connect(self.clear_slot)
        
        menu.exec_(self.slots_table.viewport().mapToGlobal(position))
    
    def clear_slot(self):
        """Clear the selected slot."""
        if not self.pcg:
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        selected_rows = self.slots_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a slot to clear")
            return
        
        row = selected_rows[0].row()
        
        # Find and remove the slot
        for i, slot in enumerate(setlist.slots):
            if slot.slot_index == row:
                reply = QMessageBox.question(
                    self,
                    "Clear Slot",
                    f"Clear slot {row}: '{slot.name}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    setlist.slots.pop(i)
                    self.mark_dirty()
                    self.load_setlist_slots()
                break
    
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
    
    def revert_to_saved(self):
        """Revert to last saved version of file."""
        if not self.filepath:
            QMessageBox.information(self, "Info", "No file is currently open")
            return
        
        if not self.is_dirty:
            QMessageBox.information(self, "Info", "No changes to revert")
            return
        
        reply = QMessageBox.question(
            self,
            "Revert to Saved",
            "Discard all changes and reload the last saved version?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Reload the file
                from .reader import read_pcg_file
                self.pcg = read_pcg_file(self.filepath)
                self.is_dirty = False
                self.setWindowTitle(f"PCG Tools - {Path(self.filepath).name}")
                
                # Refresh all displays
                self.load_programs()
                self.load_combis()
                self.load_setlists()
                
                self.statusbar.showMessage("Reverted to saved version")
                QMessageBox.information(self, "Success", "File reverted to last saved version")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to revert file:\n{e}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About PCG Tools",
            "PCG Tools - Korg PCG File Editor\n\n"
            "Qt Version with native macOS interface\n\n"
            "Edit programs, combis, and setlists for Korg Kronos"
        )
    
    def new_window(self):
        """Open a new window."""
        new_win = PcgMainWindow()
        new_win.show()
    
    def quit_all(self):
        """Quit all windows."""
        # Close all windows
        for window in PcgMainWindow._open_windows[:]:  # Copy list to avoid modification during iteration
            window.close()
        
        # Quit the application
        QApplication.quit()
    
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
                return
        else:
            event.accept()
        
        # Remove this window from the tracking list
        if self in PcgMainWindow._open_windows:
            PcgMainWindow._open_windows.remove(self)
    
    def sort_bank(self):
        """Sort current bank."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab not in [0, 1]:  # Programs or Combis
            QMessageBox.information(self, "Info", "Please select Programs or Combis tab")
            return
        
        # Get current bank
        bank = None
        if current_tab == 0 and self.pcg.program_banks:
            bank = self.pcg.program_banks[0]
            bank_type = "Programs"
        elif current_tab == 1 and self.pcg.combi_banks:
            bank = self.pcg.combi_banks[0]
            bank_type = "Combis"
        
        if not bank:
            return
        
        # Show sort dialog
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Sort {bank_type}")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"Sort {bank_type} by:"))
        
        sort_combo = QComboBox()
        if current_tab == 0:  # Programs
            sort_combo.addItem("Name", "name")
            sort_combo.addItem("Category", "category")
            sort_combo.addItem("Favorite", "favorite")
            sort_combo.addItem("Engine", "engine")
        else:  # Combis
            sort_combo.addItem("Name", "name")
            sort_combo.addItem("Category", "category")
            sort_combo.addItem("Favorite", "favorite")
            sort_combo.addItem("Tempo", "tempo")
        
        layout.addWidget(sort_combo)
        
        reverse_check = QCheckBox("Reverse order (Z-A)")
        layout.addWidget(reverse_check)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Sort")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            from .batch_operations import BatchOperations
            
            sort_key = sort_combo.currentData()
            reverse = reverse_check.isChecked()
            
            if current_tab == 0:
                BatchOperations.sort_programs(bank, sort_key, reverse)
            else:
                BatchOperations.sort_combis(bank, sort_key, reverse)
            
            self.mark_dirty()
            if current_tab == 0:
                self.load_programs()
            else:
                self.load_combis()
            
            QMessageBox.information(self, "Success", f"Sorted {len(bank.patches)} {bank_type.lower()}")
    
    def compact_bank(self):
        """Compact current bank by removing empty patches."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab not in [0, 1]:
            QMessageBox.information(self, "Info", "Please select Programs or Combis tab")
            return
        
        bank = None
        if current_tab == 0 and self.pcg.program_banks:
            bank = self.pcg.program_banks[0]
            bank_type = "Programs"
        elif current_tab == 1 and self.pcg.combi_banks:
            bank = self.pcg.combi_banks[0]
            bank_type = "Combis"
        
        if not bank:
            return
        
        original_count = len(bank.patches)
        
        reply = QMessageBox.question(
            self,
            "Compact Bank",
            f"Remove empty patches from {bank_type} bank?\n\n"
            f"This will remove patches with names like 'Init', '[Empty', or blank.\n"
            f"Current count: {original_count}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from .batch_operations import BatchOperations
            BatchOperations.compact_bank(bank)
            
            removed = original_count - len(bank.patches)
            
            self.mark_dirty()
            if current_tab == 0:
                self.load_programs()
            else:
                self.load_combis()
            
            QMessageBox.information(
                self,
                "Success",
                f"Removed {removed} empty patches\n"
                f"Remaining: {len(bank.patches)}"
            )
    
    def remove_duplicates(self):
        """Remove duplicate patches from current bank."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab not in [0, 1]:
            QMessageBox.information(self, "Info", "Please select Programs or Combis tab")
            return
        
        bank = None
        if current_tab == 0 and self.pcg.program_banks:
            bank = self.pcg.program_banks[0]
            bank_type = "Programs"
        elif current_tab == 1 and self.pcg.combi_banks:
            bank = self.pcg.combi_banks[0]
            bank_type = "Combis"
        
        if not bank:
            return
        
        original_count = len(bank.patches)
        
        reply = QMessageBox.question(
            self,
            "Remove Duplicates",
            f"Remove duplicate {bank_type.lower()} by name?\n\n"
            f"This will keep only the first occurrence of each name.\n"
            f"Current count: {original_count}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from .batch_operations import BatchOperations
            BatchOperations.remove_duplicates(bank, by="name")
            
            removed = original_count - len(bank.patches)
            
            self.mark_dirty()
            if current_tab == 0:
                self.load_programs()
            else:
                self.load_combis()
            
            QMessageBox.information(
                self,
                "Success",
                f"Removed {removed} duplicate(s)\n"
                f"Remaining: {len(bank.patches)}"
            )
    
    def capitalize_names(self):
        """Capitalize patch names in current bank."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab not in [0, 1]:
            QMessageBox.information(self, "Info", "Please select Programs or Combis tab")
            return
        
        bank = None
        if current_tab == 0 and self.pcg.program_banks:
            bank = self.pcg.program_banks[0]
            bank_type = "Programs"
        elif current_tab == 1 and self.pcg.combi_banks:
            bank = self.pcg.combi_banks[0]
            bank_type = "Combis"
        
        if not bank:
            return
        
        # Show capitalize dialog
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Capitalize {bank_type} Names")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Capitalization style:"))
        
        style_combo = QComboBox()
        style_combo.addItem("Title Case (Each Word)", "title")
        style_combo.addItem("UPPER CASE", "upper")
        style_combo.addItem("lower case", "lower")
        style_combo.addItem("Sentence case", "sentence")
        
        layout.addWidget(style_combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Apply")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            from .batch_operations import BatchOperations
            
            style = style_combo.currentData()
            BatchOperations.capitalize_names(bank, style)
            
            self.mark_dirty()
            if current_tab == 0:
                self.load_programs()
            else:
                self.load_combis()
            
            QMessageBox.information(self, "Success", f"Capitalized {len(bank.patches)} names")
    
    def move_favorites_to_top(self):
        """Move favorite patches to top of bank."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab not in [0, 1]:
            QMessageBox.information(self, "Info", "Please select Programs or Combis tab")
            return
        
        bank = None
        if current_tab == 0 and self.pcg.program_banks:
            bank = self.pcg.program_banks[0]
            bank_type = "Programs"
        elif current_tab == 1 and self.pcg.combi_banks:
            bank = self.pcg.combi_banks[0]
            bank_type = "Combis"
        
        if not bank:
            return
        
        from .batch_operations import BatchOperations
        
        # Count favorites
        favorites_count = sum(1 for p in bank.patches if p.favorite)
        
        if favorites_count == 0:
            QMessageBox.information(self, "Info", "No favorite patches found")
            return
        
        BatchOperations.move_favorites_to_top(bank)
        
        self.mark_dirty()
        if current_tab == 0:
            self.load_programs()
        else:
            self.load_combis()
        
        QMessageBox.information(
            self,
            "Success",
            f"Moved {favorites_count} favorite(s) to top"
        )
    
    def move_up(self):
        """Move selected item up one position."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        from .batch_operations import BatchOperations
        
        if current_tab == 0:  # Programs
            selected_rows = self.programs_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            bank = self.pcg.program_banks[0] if self.pcg.program_banks else None
            
            if bank and BatchOperations.move_patch_up(bank, row):
                self.mark_dirty()
                self.load_programs()
                # Select the moved item
                self.programs_table.selectRow(row - 1)
        
        elif current_tab == 1:  # Combis
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            bank = self.pcg.combi_banks[0] if self.pcg.combi_banks else None
            
            if bank and BatchOperations.move_patch_up(bank, row):
                self.mark_dirty()
                self.load_combis()
                self.combis_table.selectRow(row - 1)
        
        elif current_tab == 2:  # Setlists
            selected_rows = self.slots_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            setlist = self.setlist_combo.currentData()
            
            if setlist and BatchOperations.move_slot_up(setlist, row):
                self.mark_dirty()
                self.load_setlist_slots()
                self.slots_table.selectRow(row - 1)
    
    def move_down(self):
        """Move selected item down one position."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        from .batch_operations import BatchOperations
        
        if current_tab == 0:  # Programs
            selected_rows = self.programs_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            bank = self.pcg.program_banks[0] if self.pcg.program_banks else None
            
            if bank and BatchOperations.move_patch_down(bank, row):
                self.mark_dirty()
                self.load_programs()
                self.programs_table.selectRow(row + 1)
        
        elif current_tab == 1:  # Combis
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            bank = self.pcg.combi_banks[0] if self.pcg.combi_banks else None
            
            if bank and BatchOperations.move_patch_down(bank, row):
                self.mark_dirty()
                self.load_combis()
                self.combis_table.selectRow(row + 1)
        
        elif current_tab == 2:  # Setlists
            selected_rows = self.slots_table.selectedItems()
            if not selected_rows:
                return
            
            row = selected_rows[0].row()
            setlist = self.setlist_combo.currentData()
            
            if setlist and BatchOperations.move_slot_down(setlist, row):
                self.mark_dirty()
                self.load_setlist_slots()
                self.slots_table.selectRow(row + 1)


    def clear_selected(self):
        """Clear/initialize selected patch."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            selected_rows = self.programs_table.selectedItems()
            if not selected_rows:
                QMessageBox.information(self, "Info", "Please select a program to clear")
                return
            
            row = selected_rows[0].row()
            program = self._get_program_at_row(row)
            
            if program:
                reply = QMessageBox.question(
                    self,
                    "Clear Program",
                    f"Clear program '{program.name}' ({program.id})?\n\n"
                    "This will reset it to an initialized state.",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    program.name = f"Init Program {row+1:03d}"
                    program.favorite = False
                    if program.category:
                        program.category.main_category = 0
                        program.category.sub_category = 0
                    
                    self.mark_dirty()
                    self.load_programs()
                    QMessageBox.information(self, "Success", "Program cleared")
        
        elif current_tab == 1:  # Combis
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                QMessageBox.information(self, "Info", "Please select a combi to clear")
                return
            
            row = selected_rows[0].row()
            combi = self._get_combi_at_row(row)
            
            if combi:
                reply = QMessageBox.question(
                    self,
                    "Clear Combi",
                    f"Clear combi '{combi.name}' ({combi.id})?\n\n"
                    "This will reset it to an initialized state.",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    combi.name = f"Init Combi {row+1:03d}"
                    combi.favorite = False
                    if combi.category:
                        combi.category.main_category = 0
                        combi.category.sub_category = 0
                    combi.tempo = 120
                    
                    self.mark_dirty()
                    self.load_combis()
                    QMessageBox.information(self, "Success", "Combi cleared")
    
    def auto_fill_slots(self):
        """Auto-fill setlist slots with programs or combis."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab != 2:
            QMessageBox.information(self, "Info", "Please select the Setlists tab")
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        # Show dialog to choose what to fill with
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QRadioButton, QButtonGroup
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Auto-Fill Setlist Slots")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Fill empty slots with:"))
        
        # Radio buttons for patch type
        type_group = QButtonGroup(dialog)
        programs_radio = QRadioButton("Programs")
        combis_radio = QRadioButton("Combis")
        programs_radio.setChecked(True)
        type_group.addButton(programs_radio)
        type_group.addButton(combis_radio)
        
        layout.addWidget(programs_radio)
        layout.addWidget(combis_radio)
        
        layout.addWidget(QLabel("\nFill mode:"))
        
        mode_combo = QComboBox()
        mode_combo.addItem("Fill all empty slots", "all")
        mode_combo.addItem("Fill first N slots", "first")
        layout.addWidget(mode_combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Fill")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            patch_type = "Program" if programs_radio.isChecked() else "Combi"
            
            # Get patches to fill with
            if patch_type == "Program":
                patches = []
                for bank in self.pcg.program_banks:
                    patches.extend(bank.patches)
            else:
                patches = []
                for bank in self.pcg.combi_banks:
                    patches.extend(bank.patches)
            
            if not patches:
                QMessageBox.warning(self, "Warning", f"No {patch_type.lower()}s found")
                return
            
            # Fill slots
            from .models import SetListSlot
            filled_count = 0
            
            for i, patch in enumerate(patches[:128]):  # Max 128 slots
                # Check if slot exists
                slot_exists = any(s.slot_index == i for s in setlist.slots)
                
                if not slot_exists:
                    # Create new slot
                    slot = SetListSlot(
                        set_list_index=setlist.index,
                        slot_index=i,
                        name=patch.name[:24],  # Truncate to 24 chars
                        notes="",
                        patch_type=patch_type,
                        patch_bank=patch.id[:-3],  # e.g., "I-A" from "I-A042"
                        patch_index=int(patch.id[-3:]),  # e.g., 42 from "I-A042"
                        transpose=0,
                        volume=127
                    )
                    setlist.slots.append(slot)
                    filled_count += 1
            
            self.mark_dirty()
            self.load_setlist_slots()
            
            QMessageBox.information(
                self,
                "Success",
                f"Auto-filled {filled_count} slots with {patch_type.lower()}s"
            )


    def filter_programs(self):
        """Filter programs table based on search text and favorite status."""
        if not self.pcg or not self.pcg.program_banks:
            return
        
        filter_text = self.program_filter.text().lower()
        fav_only = self.program_fav_filter.isChecked()
        
        for row in range(self.programs_table.rowCount()):
            show_row = True
            
            # Check text filter
            if filter_text:
                name_item = self.programs_table.item(row, 1)  # Name column
                if name_item and filter_text not in name_item.text().lower():
                    show_row = False
            
            # Check favorite filter
            if fav_only and show_row:
                fav_item = self.programs_table.item(row, 5)  # Fav column
                if fav_item and fav_item.text() != "★":
                    show_row = False
            
            self.programs_table.setRowHidden(row, not show_row)
    
    def clear_program_filter(self):
        """Clear program filters."""
        self.program_filter.clear()
        self.program_fav_filter.setChecked(False)
        self.filter_programs()
    
    def cut_selected(self):
        """Cut selected item (copy + clear)."""
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            # First copy
            self.copy_selected()
            
            # Then clear
            selected_rows = self.programs_table.selectedItems()
            if selected_rows:
                row = selected_rows[0].row()
                program = self._get_program_at_row(row)
                
                if program:
                    program.name = f"Init Program {row+1:03d}"
                    program.favorite = False
                    if program.category:
                        program.category.main_category = 0
                        program.category.sub_category = 0
                    
                    self.mark_dirty()
                    self.load_programs()
        
        elif current_tab == 1:  # Combis
            self.copy_selected()
            
            selected_rows = self.combis_table.selectedItems()
            if selected_rows:
                row = selected_rows[0].row()
                combi = self._get_combi_at_row(row)
                
                if combi:
                    combi.name = f"Init Combi {row+1:03d}"
                    combi.favorite = False
                    if combi.category:
                        combi.category.main_category = 0
                        combi.category.sub_category = 0
                    
                    self.mark_dirty()
                    self.load_combis()
        
        elif current_tab == 2:  # Setlists
            self.copy_selected()
            self.clear_slot()


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
