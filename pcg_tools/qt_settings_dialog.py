"""Settings Dialog for PCG Tools.

Ported from C# SettingsWindow.xaml - provides complete settings UI parity.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QGroupBox, QCheckBox, QRadioButton, QLabel, QLineEdit,
    QPushButton, QSpinBox, QFileDialog, QButtonGroup
)
from PySide6.QtCore import Qt

from .settings import (
    get_settings, Settings,
    ClearPatchesAlgorithm, AutoLoadMasterFiles,
    PatchDuplication, SortOrder
)


class SettingsDialog(QDialog):
    """Settings dialog matching C# SettingsWindow."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = get_settings()
        
        self.setWindowTitle("Settings")
        self.setMinimumWidth(640)
        self.setMinimumHeight(590)
        
        self._create_ui()
        self._load_settings()
    
    def _create_ui(self):
        """Create the settings UI with tabs."""
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs matching C# SettingsWindow
        self.tab_widget.addTab(self._create_pcg_window_tab(), "PCG Window")
        self.tab_widget.addTab(self._create_files_tab(), "Files")
        self.tab_widget.addTab(self._create_edit_tab(), "Edit")
        self.tab_widget.addTab(self._create_copy_paste_tab(), "Cut/Copy/Paste")
        self.tab_widget.addTab(self._create_sort_tab(), "Sort")
        self.tab_widget.addTab(self._create_categories_tab(), "Categories")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        ok_button = QPushButton("OK")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self._save_and_close)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)

    def _create_pcg_window_tab(self) -> QWidget:
        """Create PCG Window settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Show Number of References Column
        self.show_refs_checkbox = QCheckBox("Show Number of References Column")
        layout.addWidget(self.show_refs_checkbox)
        
        # Show Single-Lined Set List Slot Descriptions
        self.single_line_desc_checkbox = QCheckBox("Show Single-Lined Set List Slot Descriptions")
        layout.addWidget(self.single_line_desc_checkbox)
        
        # Clear Patches group
        clear_group = QGroupBox("Clear Patches")
        clear_layout = QVBoxLayout(clear_group)
        
        radio_layout = QHBoxLayout()
        self.clear_patches_group = QButtonGroup(self)
        
        self.clear_none_radio = QRadioButton("None")
        self.clear_patches_group.addButton(self.clear_none_radio, ClearPatchesAlgorithm.NONE)
        radio_layout.addWidget(self.clear_none_radio)
        
        self.clear_unused_radio = QRadioButton("Unused Only")
        self.clear_patches_group.addButton(self.clear_unused_radio, ClearPatchesAlgorithm.UNUSED_ONLY)
        radio_layout.addWidget(self.clear_unused_radio)
        
        self.clear_ask_radio = QRadioButton("Ask")
        self.clear_patches_group.addButton(self.clear_ask_radio, ClearPatchesAlgorithm.ASK)
        radio_layout.addWidget(self.clear_ask_radio)
        
        self.clear_all_radio = QRadioButton("Unused and Used")
        self.clear_patches_group.addButton(self.clear_all_radio, ClearPatchesAlgorithm.UNUSED_AND_USED)
        radio_layout.addWidget(self.clear_all_radio)
        
        clear_layout.addLayout(radio_layout)
        
        self.fix_refs_checkbox = QCheckBox("Fix References to Cleared Used Patches")
        clear_layout.addWidget(self.fix_refs_checkbox)
        
        layout.addWidget(clear_group)
        layout.addStretch()
        
        return widget
    
    def _create_files_tab(self) -> QWidget:
        """Create Files settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Auto Backup Files group
        backup_group = QGroupBox("Auto Backup Files")
        backup_layout = QHBoxLayout(backup_group)
        
        self.backup_enabled_checkbox = QCheckBox("Enabled")
        backup_layout.addWidget(self.backup_enabled_checkbox)
        
        backup_layout.addWidget(QLabel("Interval (minutes):"))
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 60)
        self.backup_interval_spin.setValue(5)
        backup_layout.addWidget(self.backup_interval_spin)
        
        backup_layout.addWidget(QLabel("Max Storage (MB):"))
        self.backup_max_storage_spin = QSpinBox()
        self.backup_max_storage_spin.setRange(1, 2048)
        self.backup_max_storage_spin.setValue(500)
        backup_layout.addWidget(self.backup_max_storage_spin)
        
        layout.addWidget(backup_group)
        
        # Auto Load Master File group
        master_group = QGroupBox("Auto Load Master File")
        master_layout = QHBoxLayout(master_group)
        
        self.master_load_group = QButtonGroup(self)
        
        self.master_always_radio = QRadioButton("Always")
        self.master_load_group.addButton(self.master_always_radio, AutoLoadMasterFiles.ALWAYS)
        master_layout.addWidget(self.master_always_radio)
        
        self.master_ask_radio = QRadioButton("Ask")
        self.master_load_group.addButton(self.master_ask_radio, AutoLoadMasterFiles.ASK)
        master_layout.addWidget(self.master_ask_radio)
        
        self.master_never_radio = QRadioButton("Never")
        self.master_load_group.addButton(self.master_never_radio, AutoLoadMasterFiles.NEVER)
        master_layout.addWidget(self.master_never_radio)
        
        layout.addWidget(master_group)
        
        # List Generator Output Directory
        list_gen_group = QGroupBox("List Generator")
        list_gen_layout = QVBoxLayout(list_gen_group)
        
        list_gen_layout.addWidget(QLabel("Default Output Directory:"))
        dir_layout = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.output_dir_edit)
        browse_btn = QPushButton("...")
        browse_btn.setMaximumWidth(50)
        browse_btn.clicked.connect(self._browse_output_dir)
        dir_layout.addWidget(browse_btn)
        list_gen_layout.addLayout(dir_layout)
        
        layout.addWidget(list_gen_group)
        
        # Sequencer Files Output Directory
        seq_group = QGroupBox("Sequencer Files")
        seq_layout = QVBoxLayout(seq_group)
        
        seq_layout.addWidget(QLabel("Default Output Directory:"))
        seq_dir_layout = QHBoxLayout()
        self.seq_output_dir_edit = QLineEdit()
        self.seq_output_dir_edit.setReadOnly(True)
        seq_dir_layout.addWidget(self.seq_output_dir_edit)
        seq_browse_btn = QPushButton("...")
        seq_browse_btn.setMaximumWidth(50)
        seq_browse_btn.clicked.connect(self._browse_seq_output_dir)
        seq_dir_layout.addWidget(seq_browse_btn)
        seq_layout.addLayout(seq_dir_layout)
        
        layout.addWidget(seq_group)
        
        # Manual Path
        manual_group = QGroupBox("Manual")
        manual_layout = QVBoxLayout(manual_group)
        
        manual_layout.addWidget(QLabel("Path:"))
        manual_dir_layout = QHBoxLayout()
        self.manual_path_edit = QLineEdit()
        manual_dir_layout.addWidget(self.manual_path_edit)
        manual_browse_btn = QPushButton("...")
        manual_browse_btn.setMaximumWidth(50)
        manual_browse_btn.clicked.connect(self._browse_manual_path)
        manual_dir_layout.addWidget(manual_browse_btn)
        manual_layout.addLayout(manual_dir_layout)
        
        layout.addWidget(manual_group)
        
        layout.addStretch()
        return widget
    
    def _create_edit_tab(self) -> QWidget:
        """Create Edit settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Single Patch Files group
        single_group = QGroupBox("Single Patch Files")
        single_layout = QVBoxLayout(single_group)
        
        self.rename_file_checkbox = QCheckBox("Rename File When Patch Name Changes")
        single_layout.addWidget(self.rename_file_checkbox)
        
        layout.addWidget(single_group)
        layout.addStretch()
        
        return widget

    def _create_copy_paste_tab(self) -> QWidget:
        """Create Cut/Copy/Paste settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Copy settings
        self.copy_incomplete_slots_checkbox = QCheckBox(
            "Copy Incomplete Set List Slots")
        self.copy_incomplete_slots_checkbox.setToolTip(
            "Copy set list slots even if referenced patch is missing")
        layout.addWidget(self.copy_incomplete_slots_checkbox)
        
        self.copy_incomplete_combis_checkbox = QCheckBox(
            "Copy Incomplete Combis")
        self.copy_incomplete_combis_checkbox.setToolTip(
            "Copy combis even if referenced programs are missing")
        layout.addWidget(self.copy_incomplete_combis_checkbox)
        
        self.copy_from_master_checkbox = QCheckBox(
            "Copy Patches from Master File")
        self.copy_from_master_checkbox.setToolTip(
            "Include patches from master file when copying")
        layout.addWidget(self.copy_from_master_checkbox)
        
        # Paste duplicate settings
        self.paste_dup_programs_checkbox = QCheckBox("Paste Duplicate Programs")
        self.paste_dup_programs_checkbox.setToolTip(
            "Allow pasting programs that already exist in destination")
        layout.addWidget(self.paste_dup_programs_checkbox)
        
        self.paste_dup_combis_checkbox = QCheckBox("Paste Duplicate Combis")
        layout.addWidget(self.paste_dup_combis_checkbox)
        
        self.paste_dup_slots_checkbox = QCheckBox("Paste Duplicate Set List Slots")
        layout.addWidget(self.paste_dup_slots_checkbox)
        
        self.paste_dup_drum_kits_checkbox = QCheckBox("Paste Duplicate Drum Kits")
        layout.addWidget(self.paste_dup_drum_kits_checkbox)
        
        self.paste_dup_drum_patterns_checkbox = QCheckBox("Paste Duplicate Drum Patterns")
        layout.addWidget(self.paste_dup_drum_patterns_checkbox)
        
        self.paste_dup_wave_seqs_checkbox = QCheckBox("Paste Duplicate Wave Sequences")
        layout.addWidget(self.paste_dup_wave_seqs_checkbox)
        
        # Auto extend paste
        self.auto_extend_paste_checkbox = QCheckBox("Auto Extend Paste")
        self.auto_extend_paste_checkbox.setToolTip(
            "Automatically extend selection when pasting single patch")
        layout.addWidget(self.auto_extend_paste_checkbox)
        
        # Patch duplication checking
        self.dup_check_group = QButtonGroup(self)
        
        self.dup_no_names_radio = QRadioButton(
            "Do Not Use Patch Names for Patch Duplication Checking")
        self.dup_check_group.addButton(self.dup_no_names_radio, 
                                        PatchDuplication.DO_NOT_USE_PATCH_NAMES)
        layout.addWidget(self.dup_no_names_radio)
        
        self.dup_equal_names_radio = QRadioButton(
            "Treat Equally Named Patches as Duplicates")
        self.dup_check_group.addButton(self.dup_equal_names_radio,
                                        PatchDuplication.EQUAL_NAMES)
        layout.addWidget(self.dup_equal_names_radio)
        
        self.dup_like_names_radio = QRadioButton(
            "Treat Like-Named Patches as Duplicates")
        self.dup_check_group.addButton(self.dup_like_names_radio,
                                        PatchDuplication.LIKE_NAMED_NAMES)
        layout.addWidget(self.dup_like_names_radio)
        
        # Ignore characters
        ignore_layout = QHBoxLayout()
        self.ignore_chars_label = QLabel("Ignore Characters:")
        ignore_layout.addWidget(self.ignore_chars_label)
        self.ignore_chars_edit = QLineEdit()
        self.ignore_chars_edit.setMaximumWidth(100)
        ignore_layout.addWidget(self.ignore_chars_edit)
        ignore_layout.addStretch()
        layout.addLayout(ignore_layout)
        
        # Connect radio button to enable/disable ignore chars
        self.dup_like_names_radio.toggled.connect(self._update_ignore_chars_state)
        
        # Overwrite settings
        self.overwrite_programs_checkbox = QCheckBox("Overwrite Filled Programs")
        layout.addWidget(self.overwrite_programs_checkbox)
        
        self.overwrite_combis_checkbox = QCheckBox("Overwrite Filled Combis")
        layout.addWidget(self.overwrite_combis_checkbox)
        
        self.overwrite_slots_checkbox = QCheckBox("Overwrite Filled Set List Slots")
        layout.addWidget(self.overwrite_slots_checkbox)
        
        self.overwrite_drum_kits_checkbox = QCheckBox("Overwrite Filled Drum Kits")
        layout.addWidget(self.overwrite_drum_kits_checkbox)
        
        self.overwrite_drum_patterns_checkbox = QCheckBox("Overwrite Filled Drum Patterns")
        layout.addWidget(self.overwrite_drum_patterns_checkbox)
        
        self.overwrite_wave_seqs_checkbox = QCheckBox("Overwrite Filled Wave Sequences")
        layout.addWidget(self.overwrite_wave_seqs_checkbox)
        
        # Restore defaults button
        restore_btn = QPushButton("Restore Defaults")
        restore_btn.clicked.connect(self._restore_copy_paste_defaults)
        layout.addWidget(restore_btn)
        
        layout.addStretch()
        return widget
    
    def _create_sort_tab(self) -> QWidget:
        """Create Sort settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Split character
        split_layout = QHBoxLayout()
        split_layout.addWidget(QLabel("Split Character:"))
        self.split_char_edit = QLineEdit()
        self.split_char_edit.setMaximumWidth(30)
        self.split_char_edit.setMaxLength(1)
        self.split_char_edit.textChanged.connect(self._update_sort_options)
        split_layout.addWidget(self.split_char_edit)
        split_layout.addStretch()
        layout.addLayout(split_layout)
        
        # Title/Artist Order group
        order_group = QGroupBox("Title/Artist Order")
        order_layout = QVBoxLayout(order_group)
        
        self.title_artist_group = QButtonGroup(self)
        
        self.title_artist_radio = QRadioButton("Title - Artist")
        self.title_artist_group.addButton(self.title_artist_radio, 0)
        order_layout.addWidget(self.title_artist_radio)
        
        self.artist_title_radio = QRadioButton("Artist - Title")
        self.title_artist_group.addButton(self.artist_title_radio, 1)
        order_layout.addWidget(self.artist_title_radio)
        
        layout.addWidget(order_group)
        
        # Sort Order group
        sort_order_group = QGroupBox("Sort Order")
        sort_order_layout = QVBoxLayout(sort_order_group)
        
        self.sort_order_group = QButtonGroup(self)
        
        self.sort_name_cat_radio = QRadioButton("Name, Category")
        self.sort_order_group.addButton(self.sort_name_cat_radio, SortOrder.NAME_CATEGORY)
        sort_order_layout.addWidget(self.sort_name_cat_radio)
        
        self.sort_title_artist_cat_radio = QRadioButton("Title/Artist, Category")
        self.sort_order_group.addButton(self.sort_title_artist_cat_radio, SortOrder.TITLE_ARTIST_CATEGORY)
        sort_order_layout.addWidget(self.sort_title_artist_cat_radio)
        
        self.sort_artist_title_cat_radio = QRadioButton("Artist/Title, Category")
        self.sort_order_group.addButton(self.sort_artist_title_cat_radio, SortOrder.ARTIST_TITLE_CATEGORY)
        sort_order_layout.addWidget(self.sort_artist_title_cat_radio)
        
        self.sort_cat_name_radio = QRadioButton("Category, Name")
        self.sort_order_group.addButton(self.sort_cat_name_radio, SortOrder.CATEGORY_NAME)
        sort_order_layout.addWidget(self.sort_cat_name_radio)
        
        self.sort_cat_title_artist_radio = QRadioButton("Category, Title/Artist")
        self.sort_order_group.addButton(self.sort_cat_title_artist_radio, SortOrder.CATEGORY_TITLE_ARTIST)
        sort_order_layout.addWidget(self.sort_cat_title_artist_radio)
        
        self.sort_cat_artist_title_radio = QRadioButton("Category, Artist/Title")
        self.sort_order_group.addButton(self.sort_cat_artist_title_radio, SortOrder.CATEGORY_ARTIST_TITLE)
        sort_order_layout.addWidget(self.sort_cat_artist_title_radio)
        
        layout.addWidget(sort_order_group)
        
        layout.addStretch()
        return widget
    
    def _create_categories_tab(self) -> QWidget:
        """Create Categories settings tab (Trinity-specific)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Category Set Selection group
        cat_group = QGroupBox("Category Set Selection")
        cat_layout = QVBoxLayout(cat_group)
        
        self.category_set_group = QButtonGroup(self)
        
        self.category_a_radio = QRadioButton("Category Set A")
        self.category_set_group.addButton(self.category_a_radio, 1)
        cat_layout.addWidget(self.category_a_radio)
        
        self.category_b_radio = QRadioButton("Category Set B")
        self.category_set_group.addButton(self.category_b_radio, 0)
        cat_layout.addWidget(self.category_b_radio)
        
        layout.addWidget(cat_group)
        layout.addStretch()
        
        return widget

    def _load_settings(self):
        """Load current settings into UI controls."""
        s = self.settings
        
        # Restore last tab
        self.tab_widget.setCurrentIndex(s.settings_tab_index)
        
        # PCG Window tab
        self.show_refs_checkbox.setChecked(s.show_number_of_references_column)
        self.single_line_desc_checkbox.setChecked(s.single_lined_setlist_slot_descriptions)
        
        # Clear patches
        if s.clear_patches_algorithm == ClearPatchesAlgorithm.NONE:
            self.clear_none_radio.setChecked(True)
        elif s.clear_patches_algorithm == ClearPatchesAlgorithm.UNUSED_ONLY:
            self.clear_unused_radio.setChecked(True)
        elif s.clear_patches_algorithm == ClearPatchesAlgorithm.ASK:
            self.clear_ask_radio.setChecked(True)
        else:
            self.clear_all_radio.setChecked(True)
        
        self.fix_refs_checkbox.setChecked(s.clear_patches_fix_references)
        
        # Files tab
        self.backup_enabled_checkbox.setChecked(s.auto_backup_enabled)
        self.backup_interval_spin.setValue(s.auto_backup_interval_minutes)
        self.backup_max_storage_spin.setValue(s.auto_backup_max_storage_mb)
        
        if s.master_files_auto_load == AutoLoadMasterFiles.ALWAYS:
            self.master_always_radio.setChecked(True)
        elif s.master_files_auto_load == AutoLoadMasterFiles.ASK:
            self.master_ask_radio.setChecked(True)
        else:
            self.master_never_radio.setChecked(True)
        
        self.output_dir_edit.setText(s.default_output_directory)
        self.seq_output_dir_edit.setText(s.default_output_directory_sequencer)
        self.manual_path_edit.setText(s.default_manual_path)
        
        # Edit tab
        self.rename_file_checkbox.setChecked(s.rename_file_when_patch_name_changes)
        
        # Cut/Copy/Paste tab
        self.copy_incomplete_slots_checkbox.setChecked(s.copy_incomplete_setlist_slots)
        self.copy_incomplete_combis_checkbox.setChecked(s.copy_incomplete_combis)
        self.copy_from_master_checkbox.setChecked(s.copy_patches_from_master_file)
        
        self.paste_dup_programs_checkbox.setChecked(s.paste_duplicate_programs)
        self.paste_dup_combis_checkbox.setChecked(s.paste_duplicate_combis)
        self.paste_dup_slots_checkbox.setChecked(s.paste_duplicate_setlist_slots)
        self.paste_dup_drum_kits_checkbox.setChecked(s.paste_duplicate_drum_kits)
        self.paste_dup_drum_patterns_checkbox.setChecked(s.paste_duplicate_drum_patterns)
        self.paste_dup_wave_seqs_checkbox.setChecked(s.paste_duplicate_wave_sequences)
        
        self.auto_extend_paste_checkbox.setChecked(s.auto_extend_paste)
        
        if s.patch_duplication_checking == PatchDuplication.DO_NOT_USE_PATCH_NAMES:
            self.dup_no_names_radio.setChecked(True)
        elif s.patch_duplication_checking == PatchDuplication.EQUAL_NAMES:
            self.dup_equal_names_radio.setChecked(True)
        else:
            self.dup_like_names_radio.setChecked(True)
        
        self.ignore_chars_edit.setText(s.ignore_characters_for_duplication)
        self._update_ignore_chars_state()
        
        self.overwrite_programs_checkbox.setChecked(s.overwrite_filled_programs)
        self.overwrite_combis_checkbox.setChecked(s.overwrite_filled_combis)
        self.overwrite_slots_checkbox.setChecked(s.overwrite_filled_setlist_slots)
        self.overwrite_drum_kits_checkbox.setChecked(s.overwrite_filled_drum_kits)
        self.overwrite_drum_patterns_checkbox.setChecked(s.overwrite_filled_drum_patterns)
        self.overwrite_wave_seqs_checkbox.setChecked(s.overwrite_filled_wave_sequences)
        
        # Sort tab
        self.split_char_edit.setText(s.sort_split_character)
        
        if s.sort_artist_title_order:
            self.artist_title_radio.setChecked(True)
        else:
            self.title_artist_radio.setChecked(True)
        
        sort_order = s.sort_order
        if sort_order == SortOrder.NAME_CATEGORY:
            self.sort_name_cat_radio.setChecked(True)
        elif sort_order == SortOrder.TITLE_ARTIST_CATEGORY:
            self.sort_title_artist_cat_radio.setChecked(True)
        elif sort_order == SortOrder.ARTIST_TITLE_CATEGORY:
            self.sort_artist_title_cat_radio.setChecked(True)
        elif sort_order == SortOrder.CATEGORY_NAME:
            self.sort_cat_name_radio.setChecked(True)
        elif sort_order == SortOrder.CATEGORY_TITLE_ARTIST:
            self.sort_cat_title_artist_radio.setChecked(True)
        else:
            self.sort_cat_artist_title_radio.setChecked(True)
        
        self._update_sort_options()
        
        # Categories tab
        if s.trinity_category_set_a:
            self.category_a_radio.setChecked(True)
        else:
            self.category_b_radio.setChecked(True)
    
    def _save_settings(self):
        """Save UI values to settings."""
        s = self.settings
        
        # Save tab index
        s.settings_tab_index = self.tab_widget.currentIndex()
        
        # PCG Window tab
        s.show_number_of_references_column = self.show_refs_checkbox.isChecked()
        s.single_lined_setlist_slot_descriptions = self.single_line_desc_checkbox.isChecked()
        
        checked_id = self.clear_patches_group.checkedId()
        if checked_id >= 0:
            s.clear_patches_algorithm = ClearPatchesAlgorithm(checked_id)
        
        s.clear_patches_fix_references = self.fix_refs_checkbox.isChecked()
        
        # Files tab
        s.auto_backup_enabled = self.backup_enabled_checkbox.isChecked()
        s.auto_backup_interval_minutes = self.backup_interval_spin.value()
        s.auto_backup_max_storage_mb = self.backup_max_storage_spin.value()
        
        master_id = self.master_load_group.checkedId()
        if master_id >= 0:
            s.master_files_auto_load = AutoLoadMasterFiles(master_id)
        
        s.default_output_directory = self.output_dir_edit.text()
        s.default_output_directory_sequencer = self.seq_output_dir_edit.text()
        s.default_manual_path = self.manual_path_edit.text()
        
        # Edit tab
        s.rename_file_when_patch_name_changes = self.rename_file_checkbox.isChecked()
        
        # Cut/Copy/Paste tab
        s.copy_incomplete_setlist_slots = self.copy_incomplete_slots_checkbox.isChecked()
        s.copy_incomplete_combis = self.copy_incomplete_combis_checkbox.isChecked()
        s.copy_patches_from_master_file = self.copy_from_master_checkbox.isChecked()
        
        s.paste_duplicate_programs = self.paste_dup_programs_checkbox.isChecked()
        s.paste_duplicate_combis = self.paste_dup_combis_checkbox.isChecked()
        s.paste_duplicate_setlist_slots = self.paste_dup_slots_checkbox.isChecked()
        s.paste_duplicate_drum_kits = self.paste_dup_drum_kits_checkbox.isChecked()
        s.paste_duplicate_drum_patterns = self.paste_dup_drum_patterns_checkbox.isChecked()
        s.paste_duplicate_wave_sequences = self.paste_dup_wave_seqs_checkbox.isChecked()
        
        s.auto_extend_paste = self.auto_extend_paste_checkbox.isChecked()
        
        dup_id = self.dup_check_group.checkedId()
        if dup_id >= 0:
            s.patch_duplication_checking = PatchDuplication(dup_id)
        
        s.ignore_characters_for_duplication = self.ignore_chars_edit.text()
        
        s.overwrite_filled_programs = self.overwrite_programs_checkbox.isChecked()
        s.overwrite_filled_combis = self.overwrite_combis_checkbox.isChecked()
        s.overwrite_filled_setlist_slots = self.overwrite_slots_checkbox.isChecked()
        s.overwrite_filled_drum_kits = self.overwrite_drum_kits_checkbox.isChecked()
        s.overwrite_filled_drum_patterns = self.overwrite_drum_patterns_checkbox.isChecked()
        s.overwrite_filled_wave_sequences = self.overwrite_wave_seqs_checkbox.isChecked()
        
        # Sort tab
        s.sort_split_character = self.split_char_edit.text()
        s.sort_artist_title_order = self.artist_title_radio.isChecked()
        
        sort_id = self.sort_order_group.checkedId()
        if sort_id >= 0:
            s.sort_order = SortOrder(sort_id)
        
        # Categories tab
        s.trinity_category_set_a = self.category_a_radio.isChecked()
        
        # Save to file
        s.save()
    
    def _save_and_close(self):
        """Save settings and close dialog."""
        self._save_settings()
        self.accept()
    
    def _browse_output_dir(self):
        """Browse for output directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output Directory",
            self.output_dir_edit.text() or str(Path.home())
        )
        if directory:
            self.output_dir_edit.setText(directory)
    
    def _browse_seq_output_dir(self):
        """Browse for sequencer output directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Sequencer Output Directory",
            self.seq_output_dir_edit.text() or str(Path.home())
        )
        if directory:
            self.seq_output_dir_edit.setText(directory)
    
    def _browse_manual_path(self):
        """Browse for manual PDF file."""
        from pathlib import Path
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Manual PDF",
            self.manual_path_edit.text() or str(Path.home()),
            "PDF Files (*.pdf)"
        )
        if filename:
            self.manual_path_edit.setText(filename)
    
    def _update_ignore_chars_state(self):
        """Enable/disable ignore characters based on duplication mode."""
        enabled = self.dup_like_names_radio.isChecked()
        self.ignore_chars_label.setEnabled(enabled)
        self.ignore_chars_edit.setEnabled(enabled)
    
    def _update_sort_options(self):
        """Enable/disable sort options based on split character."""
        has_split = bool(self.split_char_edit.text())
        
        # Title/Artist order options
        self.title_artist_radio.setEnabled(has_split)
        self.artist_title_radio.setEnabled(has_split)
        
        # Sort order options that use title/artist
        self.sort_title_artist_cat_radio.setEnabled(has_split)
        self.sort_artist_title_cat_radio.setEnabled(has_split)
        self.sort_cat_title_artist_radio.setEnabled(has_split)
        self.sort_cat_artist_title_radio.setEnabled(has_split)
        
        # If a disabled option is selected, switch to a valid one
        if not has_split:
            if self.sort_title_artist_cat_radio.isChecked() or \
               self.sort_artist_title_cat_radio.isChecked():
                self.sort_name_cat_radio.setChecked(True)
            if self.sort_cat_title_artist_radio.isChecked() or \
               self.sort_cat_artist_title_radio.isChecked():
                self.sort_cat_name_radio.setChecked(True)
    
    def _restore_copy_paste_defaults(self):
        """Restore copy/paste settings to defaults (matching C# ButtonRestoreClick).
        
        C# defaults from Settings.Designer.cs:
        - CopyPaste_CopyIncompleteCombis = True
        - CopyPaste_CopyIncompleteSetListSlots = True
        - CopyPaste_CopyPatchesFromMasterFile = False
        - CopyPaste_PasteDuplicatePrograms = False
        - CopyPaste_PasteDuplicateCombis = False
        - CopyPaste_PasteDuplicateSetListSlots = True
        - CopyPaste_PasteDuplicateDrumKits = False
        - CopyPaste_PasteDuplicateDrumPatterns = False
        - CopyPaste_PasteDuplicateWaveSequences = False
        - CopyPaste_AutoExtendedSinglePatchSelectionPaste = True
        - CopyPaste_OverwriteFilledPrograms = False
        - CopyPaste_OverwriteFilledCombis = False
        - CopyPaste_OverwriteFilledSetListSlots = True
        - CopyPaste_OverwriteFilledDrumKits = False
        - CopyPaste_OverwriteFilledDrumPatterns = False
        - CopyPaste_OverwriteFilledWaveSequences = False
        """
        self.copy_incomplete_combis_checkbox.setChecked(True)  # C# default: True
        self.copy_incomplete_slots_checkbox.setChecked(True)  # C# default: True
        self.copy_from_master_checkbox.setChecked(False)  # C# default: False
        
        self.paste_dup_programs_checkbox.setChecked(False)  # C# default: False
        self.paste_dup_combis_checkbox.setChecked(False)  # C# default: False
        self.paste_dup_slots_checkbox.setChecked(True)  # C# default: True
        self.paste_dup_drum_kits_checkbox.setChecked(False)  # C# default: False
        self.paste_dup_drum_patterns_checkbox.setChecked(False)  # C# default: False
        self.paste_dup_wave_seqs_checkbox.setChecked(False)  # C# default: False
        
        self.auto_extend_paste_checkbox.setChecked(True)  # C# default: True
        
        self.overwrite_programs_checkbox.setChecked(False)  # C# default: False
        self.overwrite_combis_checkbox.setChecked(False)  # C# default: False
        self.overwrite_slots_checkbox.setChecked(True)  # C# default: True
        self.overwrite_drum_kits_checkbox.setChecked(False)  # C# default: False
        self.overwrite_drum_patterns_checkbox.setChecked(False)  # C# default: False
        self.overwrite_wave_seqs_checkbox.setChecked(False)  # C# default: False


# Import Path at module level for _browse_manual_path
from pathlib import Path
