"""
SNG file parser for Korg song files.

Based on C# implementation:
- Model/Common/File/SongFileReader.cs
- Model/KronosSpecific/Song/KronosSongFileReader.cs

SNG file structure:
- Header (32 bytes)
- SNG1 chunk containing:
  - SDK1: Song definitions (names)
  - SGS1: Song data containing SDT1 chunks
  - RGN1: Audio regions/samples
"""

import struct
from typing import Optional, Tuple

from .sng_models import SngFile, Song, SongTimbre, Region


class SngParser:
    """
    Parser for Korg SNG (song) files.
    
    Based on C# SongFileReader.cs and KronosSongFileReader.cs.
    """
    
    # Constants from C# KronosSongFileReader.cs
    KRONOS_TIMBRE_BYTE_LENGTH = 188
    KRONOS_NUM_SONG_TRACKS = 16
    KRONOS_TIMBRES_BYTE_OFFSET = 0x12C2 + 12  # 4802 + 12 = 4814
    
    # Region constants from C# SongFileReader.cs ReadRgn1Chunk
    MAX_REGION_NAME_SIZE = 24
    MAX_REGION_SAMPLE_FILENAME_SIZE = 84
    
    def __init__(self):
        self._index = 0
        self._content: bytes = b''
        self._sng_file: Optional[SngFile] = None
    
    def parse(self, filename: str) -> SngFile:
        """
        Parse an SNG file and return an SngFile object.
        
        Args:
            filename: Path to the SNG file
            
        Returns:
            SngFile object containing parsed data
        """
        with open(filename, 'rb') as f:
            self._content = f.read()
        
        self._sng_file = SngFile(filename=filename, content=self._content)
        self._read_chunks()
        
        return self._sng_file
    
    def parse_bytes(self, content: bytes, filename: str = "") -> SngFile:
        """
        Parse SNG file content from bytes.
        
        Args:
            content: Raw bytes of the SNG file
            filename: Optional filename for reference
            
        Returns:
            SngFile object containing parsed data
        """
        self._content = content
        self._sng_file = SngFile(filename=filename, content=content)
        self._read_chunks()
        
        return self._sng_file
    
    def _read_chunks(self):
        """
        Read all chunks from the SNG file.
        
        Based on C# SongFileReader.ReadChunks().
        """
        # Start after header (32 bytes) - from C#: _index = 32; // Sng1Offset
        self._index = 32
        
        # Read header size and skip
        header_size = self._get_int(self._index, 4)
        self._index += 4 + header_size
        
        # Read chunks until end of file
        while self._index < len(self._content):
            chunk_name = self._get_chars(self._index, 4)
            chunk_size = self._get_int(self._index + 4, 4)
            self._index += 12  # Skip chunk header (4 name + 4 size + 4 reserved)
            
            if chunk_name == "CUE1":
                self._read_cue1_chunk(chunk_size)
            elif chunk_name == "PDX1":
                self._read_pdx1_chunk(chunk_size)
            elif chunk_name == "RGN1":
                self._read_rgn1_chunk(chunk_size)
            elif chunk_name == "SNG1":
                self._read_sng1_chunk(chunk_size)
            else:
                # Unknown chunk - skip it
                self._index += chunk_size
    
    def _read_sng1_chunk(self, chunk_size: int):
        """
        Read the main SNG1 chunk containing song data.
        
        Based on C# SongFileReader.ReadSng1Chunk().
        """
        end_of_chunk = self._index + chunk_size
        
        while self._index < len(self._content) and self._index < end_of_chunk:
            chunk_name = self._get_chars(self._index, 4)
            chunk_size = self._get_int(self._index + 4, 4)
            self._index += 12
            
            if chunk_name == "CUE1":
                self._read_cue1_chunk(chunk_size)
            elif chunk_name == "PDX1":
                self._read_pdx1_chunk(chunk_size)
            elif chunk_name == "RGN1":
                self._read_rgn1_chunk(chunk_size)
            elif chunk_name == "SDK1":
                self._read_sdk1_chunk()
            elif chunk_name == "SGS1":
                self._read_sgs1_chunk(chunk_size)
            else:
                # Unknown chunk - skip
                self._index += chunk_size
    
    def _read_sdk1_chunk(self):
        """
        Read SDK1 chunk containing song definitions (names).
        
        Based on C# SongFileReader.ReadSdk1Chunk().
        """
        amount_of_songs = self._get_int(self._index, 4)
        self._index += 4
        song_size = self._get_int(self._index, 4)
        self._index += 8  # Skip song_size and 4 bytes padding
        
        # Read song names
        for item_index in range(amount_of_songs):
            song_name = self._get_chars(self._index, 24).rstrip('\x00')
            
            # Create song with timbres
            song = Song(
                index=item_index,
                name=song_name,
            )
            
            # Create timbres for this song
            for timbre_index in range(self.KRONOS_NUM_SONG_TRACKS):
                timbre = SongTimbre(index=timbre_index)
                song.timbres.append(timbre)
            
            self._sng_file.songs.append(song)
            self._index += song_size
    
    def _read_sgs1_chunk(self, chunk_size: int):
        """
        Read SGS1 chunk containing song data (SDT1 chunks).
        
        Based on C# SongFileReader.ReadSgs1Chunk().
        """
        for song in self._sng_file.songs:
            self._read_sdt1_chunk(song)
    
    def _read_sdt1_chunk(self, song: Song):
        """
        Read SDT1 chunk for a specific song.
        
        Based on C# SongFileReader.ReadSdt1Chunk().
        """
        # Read SDT1 header
        sdt1_chunk_size = self._get_int(self._index + 4, 4)
        self._index += 12
        end_of_chunk = self._index + sdt1_chunk_size
        
        while self._index < end_of_chunk:
            chunk_name = self._get_chars(self._index, 4)
            chunk_size = self._get_int(self._index + 4, 4)
            self._index += 12
            
            if chunk_name == "ADT1":
                self._read_adt1_chunk(chunk_size)
            elif chunk_name == "SPR1":
                self._read_spr1_chunk(chunk_size)
            elif chunk_name == "BMT1":
                self._read_bmt1_chunk(song, chunk_size)
            elif chunk_name == "BMT2":
                self._read_bmt2_chunk()
            elif chunk_name == "MDT1":
                self._read_mdt1_chunk(chunk_size)
            elif chunk_name == "PTN1":
                self._read_ptn1_chunk(chunk_size)
            elif chunk_name == "RGN1":
                self._read_rgn1_chunk(chunk_size)
            elif chunk_name == "SDT1":
                self._read_sdt1_in_sdt1_chunk(chunk_size)
            elif chunk_name == "TRK1":
                self._read_trk1_chunk(chunk_size)
            else:
                # Unknown chunk - skip
                self._index += chunk_size
    
    def _read_bmt1_chunk(self, song: Song, chunk_size: int):
        """
        Read BMT1 chunk containing timbre/track data.
        
        Based on C# SongFileReader.ReadBmt1Chunk().
        """
        # Set song byte offset (from C#: song.ByteOffset = _index + 0x12C2 + 12)
        song.byte_offset = self._index + self.KRONOS_TIMBRES_BYTE_OFFSET
        
        # Set timbre byte offsets
        for timbre_index, timbre in enumerate(song.timbres):
            timbre.byte_offset = song.byte_offset + (timbre_index * self.KRONOS_TIMBRE_BYTE_LENGTH)
        
        self._index += chunk_size
    
    def _read_bmt2_chunk(self):
        """
        Read BMT2 chunk (obsolete for Kronos OS 1.5/1.6).
        
        Based on C# SongFileReader.ReadBmt2Chunk().
        """
        self._index += 4  # 4 zero's padding
        self._index += 2 * 16  # Skip banks and programs
    
    def _read_rgn1_chunk(self, chunk_size: int):
        """
        Read RGN1 chunk containing audio regions/samples.
        
        Based on C# SongFileReader.ReadRgn1Chunk().
        """
        amount = self._get_int(self._index, 4)
        start_index = self._index
        self._index += 12  # Skip until first region
        
        for item_index in range(amount):
            region_name = self._get_chars(self._index, self.MAX_REGION_NAME_SIZE).rstrip('\x00')
            sample_filename = self._get_chars(
                self._index + self.MAX_REGION_NAME_SIZE,
                self.MAX_REGION_SAMPLE_FILENAME_SIZE
            ).rstrip('\x00')
            
            region = Region(
                index=item_index,
                name=region_name,
                sample_filename=sample_filename
            )
            self._sng_file.regions.append(region)
            
            self._index += self.MAX_REGION_NAME_SIZE + self.MAX_REGION_SAMPLE_FILENAME_SIZE + 16
        
        # Ensure we're at the end of the chunk
        self._index = start_index + chunk_size
    
    def _read_cue1_chunk(self, chunk_size: int):
        """Read CUE1 chunk (found on M50 preload SNG)."""
        self._index += chunk_size
    
    def _read_pdx1_chunk(self, chunk_size: int):
        """Read PDX1 chunk (found on M50 preload SNG)."""
        self._index += chunk_size
    
    def _read_adt1_chunk(self, chunk_size: int):
        """Read ADT1 chunk."""
        self._index += chunk_size
    
    def _read_spr1_chunk(self, chunk_size: int):
        """Read SPR1 chunk."""
        self._index += chunk_size
    
    def _read_mdt1_chunk(self, chunk_size: int):
        """Read MDT1 chunk."""
        self._index += chunk_size
    
    def _read_ptn1_chunk(self, chunk_size: int):
        """Read PTN1 chunk."""
        self._index += chunk_size
    
    def _read_sdt1_in_sdt1_chunk(self, chunk_size: int):
        """Read nested SDT1 chunk."""
        self._index += chunk_size
    
    def _read_trk1_chunk(self, chunk_size: int):
        """Read TRK1 chunk."""
        self._index += chunk_size
    
    def _get_int(self, offset: int, length: int) -> int:
        """
        Get an integer value from the content at the specified offset.
        
        Args:
            offset: Byte offset in content
            length: Number of bytes (1, 2, or 4)
            
        Returns:
            Integer value (little-endian)
        """
        if offset + length > len(self._content):
            return 0
        
        if length == 1:
            return self._content[offset]
        elif length == 2:
            return struct.unpack('<H', self._content[offset:offset + 2])[0]
        elif length == 4:
            return struct.unpack('<I', self._content[offset:offset + 4])[0]
        return 0
    
    def _get_chars(self, offset: int, length: int) -> str:
        """
        Get a string from the content at the specified offset.
        
        Args:
            offset: Byte offset in content
            length: Number of bytes to read
            
        Returns:
            String value (ASCII decoded)
        """
        if offset + length > len(self._content):
            return ""
        
        try:
            return self._content[offset:offset + length].decode('ascii', errors='replace')
        except Exception:
            return ""


def read_sng_file(filename: str) -> SngFile:
    """
    Convenience function to read an SNG file.
    
    Args:
        filename: Path to the SNG file
        
    Returns:
        SngFile object containing parsed data
    """
    parser = SngParser()
    return parser.parse(filename)
