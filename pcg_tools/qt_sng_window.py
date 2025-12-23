"""
Qt-based SNG file window for viewing song files.

Based on C# implementation:
- SongWindow.xaml
- SongWindow.xaml.cs
- SongTimbresWindow.xaml
- SongTimbresWindow.xaml.cs

Features:
- Songs tab: List of songs with index and name
- Samples tab: List of audio regions with name and sample filename
- Export to file functionality
- MIDI Tracks button (shows timbres for selected song)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QAbstractItemView, QMessageBox,
    QFileDialog, QDialog, QLabel
)
from PySide6.QtCore import Qt

from .sng_models import SngFile, Song


class SongTimbresDialog(QDialog):
    """
    Dialog showing timbres/tracks for a selected song.
    
    Based on C# SongTimbresWindow.xaml.
    """
    
    def __init__(self, song: Song, parent=None):
        super().__init__(parent)
        self.song = song
        self.setWindowTitle(f"MIDI Tracks - {song.name}")
        self.setMinimumSize(500, 400)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(f"Song: {self.song.name} (Index: {self.song.index})")
        layout.addWidget(info_label)
        
        # Timbres table
        self.timbres_table = QTableWidget()
        self.timbres_table.setColumnCount(3)
        self.timbres_table.setHorizontalHeaderLabels(["Track", "Program ID", "Byte Offset"])
        self.timbres_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.timbres_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.timbres_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Populate timbres
        self.timbres_table.setRowCount(len(self.song.timbres))
        for row, timbre in enumerate(self.song.timbres):
            self.timbres_table.setItem(row, 0, QTableWidgetItem(str(timbre.index + 1)))
            self.timbres_table.setItem(row, 1, QTableWidgetItem(timbre.program_id))
            self.timbres_table.setItem(row, 2, QTableWidgetItem(f"0x{timbre.byte_offset:08X}"))
        
        layout.addWidget(self.timbres_table)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class SngWindow(QWidget):
    """
    Window for viewing SNG (song) files.
    
    Based on C# SongWindow.xaml and SongWindow.xaml.cs.
    """
    
    def __init__(self, sng_file: SngFile, parent=None):
        super().__init__(parent)
        self.sng_file = sng_file
        self.setWindowTitle(f"Song File - {sng_file.filename}")
        self.setMinimumSize(700, 500)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tab widget (Songs / Samples)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Songs tab
        songs_widget = QWidget()
        songs_layout = QVBoxLayout(songs_widget)
        
        self.songs_table = QTableWidget()
        self.songs_table.setColumnCount(2)
        self.songs_table.setHorizontalHeaderLabels(["Index", "Name"])
        self.songs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.songs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.songs_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.songs_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.songs_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.songs_table.itemSelectionChanged.connect(self._on_song_selection_changed)
        songs_layout.addWidget(self.songs_table)
        
        # Songs buttons
        songs_btn_layout = QHBoxLayout()
        self.midi_tracks_btn = QPushButton("MIDI Tracks")
        self.midi_tracks_btn.setEnabled(False)
        self.midi_tracks_btn.clicked.connect(self._show_midi_tracks)
        songs_btn_layout.addWidget(self.midi_tracks_btn)
        
        self.export_songs_btn = QPushButton("Export to File")
        self.export_songs_btn.clicked.connect(self._export_songs)
        songs_btn_layout.addWidget(self.export_songs_btn)
        
        songs_btn_layout.addStretch()
        songs_layout.addLayout(songs_btn_layout)
        
        self.tab_widget.addTab(songs_widget, "Songs")
        
        # Samples tab
        samples_widget = QWidget()
        samples_layout = QVBoxLayout(samples_widget)
        
        self.samples_table = QTableWidget()
        self.samples_table.setColumnCount(3)
        self.samples_table.setHorizontalHeaderLabels(["Index", "Name", "Sample File Name"])
        self.samples_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.samples_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.samples_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.samples_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.samples_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.samples_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        samples_layout.addWidget(self.samples_table)
        
        # Samples buttons
        samples_btn_layout = QHBoxLayout()
        self.export_samples_btn = QPushButton("Export to File")
        self.export_samples_btn.clicked.connect(self._export_samples)
        samples_btn_layout.addWidget(self.export_samples_btn)
        samples_btn_layout.addStretch()
        samples_layout.addLayout(samples_btn_layout)
        
        self.tab_widget.addTab(samples_widget, "Samples")
    
    def _load_data(self):
        """Load data from the SNG file into the tables."""
        # Load songs
        self.songs_table.setRowCount(len(self.sng_file.songs))
        for row, song in enumerate(self.sng_file.songs):
            index_item = QTableWidgetItem(str(song.index + 1))
            index_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.songs_table.setItem(row, 0, index_item)
            self.songs_table.setItem(row, 1, QTableWidgetItem(song.name))
        
        # Load samples/regions
        self.samples_table.setRowCount(len(self.sng_file.regions))
        for row, region in enumerate(self.sng_file.regions):
            index_item = QTableWidgetItem(str(region.index + 1))
            index_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.samples_table.setItem(row, 0, index_item)
            self.samples_table.setItem(row, 1, QTableWidgetItem(region.name))
            self.samples_table.setItem(row, 2, QTableWidgetItem(region.sample_filename))
    
    def _on_song_selection_changed(self):
        """Handle song selection change."""
        selected_rows = self.songs_table.selectionModel().selectedRows()
        self.midi_tracks_btn.setEnabled(len(selected_rows) == 1)
    
    def _show_midi_tracks(self):
        """Show MIDI tracks/timbres for the selected song."""
        selected_rows = self.songs_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if 0 <= row < len(self.sng_file.songs):
            song = self.sng_file.songs[row]
            dialog = SongTimbresDialog(song, self)
            dialog.exec()
    
    def _export_songs(self):
        """
        Export songs list to a text file.
        
        Based on C# SongWindow.ExportToFile_Click().
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Songs",
            f"{self.sng_file.filename}_songs.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            lines = []
            lines.append(" #  Song Name")
            lines.append("--- " + "-" * 60)
            
            for song in self.sng_file.songs:
                lines.append(f"{song.index + 1:3} {song.name}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            QMessageBox.information(
                self,
                "Export Complete",
                f"Songs exported to:\n{filename}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export songs:\n{str(e)}"
            )
    
    def _export_samples(self):
        """
        Export samples list to a text file.
        
        Based on C# SongWindow.SamplesExportToFile_Click().
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Samples",
            f"{self.sng_file.filename}_samples.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            lines = []
            lines.append(" #  Sample Name" + " " * 48 + "Sample File Name")
            lines.append("--- " + "-" * 60 + " " + "-" * 60)
            
            for region in self.sng_file.regions:
                lines.append(f"{region.index + 1:3} {region.name:<60} {region.sample_filename:<60}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            QMessageBox.information(
                self,
                "Export Complete",
                f"Samples exported to:\n{filename}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export samples:\n{str(e)}"
            )
