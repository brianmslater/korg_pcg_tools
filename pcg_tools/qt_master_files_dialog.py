"""Qt-based Master Files management dialog.

Ported from C# MasterFiles/MasterFilesWindow.xaml
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox, QComboBox, QGroupBox
)
from PySide6.QtCore import Qt

from .master_files import (
    MasterFiles, MasterFileEntry, FileState, AutoLoadOption,
    get_master_files
)


class QtMasterFilesDialog(QDialog):
    """Dialog for managing master files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.master_files = get_master_files()
        
        self.setWindowTitle("Master Files")
        self.setMinimumWidth(700)
        self.setMinimumHeight(450)
        self.setModal(True)
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Help text
        help_label = QLabel(
            "Master files provide reference data (categories, etc.) for PCG files "
            "that don't have a global chunk. Set a master file for each model you use."
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; margin-bottom: 8px;")
        layout.addWidget(help_label)
        
        # Auto-load setting
        auto_load_group = QGroupBox("Auto-Load Setting")
        auto_load_layout = QHBoxLayout(auto_load_group)
        
        auto_load_label = QLabel("When opening a file without global data:")
        auto_load_layout.addWidget(auto_load_label)
        
        self.auto_load_combo = QComboBox()
        self.auto_load_combo.addItem("Always load master file", AutoLoadOption.ALWAYS)
        self.auto_load_combo.addItem("Ask before loading", AutoLoadOption.ASK)
        self.auto_load_combo.addItem("Never load master file", AutoLoadOption.NEVER)
        self.auto_load_combo.currentIndexChanged.connect(self._on_auto_load_changed)
        auto_load_layout.addWidget(self.auto_load_combo)
        auto_load_layout.addStretch()
        
        layout.addWidget(auto_load_group)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Workstation Model", "OS Version", "PCG File", "Status"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        assign_btn = QPushButton("Assign File...")
        assign_btn.clicked.connect(self._on_assign)
        button_layout.addWidget(assign_btn)
        
        unassign_btn = QPushButton("Unassign")
        unassign_btn.clicked.connect(self._on_unassign)
        button_layout.addWidget(unassign_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def _load_data(self):
        """Load master files data into the table."""
        entries = self.master_files.get_entries()
        self.table.setRowCount(len(entries))
        
        for row, entry in enumerate(entries):
            # Model
            model_item = QTableWidgetItem(entry.model)
            model_item.setFlags(model_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, model_item)
            
            # OS Version
            os_item = QTableWidgetItem(entry.os_version or "-")
            os_item.setFlags(os_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, os_item)
            
            # File path
            file_item = QTableWidgetItem(entry.file_path or "(not assigned)")
            file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
            if not entry.file_path:
                file_item.setForeground(Qt.gray)
            self.table.setItem(row, 2, file_item)
            
            # Status
            status = entry.file_state
            status_item = QTableWidgetItem(status.value)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            if status == FileState.NOT_PRESENT:
                status_item.setForeground(Qt.red)
            elif status == FileState.LOADED:
                status_item.setForeground(Qt.darkGreen)
            self.table.setItem(row, 3, status_item)
        
        # Set auto-load combo
        for i in range(self.auto_load_combo.count()):
            if self.auto_load_combo.itemData(i) == self.master_files.auto_load:
                self.auto_load_combo.setCurrentIndex(i)
                break
    
    def _get_selected_entry(self) -> tuple:
        """Get the selected entry's model and OS version."""
        row = self.table.currentRow()
        if row < 0:
            return None, None
        
        model = self.table.item(row, 0).text()
        os_version = self.table.item(row, 1).text()
        if os_version == "-":
            os_version = ""
        
        return model, os_version
    
    def _on_assign(self):
        """Assign a master file to the selected entry."""
        model, os_version = self._get_selected_entry()
        if model is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a model to assign a master file."
            )
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Master File for {model} {os_version}".strip(),
            "",
            "PCG Files (*.pcg *.PCG);;All Files (*)"
        )
        
        if file_path:
            self.master_files.set_master_file(model, os_version, file_path)
            self._load_data()
    
    def _on_unassign(self):
        """Unassign the master file from the selected entry."""
        model, os_version = self._get_selected_entry()
        if model is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a model to unassign."
            )
            return
        
        entry = self.master_files.get_entry(model, os_version)
        if entry and entry.file_path:
            self.master_files.set_master_file(model, os_version, "")
            self._load_data()
    
    def _on_auto_load_changed(self, index: int):
        """Handle auto-load setting change."""
        option = self.auto_load_combo.itemData(index)
        if option:
            self.master_files.auto_load = option
            self.master_files.save_settings()
