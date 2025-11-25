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
        self.slots_table.setColumnCount(5)
        self.slots_table.setHorizontalHeaderLabels(["Slot", "Slot Name", "Patch Name", "Transpose", "Volume"])
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
        
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                row = self.programs_table.rowCount()
                self.programs_table.insertRow(row)
                
                self.programs_table.setItem(row, 0, QTableWidgetItem(prog.id))
                self.programs_table.setItem(row, 1, QTableWidgetItem(prog.name))
                self.programs_table.setItem(row, 2, QTableWidgetItem(prog.category.name if prog.category else ""))
                self.programs_table.setItem(row, 3, QTableWidgetItem(prog.category.sub_name if prog.category else ""))
                self.programs_table.setItem(row, 4, QTableWidgetItem(prog.engine if hasattr(prog, 'engine') else ""))
                self.programs_table.setItem(row, 5, QTableWidgetItem("✓" if prog.favorite else ""))
    
    def load_combis(self):
        """Load combis into table."""
        self.combis_table.setRowCount(0)
        
        if not self.pcg:
            return
        
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                row = self.combis_table.rowCount()
                self.combis_table.insertRow(row)
                
                self.combis_table.setItem(row, 0, QTableWidgetItem(combi.id))
                self.combis_table.setItem(row, 1, QTableWidgetItem(combi.name))
                self.combis_table.setItem(row, 2, QTableWidgetItem(combi.category.name if combi.category else ""))
                self.combis_table.setItem(row, 3, QTableWidgetItem(combi.category.sub_name if combi.category else ""))
                self.combis_table.setItem(row, 4, QTableWidgetItem("✓" if combi.favorite else ""))
    
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
            
            # Custom label (from SLS1) - editable
            label_item = QTableWidgetItem(slot.description if slot.description else "")
            self.slots_table.setItem(row, 1, label_item)
            
            # Actual patch name (from SLD1) - read-only for now
            name_item = QTableWidgetItem(slot.name if slot.name else "(no name)")
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.slots_table.setItem(row, 2, name_item)
            
            # Transpose - editable
            transpose_item = QTableWidgetItem(str(slot.transpose))
            self.slots_table.setItem(row, 3, transpose_item)
            
            # Volume - editable
            volume_item = QTableWidgetItem(str(slot.volume))
            self.slots_table.setItem(row, 4, volume_item)
        
        self.slots_table.blockSignals(False)
    
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
                    item.setText(slot.description if slot.description else "")
                    return
                slot.description = new_name
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
        
        if current_tab == 2:  # Setlists
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
    
    def edit_slot_name(self, slot):
        """Edit slot name."""
        from PySide6.QtWidgets import QInputDialog
        
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Slot Name",
            "Slot Name (max 24 characters):",
            text=slot.name
        )
        
        if ok and new_name:
            if len(new_name) > 24:
                QMessageBox.warning(self, "Warning", "Name too long. Maximum 24 characters.")
                return
            
            slot.name = new_name
            self.mark_dirty()
            self.load_setlist_slots()
    
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
            return
        
        row = selected_rows[0].row()
        if row < len(setlist.slots):
            slot = setlist.slots[row]
            self.notes_text.blockSignals(True)
            self.notes_text.setPlainText(slot.notes if slot.notes else "")
            self.notes_text.blockSignals(False)
    
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
        """Handle font size change for comments."""
        # Map size labels to point sizes
        size_map = {
            "XS": 8,
            "S": 10,
            "M": 12,
            "L": 14,
            "XL": 16
        }
        
        point_size = size_map.get(size_text, 12)
        font = self.notes_text.font()
        font.setPointSize(point_size)
        self.notes_text.setFont(font)
    
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
