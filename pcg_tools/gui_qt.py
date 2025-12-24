"""Qt-based GUI for PCG Tools - Modern, native-looking interface."""

import sys
from pathlib import Path
from copy import deepcopy
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget,
    QFileDialog, QMessageBox, QComboBox, QTextEdit, QHeaderView,
    QMenuBar, QMenu, QStatusBar, QLineEdit, QCheckBox, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QActionGroup, QFont

from .reader import read_pcg_file
from .writer import write_pcg_file
from .undo import UndoManager, UndoableEdit, Action
from .bank_creator import insert_bank_into_pcg, get_missing_banks


class PcgMainWindow(QMainWindow):
    """Main PCG Tools window."""
    
    # Class variable to track all open windows
    _open_windows = []
    
    def __init__(self):
        super().__init__()
        self.pcg = None
        self.filepath = None
        self.is_dirty = False
        
        # Initialize undo manager
        self.undo_manager = UndoManager(max_history=50)
        self.undo_manager.add_callback(self._update_undo_menu_state)
        
        # Track last selected program or combi for Assign to Set List Slot
        # Based on C# PcgViewModel.LastSelectedProgramOrCombi
        self.last_selected_program_or_combi = None
        
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
        
        open_action = QAction("&Open PCG...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        open_sng_action = QAction("Open &SNG...", self)
        open_sng_action.setShortcut("Ctrl+Shift+O")
        open_sng_action.triggered.connect(self.open_sng_file)
        file_menu.addAction(open_sng_action)
        
        file_menu.addSeparator()
        
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
        
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut("Ctrl+Shift+Z")
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_selected)
        edit_menu.addAction(paste_action)
        
        paste_from_action = QAction("Paste from &Other Window...", self)
        paste_from_action.triggered.connect(self.paste_from_other_window)
        edit_menu.addAction(paste_from_action)
        
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut_selected)
        edit_menu.addAction(cut_action)
        
        # Exit Copy/Paste Mode and Recall - C# ExitCopyPasteModeCommand, RecallCommand
        exit_copy_paste_action = QAction("E&xit Copy/Paste Mode", self)
        exit_copy_paste_action.triggered.connect(self.exit_copy_paste_mode)
        edit_menu.addAction(exit_copy_paste_action)
        
        recall_action = QAction("&Recall", self)
        recall_action.triggered.connect(self.recall_clipboard)
        edit_menu.addAction(recall_action)
        
        edit_menu.addSeparator()
        
        move_up_action = QAction("Move &Up", self)
        move_up_action.setShortcut("Ctrl+Up")
        move_up_action.triggered.connect(self.move_up)
        edit_menu.addAction(move_up_action)
        
        move_down_action = QAction("Move &Down", self)
        move_down_action.setShortcut("Ctrl+Down")
        move_down_action.triggered.connect(self.move_down)
        edit_menu.addAction(move_down_action)
        
        edit_menu.addSeparator()
        
        # Set/Unset Favorite - C# SetFavoriteCommand/UnsetFavoriteCommand
        set_favorite_action = QAction("Set &Favorite", self)
        set_favorite_action.triggered.connect(lambda: self.set_favorite(True))
        edit_menu.addAction(set_favorite_action)
        
        unset_favorite_action = QAction("U&nset Favorite", self)
        unset_favorite_action.triggered.connect(lambda: self.set_favorite(False))
        edit_menu.addAction(unset_favorite_action)
        
        edit_menu.addSeparator()
        
        change_volume_action = QAction("Change &Volume...", self)
        change_volume_action.triggered.connect(self.change_volume)
        edit_menu.addAction(change_volume_action)
        
        edit_menu.addSeparator()
        
        # Assign to Set List Slot - C# AssignCommand
        self.assign_to_slot_action = QAction("&Assign to Set List Slot", self)
        self.assign_to_slot_action.triggered.connect(self.assign_to_setlist_slot)
        self.assign_to_slot_action.setEnabled(False)
        edit_menu.addAction(self.assign_to_slot_action)
        
        edit_menu.addSeparator()
        
        # Multi-edit actions
        edit_multiple_action = QAction("Edit &Multiple Selected...", self)
        edit_multiple_action.setShortcut("Ctrl+Shift+E")
        edit_multiple_action.triggered.connect(self.edit_multiple_selected)
        edit_menu.addAction(edit_multiple_action)
        
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
        
        init_mpe_action = QAction("Init as &MPE Combi", self)
        init_mpe_action.triggered.connect(self.init_as_mpe_combi)
        tools_menu.addAction(init_mpe_action)
        
        set_clear_prog_action = QAction("Set as Clear &Program", self)
        set_clear_prog_action.triggered.connect(self.set_as_clear_program)
        tools_menu.addAction(set_clear_prog_action)
        
        auto_fill_action = QAction("Auto-&Fill Setlist Slots", self)
        auto_fill_action.triggered.connect(self.auto_fill_slots)
        tools_menu.addAction(auto_fill_action)
        
        # Auto-Fill Slot Names - C# AutoFillInSetListSlotNamesCommand
        auto_fill_names_action = QAction("Auto-Fill Slot &Names", self)
        auto_fill_names_action.triggered.connect(self.auto_fill_slot_names)
        tools_menu.addAction(auto_fill_names_action)
        
        double_to_single_action = QAction("&Double to Single Keyboard...", self)
        double_to_single_action.triggered.connect(self.show_double_to_single)
        tools_menu.addAction(double_to_single_action)
        
        tools_menu.addSeparator()
        
        create_bank_action = QAction("Create &User Bank...", self)
        create_bank_action.triggered.connect(self.create_user_bank)
        tools_menu.addAction(create_bank_action)
        
        tools_menu.addSeparator()
        
        ref_changer_action = QAction("Program &Reference Changer...", self)
        ref_changer_action.triggered.connect(self.show_reference_changer)
        tools_menu.addAction(ref_changer_action)
        
        tools_menu.addSeparator()
        
        master_files_action = QAction("&Master Files...", self)
        master_files_action.triggered.connect(self.show_master_files)
        tools_menu.addAction(master_files_action)
        
        set_as_master_action = QAction("Set as Master &File", self)
        set_as_master_action.triggered.connect(self.set_as_master_file)
        tools_menu.addAction(set_as_master_action)
        
        tools_menu.addSeparator()
        
        # List Generator (based on C# ListGeneratorWindow)
        list_generator_action = QAction("Generate &List...", self)
        list_generator_action.triggered.connect(self.show_list_generator)
        tools_menu.addAction(list_generator_action)
        
        tools_menu.addSeparator()
        
        # Export submenu
        export_menu = tools_menu.addMenu("&Export")
        
        cubase_export_action = QAction("Export to &Cubase...", self)
        cubase_export_action.triggered.connect(self.export_to_cubase)
        export_menu.addAction(cubase_export_action)
        
        hex_export_action = QAction("&Hex Export Selected...", self)
        hex_export_action.triggered.connect(self.hex_export_selected)
        export_menu.addAction(hex_export_action)
        
        tools_menu.addSeparator()
        
        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # View menu (based on C# MainWindow.xaml View menu)
        view_menu = menubar.addMenu("&View")
        
        # Theme submenu (based on C# MainViewModel.Theme)
        theme_menu = view_menu.addMenu("&Theme")
        
        # Theme actions - checkable, mutually exclusive
        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        
        from .theme_manager import ThemeType, get_theme_name, get_theme_tooltip
        
        self.theme_generic_action = QAction(get_theme_name(ThemeType.GENERIC), self)
        self.theme_generic_action.setCheckable(True)
        self.theme_generic_action.setToolTip(get_theme_tooltip(ThemeType.GENERIC))
        self.theme_generic_action.triggered.connect(lambda: self._set_theme(ThemeType.GENERIC))
        self.theme_action_group.addAction(self.theme_generic_action)
        theme_menu.addAction(self.theme_generic_action)
        
        self.theme_luna_action = QAction(get_theme_name(ThemeType.LUNA), self)
        self.theme_luna_action.setCheckable(True)
        self.theme_luna_action.setToolTip(get_theme_tooltip(ThemeType.LUNA))
        self.theme_luna_action.triggered.connect(lambda: self._set_theme(ThemeType.LUNA))
        self.theme_action_group.addAction(self.theme_luna_action)
        theme_menu.addAction(self.theme_luna_action)
        
        self.theme_aero_action = QAction(get_theme_name(ThemeType.AERO), self)
        self.theme_aero_action.setCheckable(True)
        self.theme_aero_action.setToolTip(get_theme_tooltip(ThemeType.AERO))
        self.theme_aero_action.triggered.connect(lambda: self._set_theme(ThemeType.AERO))
        self.theme_action_group.addAction(self.theme_aero_action)
        theme_menu.addAction(self.theme_aero_action)
        
        # Set initial theme from settings
        self._update_theme_menu()
        
        view_menu.addSeparator()
        
        # Window navigation (based on C# MainWindow.xaml GotoNextWindow/GotoPreviousWindow)
        # In Python version, this navigates between tabs since we don't use MDI
        goto_next_tab_action = QAction("Goto &Next Tab", self)
        goto_next_tab_action.setShortcut("F6")
        goto_next_tab_action.triggered.connect(self._goto_next_tab)
        view_menu.addAction(goto_next_tab_action)
        
        goto_prev_tab_action = QAction("Goto &Previous Tab", self)
        goto_prev_tab_action.setShortcut("Ctrl+F6")
        goto_prev_tab_action.triggered.connect(self._goto_previous_tab)
        view_menu.addAction(goto_prev_tab_action)
        
        # Help menu (based on C# MainWindow.xaml Help menu)
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_menu.addSeparator()
        
        # Home page link (based on C# ShowHomePageCommand)
        home_page_action = QAction("PCG Tools &Home Page", self)
        home_page_action.triggered.connect(self._show_home_page)
        help_menu.addAction(home_page_action)
        
        # Manual link (based on C# ShowManualCommand)
        manual_action = QAction("&Manual", self)
        manual_action.triggered.connect(self._show_manual)
        help_menu.addAction(manual_action)
        
        help_menu.addSeparator()
        
        # GitHub repository (Python version specific)
        github_action = QAction("&GitHub Repository", self)
        github_action.triggered.connect(self._show_github)
        help_menu.addAction(github_action)
    
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
        self.tabs.addTab(self._create_drum_kits_tab(), "Drum Kits")
        self.tabs.addTab(self._create_wave_sequences_tab(), "Wave Seqs")
        self.tabs.addTab(self._create_all_patches_tab(), "All Patches")
        
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
        self.programs_table.setColumnCount(7)
        self.programs_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Engine", "Fav", "# Refs"])
        self.programs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.programs_table.doubleClicked.connect(self.edit_selected)
        self.programs_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.programs_table.customContextMenuRequested.connect(self.show_program_context_menu)
        # Track selection for Assign to Set List Slot feature
        self.programs_table.itemSelectionChanged.connect(self._track_selected_program_or_combi)
        
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
        self.combis_table.setColumnCount(6)
        self.combis_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Sub-Category", "Fav", "# Refs"])
        self.combis_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.combis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.combis_table.doubleClicked.connect(self.edit_selected)
        self.combis_table.itemSelectionChanged.connect(self.load_combi_timbres)
        # Track selection for Assign to Set List Slot feature
        self.combis_table.itemSelectionChanged.connect(self._track_selected_program_or_combi)
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
        self.timbres_table.cellClicked.connect(self.on_timbre_cell_clicked)
        self.timbres_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.timbres_table.customContextMenuRequested.connect(self.show_timbre_context_menu)
        
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
    
    def _create_drum_kits_tab(self):
        """Create drum kits tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Bank selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Bank:"))
        
        self.drum_kit_bank_combo = QComboBox()
        self.drum_kit_bank_combo.currentIndexChanged.connect(self.load_drum_kits)
        selector_layout.addWidget(self.drum_kit_bank_combo)
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Drum kits table
        self.drum_kits_table = QTableWidget()
        self.drum_kits_table.setColumnCount(3)
        self.drum_kits_table.setHorizontalHeaderLabels(["#", "ID", "Name"])
        self.drum_kits_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.drum_kits_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.drum_kits_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only for now
        
        layout.addWidget(self.drum_kits_table)
        
        return widget
    
    def _create_wave_sequences_tab(self):
        """Create wave sequences tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Bank selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Bank:"))
        
        self.wave_seq_bank_combo = QComboBox()
        self.wave_seq_bank_combo.currentIndexChanged.connect(self.load_wave_sequences)
        selector_layout.addWidget(self.wave_seq_bank_combo)
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Wave sequences table
        self.wave_seqs_table = QTableWidget()
        self.wave_seqs_table.setColumnCount(3)
        self.wave_seqs_table.setHorizontalHeaderLabels(["#", "ID", "Name"])
        self.wave_seqs_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.wave_seqs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.wave_seqs_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only for now
        
        layout.addWidget(self.wave_seqs_table)
        
        return widget
    
    def _create_all_patches_tab(self):
        """Create all patches tab - shows all patch types in a single view.
        
        Based on C# PcgWindow.SetAllPatchesGridViews() and PcgViewModel.BanksChanged().
        Shows all non-empty patches from all banks (programs, combis, set lists,
        drum kits, drum patterns, wave sequences) in a single combined list.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        # Patch type filter
        filter_layout.addWidget(QLabel("Filter Type:"))
        self.all_patches_type_filter = QComboBox()
        self.all_patches_type_filter.addItems([
            "All Types", "Programs", "Combis", "Set List Slots", 
            "Drum Kits", "Wave Sequences"
        ])
        self.all_patches_type_filter.currentIndexChanged.connect(self.load_all_patches)
        filter_layout.addWidget(self.all_patches_type_filter)
        
        filter_layout.addSpacing(20)
        
        # Text filter
        filter_layout.addWidget(QLabel("Search:"))
        self.all_patches_filter = QLineEdit()
        self.all_patches_filter.setPlaceholderText("Filter by name...")
        self.all_patches_filter.textChanged.connect(self.load_all_patches)
        filter_layout.addWidget(self.all_patches_filter)
        
        # Favorites only checkbox
        self.all_patches_fav_only = QCheckBox("Favorites Only")
        self.all_patches_fav_only.stateChanged.connect(self.load_all_patches)
        filter_layout.addWidget(self.all_patches_fav_only)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # All patches table
        # Columns based on C# SetAllPatchesGridViews: Type, ID, Name, Fav, Category, Sub-Category, Reference, Patch Name, # Refs
        self.all_patches_table = QTableWidget()
        self.all_patches_table.setColumnCount(9)
        self.all_patches_table.setHorizontalHeaderLabels([
            "Type", "ID", "Name", "Fav", "Category", "Sub-Category", 
            "Reference", "Patch Name", "# Refs"
        ])
        self.all_patches_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.all_patches_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.all_patches_table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.all_patches_table.doubleClicked.connect(self.edit_selected_all_patches)
        self.all_patches_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.all_patches_table.customContextMenuRequested.connect(self.show_all_patches_context_menu)
        
        layout.addWidget(self.all_patches_table)
        
        # Status label
        self.all_patches_status = QLabel("0 patches")
        layout.addWidget(self.all_patches_status)
        
        return widget
    
    def _create_statusbar(self):
        """Create status bar with multiple sections.
        
        Based on C# MainWindow.xaml StatusBar structure.
        Shows: Model, FileType, Programs, Combis, SetLists, DrumKits, DrumPatterns, WaveSequences, Clipboard
        """
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Create status bar labels (matching C# StatusBarItem elements)
        # Model label (blue)
        self.status_model = QLabel("")
        self.status_model.setStyleSheet("color: blue; margin-right: 8px;")
        self.statusbar.addWidget(self.status_model)
        
        # File type label
        self.status_file_type = QLabel("")
        self.status_file_type.setStyleSheet("margin-right: 8px;")
        self.statusbar.addWidget(self.status_file_type)
        
        # Programs label (dark green)
        self.status_programs = QLabel("")
        self.status_programs.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_programs)
        
        # Combis label (dark green)
        self.status_combis = QLabel("")
        self.status_combis.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_combis)
        
        # SetLists label (dark green)
        self.status_setlists = QLabel("")
        self.status_setlists.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_setlists)
        
        # DrumKits label (dark green)
        self.status_drum_kits = QLabel("")
        self.status_drum_kits.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_drum_kits)
        
        # DrumPatterns label (dark green)
        self.status_drum_patterns = QLabel("")
        self.status_drum_patterns.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_drum_patterns)
        
        # WaveSequences label (dark green)
        self.status_wave_sequences = QLabel("")
        self.status_wave_sequences.setStyleSheet("color: darkgreen; margin-right: 8px;")
        self.statusbar.addWidget(self.status_wave_sequences)
        
        # Separator and clipboard (dark red) - permanent widget on right
        self.status_clipboard = QLabel("")
        self.status_clipboard.setStyleSheet("color: darkred;")
        self.statusbar.addPermanentWidget(self.status_clipboard)
        
        self.statusbar.showMessage("Ready")
    
    def _update_status_bar_counts(self):
        """Update status bar with file statistics.
        
        Based on C# MainViewModel.RecalculateStatusBar* methods.
        """
        if not self.pcg:
            self._clear_status_bar_counts()
            return
        
        # Model (from C# StatusBarModel)
        model_name = getattr(self.pcg, 'model', 'Unknown')
        self.status_model.setText(model_name)
        
        # File type
        self.status_file_type.setText("PCG")
        
        # Programs
        self._update_status_bar_programs()
        
        # Combis
        self._update_status_bar_combis()
        
        # SetLists
        self._update_status_bar_setlists()
        
        # DrumKits
        self._update_status_bar_drum_kits()
        
        # DrumPatterns
        self._update_status_bar_drum_patterns()
        
        # WaveSequences
        self._update_status_bar_wave_sequences()
    
    def _clear_status_bar_counts(self):
        """Clear all status bar count labels."""
        self.status_model.setText("")
        self.status_file_type.setText("")
        self.status_programs.setText("")
        self.status_combis.setText("")
        self.status_setlists.setText("")
        self.status_drum_kits.setText("")
        self.status_drum_patterns.setText("")
        self.status_wave_sequences.setText("")
        self.status_clipboard.setText("")
    
    def _update_status_bar_programs(self):
        """Update programs count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarPrograms().
        """
        if not self.pcg or not self.pcg.program_banks:
            self.status_programs.setText("")
            return
        
        programs = sum(1 for bank in self.pcg.program_banks for p in bank.patches if p and p.name and p.name.strip())
        banks = sum(1 for bank in self.pcg.program_banks if any(p and p.name and p.name.strip() for p in bank.patches))
        
        if programs == 0:
            self.status_programs.setText("")
        elif programs == 1:
            if banks == 1:
                self.status_programs.setText("1 program in 1 bank")
            else:
                self.status_programs.setText(f"1 program in {banks} banks")
        else:
            if banks == 1:
                self.status_programs.setText(f"{programs} programs in 1 bank")
            else:
                self.status_programs.setText(f"{programs} programs in {banks} banks")
    
    def _update_status_bar_combis(self):
        """Update combis count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarCombis().
        """
        if not self.pcg or not self.pcg.combi_banks:
            self.status_combis.setText("")
            return
        
        combis = sum(1 for bank in self.pcg.combi_banks for c in bank.patches if c and c.name and c.name.strip())
        banks = sum(1 for bank in self.pcg.combi_banks if any(c and c.name and c.name.strip() for c in bank.patches))
        
        if combis == 0:
            self.status_combis.setText("")
        elif combis == 1:
            if banks == 1:
                self.status_combis.setText("1 combi in 1 bank")
            else:
                self.status_combis.setText(f"1 combi in {banks} banks")
        else:
            if banks == 1:
                self.status_combis.setText(f"{combis} combis in 1 bank")
            else:
                self.status_combis.setText(f"{combis} combis in {banks} banks")
    
    def _update_status_bar_setlists(self):
        """Update setlists count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarSetListSlots().
        """
        if not self.pcg or not self.pcg.set_lists:
            self.status_setlists.setText("")
            return
        
        # A slot is empty if it has no name and references Program I-A 000
        def slot_is_empty(s):
            return not s.name and s.patch_type == "Program" and s.patch_bank == "I-A" and s.patch_index == 0
        
        slots = sum(1 for sl in self.pcg.set_lists for s in sl.slots if s and not slot_is_empty(s))
        setlists = sum(1 for sl in self.pcg.set_lists if any(s and not slot_is_empty(s) for s in sl.slots))
        
        if slots == 0:
            self.status_setlists.setText("")
        elif slots == 1:
            if setlists == 1:
                self.status_setlists.setText("1 slot in 1 set list")
            else:
                self.status_setlists.setText(f"1 slot in {setlists} set lists")
        else:
            if setlists == 1:
                self.status_setlists.setText(f"{slots} slots in 1 set list")
            else:
                self.status_setlists.setText(f"{slots} slots in {setlists} set lists")
    
    def _update_status_bar_drum_kits(self):
        """Update drum kits count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarDrumKits().
        """
        if not self.pcg or not hasattr(self.pcg, 'drum_kit_banks') or not self.pcg.drum_kit_banks:
            self.status_drum_kits.setText("")
            return
        
        drum_kits = sum(1 for bank in self.pcg.drum_kit_banks for dk in bank.drum_kits if dk and dk.name and dk.name.strip())
        banks = sum(1 for bank in self.pcg.drum_kit_banks if any(dk and dk.name and dk.name.strip() for dk in bank.drum_kits))
        
        if drum_kits == 0:
            self.status_drum_kits.setText("")
        elif drum_kits == 1:
            if banks == 1:
                self.status_drum_kits.setText("1 drum kit in 1 bank")
            else:
                self.status_drum_kits.setText(f"1 drum kit in {banks} banks")
        else:
            if banks == 1:
                self.status_drum_kits.setText(f"{drum_kits} drum kits in 1 bank")
            else:
                self.status_drum_kits.setText(f"{drum_kits} drum kits in {banks} banks")
    
    def _update_status_bar_drum_patterns(self):
        """Update drum patterns count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarDrumPatterns().
        """
        if not self.pcg or not hasattr(self.pcg, 'drum_pattern_banks') or not self.pcg.drum_pattern_banks:
            self.status_drum_patterns.setText("")
            return
        
        drum_patterns = sum(1 for bank in self.pcg.drum_pattern_banks for dp in bank.drum_patterns if dp and dp.name and dp.name.strip())
        banks = sum(1 for bank in self.pcg.drum_pattern_banks if any(dp and dp.name and dp.name.strip() for dp in bank.drum_patterns))
        
        if drum_patterns == 0:
            self.status_drum_patterns.setText("")
        elif drum_patterns == 1:
            if banks == 1:
                self.status_drum_patterns.setText("1 drum pattern in 1 bank")
            else:
                self.status_drum_patterns.setText(f"1 drum pattern in {banks} banks")
        else:
            if banks == 1:
                self.status_drum_patterns.setText(f"{drum_patterns} drum patterns in 1 bank")
            else:
                self.status_drum_patterns.setText(f"{drum_patterns} drum patterns in {banks} banks")
    
    def _update_status_bar_wave_sequences(self):
        """Update wave sequences count in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarWaveSequences().
        """
        if not self.pcg or not hasattr(self.pcg, 'wave_sequence_banks') or not self.pcg.wave_sequence_banks:
            self.status_wave_sequences.setText("")
            return
        
        wave_seqs = sum(1 for bank in self.pcg.wave_sequence_banks for ws in bank.wave_sequences if ws and ws.name and ws.name.strip())
        banks = sum(1 for bank in self.pcg.wave_sequence_banks if any(ws and ws.name and ws.name.strip() for ws in bank.wave_sequences))
        
        if wave_seqs == 0:
            self.status_wave_sequences.setText("")
        elif wave_seqs == 1:
            if banks == 1:
                self.status_wave_sequences.setText("1 wave sequence in 1 bank")
            else:
                self.status_wave_sequences.setText(f"1 wave sequence in {banks} banks")
        else:
            if banks == 1:
                self.status_wave_sequences.setText(f"{wave_seqs} wave sequences in 1 bank")
            else:
                self.status_wave_sequences.setText(f"{wave_seqs} wave sequences in {banks} banks")
    
    def _update_status_bar_clipboard(self):
        """Update clipboard status in status bar.
        
        Based on C# MainViewModel.RecalculateStatusBarClipBoard().
        """
        from .clipboard import get_clipboard
        
        clipboard = get_clipboard()
        parts = []
        
        if clipboard.has_program():
            parts.append("1 program")
        
        if clipboard.has_combi():
            parts.append("1 combi")
        
        if clipboard.has_slot():
            parts.append("1 slot")
        
        if clipboard.has_drum_kit():
            parts.append("1 drum kit")
        
        if clipboard.has_wave_sequence():
            parts.append("1 wave sequence")
        
        if parts:
            self.status_clipboard.setText("Clipboard: " + ", ".join(parts))
        else:
            self.status_clipboard.setText("")
    
    def open_file(self):
        """Open a PCG file in a new window."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open PCG File",
            "",
            "PCG Files (*.PCG *.pcg);;All Files (*)"
        )
        
        if filename:
            try:
                # Always open in a new window
                new_win = PcgMainWindow()
                new_win.pcg = read_pcg_file(filename)
                new_win.filepath = filename
                new_win.is_dirty = False
                
                new_win.welcome_widget.hide()
                new_win.content_widget.show()
                
                new_win.populate_bank_lists()
                new_win.load_programs()
                new_win.load_combis()
                new_win.load_setlists()
                new_win.load_drum_kit_banks()
                new_win.load_wave_sequence_banks()
                new_win.load_all_patches()
                
                new_win.setWindowTitle(f"PCG Tools - {Path(filename).name}")
                new_win.statusbar.showMessage(f"Loaded: {Path(filename).name}")
                
                # Update status bar counts
                new_win._update_status_bar_counts()
                
                # Offset window position based on number of open windows
                # so they don't stack exactly on top of each other
                window_count = len(PcgMainWindow._open_windows)
                if window_count > 1:
                    offset = (window_count - 1) * 30
                    current_pos = new_win.pos()
                    new_win.move(current_pos.x() + offset, current_pos.y() + offset)
                
                new_win.show()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")
    
    def open_sng_file(self):
        """Open an SNG (song) file in a separate window."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open SNG File",
            "",
            "SNG Files (*.SNG *.sng);;All Files (*)"
        )
        
        if filename:
            try:
                from .sng_parser import read_sng_file
                from .qt_sng_window import SngWindow
                
                sng_file = read_sng_file(filename)
                
                # Create and show the SNG window
                sng_window = SngWindow(sng_file)
                sng_window.setWindowTitle(f"Song File - {Path(filename).name}")
                sng_window.show()
                
                # Keep a reference to prevent garbage collection
                if not hasattr(self, '_sng_windows'):
                    self._sng_windows = []
                self._sng_windows.append(sng_window)
                
                self.statusbar.showMessage(f"Opened SNG: {Path(filename).name} ({sng_file.song_count} songs, {sng_file.region_count} samples)")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open SNG file:\n{e}")
    
    def load_programs(self):
        """Load programs into table."""
        self.programs_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        from .models import format_bank_id_for_display
        from .reference_tracker import ReferenceTracker
        
        # Build reference tracker for counting
        ref_tracker = ReferenceTracker(self.pcg)
        
        # Get selected bank (0 = "All Banks")
        selected_bank_index = self.program_bank_list.currentRow() if hasattr(self, 'program_bank_list') else 0
        selected_bank_display_name = None
        if selected_bank_index > 0 and hasattr(self, 'program_bank_list'):
            selected_bank_display_name = self.program_bank_list.currentItem().text()
        
        # Check if an empty bank is selected
        if hasattr(self, '_selected_empty_bank_id') and self._selected_empty_bank_id:
            # Show 128 empty slots for the empty bank
            bank_id = self._selected_empty_bank_id
            display_bank = format_bank_id_for_display(bank_id)
            for i in range(128):
                row = self.programs_table.rowCount()
                self.programs_table.insertRow(row)
                
                id_item = QTableWidgetItem(f"{display_bank}{i:03d}")
                id_item.setForeground(Qt.gray)
                self.programs_table.setItem(row, 0, id_item)
                
                name_item = QTableWidgetItem("[Empty - Right-click to create bank]")
                name_item.setForeground(Qt.gray)
                self.programs_table.setItem(row, 1, name_item)
                
                # Empty columns for category, sub-category, engine, favorite, refs
                for col in range(2, 7):
                    empty_item = QTableWidgetItem("")
                    empty_item.setForeground(Qt.gray)
                    self.programs_table.setItem(row, col, empty_item)
            
            self.statusbar.showMessage(f"Bank {display_bank} is empty - use Tools → Create User Bank to add it")
            return
        
        program_count = 0
        for bank in self.pcg.program_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_display_name:
                bank_display_name = format_bank_id_for_display(bank.bank_id)
                # Handle [ROM] suffix in display name
                if not selected_bank_display_name.startswith(bank_display_name):
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
                
                # Reference count
                ref_count = ref_tracker.get_program_reference_count(prog.id)
                ref_item = QTableWidgetItem(str(ref_count) if ref_count > 0 else "")
                ref_item.setTextAlignment(Qt.AlignCenter)
                self.programs_table.setItem(row, 6, ref_item)
                
                program_count += 1
        
        # Update status bar with count
        bank_info = f" from bank {selected_bank_display_name}" if selected_bank_display_name else f" from {len(self.pcg.program_banks)} banks"
        if program_count == 0:
            self.statusbar.showMessage(f"No programs found{bank_info}")
        else:
            self.statusbar.showMessage(f"Loaded {program_count} programs{bank_info}")
    
    def load_combis(self):
        """Load combis into table."""
        self.combis_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        from .models import format_bank_id_for_display
        from .reference_tracker import ReferenceTracker
        
        # Build reference tracker for counting
        ref_tracker = ReferenceTracker(self.pcg)
        
        # Get selected bank (0 = "All Banks")
        selected_bank_index = self.combi_bank_list.currentRow() if hasattr(self, 'combi_bank_list') else 0
        selected_bank_display_name = None
        if selected_bank_index > 0 and hasattr(self, 'combi_bank_list'):
            selected_bank_display_name = self.combi_bank_list.currentItem().text()
        
        # Check if an empty bank is selected
        if hasattr(self, '_selected_empty_combi_bank_id') and self._selected_empty_combi_bank_id:
            # Show 128 empty slots for the empty bank
            bank_id = self._selected_empty_combi_bank_id
            display_bank = format_bank_id_for_display(bank_id)
            for i in range(128):
                row = self.combis_table.rowCount()
                self.combis_table.insertRow(row)
                
                id_item = QTableWidgetItem(f"{display_bank}{i:03d}")
                id_item.setForeground(Qt.gray)
                self.combis_table.setItem(row, 0, id_item)
                
                name_item = QTableWidgetItem("[Empty - Right-click to create bank]")
                name_item.setForeground(Qt.gray)
                self.combis_table.setItem(row, 1, name_item)
                
                # Empty columns for category, sub-category, favorite, refs
                for col in range(2, 6):
                    empty_item = QTableWidgetItem("")
                    empty_item.setForeground(Qt.gray)
                    self.combis_table.setItem(row, col, empty_item)
            
            self.statusbar.showMessage(f"Bank {display_bank} is empty - use Tools → Create User Bank to add it")
            return
        
        combi_count = 0
        for bank in self.pcg.combi_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_display_name:
                bank_display_name = format_bank_id_for_display(bank.bank_id)
                # Handle [ROM] suffix in display name
                if not selected_bank_display_name.startswith(bank_display_name):
                    continue
                
            for combi in bank.patches:
                row = self.combis_table.rowCount()
                self.combis_table.insertRow(row)
                
                self.combis_table.setItem(row, 0, QTableWidgetItem(combi.id))
                self.combis_table.setItem(row, 1, QTableWidgetItem(combi.name))
                self.combis_table.setItem(row, 2, QTableWidgetItem(str(combi.category.main_category) if combi.category else ""))
                self.combis_table.setItem(row, 3, QTableWidgetItem(str(combi.category.sub_category) if combi.category else ""))
                self.combis_table.setItem(row, 4, QTableWidgetItem("✓" if combi.favorite else ""))
                
                # Reference count (combis are referenced by set list slots)
                ref_count = ref_tracker.get_combi_reference_count(combi.id)
                ref_item = QTableWidgetItem(str(ref_count) if ref_count > 0 else "")
                ref_item.setTextAlignment(Qt.AlignCenter)
                self.combis_table.setItem(row, 5, ref_item)
                
                combi_count += 1
        
        # Update status bar with count
        bank_info = f" from bank {selected_bank_display_name}" if selected_bank_display_name else f" from {len(self.pcg.combi_banks)} banks"
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
            
            # Debug: Print first timbre details
            if i == 1:
                print(f"DEBUG: First timbre of {combi.name}:")
                print(f"  program_bank: {timbre.program_bank}")
                print(f"  program_index: {timbre.program_index}")
                print(f"  program_id: {timbre.program_id}")
            
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
    
    def on_timbre_cell_clicked(self, row, column):
        """Handle click on timbre table cell - show program selector dialog."""
        # Only handle clicks on the "Program" column (column 1)
        if column != 1:
            return
        
        if not self.pcg:
            return
        
        # Get the selected combi
        combi_rows = self.combis_table.selectedItems()
        if not combi_rows:
            return
        
        combi_row = combi_rows[0].row()
        combi = self._get_combi_at_row(combi_row)
        
        if not combi or row >= len(combi.timbres):
            return
        
        timbre = combi.timbres[row]
        
        # Show program selector dialog
        selected_program = self._show_program_selector_dialog(timbre.program_id)
        
        if selected_program:
            # Parse the program ID (e.g., "INT-A042" -> bank="I-A", index=42)
            if selected_program.startswith("INT-"):
                timbre.program_bank = "I-" + selected_program[4:-3]
            elif selected_program.startswith("USER-"):
                timbre.program_bank = "U-" + selected_program[5:-3]
            else:
                # GM, g(1)-g(9), g(d), U-AA, etc.
                timbre.program_bank = selected_program[:-3]
            
            timbre.program_index = int(selected_program[-3:])
            
            self.mark_dirty()
            self.load_combi_timbres()  # Refresh display
    
    def _show_program_selector_dialog(self, current_program_id):
        """Show a searchable, bank-organized program selector dialog."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Program")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Search box at top
        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search programs by name...")
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(search_box)
        layout.addLayout(search_layout)
        
        # Horizontal layout for banks and programs
        content_layout = QHBoxLayout()
        
        # Left: Bank list
        bank_list = QListWidget()
        bank_list.setMaximumWidth(200)
        content_layout.addWidget(bank_list)
        
        # Right: Program list
        program_list = QListWidget()
        content_layout.addWidget(program_list)
        
        layout.addLayout(content_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Populate banks
        bank_list.addItem("All Banks")
        for bank in self.pcg.program_banks:
            bank_list.addItem(f"{bank.bank_id} ({len(bank.patches)} programs)")
        
        selected_program = [None]  # Use list to allow modification in nested function
        
        def load_programs(bank_index=None, search_text=""):
            """Load programs for selected bank with optional search filter."""
            program_list.clear()
            
            search_lower = search_text.lower()
            
            if bank_index == 0 or bank_index is None:
                # All banks
                for bank in self.pcg.program_banks:
                    for prog in bank.patches:
                        if not search_text or search_lower in prog.name.lower():
                            item = QListWidgetItem(f"{prog.id}: {prog.name}")
                            item.setData(Qt.UserRole, prog.id)
                            program_list.addItem(item)
                            if prog.id == current_program_id:
                                program_list.setCurrentItem(item)
            else:
                # Specific bank
                bank = self.pcg.program_banks[bank_index - 1]
                for prog in bank.patches:
                    if not search_text or search_lower in prog.name.lower():
                        item = QListWidgetItem(f"{prog.id}: {prog.name}")
                        item.setData(Qt.UserRole, prog.id)
                        program_list.addItem(item)
                        if prog.id == current_program_id:
                            program_list.setCurrentItem(item)
        
        def on_bank_selected(row):
            load_programs(row, search_box.text())
        
        def on_search_changed(text):
            current_bank = bank_list.currentRow()
            load_programs(current_bank if current_bank >= 0 else 0, text)
        
        def on_program_double_clicked(item):
            selected_program[0] = item.data(Qt.UserRole)
            dialog.accept()
        
        def on_ok_clicked():
            current_item = program_list.currentItem()
            if current_item:
                selected_program[0] = current_item.data(Qt.UserRole)
                dialog.accept()
        
        bank_list.currentRowChanged.connect(on_bank_selected)
        search_box.textChanged.connect(on_search_changed)
        program_list.itemDoubleClicked.connect(on_program_double_clicked)
        ok_button.clicked.connect(on_ok_clicked)
        cancel_button.clicked.connect(dialog.reject)
        
        # Initial load
        bank_list.setCurrentRow(0)
        load_programs(0)
        
        # Show dialog
        if dialog.exec() == QDialog.Accepted:
            return selected_program[0]
        return None
    
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
            
            # Look up the actual patch name first (needed for both columns)
            patch_name = ""
            if slot.patch_bank and slot.patch_type and self.pcg:
                if slot.patch_type == "Program":
                    prog = self.pcg.find_program(slot.patch_bank, slot.patch_index)
                    if prog:
                        patch_name = prog.name
                elif slot.patch_type == "Combi":
                    combi = self.pcg.find_combi(slot.patch_bank, slot.patch_index)
                    if combi:
                        patch_name = combi.name
            
            # Slot Name column - show custom name, or patch name in brackets if no custom name
            from PySide6.QtGui import QColor
            if slot.name and slot.name.strip():
                # Has custom name - show it normally
                name_item = QTableWidgetItem(slot.name)
            elif patch_name:
                # No custom name but has patch - show patch name in brackets (grayed)
                name_item = QTableWidgetItem(f"[{patch_name}]")
                name_item.setForeground(QColor(128, 128, 128))  # Gray text
            else:
                # Empty slot
                name_item = QTableWidgetItem("")
            self.slots_table.setItem(row, 1, name_item)
            
            # Patch Name column (read-only - always shows actual patch name)
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
        """Populate bank selector lists for programs, combis, and setlists.
        
        Shows all possible banks (like C# version), with unloaded banks marked
        so users can create them and paste programs/combis into them.
        Engine type (EXi/HD-1) is shown for each bank.
        """
        if not self.pcg:
            return
        
        from .models import format_bank_id_for_display, get_all_program_bank_ids, get_all_combi_bank_ids
        from .bank_creator import get_bank_engine_type
        
        # Get existing bank IDs
        existing_program_banks = {bank.bank_id for bank in self.pcg.program_banks}
        existing_combi_banks = {bank.bank_id for bank in self.pcg.combi_banks}
        
        # Populate program banks - show all possible banks
        self.program_bank_list.clear()
        self.program_bank_list.addItem("All Banks")
        
        # First add existing banks with engine type
        for bank in self.pcg.program_banks:
            display_name = format_bank_id_for_display(bank.bank_id)
            # Get engine type from first program or use factory default
            engine_type = get_bank_engine_type(bank.bank_id)
            if bank.patches and hasattr(bank.patches[0], 'engine') and bank.patches[0].engine:
                engine_type = bank.patches[0].engine
            display_name += f" [{engine_type}]"
            # Add ROM indicator for read-only banks
            if bank.is_read_only:
                display_name += " [ROM]"
            self.program_bank_list.addItem(display_name)
        
        # Then add placeholder banks for banks that don't exist yet
        all_program_banks = get_all_program_bank_ids()
        for bank_id in all_program_banks:
            if bank_id not in existing_program_banks:
                display_name = format_bank_id_for_display(bank_id)
                engine_type = get_bank_engine_type(bank_id)
                item = QListWidgetItem(f"{display_name} [{engine_type}] [empty]")
                item.setForeground(Qt.gray)
                item.setData(Qt.UserRole, bank_id)  # Store bank_id for creation
                self.program_bank_list.addItem(item)
        
        self.program_bank_list.setCurrentRow(0)
        
        # Populate combi banks - show all possible banks
        self.combi_bank_list.clear()
        self.combi_bank_list.addItem("All Banks")
        
        # First add existing banks
        for bank in self.pcg.combi_banks:
            display_name = format_bank_id_for_display(bank.bank_id)
            # Add ROM indicator for read-only banks (if any)
            if bank.is_read_only:
                display_name += " [ROM]"
            self.combi_bank_list.addItem(display_name)
        
        # Then add placeholder banks for banks that don't exist yet
        all_combi_banks = get_all_combi_bank_ids()
        for bank_id in all_combi_banks:
            if bank_id not in existing_combi_banks:
                display_name = format_bank_id_for_display(bank_id)
                item = QListWidgetItem(f"{display_name} [empty]")
                item.setForeground(Qt.gray)
                item.setData(Qt.UserRole, bank_id)  # Store bank_id for creation
                self.combi_bank_list.addItem(item)
        
        self.combi_bank_list.setCurrentRow(0)
    
    def load_drum_kit_banks(self):
        """Load drum kit banks into combo box."""
        self.drum_kit_bank_combo.clear()
        
        if not self.pcg or not self.pcg.drum_kit_banks:
            self.drum_kit_bank_combo.addItem("No drum kits")
            return
        
        for bank in self.pcg.drum_kit_banks:
            count = len(bank.drum_kits)
            self.drum_kit_bank_combo.addItem(f"{bank.bank_id} ({count} kits)", bank)
        
        if self.drum_kit_bank_combo.count() > 0:
            self.drum_kit_bank_combo.setCurrentIndex(0)
    
    def load_drum_kits(self):
        """Load drum kits for selected bank."""
        self.drum_kits_table.setRowCount(0)
        
        bank = self.drum_kit_bank_combo.currentData()
        if not bank:
            return
        
        for drum_kit in bank.drum_kits:
            row = self.drum_kits_table.rowCount()
            self.drum_kits_table.insertRow(row)
            
            # Index
            idx_item = QTableWidgetItem(str(drum_kit.index))
            idx_item.setFlags(idx_item.flags() & ~Qt.ItemIsEditable)
            self.drum_kits_table.setItem(row, 0, idx_item)
            
            # ID
            id_item = QTableWidgetItem(drum_kit.id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.drum_kits_table.setItem(row, 1, id_item)
            
            # Name
            name_item = QTableWidgetItem(drum_kit.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.drum_kits_table.setItem(row, 2, name_item)
    
    def load_wave_sequence_banks(self):
        """Load wave sequence banks into combo box."""
        self.wave_seq_bank_combo.clear()
        
        if not self.pcg or not self.pcg.wave_sequence_banks:
            self.wave_seq_bank_combo.addItem("No wave sequences")
            return
        
        for bank in self.pcg.wave_sequence_banks:
            count = len(bank.wave_sequences)
            self.wave_seq_bank_combo.addItem(f"{bank.bank_id} ({count} seqs)", bank)
        
        if self.wave_seq_bank_combo.count() > 0:
            self.wave_seq_bank_combo.setCurrentIndex(0)
    
    def load_wave_sequences(self):
        """Load wave sequences for selected bank."""
        self.wave_seqs_table.setRowCount(0)
        
        bank = self.wave_seq_bank_combo.currentData()
        if not bank:
            return
        
        for wave_seq in bank.wave_sequences:
            row = self.wave_seqs_table.rowCount()
            self.wave_seqs_table.insertRow(row)
            
            # Index
            idx_item = QTableWidgetItem(str(wave_seq.index))
            idx_item.setFlags(idx_item.flags() & ~Qt.ItemIsEditable)
            self.wave_seqs_table.setItem(row, 0, idx_item)
            
            # ID
            id_item = QTableWidgetItem(wave_seq.id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.wave_seqs_table.setItem(row, 1, id_item)
            
            # Name
            name_item = QTableWidgetItem(wave_seq.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.wave_seqs_table.setItem(row, 2, name_item)
    
    def load_all_patches(self):
        """Load all patches from all banks into the All Patches table.
        
        Based on C# PcgViewModel.BanksChanged() when AllPatchesSelected is true.
        Shows all non-empty patches from programs, combis, set lists, drum kits,
        and wave sequences in a single combined view.
        """
        self.all_patches_table.setRowCount(0)
        
        if not self.pcg:
            self.all_patches_status.setText("0 patches")
            return
        
        # Get filter settings
        type_filter = self.all_patches_type_filter.currentText()
        text_filter = self.all_patches_filter.text().lower()
        fav_only = self.all_patches_fav_only.isChecked()
        
        patch_count = 0
        
        # Collect all patches based on C# implementation
        all_patches = []
        
        # Add programs (if filter allows)
        if type_filter in ["All Types", "Programs"]:
            for bank in self.pcg.program_banks:
                for prog in bank.patches:
                    # Skip empty/init patches (C#: !patch.IsEmptyOrInit)
                    if not prog.name or prog.name.strip() == "" or prog.name.startswith("Init "):
                        continue
                    all_patches.append(("Program", prog, bank))
        
        # Add combis (if filter allows)
        if type_filter in ["All Types", "Combis"]:
            for bank in self.pcg.combi_banks:
                for combi in bank.patches:
                    # Skip empty/init patches
                    if not combi.name or combi.name.strip() == "" or combi.name.startswith("Init "):
                        continue
                    all_patches.append(("Combi", combi, bank))
        
        # Add set list slots (if filter allows)
        if type_filter in ["All Types", "Set List Slots"]:
            for setlist in self.pcg.set_lists:
                for slot in setlist.slots:
                    # Skip empty slots (C#: !patch.IsEmptyOrInit)
                    # A slot is considered non-empty if it has a name or references a valid patch
                    if not slot.name and slot.patch_type == "Program" and slot.patch_bank == "I-A" and slot.patch_index == 0:
                        continue
                    all_patches.append(("Set List Slot", slot, setlist))
        
        # Add drum kits (if filter allows)
        if type_filter in ["All Types", "Drum Kits"]:
            for bank in getattr(self.pcg, 'drum_kit_banks', []) or []:
                for kit in getattr(bank, 'drum_kits', []) or []:
                    if not kit.name or kit.name.strip() == "":
                        continue
                    all_patches.append(("Drum Kit", kit, bank))
        
        # Add wave sequences (if filter allows)
        if type_filter in ["All Types", "Wave Sequences"]:
            for bank in getattr(self.pcg, 'wave_sequence_banks', []) or []:
                for ws in getattr(bank, 'wave_sequences', []) or []:
                    if not ws.name or ws.name.strip() == "":
                        continue
                    all_patches.append(("Wave Sequence", ws, bank))
        
        # Apply text filter
        if text_filter:
            all_patches = [
                (ptype, patch, bank) for ptype, patch, bank in all_patches
                if text_filter in getattr(patch, 'name', '').lower()
            ]
        
        # Apply favorites filter
        if fav_only:
            all_patches = [
                (ptype, patch, bank) for ptype, patch, bank in all_patches
                if getattr(patch, 'favorite', False)
            ]
        
        # Populate table
        for patch_type, patch, bank in all_patches:
            row = self.all_patches_table.rowCount()
            self.all_patches_table.insertRow(row)
            
            # Type column (C#: PatchTypeAsString)
            type_item = QTableWidgetItem(patch_type)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 0, type_item)
            
            # ID column
            patch_id = getattr(patch, 'id', '')
            id_item = QTableWidgetItem(patch_id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 1, id_item)
            
            # Name column
            name = getattr(patch, 'name', '')
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 2, name_item)
            
            # Fav column
            fav = getattr(patch, 'favorite', False)
            fav_item = QTableWidgetItem("✓" if fav else "")
            fav_item.setFlags(fav_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 3, fav_item)
            
            # Category column
            category = ""
            if hasattr(patch, 'category') and patch.category:
                category = str(patch.category.main_category) if hasattr(patch.category, 'main_category') else str(patch.category)
            cat_item = QTableWidgetItem(category)
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 4, cat_item)
            
            # Sub-Category column
            sub_category = ""
            if hasattr(patch, 'category') and patch.category and hasattr(patch.category, 'sub_category'):
                sub_category = str(patch.category.sub_category)
            subcat_item = QTableWidgetItem(sub_category)
            subcat_item.setFlags(subcat_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 5, subcat_item)
            
            # Reference column (for set list slots - C#: Reference/FullPatchId)
            reference = ""
            if patch_type == "Set List Slot":
                ref_type = getattr(patch, 'patch_type', 'Program')
                ref_bank = getattr(patch, 'patch_bank', '')
                ref_idx = getattr(patch, 'patch_index', 0)
                prefix = "Prg" if ref_type == "Program" else "Cmb"
                reference = f"{prefix} {ref_bank}-{ref_idx:03d}"
            ref_item = QTableWidgetItem(reference)
            ref_item.setFlags(ref_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 6, ref_item)
            
            # Patch Name column (for set list slots - C#: ProgramCombiName)
            patch_name = ""
            if patch_type == "Set List Slot":
                patch_name = self._get_referenced_patch_name(patch)
            pname_item = QTableWidgetItem(patch_name)
            pname_item.setFlags(pname_item.flags() & ~Qt.ItemIsEditable)
            self.all_patches_table.setItem(row, 7, pname_item)
            
            # # Refs column (C#: NumberOfReferencesAsString)
            ref_count = 0
            if patch_type == "Program":
                ref_count = self._count_program_references(patch)
            elif patch_type == "Combi":
                ref_count = self._count_combi_references(patch)
            refs_item = QTableWidgetItem(str(ref_count) if ref_count > 0 else "")
            refs_item.setFlags(refs_item.flags() & ~Qt.ItemIsEditable)
            refs_item.setTextAlignment(Qt.AlignCenter)
            self.all_patches_table.setItem(row, 8, refs_item)
            
            # Store patch data for later use
            type_item.setData(Qt.UserRole, (patch_type, patch, bank))
            
            patch_count += 1
        
        self.all_patches_status.setText(f"{patch_count} patches")
    
    def _get_referenced_patch_name(self, slot):
        """Get the name of the program/combi referenced by a set list slot.
        
        Based on C# SetListSlot.ProgramCombiName property.
        """
        if not self.pcg:
            return "(Unknown)"
        
        patch_type = getattr(slot, 'patch_type', 'Program')
        patch_bank = getattr(slot, 'patch_bank', '')
        patch_index = getattr(slot, 'patch_index', 0)
        
        try:
            if patch_type == "Program":
                # Find the bank by name
                for bank in self.pcg.program_banks:
                    if bank.bank_id == patch_bank:
                        if patch_index < len(bank.patches):
                            return bank.patches[patch_index].name
                        break
            elif patch_type == "Combi":
                # Find the bank by name
                for bank in self.pcg.combi_banks:
                    if bank.bank_id == patch_bank:
                        if patch_index < len(bank.patches):
                            return bank.patches[patch_index].name
                        break
        except (IndexError, AttributeError):
            pass
        
        return "(Unknown)"
    
    def _count_program_references(self, program):
        """Count how many combis and set list slots reference this program.
        
        Based on C# Program.NumberOfReferences property.
        """
        if not self.pcg:
            return 0
        
        count = 0
        prog_bank = getattr(program, 'bank', '')
        prog_idx = getattr(program, 'index', 0)
        
        # Count references in combis (timbres)
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                for timbre in getattr(combi, 'timbres', []) or []:
                    if (getattr(timbre, 'program_bank', '') == prog_bank and 
                        getattr(timbre, 'program_index', -1) == prog_idx):
                        count += 1
                        break  # Only count once per combi
        
        # Count references in set list slots
        for setlist in self.pcg.set_lists:
            for slot in setlist.slots:
                if (getattr(slot, 'patch_type', '') == 'Program' and
                    getattr(slot, 'patch_bank', '') == prog_bank and
                    getattr(slot, 'patch_index', -1) == prog_idx):
                    count += 1
        
        return count
    
    def _count_combi_references(self, combi):
        """Count how many set list slots reference this combi.
        
        Based on C# Combi.NumberOfReferences property.
        """
        if not self.pcg:
            return 0
        
        count = 0
        combi_bank = getattr(combi, 'bank', '')
        combi_idx = getattr(combi, 'index', 0)
        
        # Count references in set list slots
        for setlist in self.pcg.set_lists:
            for slot in setlist.slots:
                if (getattr(slot, 'patch_type', '') == 'Combi' and
                    getattr(slot, 'patch_bank', '') == combi_bank and
                    getattr(slot, 'patch_index', -1) == combi_idx):
                    count += 1
        
        return count
    
    def edit_selected_all_patches(self):
        """Edit the selected patch in the All Patches view."""
        selected_items = self.all_patches_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        type_item = self.all_patches_table.item(row, 0)
        if not type_item:
            return
        
        data = type_item.data(Qt.UserRole)
        if not data:
            return
        
        patch_type, patch, bank = data
        
        # Open appropriate edit dialog based on patch type
        if patch_type == "Program":
            self._edit_program_dialog(patch)
        elif patch_type == "Combi":
            self._edit_combi_dialog(patch)
        elif patch_type == "Set List Slot":
            self._edit_setlist_slot_dialog(patch, bank)
        # Drum kits and wave sequences are read-only for now
    
    def show_all_patches_context_menu(self, position):
        """Show context menu for All Patches table.
        
        Based on C# - paste is disabled in All Patches view, only copy is allowed.
        """
        menu = QMenu()
        
        selected_items = self.all_patches_table.selectedItems()
        if selected_items:
            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(self.copy_selected_all_patches)
            
            menu.addSeparator()
            
            edit_action = menu.addAction("Edit...")
            edit_action.triggered.connect(self.edit_selected_all_patches)
        
        menu.exec_(self.all_patches_table.viewport().mapToGlobal(position))
    
    def copy_selected_all_patches(self):
        """Copy selected patches from All Patches view.
        
        Based on C# CopyPasteCommands when AllPatchesSelected is true.
        Copies each patch type separately to the clipboard.
        """
        selected_rows = set()
        for item in self.all_patches_table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            return
        
        # Collect patches by type (C# copies each type separately)
        programs = []
        combis = []
        slots = []
        
        for row in selected_rows:
            type_item = self.all_patches_table.item(row, 0)
            if not type_item:
                continue
            
            data = type_item.data(Qt.UserRole)
            if not data:
                continue
            
            patch_type, patch, bank = data
            
            if patch_type == "Program":
                programs.append(patch)
            elif patch_type == "Combi":
                combis.append(patch)
            elif patch_type == "Set List Slot":
                slots.append(patch)
        
        # Copy to clipboard (simplified - just copy programs for now)
        from .clipboard import Clipboard
        clipboard = Clipboard()
        
        for prog in programs:
            clipboard.copy_program(prog)
        
        for combi in combis:
            clipboard.copy_combi(combi)
        
        # Store clipboard for paste operations
        self._clipboard = clipboard
        
        total = len(programs) + len(combis) + len(slots)
        self.statusbar.showMessage(f"Copied {total} patch(es) to clipboard")
        
        # Update clipboard status bar
        self._update_status_bar_clipboard()
    
    def on_program_bank_changed(self, index):
        """Handle program bank selection change."""
        # Store current bank for read-only checks
        self.current_program_bank = None
        self._selected_empty_bank_id = None  # Track if an empty bank is selected
        
        if index > 0 and self.pcg:
            # Check if this is an existing bank or an empty placeholder
            item = self.program_bank_list.item(index)
            empty_bank_id = item.data(Qt.UserRole) if item else None
            
            if empty_bank_id:
                # This is an empty bank - store its ID for potential creation
                self._selected_empty_bank_id = empty_bank_id
                self.current_program_bank = None
            elif self.pcg.program_banks:
                # Get the actual bank (index-1 because of "All Banks" at position 0)
                # But we need to account for the fact that empty banks are listed after existing ones
                existing_bank_count = len(self.pcg.program_banks)
                bank_index = index - 1
                if bank_index < existing_bank_count:
                    self.current_program_bank = self.pcg.program_banks[bank_index]
                    
                    # Check if this is a placeholder bank (should not happen anymore)
                    if self.current_program_bank.is_placeholder:
                        QMessageBox.information(
                            self,
                            "Bank Not Implemented",
                            f"Bank {self.current_program_bank.bank_id} is not yet implemented.\n\n"
                            f"This bank exists on the Kronos hardware but is not currently "
                            f"parsed from PCG files."
                        )
                        # Reset to "All Banks"
                        self.program_bank_list.setCurrentRow(0)
                        self.current_program_bank = None
                        return
        
        self.load_programs()
        self._update_program_buttons_state()
    
    def on_combi_bank_changed(self, index):
        """Handle combi bank selection change."""
        self._selected_empty_combi_bank_id = None  # Track if an empty bank is selected
        
        if index > 0 and self.pcg:
            # Check if this is an existing bank or an empty placeholder
            item = self.combi_bank_list.item(index)
            empty_bank_id = item.data(Qt.UserRole) if item else None
            
            if empty_bank_id:
                # This is an empty bank - store its ID for potential creation
                self._selected_empty_combi_bank_id = empty_bank_id
        
        self.load_combis()
    
    def _update_program_buttons_state(self):
        """Update program edit/paste button states based on current bank."""
        is_readonly = False
        
        if hasattr(self, 'current_program_bank') and self.current_program_bank:
            is_readonly = self.current_program_bank.is_read_only
        
        # Edit and Paste should be disabled for read-only banks
        if hasattr(self, 'edit_button'):
            self.edit_button.setEnabled(not is_readonly)
            if is_readonly:
                self.edit_button.setToolTip("Cannot edit programs in ROM banks")
            else:
                self.edit_button.setToolTip("Edit selected program")
        
        if hasattr(self, 'paste_button'):
            self.paste_button.setEnabled(not is_readonly)
            if is_readonly:
                self.paste_button.setToolTip("Cannot paste into ROM banks")
            else:
                self.paste_button.setToolTip("Paste program from clipboard")
        
        # Copy should always be enabled (can copy from ROM banks)
        if hasattr(self, 'copy_button'):
            self.copy_button.setEnabled(True)
            if is_readonly:
                self.copy_button.setToolTip("Copy program from ROM bank")
            else:
                self.copy_button.setToolTip("Copy selected program")
    
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
            # Check if current bank is read-only
            if hasattr(self, 'current_program_bank') and self.current_program_bank:
                if self.current_program_bank.is_read_only:
                    QMessageBox.warning(
                        self,
                        "ROM Bank",
                        f"Cannot edit programs in ROM bank '{self.current_program_bank.bank_id}'.\n\n"
                        f"This is a read-only bank stored in the Kronos firmware.\n"
                        f"You can copy programs from this bank to a user bank and edit them there."
                    )
                    return
            
            row = self.programs_table.currentRow()
            if row >= 0:
                # Get the program from the PCG file
                program = self._get_program_at_row(row)
                if program:
                    # Additional check: verify program is not in a ROM bank
                    for bank in self.pcg.program_banks:
                        if bank.bank_id == program.bank and bank.is_read_only:
                            QMessageBox.warning(
                                self,
                                "ROM Bank",
                                f"Cannot edit program in ROM bank '{bank.bank_id}'.\n\n"
                                f"You can copy this program to a user bank and edit it there."
                            )
                            return
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
    
    def edit_multiple_selected(self):
        """Edit multiple selected items using batch edit dialogs.
        
        Ported from C# WindowEditMultipleCombis.xaml.cs and WindowEditMultipleSetListSlots.xaml.cs
        """
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            # Get selected rows
            selected_rows = set()
            for item in self.programs_table.selectedItems():
                selected_rows.add(item.row())
            
            if len(selected_rows) < 2:
                QMessageBox.information(
                    self,
                    "Edit Multiple",
                    "Please select at least 2 programs to use batch edit.\n\n"
                    "Use Ctrl+Click or Shift+Click to select multiple items."
                )
                return
            
            # Check if any selected programs are in ROM banks
            programs = []
            for row in sorted(selected_rows):
                prog = self._get_program_at_row(row)
                if prog:
                    # Check if program is in a ROM bank
                    for bank in self.pcg.program_banks:
                        if bank.bank_id == prog.bank and bank.is_read_only:
                            QMessageBox.warning(
                                self,
                                "ROM Bank",
                                f"Cannot edit programs in ROM bank '{bank.bank_id}'.\n\n"
                                f"Please deselect ROM bank programs and try again."
                            )
                            return
                    programs.append(prog)
            
            if not programs:
                return
            
            # Open multi-edit dialog
            from .qt_multi_edit_dialog import EditMultipleProgamsDialog
            dialog = EditMultipleProgamsDialog(self, programs)
            if dialog.exec() and dialog.get_result():
                self.mark_dirty()
                self.load_programs()
        
        elif current_tab == 1:  # Combis
            # Get selected rows
            selected_rows = set()
            for item in self.combis_table.selectedItems():
                selected_rows.add(item.row())
            
            if len(selected_rows) < 2:
                QMessageBox.information(
                    self,
                    "Edit Multiple",
                    "Please select at least 2 combis to use batch edit.\n\n"
                    "Use Ctrl+Click or Shift+Click to select multiple items."
                )
                return
            
            # Get combis
            combis = []
            for row in sorted(selected_rows):
                combi = self._get_combi_at_row(row)
                if combi:
                    combis.append(combi)
            
            if not combis:
                return
            
            # Open multi-edit dialog
            from .qt_multi_edit_dialog import EditMultipleCombisDialog
            dialog = EditMultipleCombisDialog(self, combis)
            if dialog.exec() and dialog.get_result():
                self.mark_dirty()
                self.load_combis()
        
        elif current_tab == 2:  # Setlists
            # Get selected rows
            selected_rows = set()
            for item in self.slots_table.selectedItems():
                selected_rows.add(item.row())
            
            if len(selected_rows) < 2:
                QMessageBox.information(
                    self,
                    "Edit Multiple",
                    "Please select at least 2 set list slots to use batch edit.\n\n"
                    "Use Ctrl+Click or Shift+Click to select multiple items."
                )
                return
            
            # Get current setlist
            setlist = self.setlist_combo.currentData()
            if not setlist:
                return
            
            # Get slots
            slots = []
            for row in sorted(selected_rows):
                if row < 128:
                    # Find slot by index
                    slot = None
                    for s in setlist.slots:
                        if s.slot_index == row:
                            slot = s
                            break
                    
                    if slot:
                        slots.append(slot)
            
            if not slots:
                QMessageBox.information(
                    self,
                    "Edit Multiple",
                    "No valid slots selected. Please select slots that have been assigned."
                )
                return
            
            # Open multi-edit dialog
            from .qt_multi_edit_dialog import EditMultipleSetListSlotsDialog
            dialog = EditMultipleSetListSlotsDialog(self, slots)
            if dialog.exec() and dialog.get_result():
                self.mark_dirty()
                self.load_setlist_slots()
    
    def _get_program_at_row(self, row):
        """Get program at specified table row."""
        if not self.pcg:
            return None
        
        # Get selected bank filter (if any)
        selected_bank_index = self.program_bank_list.currentRow() if hasattr(self, 'program_bank_list') else 0
        selected_bank_display_name = None
        if selected_bank_index > 0 and hasattr(self, 'program_bank_list'):
            selected_bank_display_name = self.program_bank_list.currentItem().text()
        
        current_row = 0
        for bank in self.pcg.program_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_display_name:
                from .models import format_bank_id_for_display
                bank_display_name = format_bank_id_for_display(bank.bank_id)
                # Handle [ROM] suffix in display name (match load_programs logic)
                if not selected_bank_display_name.startswith(bank_display_name):
                    continue
            
            for prog in bank.patches:
                if current_row == row:
                    return prog
                current_row += 1
        return None
    
    def _get_combi_at_row(self, row):
        """Get combi at specified table row."""
        if not self.pcg:
            return None
        
        # Get selected bank filter (if any)
        selected_bank_index = self.combi_bank_list.currentRow() if hasattr(self, 'combi_bank_list') else 0
        selected_bank_display_name = None
        if selected_bank_index > 0 and hasattr(self, 'combi_bank_list'):
            selected_bank_display_name = self.combi_bank_list.currentItem().text()
        
        current_row = 0
        for bank in self.pcg.combi_banks:
            # Skip if filtering by bank and this isn't the selected bank
            if selected_bank_display_name:
                from .models import format_bank_id_for_display
                bank_display_name = format_bank_id_for_display(bank.bank_id)
                # Handle [ROM] suffix in display name (match load_combis logic)
                if not selected_bank_display_name.startswith(bank_display_name):
                    continue
            
            for combi in bank.patches:
                if current_row == row:
                    return combi
                current_row += 1
        return None
    
    def edit_program(self, program):
        """Edit a program using the Qt edit dialog."""
        from .qt_edit_dialog import QtEditPatchDialog
        
        dialog = QtEditPatchDialog(self, program, "program")
        if dialog.exec() and dialog.result:
            # Update the program with edited values
            program.name = dialog.result.get('name', program.name)
            if 'favorite' in dialog.result:
                program.favorite = dialog.result['favorite']
            if 'category' in dialog.result and program.category:
                program.category.main_category = dialog.result['category']
            
            self.mark_dirty()
            self.load_programs()  # Refresh display
    
    def edit_combi(self, combi):
        """Edit a combi using the Qt edit dialog."""
        from .qt_edit_dialog import QtEditPatchDialog
        
        dialog = QtEditPatchDialog(self, combi, "combi")
        if dialog.exec() and dialog.result:
            # Update the combi with edited values
            combi.name = dialog.result.get('name', combi.name)
            if 'favorite' in dialog.result:
                combi.favorite = dialog.result['favorite']
            if 'category' in dialog.result and combi.category:
                combi.category.main_category = dialog.result['category']
            
            self.mark_dirty()
            self.load_combis()  # Refresh display
    
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
        from .models import SlotTextSize
        size_combo = QComboBox()
        size_options = [
            ("S (Small)", SlotTextSize.S),
            ("XS (Extra Small)", SlotTextSize.XS),
            ("M (Medium)", SlotTextSize.M),
            ("L (Large)", SlotTextSize.L),
            ("XL (Extra Large)", SlotTextSize.XL),
        ]
        for size_name, size_enum in size_options:
            size_combo.addItem(size_name, size_enum)
        
        # Find current text size
        current_index = 2  # Default to M
        for i, (_, size_enum) in enumerate(size_options):
            if size_enum.value == slot._text_size:
                current_index = i
                break
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
                # Convert internal bank format to display format for matching
                from .models import format_bank_id_for_display
                display_bank = format_bank_id_for_display(slot.patch_bank)
                current_id = f"{display_bank}{slot.patch_index:03d}"
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
                    # Parse patch ID (e.g., "INT-A042" or "USER-B001")
                    # Extract bank and index
                    display_bank = patch_id[:-3]
                    index = int(patch_id[-3:])
                    
                    # Convert display format back to internal format
                    if display_bank.startswith("INT-"):
                        internal_bank = "I-" + display_bank[4:]
                    elif display_bank.startswith("USER-"):
                        internal_bank = "U-" + display_bank[5:]
                    else:
                        # GM, g(1)-g(9), g(d) remain unchanged
                        internal_bank = display_bank
                    
                    slot.patch_bank = internal_bank
                    slot.patch_index = index
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
                
                # Update clipboard status bar
                self._update_status_bar_clipboard()
                
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
                
                # Update clipboard status bar
                self._update_status_bar_clipboard()
                
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
                    
                    # Update clipboard status bar
                    self._update_status_bar_clipboard()
                    
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
            # Check if pasting into an empty bank
            if hasattr(self, '_selected_empty_bank_id') and self._selected_empty_bank_id:
                if not clipboard.has_program():
                    QMessageBox.warning(self, "Nothing to Paste", "Clipboard is empty. Copy a program first.")
                    return
                
                # Need to create the bank first
                from .bank_creator import insert_bank_into_pcg, get_bank_engine_type
                from .models import format_bank_id_for_display
                
                bank_id = self._selected_empty_bank_id
                display_name = format_bank_id_for_display(bank_id)
                source_engine = clipboard.program.engine if hasattr(clipboard.program, 'engine') else 'HD-1'
                target_engine = get_bank_engine_type(bank_id)
                
                # Check engine compatibility
                if source_engine != target_engine:
                    QMessageBox.warning(
                        self,
                        "Engine Mismatch",
                        f"Cannot paste {source_engine} program into {target_engine} bank.\n\n"
                        f"Source: {clipboard.program.name} ({source_engine})\n"
                        f"Target: {display_name} ({target_engine})\n\n"
                        f"Please select a compatible bank."
                    )
                    return
                
                # Get selected row to determine target index
                selected_rows = self.programs_table.selectedItems()
                if not selected_rows:
                    QMessageBox.warning(self, "No Selection", "Please select a destination program slot")
                    return
                
                row = selected_rows[0].row()
                
                # Confirm bank creation and paste
                reply = QMessageBox.question(
                    self,
                    "Create Bank and Paste",
                    f"Bank {display_name} doesn't exist yet.\n\n"
                    f"Create bank and paste '{clipboard.program.name}' to slot {row:03d}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.No:
                    return
                
                # Create the bank
                if not insert_bank_into_pcg(self.pcg, bank_id):
                    QMessageBox.critical(self, "Error", f"Failed to create bank {display_name}")
                    return
                
                # Clear the empty bank selection since bank now exists
                self._selected_empty_bank_id = None
                
                # Get the newly created bank and target program
                new_bank = self.pcg.get_program_bank(bank_id)
                if not new_bank or row >= len(new_bank.patches):
                    QMessageBox.critical(self, "Error", "Failed to find target program after bank creation")
                    return
                
                target_program = new_bank.patches[row]
                
                # Paste the program
                clipboard.paste_program(target_program)
                
                QMessageBox.information(
                    self,
                    "Pasted",
                    f"Created bank {display_name} and pasted program to slot {row:03d}\n"
                    f"Name: {target_program.name}"
                )
                
                # Mark as dirty and refresh
                self.mark_dirty()
                self.populate_bank_lists()  # Refresh bank list since we added a bank
                
                # Re-select the new bank
                for i in range(self.program_bank_list.count()):
                    item = self.program_bank_list.item(i)
                    if item and display_name in item.text():
                        self.program_bank_list.setCurrentRow(i)
                        break
                
                self.load_programs()
                return
            
            # Check if current bank is read-only
            if hasattr(self, 'current_program_bank') and self.current_program_bank:
                if self.current_program_bank.is_read_only:
                    QMessageBox.warning(
                        self,
                        "ROM Bank",
                        f"Cannot paste into ROM bank '{self.current_program_bank.bank_id}'.\n\n"
                        f"This is a read-only bank stored in the Kronos firmware.\n"
                        f"Please select a user bank (USER-A through USER-GG) to paste."
                    )
                    return
            
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
            
            # Check engine compatibility
            from .bank_creator import get_bank_engine_type
            source_engine = clipboard.program.engine if hasattr(clipboard.program, 'engine') else 'HD-1'
            target_engine = target_program.engine if hasattr(target_program, 'engine') else get_bank_engine_type(target_program.bank)
            
            if source_engine != target_engine:
                QMessageBox.warning(
                    self,
                    "Engine Mismatch",
                    f"Cannot paste {source_engine} program into {target_engine} slot.\n\n"
                    f"Source: {clipboard.program.name} ({source_engine})\n"
                    f"Target: {target_program.id} ({target_engine})\n\n"
                    f"Please select a compatible destination."
                )
                return
            
            # Additional check: verify target program is not in a ROM bank
            for bank in self.pcg.program_banks:
                if bank.bank_id == target_program.bank and bank.is_read_only:
                    QMessageBox.warning(
                        self,
                        "ROM Bank",
                        f"Cannot paste into ROM bank '{bank.bank_id}'.\n\n"
                        f"Please select a program in a user bank."
                    )
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
            
            # Check for user sample warning
            user_sample_warning = clipboard.get_user_sample_warning()
            
            msg = f"Pasted program to '{target_program.id}'\nName: {target_program.name}"
            if user_sample_warning:
                msg += f"\n\n⚠️ {user_sample_warning}"
            
            QMessageBox.information(self, "Pasted", msg)
            
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
            
            # Check for user sample warning
            user_sample_warning = clipboard.get_user_sample_warning()
            
            # Show results
            if program_remap:
                remap_msg = "\n".join([f"  {old} → {new}" for old, new in program_remap.items()])
                msg = f"Pasted combi to '{target_combi.id}'\n\nProgram remapping:\n{remap_msg}"
            else:
                msg = f"Pasted combi to '{target_combi.id}'"
            
            if user_sample_warning:
                msg += f"\n\n⚠️ {user_sample_warning}"
            
            QMessageBox.information(self, "Pasted", msg)
            
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
    
    def show_timbre_context_menu(self, position):
        """Show context menu for timbres table."""
        menu = QMenu()
        
        edit_action = menu.addAction("Edit Timbre")
        edit_action.triggered.connect(self.edit_timbre_selected)
        
        menu.addSeparator()
        
        move_up_action = menu.addAction("Move Up")
        move_up_action.triggered.connect(self.move_timbre_up)
        
        move_down_action = menu.addAction("Move Down")
        move_down_action.triggered.connect(self.move_timbre_down)
        
        menu.addSeparator()
        
        clear_action = menu.addAction("Clear Timbre")
        clear_action.triggered.connect(self.clear_timbre_selected)
        
        menu.addSeparator()
        
        sort_menu = menu.addMenu("Sort Timbres")
        sort_menu.addAction("By MIDI Channel").triggered.connect(lambda: self.sort_timbres("channel"))
        sort_menu.addAction("By Program").triggered.connect(lambda: self.sort_timbres("program"))
        sort_menu.addAction("By Status").triggered.connect(lambda: self.sort_timbres("status"))
        
        menu.addSeparator()
        
        clear_unused_action = menu.addAction("Clear Unused Timbres")
        clear_unused_action.triggered.connect(self.clear_unused_timbres)
        
        menu.exec_(self.timbres_table.viewport().mapToGlobal(position))
    
    def edit_timbre_selected(self):
        """Edit selected timbre."""
        selected_rows = self.timbres_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            # Get the selected combi
            combi = self._get_selected_combi()
            if combi and row < len(combi.timbres):
                self.edit_timbre(combi.timbres[row])
    
    def move_timbre_up(self):
        """Move selected timbre up."""
        if not self.pcg:
            return
        
        selected_rows = self.timbres_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        combi = self._get_selected_combi()
        
        if combi:
            from .batch_operations import BatchOperations
            if BatchOperations.move_timbre_up(combi, row):
                self.mark_dirty()
                self.load_combi_timbres()
                self.timbres_table.selectRow(row - 1)
    
    def move_timbre_down(self):
        """Move selected timbre down."""
        if not self.pcg:
            return
        
        selected_rows = self.timbres_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        combi = self._get_selected_combi()
        
        if combi:
            from .batch_operations import BatchOperations
            if BatchOperations.move_timbre_down(combi, row):
                self.mark_dirty()
                self.load_combi_timbres()
                self.timbres_table.selectRow(row + 1)
    
    def clear_timbre_selected(self):
        """Clear selected timbre."""
        if not self.pcg:
            return
        
        selected_rows = self.timbres_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a timbre to clear")
            return
        
        row = selected_rows[0].row()
        combi = self._get_selected_combi()
        
        if combi:
            reply = QMessageBox.question(
                self,
                "Clear Timbre",
                f"Clear timbre {row + 1}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from .batch_operations import BatchOperations
                if BatchOperations.clear_timbre(combi, row):
                    self.mark_dirty()
                    self.load_combi_timbres()
    
    def sort_timbres(self, key):
        """Sort timbres in selected combi."""
        if not self.pcg:
            return
        
        combi = self._get_selected_combi()
        if combi:
            from .batch_operations import BatchOperations
            BatchOperations.sort_timbres(combi, key)
            self.mark_dirty()
            self.load_combi_timbres()
            QMessageBox.information(self, "Sorted", f"Timbres sorted by {key}")
    
    def clear_unused_timbres(self):
        """Clear unused timbres in selected combi."""
        if not self.pcg:
            return
        
        combi = self._get_selected_combi()
        if combi:
            reply = QMessageBox.question(
                self,
                "Clear Unused Timbres",
                "Clear all muted or OFF timbres?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from .batch_operations import BatchOperations
                cleared = BatchOperations.clear_unused_timbres(combi)
                self.mark_dirty()
                self.load_combi_timbres()
                QMessageBox.information(self, "Cleared", f"Cleared {cleared} unused timbres")
    
    def _get_selected_combi(self):
        """Get currently selected combi."""
        selected_rows = self.combis_table.selectedItems()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        return self._get_combi_at_row(row)
    
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
            "Python/Qt Version\n\n"
            "Edit programs, combis, and setlists for Korg synthesizers\n"
            "(Kronos, Oasys, Triton, M3, Krome, etc.)\n\n"
            "Based on PCG Tools by Michel Keijzers\n"
            "Python port with PySide6 (Qt)"
        )
    
    def _show_home_page(self):
        """Open PCG Tools home page in browser.
        
        Based on C# MainViewModel.ShowHomePage().
        """
        import webbrowser
        try:
            webbrowser.open("http://pcgtools.mkspace.nl")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open home page:\n{e}"
            )
    
    def _show_manual(self):
        """Open PCG Tools manual in browser.
        
        Based on C# MainViewModel.ShowManual().
        """
        import webbrowser
        try:
            # Link to online manual/documentation
            webbrowser.open("http://pcgtools.mkspace.nl/manual")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open manual:\n{e}"
            )
    
    def _show_github(self):
        """Open GitHub repository in browser.
        
        Python version specific - links to the Python port repository.
        """
        import webbrowser
        try:
            # Original C# repository
            webbrowser.open("https://github.com/DaBlick/PCG-Tools")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open GitHub:\n{e}"
            )
    
    def _set_theme(self, theme):
        """Set application theme.
        
        Based on C# MainWindow.xaml.cs SelectedTheme property changed handler.
        
        Args:
            theme: ThemeType enum value
        """
        from .theme_manager import apply_theme, ThemeType
        from .settings import Settings, Theme
        
        # Apply theme
        apply_theme(theme)
        
        # Save to settings
        settings = Settings()
        settings.selected_theme = Theme(int(theme))
        settings.save()
        
        # Update menu checkmarks
        self._update_theme_menu()
    
    def _update_theme_menu(self):
        """Update theme menu checkmarks based on current setting."""
        from .theme_manager import ThemeType
        from .settings import Settings
        
        settings = Settings()
        current_theme = settings.selected_theme
        
        self.theme_generic_action.setChecked(current_theme == ThemeType.GENERIC)
        self.theme_luna_action.setChecked(current_theme == ThemeType.LUNA)
        self.theme_aero_action.setChecked(current_theme == ThemeType.AERO)
    
    def _goto_next_tab(self):
        """Go to next tab.
        
        Based on C# MainViewModel.GotoNextWindow - adapted for tab-based UI.
        In C# this navigates MDI child windows, in Python we navigate tabs.
        """
        if not hasattr(self, 'tabs') or not self.tabs:
            return
        
        current_index = self.tabs.currentIndex()
        tab_count = self.tabs.count()
        
        if tab_count > 0:
            next_index = (current_index + 1) % tab_count
            self.tabs.setCurrentIndex(next_index)
    
    def _goto_previous_tab(self):
        """Go to previous tab.
        
        Based on C# MainViewModel.GotoPreviousWindow - adapted for tab-based UI.
        In C# this navigates MDI child windows, in Python we navigate tabs.
        """
        if not hasattr(self, 'tabs') or not self.tabs:
            return
        
        current_index = self.tabs.currentIndex()
        tab_count = self.tabs.count()
        
        if tab_count > 0:
            prev_index = (current_index - 1 + tab_count) % tab_count
            self.tabs.setCurrentIndex(prev_index)
    
    def show_settings(self):
        """Show settings dialog."""
        from .qt_settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def export_to_cubase(self):
        """Export programs to Cubase instrument definition format."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first.")
            return
        
        from .cubase_export import export_to_cubase
        
        # Get output filename
        default_name = Path(self.filepath).stem + "_Cubase.txt" if self.filepath else "Cubase.txt"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export to Cubase",
            default_name,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                export_to_cubase(self.pcg, filename)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    f"Cubase instrument definition exported to:\n{filename}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export to Cubase:\n{str(e)}"
                )
    
    def hex_export_selected(self):
        """Show hex export for selected patches."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first.")
            return
        
        # Get selected patches from current tab
        current_tab = self.tabs.currentIndex()
        selected_patches = []
        
        if current_tab == 0:  # Programs
            selected_rows = self.programs_table.selectionModel().selectedRows()
            for row_index in selected_rows:
                row = row_index.row()
                prog_id = self.programs_table.item(row, 0).text()
                # Find the program
                for bank in self.pcg.program_banks:
                    for prog in bank.patches:
                        if prog.id == prog_id:
                            selected_patches.append(prog)
                            break
        elif current_tab == 1:  # Combis
            selected_rows = self.combis_table.selectionModel().selectedRows()
            for row_index in selected_rows:
                row = row_index.row()
                combi_id = self.combis_table.item(row, 0).text()
                # Find the combi
                for bank in self.pcg.combi_banks:
                    for combi in bank.patches:
                        if combi.id == combi_id:
                            selected_patches.append(combi)
                            break
        elif current_tab == 2:  # Setlists
            selected_rows = self.setlist_slots_table.selectionModel().selectedRows()
            for row_index in selected_rows:
                row = row_index.row()
                # Get slot from current setlist
                setlist_idx = self.setlist_list.currentRow()
                if 0 <= setlist_idx < len(self.pcg.set_lists):
                    setlist = self.pcg.set_lists[setlist_idx]
                    if 0 <= row < len(setlist.slots):
                        selected_patches.append(setlist.slots[row])
        
        if not selected_patches:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select one or more patches to export."
            )
            return
        
        from .hex_export import generate_hex_export
        from .qt_hex_export_dialog import HexExportDialog
        
        hex_text = generate_hex_export(selected_patches, self.pcg.raw_data)
        
        if not hex_text.strip():
            QMessageBox.warning(
                self,
                "No Data",
                "No hex data available for the selected patches."
            )
            return
        
        dialog = HexExportDialog(hex_text, "Hex Export", self)
        dialog.exec()
    
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
    
    def set_favorite(self, favorite: bool):
        """Set or unset favorite flag on selected programs/combis.
        
        Ported from C# PcgViewModel.SetFavorite(bool favorite).
        Works on selected programs or combis in the current view.
        """
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        
        # Only works on Programs (0) or Combis (1) tabs - not setlists
        if current_tab not in [0, 1]:
            QMessageBox.information(
                self,
                "Set Favorite",
                "Please select the Programs or Combis tab to set favorites."
            )
            return
        
        modified_count = 0
        
        if current_tab == 0:  # Programs
            selected_rows = set()
            for item in self.programs_table.selectedItems():
                selected_rows.add(item.row())
            
            if not selected_rows:
                QMessageBox.information(self, "Set Favorite", "No programs selected.")
                return
            
            for row in selected_rows:
                program = self._get_program_at_row(row)
                if program:
                    # Check if program is in a ROM bank
                    is_rom = False
                    for bank in self.pcg.program_banks:
                        if bank.bank_id == program.bank and bank.is_read_only:
                            is_rom = True
                            break
                    
                    if not is_rom:
                        program.favorite = favorite
                        modified_count += 1
            
            self.load_programs()
            
        elif current_tab == 1:  # Combis
            selected_rows = set()
            for item in self.combis_table.selectedItems():
                selected_rows.add(item.row())
            
            if not selected_rows:
                QMessageBox.information(self, "Set Favorite", "No combis selected.")
                return
            
            for row in selected_rows:
                combi = self._get_combi_at_row(row)
                if combi:
                    combi.favorite = favorite
                    modified_count += 1
            
            self.load_combis()
        
        if modified_count > 0:
            self.mark_dirty()
            action = "marked as favorite" if favorite else "unmarked as favorite"
            QMessageBox.information(
                self,
                "Set Favorite",
                f"{modified_count} patch(es) {action}."
            )
    
    def assign_to_setlist_slot(self):
        """Assign the last selected program/combi to the currently selected set list slot.
        
        Ported from C# PcgViewModel.Assign().
        Requires:
        - A program or combi was previously selected (stored in last_selected_program_or_combi)
        - Exactly one set list slot is currently selected
        """
        if not self.pcg:
            return
        
        if self.last_selected_program_or_combi is None:
            QMessageBox.information(
                self,
                "Assign to Slot",
                "No program or combi selected.\n\n"
                "First select a program or combi, then switch to the Setlists tab "
                "and select a slot to assign it to."
            )
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab != 2:  # Setlists tab
            QMessageBox.information(
                self,
                "Assign to Slot",
                "Please select a set list slot to assign the patch to."
            )
            return
        
        # Get selected slot
        selected_rows = set()
        for item in self.slots_table.selectedItems():
            selected_rows.add(item.row())
        
        if len(selected_rows) != 1:
            QMessageBox.information(
                self,
                "Assign to Slot",
                "Please select exactly one set list slot."
            )
            return
        
        slot_row = list(selected_rows)[0]
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        # Find or create the slot
        slot = None
        for s in setlist.slots:
            if s.slot_index == slot_row:
                slot = s
                break
        
        if slot is None:
            # Create new slot
            from .models import SetListSlot
            slot = SetListSlot(
                set_list_index=setlist.index,
                slot_index=slot_row,
                name="",
                notes="",
                patch_type="",
                patch_bank="",
                patch_index=0,
                transpose=0,
                volume=127
            )
            setlist.slots.append(slot)
        
        # Assign the patch to the slot
        patch = self.last_selected_program_or_combi
        patch_type, patch_obj, patch_bank = patch
        
        slot.patch_type = patch_type  # "Program" or "Combi"
        slot.patch_bank = patch_bank
        slot.patch_index = patch_obj.index if hasattr(patch_obj, 'index') else 0
        
        # Clear the last selected after assignment (per C# behavior)
        self.last_selected_program_or_combi = None
        self._update_assign_action_state()
        
        self.mark_dirty()
        self.load_setlist_slots()
        
        QMessageBox.information(
            self,
            "Assign to Slot",
            f"Assigned {patch_type} '{patch_obj.name}' to slot {slot_row}."
        )
    
    def _update_assign_action_state(self):
        """Update the enabled state of the Assign to Set List Slot action."""
        if hasattr(self, 'assign_to_slot_action'):
            enabled = self.last_selected_program_or_combi is not None
            self.assign_to_slot_action.setEnabled(enabled)
            
            # Update tooltip to show what will be assigned
            if enabled:
                patch_type, patch_obj, _ = self.last_selected_program_or_combi
                self.assign_to_slot_action.setToolTip(
                    f"Assign {patch_type}: {patch_obj.name}"
                )
            else:
                self.assign_to_slot_action.setToolTip("")
    
    def _track_selected_program_or_combi(self):
        """Track the last selected program or combi for Assign to Set List Slot.
        
        Based on C# PcgViewModel.LastSelectedProgramOrCombi.
        Called when selection changes in Programs or Combis tabs.
        """
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            selected_rows = set()
            for item in self.programs_table.selectedItems():
                selected_rows.add(item.row())
            
            if len(selected_rows) == 1:
                row = list(selected_rows)[0]
                program = self._get_program_at_row(row)
                if program:
                    # Store as tuple: (type, patch_object, bank_id)
                    self.last_selected_program_or_combi = ("Program", program, program.bank)
                    self._update_assign_action_state()
                    
        elif current_tab == 1:  # Combis
            selected_rows = set()
            for item in self.combis_table.selectedItems():
                selected_rows.add(item.row())
            
            if len(selected_rows) == 1:
                row = list(selected_rows)[0]
                combi = self._get_combi_at_row(row)
                if combi:
                    # Store as tuple: (type, patch_object, bank_id)
                    self.last_selected_program_or_combi = ("Combi", combi, combi.bank)
                    self._update_assign_action_state()
    
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

    def change_volume(self):
        """Change volume of selected combis or set list slots."""
        if not self.pcg:
            QMessageBox.information(self, "Info", "Please open a PCG file first")
            return
        
        current_tab = self.tabs.currentIndex()
        
        # Only works for combis and setlists
        if current_tab == 0:  # Programs
            QMessageBox.information(
                self, "Info", 
                "Volume change is only available for Combis and Set List Slots.\n"
                "Programs don't have a volume parameter."
            )
            return
        
        from .qt_volume_change_dialog import QtVolumeChangeDialog
        from .volume_change import (
            change_combi_volume, change_slot_volume,
            find_volume_range_combis, find_volume_range_slots,
            VolumeChangeType
        )
        
        if current_tab == 1:  # Combis
            selected_rows = self.combis_table.selectedItems()
            if not selected_rows:
                QMessageBox.information(self, "Info", "Please select one or more combis")
                return
            
            # Get unique selected rows
            rows = sorted(set(item.row() for item in selected_rows))
            combis = []
            for row in rows:
                combi = self._get_combi_at_row(row)
                if combi and combi.name.strip():  # Skip empty combis
                    combis.append(combi)
            
            if not combis:
                QMessageBox.information(self, "Info", "No non-empty combis selected")
                return
            
            # Show dialog
            dialog = QtVolumeChangeDialog(self)
            if dialog.exec() != dialog.Accepted:
                return
            
            params = dialog.get_parameters()
            
            # Calculate min/max for smart mapping
            min_val, max_val = 0, 127
            if params.change_type == VolumeChangeType.SMART_MAPPED:
                min_val, max_val = find_volume_range_combis(combis)
            
            # Apply changes
            for combi in combis:
                change_combi_volume(combi, params, min_val, max_val)
            
            self.mark_dirty()
            self.load_combis()
            QMessageBox.information(
                self, "Success", 
                f"Changed volume for {len(combis)} combi(s)"
            )
        
        elif current_tab == 2:  # Setlists
            selected_rows = self.slots_table.selectedItems()
            if not selected_rows:
                QMessageBox.information(self, "Info", "Please select one or more slots")
                return
            
            # Get unique selected rows
            rows = sorted(set(item.row() for item in selected_rows))
            setlist = self.setlist_combo.currentData()
            
            if not setlist:
                return
            
            slots = []
            for row in rows:
                if row < len(setlist.slots):
                    slot = setlist.slots[row]
                    if slot.patch_type:  # Skip empty slots
                        slots.append(slot)
            
            if not slots:
                QMessageBox.information(self, "Info", "No non-empty slots selected")
                return
            
            # Show dialog
            dialog = QtVolumeChangeDialog(self)
            if dialog.exec() != dialog.Accepted:
                return
            
            params = dialog.get_parameters()
            
            # Calculate min/max for smart mapping
            min_val, max_val = 0, 127
            if params.change_type == VolumeChangeType.SMART_MAPPED:
                min_val, max_val = find_volume_range_slots(slots)
            
            # Apply changes
            for slot in slots:
                change_slot_volume(slot, params, min_val, max_val)
            
            self.mark_dirty()
            self.load_setlist_slots()
            QMessageBox.information(
                self, "Success", 
                f"Changed volume for {len(slots)} slot(s)"
            )

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
    
    def init_as_mpe_combi(self):
        """Initialize selected combi for MPE (MIDI Polyphonic Expression)."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first.")
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab != 1:  # Combis tab
            QMessageBox.information(self, "Info", "Please select a combi in the Combis tab")
            return
        
        selected_rows = self.combis_table.selectedItems()
        if not selected_rows:
            QMessageBox.information(self, "Info", "Please select a combi to initialize for MPE")
            return
        
        row = selected_rows[0].row()
        combi = self._get_combi_at_row(row)
        
        if not combi:
            return
        
        from .mpe_init import init_combi_as_mpe, can_init_as_mpe
        
        if not can_init_as_mpe(combi):
            QMessageBox.warning(self, "Error", "Cannot initialize this combi for MPE")
            return
        
        reply = QMessageBox.question(
            self,
            "Init as MPE Combi",
            f"Initialize combi '{combi.name}' ({combi.id}) for MPE?\n\n"
            "This will:\n"
            "• Set each timbre to a unique MIDI channel (1-16)\n"
            "• Copy all parameters from timbre 1 to all other timbres\n"
            "• Copy the program reference from timbre 1 to all timbres",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            init_combi_as_mpe(combi)
            self.mark_dirty()
            QMessageBox.information(self, "Success", f"Combi '{combi.name}' initialized for MPE")
    
    def set_as_clear_program(self):
        """Set selected program as the clear program for timbres."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first.")
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab != 0:  # Programs tab
            QMessageBox.information(self, "Info", "Please select a program in the Programs tab")
            return
        
        selected_rows = self.programs_table.selectedItems()
        if not selected_rows:
            QMessageBox.information(self, "Info", "Please select a program to set as clear program")
            return
        
        row = selected_rows[0].row()
        program = self._get_program_at_row(row)
        
        if not program:
            return
        
        # Store the clear program reference
        if not hasattr(self, '_clear_program_manager'):
            from .clear_program import ClearProgramManager
            self._clear_program_manager = ClearProgramManager(self.pcg)
        
        self._clear_program_manager.assigned_clear_program = program
        
        QMessageBox.information(
            self,
            "Clear Program Set",
            f"'{program.name}' ({program.id}) is now the assigned clear program.\n\n"
            "This program will be used when clearing timbres in combis."
        )
    
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

    def auto_fill_slot_names(self):
        """Auto-fill set list slot names from referenced patch names.
        
        Ported from C# PcgViewModel.AutoFillInSetListSlotNames().
        For each selected slot that has a referenced patch, copies the patch name to the slot name.
        """
        if not self.pcg:
            return
        
        current_tab = self.tabs.currentIndex()
        if current_tab != 2:
            QMessageBox.information(self, "Info", "Please select the Setlists tab")
            return
        
        setlist = self.setlist_combo.currentData()
        if not setlist:
            return
        
        # Get selected rows
        selected_rows = set()
        for item in self.slots_table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(
                self,
                "Auto-Fill Slot Names",
                "Please select one or more slots to fill their names."
            )
            return
        
        filled_count = 0
        
        for row in selected_rows:
            # Find the slot
            slot = None
            for s in setlist.slots:
                if s.slot_index == row:
                    slot = s
                    break
            
            if slot and slot.patch_type:
                # Get the referenced patch name
                patch_name = self._get_patch_name_for_slot(slot)
                if patch_name:
                    slot.name = patch_name[:24]  # Truncate to 24 chars (slot name limit)
                    filled_count += 1
        
        if filled_count > 0:
            self.mark_dirty()
            self.load_setlist_slots()
            QMessageBox.information(
                self,
                "Auto-Fill Slot Names",
                f"Filled {filled_count} slot name(s) from referenced patches."
            )
        else:
            QMessageBox.information(
                self,
                "Auto-Fill Slot Names",
                "No slots with valid patch references were selected."
            )
    
    def _get_patch_name_for_slot(self, slot) -> str:
        """Get the name of the patch referenced by a set list slot.
        
        Returns the patch name or empty string if not found.
        """
        if not slot.patch_type or not slot.patch_bank:
            return ""
        
        if slot.patch_type == "Program":
            for bank in self.pcg.program_banks:
                if bank.bank_id == slot.patch_bank:
                    if 0 <= slot.patch_index < len(bank.patches):
                        return bank.patches[slot.patch_index].name
        elif slot.patch_type == "Combi":
            for bank in self.pcg.combi_banks:
                if bank.bank_id == slot.patch_bank:
                    if 0 <= slot.patch_index < len(bank.patches):
                        return bank.patches[slot.patch_index].name
        
        return ""

    def show_double_to_single(self):
        """Show the Double to Single Keyboard Setup dialog."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first.")
            return
        
        if not self.pcg.set_lists:
            QMessageBox.warning(self, "No Set Lists", "This file does not contain set lists.")
            return
        
        from .qt_double_to_single_dialog import DoubleToSingleKeyboardDialog
        
        dialog = DoubleToSingleKeyboardDialog(self.pcg, self)
        if dialog.exec() == dialog.Accepted:
            self.mark_dirty()
            self.load_setlist_slots()
            self.load_combis()


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
    
    def exit_copy_paste_mode(self):
        """Exit copy/paste mode and clear clipboard.
        
        Ported from C# PcgViewModel.ExitCopyPasteModeCommand.
        Clears the clipboard and resets any copy/paste state.
        """
        from .clipboard import get_clipboard
        clipboard = get_clipboard()
        clipboard.exit_copy_paste_mode()
        
        # Update status bar to show clipboard is empty
        self._update_status_bar_clipboard()
        
        QMessageBox.information(
            self,
            "Copy/Paste Mode",
            "Clipboard cleared. Copy/paste mode exited."
        )
    
    def recall_clipboard(self):
        """Recall previously memorized clipboard contents.
        
        Ported from C# PcgViewModel.RecallCommand.
        Restores the clipboard to its previous state before the last copy operation.
        """
        from .clipboard import get_clipboard
        clipboard = get_clipboard()
        
        if not clipboard.has_memory():
            QMessageBox.information(
                self,
                "Recall",
                "No previous clipboard contents to recall.\n\n"
                "The clipboard memory is set when you copy a new item."
            )
            return
        
        clipboard.recall()
        
        # Update status bar
        self._update_status_bar_clipboard()
        
        # Show what was recalled
        recalled_items = []
        if clipboard.has_program():
            recalled_items.append(f"Program: {clipboard.program.name}")
        if clipboard.has_combi():
            recalled_items.append(f"Combi: {clipboard.combi.name}")
        if clipboard.has_slot():
            recalled_items.append(f"Slot: {clipboard.slot.name}")
        if clipboard.has_drum_kit():
            recalled_items.append(f"Drum Kit: {clipboard.drum_kit.name}")
        if clipboard.has_wave_sequence():
            recalled_items.append(f"Wave Sequence: {clipboard.wave_sequence.name}")
        
        if recalled_items:
            QMessageBox.information(
                self,
                "Recall",
                f"Recalled clipboard contents:\n" + "\n".join(recalled_items)
            )
        else:
            QMessageBox.information(
                self,
                "Recall",
                "Clipboard recalled (empty)."
            )
    
    # ==================== Undo/Redo Support ====================
    
    def _update_undo_menu_state(self):
        """Update undo/redo menu item states."""
        if hasattr(self, 'undo_action'):
            can_undo = self.undo_manager.can_undo()
            self.undo_action.setEnabled(can_undo)
            if can_undo:
                desc = self.undo_manager.get_undo_description()
                self.undo_action.setText(f"&Undo {desc}" if desc else "&Undo")
            else:
                self.undo_action.setText("&Undo")
        
        if hasattr(self, 'redo_action'):
            can_redo = self.undo_manager.can_redo()
            self.redo_action.setEnabled(can_redo)
            if can_redo:
                desc = self.undo_manager.get_redo_description()
                self.redo_action.setText(f"&Redo {desc}" if desc else "&Redo")
            else:
                self.redo_action.setText("&Redo")
    
    def undo(self):
        """Undo the last action."""
        if self.undo_manager.can_undo():
            try:
                self.undo_manager.undo()
                self.mark_dirty()
                self._refresh_current_view()
                self.statusbar.showMessage("Undone: " + (self.undo_manager.get_redo_description() or "action"))
            except Exception as e:
                QMessageBox.warning(self, "Undo Failed", f"Could not undo: {e}")
    
    def redo(self):
        """Redo the last undone action."""
        if self.undo_manager.can_redo():
            try:
                self.undo_manager.redo()
                self.mark_dirty()
                self._refresh_current_view()
                self.statusbar.showMessage("Redone: " + (self.undo_manager.get_undo_description() or "action"))
            except Exception as e:
                QMessageBox.warning(self, "Redo Failed", f"Could not redo: {e}")
    
    def _refresh_current_view(self):
        """Refresh the current tab's view."""
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            self.load_programs()
        elif current_tab == 1:
            self.load_combis()
        elif current_tab == 2:
            self.load_setlist_slots()
    
    def _create_undo_action_for_patch(self, patch, description: str):
        """Create an undo action that saves/restores a patch's state."""
        old_state = deepcopy(patch)
        
        def undo(data):
            # Restore old state
            patch.name = data['old'].name
            patch.category = deepcopy(data['old'].category) if data['old'].category else None
            patch.favorite = data['old'].favorite
            if hasattr(patch, 'raw_data') and hasattr(data['old'], 'raw_data'):
                patch.raw_data = data['old'].raw_data
        
        def redo(data):
            # Restore new state
            patch.name = data['new'].name
            patch.category = deepcopy(data['new'].category) if data['new'].category else None
            patch.favorite = data['new'].favorite
            if hasattr(patch, 'raw_data') and hasattr(data['new'], 'raw_data'):
                patch.raw_data = data['new'].raw_data
        
        return Action(
            description=description,
            undo_func=undo,
            redo_func=redo,
            undo_data={'old': old_state, 'new': None},
            redo_data={'old': old_state, 'new': None}
        )
    
    def _finalize_undo_action(self, action, patch):
        """Finalize an undo action with the new state after modification."""
        new_state = deepcopy(patch)
        action.undo_data['new'] = new_state
        action.redo_data['new'] = new_state
        self.undo_manager.add_action(action)
    
    # ==================== Cross-File Copy/Paste ====================
    
    def paste_from_other_window(self):
        """Paste from another open PCG window."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first")
            return
        
        # Get list of other windows with loaded files
        other_windows = [w for w in PcgMainWindow._open_windows 
                        if w != self and w.pcg is not None]
        
        if not other_windows:
            QMessageBox.information(
                self, 
                "No Other Files",
                "No other PCG files are open.\n\n"
                "Open another PCG file (File → Open PCG...),\n"
                "then use this command to paste from it."
            )
            return
        
        # Show dialog to select source window and patch
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QDialogButtonBox, QGroupBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Paste from Other File")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Source file selection
        file_group = QGroupBox("Source File")
        file_layout = QVBoxLayout(file_group)
        file_list = QListWidget()
        for w in other_windows:
            filename = Path(w.filepath).name if w.filepath else "Untitled"
            file_list.addItem(filename)
        file_layout.addWidget(file_list)
        layout.addWidget(file_group)
        
        # Patch selection
        patch_group = QGroupBox("Select Patch to Copy")
        patch_layout = QVBoxLayout(patch_group)
        patch_list = QListWidget()
        patch_list.setSelectionMode(QListWidget.ExtendedSelection)
        patch_layout.addWidget(patch_list)
        layout.addWidget(patch_group)
        
        # Populate patches when file is selected
        def on_file_selected():
            patch_list.clear()
            idx = file_list.currentRow()
            if idx >= 0:
                source_window = other_windows[idx]
                current_tab = self.tabs.currentIndex()
                
                if current_tab == 0:  # Programs
                    for bank in source_window.pcg.program_banks:
                        if bank.is_read_only:
                            continue
                        for prog in bank.patches:
                            if prog.name.strip():
                                patch_list.addItem(f"{prog.id}: {prog.name}")
                elif current_tab == 1:  # Combis
                    for bank in source_window.pcg.combi_banks:
                        for combi in bank.patches:
                            if combi.name.strip():
                                patch_list.addItem(f"{combi.id}: {combi.name}")
        
        file_list.currentRowChanged.connect(on_file_selected)
        if file_list.count() > 0:
            file_list.setCurrentRow(0)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() != QDialog.Accepted:
            return
        
        # Get selected source and patches
        source_idx = file_list.currentRow()
        if source_idx < 0:
            return
        
        source_window = other_windows[source_idx]
        selected_items = patch_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select patches to copy")
            return
        
        # Parse selected patch IDs
        patch_ids = []
        for item in selected_items:
            text = item.text()
            patch_id = text.split(":")[0].strip()
            patch_ids.append(patch_id)
        
        # Perform the cross-file paste
        self._paste_patches_from_source(source_window.pcg, patch_ids)
    
    def _paste_patches_from_source(self, source_pcg, patch_ids):
        """Paste patches from source PCG to current file."""
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Programs
            self._paste_programs_from_source(source_pcg, patch_ids)
        elif current_tab == 1:  # Combis
            self._paste_combis_from_source(source_pcg, patch_ids)
    
    def _paste_programs_from_source(self, source_pcg, patch_ids):
        """Paste programs from source PCG."""
        # Find source programs
        source_programs = []
        for patch_id in patch_ids:
            for bank in source_pcg.program_banks:
                for prog in bank.patches:
                    if prog.id == patch_id:
                        source_programs.append(prog)
                        break
        
        if not source_programs:
            QMessageBox.warning(self, "Not Found", "Could not find selected programs")
            return
        
        # Get destination selection
        selected_rows = self.programs_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Destination", "Please select a destination program slot")
            return
        
        start_row = selected_rows[0].row()
        target_program = self._get_program_at_row(start_row)
        
        if not target_program:
            return
        
        # Check for ROM bank
        for bank in self.pcg.program_banks:
            if bank.bank_id == target_program.bank and bank.is_read_only:
                QMessageBox.warning(
                    self,
                    "ROM Bank",
                    f"Cannot paste into ROM bank '{bank.bank_id}'.\n"
                    f"Please select a user bank."
                )
                return
        
        # Check engine type compatibility
        validation_error = self._validate_engine_compatibility(source_programs, target_program)
        if validation_error:
            QMessageBox.warning(self, "Engine Mismatch", validation_error)
            return
        
        # Confirm paste
        reply = QMessageBox.question(
            self,
            "Paste Programs",
            f"Paste {len(source_programs)} program(s) starting at {target_program.id}?\n\n"
            f"This will overwrite existing programs.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Perform paste
        pasted = 0
        for i, source_prog in enumerate(source_programs):
            target = self._get_program_at_row(start_row + i)
            if target:
                # Copy program data
                target.name = source_prog.name
                target.category = deepcopy(source_prog.category) if source_prog.category else None
                target.favorite = source_prog.favorite
                target.engine = source_prog.engine
                target.osc_mode = source_prog.osc_mode
                if source_prog.raw_data:
                    target.raw_data = deepcopy(source_prog.raw_data)
                pasted += 1
        
        self.mark_dirty()
        self.load_programs()
        QMessageBox.information(self, "Pasted", f"Pasted {pasted} program(s)")
    
    def _paste_combis_from_source(self, source_pcg, patch_ids):
        """Paste combis from source PCG with program remapping."""
        from .clipboard import Clipboard
        
        # Find source combis
        source_combis = []
        for patch_id in patch_ids:
            for bank in source_pcg.combi_banks:
                for combi in bank.patches:
                    if combi.id == patch_id:
                        source_combis.append(combi)
                        break
        
        if not source_combis:
            QMessageBox.warning(self, "Not Found", "Could not find selected combis")
            return
        
        # Get destination selection
        selected_rows = self.combis_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Destination", "Please select a destination combi slot")
            return
        
        start_row = selected_rows[0].row()
        
        # Ask about program handling
        reply = QMessageBox.question(
            self,
            "Copy Programs?",
            f"Paste {len(source_combis)} combi(s).\n\n"
            f"Do you want to also copy the referenced programs?\n\n"
            f"Yes = Copy programs and remap references\n"
            f"No = Keep original program references",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        
        copy_programs = (reply == QMessageBox.Yes)
        
        # Perform paste
        pasted = 0
        for i, source_combi in enumerate(source_combis):
            target = self._get_combi_at_row(start_row + i)
            if target:
                # Use clipboard for proper program remapping
                clipboard = Clipboard()
                clipboard.copy_combi(source_combi, source_pcg)
                clipboard.paste_combi(target, self.pcg, remap_programs=copy_programs)
                pasted += 1
        
        self.mark_dirty()
        self.load_combis()
        self.load_programs()  # Refresh in case programs were copied
        QMessageBox.information(self, "Pasted", f"Pasted {pasted} combi(s)")
    
    # ==================== Engine Type Validation ====================
    
    def _validate_engine_compatibility(self, source_programs, target_program):
        """Validate that source programs are compatible with target bank.
        
        HD-1 and EXi programs cannot be mixed in the same bank on Kronos hardware.
        
        Returns:
            Error message string if incompatible, None if OK
        """
        if not source_programs:
            return None
        
        # Get target bank
        target_bank = None
        for bank in self.pcg.program_banks:
            if bank.bank_id == target_program.bank:
                target_bank = bank
                break
        
        if not target_bank:
            return None
        
        # Determine bank's engine type from existing programs
        bank_engine_type = self._get_bank_engine_type(target_bank)
        
        if not bank_engine_type:
            # Empty bank, any engine is OK
            return None
        
        # Check each source program
        for prog in source_programs:
            source_engine = self._classify_engine(prog.engine)
            if source_engine and bank_engine_type and source_engine != bank_engine_type:
                return (
                    f"Engine type mismatch!\n\n"
                    f"Program '{prog.name}' uses {prog.engine} ({source_engine})\n"
                    f"but target bank {target_bank.bank_id} contains {bank_engine_type} programs.\n\n"
                    f"Mixing HD-1 and EXi programs in the same bank causes\n"
                    f"load errors on Kronos hardware."
                )
        
        return None
    
    def _get_bank_engine_type(self, bank):
        """Determine the engine type of a bank (HD-1 or EXi).
        
        Returns 'HD-1', 'EXi', or None if bank is empty/mixed.
        """
        engine_types = set()
        for prog in bank.patches:
            if prog.name.strip() and not prog.name.startswith("Init"):
                engine_type = self._classify_engine(prog.engine)
                if engine_type:
                    engine_types.add(engine_type)
        
        if len(engine_types) == 1:
            return engine_types.pop()
        return None
    
    def _classify_engine(self, engine_name):
        """Classify an engine as HD-1 or EXi.
        
        HD-1 is the sample-based engine.
        EXi includes all other engines (AL-1, CX-3, STR-1, EP-1, MS-20, etc.)
        """
        if not engine_name:
            return None
        
        engine_upper = engine_name.upper()
        
        # HD-1 is the sample-based engine
        if 'HD-1' in engine_upper or 'HD1' in engine_upper:
            return 'HD-1'
        
        # EXi engines
        exi_engines = ['AL-1', 'CX-3', 'STR-1', 'EP-1', 'MS-20', 'POLYSIX', 
                       'MOD-7', 'SGX-1', 'SGX-2', 'EXI']
        for exi in exi_engines:
            if exi in engine_upper:
                return 'EXi'
        
        return None
    
    # ==================== Missing Bank Creation ====================
    
    def _check_and_create_missing_banks(self, source_pcg, patch_ids):
        """Check if any source patches require banks that don't exist in destination.
        
        If missing banks are found, prompts user to create them.
        
        Args:
            source_pcg: Source PCG file
            patch_ids: List of patch IDs to paste
        
        Returns:
            True if all required banks exist (or were created), False to cancel
        """
        # Find which banks are needed
        needed_banks = set()
        for patch_id in patch_ids:
            # Extract bank from patch ID (e.g., "USER-FF000" -> "U-FF")
            for bank in source_pcg.program_banks:
                for prog in bank.patches:
                    if prog.id == patch_id:
                        needed_banks.add(bank.bank_id)
                        break
        
        # Check which banks are missing
        missing_banks = []
        for bank_id in needed_banks:
            if bank_id.startswith('U-') and not self.pcg.has_program_bank(bank_id):
                missing_banks.append(bank_id)
        
        if not missing_banks:
            return True  # All banks exist
        
        # Ask user if they want to create missing banks
        bank_list = ", ".join(missing_banks)
        reply = QMessageBox.question(
            self,
            "Missing Banks",
            f"The following user banks don't exist in the destination file:\n\n"
            f"{bank_list}\n\n"
            f"Do you want to create these banks?\n\n"
            f"Note: Creating banks modifies the PCG file structure.",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return False
        
        if reply == QMessageBox.No:
            # User doesn't want to create banks - show available banks
            available = self.pcg.get_available_user_banks('Program')
            if available:
                QMessageBox.information(
                    self,
                    "Available Banks",
                    f"You can paste into these existing user banks:\n\n"
                    f"{', '.join(available)}\n\n"
                    f"Select a program in one of these banks as the destination."
                )
            else:
                QMessageBox.warning(
                    self,
                    "No User Banks",
                    "This file has no user banks.\n\n"
                    "You need to create user banks to paste programs."
                )
            return False
        
        # Create missing banks
        created = []
        failed = []
        for bank_id in missing_banks:
            try:
                if insert_bank_into_pcg(self.pcg, bank_id):
                    created.append(bank_id)
                else:
                    failed.append(bank_id)
            except Exception as e:
                failed.append(f"{bank_id} ({e})")
        
        if created:
            self.mark_dirty()
            self.populate_bank_lists()  # Refresh bank lists
            self.load_programs()  # Refresh program display
            
            QMessageBox.information(
                self,
                "Banks Created",
                f"Created user banks: {', '.join(created)}\n\n"
                f"You can now paste programs into these banks."
            )
        
        if failed:
            QMessageBox.warning(
                self,
                "Bank Creation Failed",
                f"Failed to create banks: {', '.join(failed)}\n\n"
                f"The PCG file structure may not support adding these banks."
            )
            return False
        
        return True
    
    def create_user_bank(self):
        """Create a new user bank in the current file."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first")
            return
        
        from PySide6.QtWidgets import QInputDialog
        from .models import get_user_bank_list
        
        # Get list of possible user banks
        all_user_banks = get_user_bank_list()
        
        # Filter out banks that already exist
        existing = set(self.pcg.get_all_bank_ids('Program'))
        available = [b for b in all_user_banks if b not in existing]
        
        if not available:
            QMessageBox.information(
                self,
                "All Banks Exist",
                "All possible user banks already exist in this file."
            )
            return
        
        # Let user select which bank to create
        bank_id, ok = QInputDialog.getItem(
            self,
            "Create User Bank",
            "Select bank to create:",
            available,
            0,
            False
        )
        
        if not ok or not bank_id:
            return
        
        # Create the bank
        try:
            if insert_bank_into_pcg(self.pcg, bank_id):
                self.mark_dirty()
                self.populate_bank_lists()
                self.load_programs()
                
                QMessageBox.information(
                    self,
                    "Bank Created",
                    f"Created user bank: {bank_id}\n\n"
                    f"The bank contains 128 empty program slots."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Creation Failed",
                    f"Could not create bank {bank_id}.\n\n"
                    f"The bank may already exist or the file structure doesn't support it."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create bank: {e}"
            )
    
    def show_reference_changer(self):
        """Show the Program Reference Changer dialog."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first")
            return
        
        from .qt_reference_changer_dialog import QtReferenceChangerDialog
        
        dialog = QtReferenceChangerDialog(self, self.pcg)
        if dialog.exec() == dialog.Accepted:
            changes = dialog.get_changes_made()
            if changes > 0:
                self.mark_dirty()
                # Refresh the display
                self.load_programs()
                self.load_combis()
                self.load_setlist_slots()
    
    def show_master_files(self):
        """Show the Master Files management dialog."""
        from .qt_master_files_dialog import QtMasterFilesDialog
        
        dialog = QtMasterFilesDialog(self)
        dialog.exec()
    
    def show_list_generator(self):
        """Show the List Generator dialog.
        
        Based on C# ListGeneratorWindow - generates various lists and reports
        from PCG files including patch lists, program usage, combi content,
        differences between files, and file content summaries.
        """
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first")
            return
        
        from .qt_list_generator_dialog import QtListGeneratorDialog
        
        # Check if there's another window open for differences comparison
        other_pcg = None
        for window in PcgMainWindow._open_windows:
            if window != self and window.pcg is not None:
                other_pcg = window.pcg
                break
        
        dialog = QtListGeneratorDialog(self.pcg, self, other_pcg=other_pcg)
        dialog.exec()
    
    def set_as_master_file(self):
        """Set the current file as the master file for its model."""
        if not self.pcg:
            QMessageBox.warning(self, "No File", "Please open a PCG file first")
            return
        
        # Get model info from the PCG file
        model = getattr(self.pcg, 'model', None)
        os_version = getattr(self.pcg, 'os_version', '')
        
        if not model:
            # Try to determine from header
            model = "Kronos"  # Default assumption
            os_version = ""
        
        from .master_files import get_master_files
        
        master_files = get_master_files()
        master_files.set_master_file(model, os_version, self.current_file)
        
        QMessageBox.information(
            self,
            "Master File Set",
            f"'{self.current_file}' has been set as the master file for {model} {os_version}".strip()
        )


def main():
    """Launch Qt GUI."""
    app = QApplication(sys.argv)
    app.setApplicationName("PCG Tools")
    app.setOrganizationName("PCG Tools")
    
    # Apply saved theme on startup (based on C# MainViewModel constructor)
    from .settings import Settings
    from .theme_manager import apply_theme, ThemeType
    
    settings = Settings()
    apply_theme(ThemeType(int(settings.selected_theme)))
    
    window = PcgMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
