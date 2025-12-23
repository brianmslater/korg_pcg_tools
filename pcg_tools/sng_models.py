"""
SNG file data models for Korg song files.

Based on C# implementation:
- Model/Common/Synth/SongsRelated/Song.cs
- Model/Common/Synth/SongsRelated/Songs.cs
- Model/Common/Synth/SongsRelated/Region.cs
- Model/Common/Synth/SongsRelated/Regions.cs
- Model/Common/Synth/SongsRelated/SongMemory.cs
- Model/Common/Synth/SongsRelated/SongTimbre.cs
- Model/Common/Synth/SongsRelated/SongTimbres.cs
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SongTimbre:
    """
    Represents a single timbre/track in a song.
    
    Based on C# SongTimbre.cs - inherits from Timbre base class.
    For Kronos: 188 bytes per timbre, 16 timbres per song.
    """
    index: int
    byte_offset: int = 0
    # Program reference (bank and program index)
    program_bank_index: int = 0
    program_index: int = 0
    
    @property
    def program_id(self) -> str:
        """Get the program ID string (e.g., 'I-A000')."""
        # Bank names for Kronos (from KronosSongMemory.cs)
        bank_names = [
            "I-A", "I-B", "I-C", "I-D", "I-E", "I-F", "GM", "g(1)", "g(2)", "g(3)",
            "g(4)", "g(5)", "g(6)", "g(7)", "g(8)", "g(9)", "g(d)",
            "U-A", "U-B", "U-C", "U-D", "U-E", "U-F", "U-G", "U-AA", "U-BB",
            "U-CC", "U-DD", "U-EE", "U-FF", "U-GG"
        ]
        if 0 <= self.program_bank_index < len(bank_names):
            bank_id = bank_names[self.program_bank_index]
        else:
            bank_id = "???"
        return f"{bank_id}{self.program_index:03d}"


@dataclass
class Song:
    """
    Represents a song in an SNG file.
    
    Based on C# Song.cs.
    """
    index: int
    name: str
    byte_offset: int = 0
    byte_length: int = 0
    timbres: List[SongTimbre] = field(default_factory=list)
    is_selected: bool = False
    
    def __post_init__(self):
        """Initialize timbres list if not provided."""
        if not self.timbres:
            self.timbres = []


@dataclass
class Region:
    """
    Represents an audio region/sample reference in an SNG file.
    
    Based on C# Region.cs.
    Contains the region name and the sample file name.
    """
    index: int
    name: str
    sample_filename: str
    is_selected: bool = False


@dataclass
class SngFile:
    """
    Represents a complete SNG (song) file.
    
    Based on C# SongMemory.cs.
    Contains songs and regions (audio samples).
    """
    filename: str
    model: str = "Kronos"  # Default to Kronos
    songs: List[Song] = field(default_factory=list)
    regions: List[Region] = field(default_factory=list)
    content: bytes = field(default_factory=bytes, repr=False)
    is_dirty: bool = False
    
    # Connected PCG file (optional)
    connected_pcg_filename: Optional[str] = None
    
    def __post_init__(self):
        """Initialize lists if not provided."""
        if not self.songs:
            self.songs = []
        if not self.regions:
            self.regions = []
    
    @property
    def song_count(self) -> int:
        """Return the number of songs."""
        return len(self.songs)
    
    @property
    def region_count(self) -> int:
        """Return the number of regions/samples."""
        return len(self.regions)
