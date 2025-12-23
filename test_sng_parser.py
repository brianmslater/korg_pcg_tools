#!/usr/bin/env python3
"""
Test script for SNG file parser.

Tests the SNG file parsing functionality based on C# implementation.
"""

import os
import sys
import unittest
from pathlib import Path

# Add pcg_tools to path
sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.sng_models import SngFile, Song, SongTimbre, Region
from pcg_tools.sng_parser import SngParser, read_sng_file


class TestSngModels(unittest.TestCase):
    """Test SNG data models."""
    
    def test_song_timbre_creation(self):
        """Test SongTimbre creation."""
        timbre = SongTimbre(index=0)
        self.assertEqual(timbre.index, 0)
        self.assertEqual(timbre.byte_offset, 0)
        self.assertEqual(timbre.program_bank_index, 0)
        self.assertEqual(timbre.program_index, 0)
    
    def test_song_timbre_program_id(self):
        """Test SongTimbre program ID generation."""
        timbre = SongTimbre(index=0, program_bank_index=0, program_index=5)
        self.assertEqual(timbre.program_id, "I-A005")
        
        timbre2 = SongTimbre(index=1, program_bank_index=17, program_index=10)
        self.assertEqual(timbre2.program_id, "U-A010")
        
        timbre3 = SongTimbre(index=2, program_bank_index=6, program_index=0)
        self.assertEqual(timbre3.program_id, "GM000")
    
    def test_song_creation(self):
        """Test Song creation."""
        song = Song(index=0, name="Test Song")
        self.assertEqual(song.index, 0)
        self.assertEqual(song.name, "Test Song")
        self.assertEqual(len(song.timbres), 0)
        self.assertFalse(song.is_selected)
    
    def test_song_with_timbres(self):
        """Test Song with timbres."""
        song = Song(index=0, name="Test Song")
        for i in range(16):
            song.timbres.append(SongTimbre(index=i))
        self.assertEqual(len(song.timbres), 16)
    
    def test_region_creation(self):
        """Test Region creation."""
        region = Region(index=0, name="Audio Track 1", sample_filename="sample.wav")
        self.assertEqual(region.index, 0)
        self.assertEqual(region.name, "Audio Track 1")
        self.assertEqual(region.sample_filename, "sample.wav")
        self.assertFalse(region.is_selected)
    
    def test_sng_file_creation(self):
        """Test SngFile creation."""
        sng = SngFile(filename="test.sng")
        self.assertEqual(sng.filename, "test.sng")
        self.assertEqual(sng.model, "Kronos")
        self.assertEqual(len(sng.songs), 0)
        self.assertEqual(len(sng.regions), 0)
        self.assertFalse(sng.is_dirty)
    
    def test_sng_file_counts(self):
        """Test SngFile song and region counts."""
        sng = SngFile(filename="test.sng")
        sng.songs.append(Song(index=0, name="Song 1"))
        sng.songs.append(Song(index=1, name="Song 2"))
        sng.regions.append(Region(index=0, name="Region 1", sample_filename="r1.wav"))
        
        self.assertEqual(sng.song_count, 2)
        self.assertEqual(sng.region_count, 1)


class TestSngParser(unittest.TestCase):
    """Test SNG parser."""
    
    def test_parser_creation(self):
        """Test SngParser creation."""
        parser = SngParser()
        self.assertIsNotNone(parser)
    
    def test_parser_constants(self):
        """Test parser constants match C# values."""
        # From KronosSongFileReader.cs
        self.assertEqual(SngParser.KRONOS_TIMBRE_BYTE_LENGTH, 188)
        self.assertEqual(SngParser.KRONOS_NUM_SONG_TRACKS, 16)
        # 0x12C2 + 12 = 4802 + 12 = 4814
        self.assertEqual(SngParser.KRONOS_TIMBRES_BYTE_OFFSET, 4814)
        
        # From SongFileReader.cs ReadRgn1Chunk
        self.assertEqual(SngParser.MAX_REGION_NAME_SIZE, 24)
        self.assertEqual(SngParser.MAX_REGION_SAMPLE_FILENAME_SIZE, 84)


class TestSngParserWithFiles(unittest.TestCase):
    """Test SNG parser with actual files (if available)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_files_dir = Path("files_2_test")
    
    def test_parse_sng_files_if_available(self):
        """Test parsing any available SNG files."""
        if not self.test_files_dir.exists():
            self.skipTest("Test files directory not found")
        
        sng_files = list(self.test_files_dir.glob("**/*.SNG")) + \
                    list(self.test_files_dir.glob("**/*.sng"))
        
        if not sng_files:
            self.skipTest("No SNG files found in test directory")
        
        for sng_path in sng_files:
            with self.subTest(file=sng_path.name):
                try:
                    sng = read_sng_file(str(sng_path))
                    self.assertIsInstance(sng, SngFile)
                    self.assertEqual(sng.filename, str(sng_path))
                    print(f"  Parsed {sng_path.name}: {sng.song_count} songs, {sng.region_count} samples")
                    
                    # Print song names
                    for song in sng.songs[:5]:  # First 5 songs
                        print(f"    Song {song.index}: {song.name}")
                    if sng.song_count > 5:
                        print(f"    ... and {sng.song_count - 5} more songs")
                        
                except Exception as e:
                    self.fail(f"Failed to parse {sng_path.name}: {e}")


class TestBankNames(unittest.TestCase):
    """Test bank name mapping for program IDs."""
    
    def test_internal_banks(self):
        """Test internal bank names (I-A through I-F)."""
        for i, name in enumerate(["I-A", "I-B", "I-C", "I-D", "I-E", "I-F"]):
            timbre = SongTimbre(index=0, program_bank_index=i, program_index=0)
            self.assertTrue(timbre.program_id.startswith(name))
    
    def test_gm_banks(self):
        """Test GM bank names."""
        timbre = SongTimbre(index=0, program_bank_index=6, program_index=0)
        self.assertEqual(timbre.program_id, "GM000")
        
        # g(1) through g(9) and g(d)
        for i, suffix in enumerate(["1", "2", "3", "4", "5", "6", "7", "8", "9", "d"], start=7):
            timbre = SongTimbre(index=0, program_bank_index=i, program_index=0)
            self.assertEqual(timbre.program_id, f"g({suffix})000")
    
    def test_user_banks(self):
        """Test user bank names (U-A through U-GG)."""
        user_banks = ["U-A", "U-B", "U-C", "U-D", "U-E", "U-F", "U-G", 
                      "U-AA", "U-BB", "U-CC", "U-DD", "U-EE", "U-FF", "U-GG"]
        for i, name in enumerate(user_banks, start=17):
            timbre = SongTimbre(index=0, program_bank_index=i, program_index=0)
            self.assertTrue(timbre.program_id.startswith(name), 
                          f"Bank index {i} should start with {name}, got {timbre.program_id}")
    
    def test_unknown_bank(self):
        """Test unknown bank index."""
        timbre = SongTimbre(index=0, program_bank_index=100, program_index=0)
        self.assertTrue(timbre.program_id.startswith("???"))


if __name__ == "__main__":
    print("=" * 60)
    print("SNG Parser Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
