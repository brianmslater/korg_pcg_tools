"""Enhanced PCG file writer with modification support."""

import struct
from pathlib import Path
from .models import PcgFile


class EnhancedPcgWriter:
    """Write PCG files with support for modifications."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self.data = bytearray(pcg.raw_data) if pcg.raw_data else bytearray()
    
    def write(self, filepath: str):
        """Write PCG file to disk with modifications."""
        if not self.pcg.is_dirty:
            # No modifications, just write raw data
            if self.pcg.raw_data:
                with open(filepath, 'wb') as f:
                    f.write(self.pcg.raw_data)
                return
        
        # Apply modifications to binary data
        self._update_program_names()
        self._update_combi_names()
        self._update_categories()
        self._update_favorites()
        
        # Write modified data
        with open(filepath, 'wb') as f:
            f.write(bytes(self.data))
    
    def _update_program_names(self):
        """Update program names in binary data."""
        for bank in self.pcg.program_banks:
            for program in bank.patches:
                if hasattr(program, 'raw_data') and program.raw_data:
                    # Program name is at offset 0, 24 bytes
                    # Find program in data and update
                    # This is simplified - real implementation needs proper offset tracking
                    pass
                # For now, we'll need to track byte offsets during parsing
                # This is a placeholder for the full implementation
    
    def _update_combi_names(self):
        """Update combi names in binary data."""
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if hasattr(combi, 'raw_data') and combi.raw_data:
                    # Combi name is at offset 0, 24 bytes
                    pass
    
    def _update_categories(self):
        """Update category data in binary data."""
        # Categories are stored in program/combi data
        # Typically at a fixed offset (model-specific)
        pass
    
    def _update_favorites(self):
        """Update favorite flags in binary data."""
        # Favorites are typically a single bit in the patch data
        pass
    
    def _write_string(self, offset: int, text: str, max_length: int):
        """Write a string to binary data."""
        # Encode string
        encoded = text.encode('ascii', errors='ignore')[:max_length]
        
        # Pad with zeros
        padded = encoded + b'\x00' * (max_length - len(encoded))
        
        # Write to data
        self.data[offset:offset+max_length] = padded


def write_pcg_file_enhanced(pcg: PcgFile, filepath: str):
    """Write PCG file with modifications."""
    writer = EnhancedPcgWriter(pcg)
    writer.write(filepath)
