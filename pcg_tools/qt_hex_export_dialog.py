"""
Qt dialog for hex export display.

Based on C# implementation:
- HexExportDlg.xaml
- HexExportDlg.xaml.cs

Displays raw hex data for selected patches in a scrollable text view.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton,
    QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont


class HexExportDialog(QDialog):
    """
    Dialog for displaying hex export of patch data.
    
    Based on C# HexExportDlg.xaml.
    """
    
    def __init__(self, hex_text: str, title: str = "Hex Export", parent=None):
        super().__init__(parent)
        self.hex_text = hex_text
        self.setWindowTitle(title)
        self.setMinimumSize(600, 500)
        self.resize(700, 600)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Text display - monospace font like C# Courier New
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier New", 10))
        self.text_edit.setPlainText(self.hex_text)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.text_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save to File...")
        save_btn.clicked.connect(self._save_to_file)
        btn_layout.addWidget(save_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def _save_to_file(self):
        """Save hex export to a text file."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Hex Export",
            "hex_export.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.hex_text)
                QMessageBox.information(
                    self,
                    "Saved",
                    f"Hex export saved to:\n{filename}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save file:\n{str(e)}"
                )
