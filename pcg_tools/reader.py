"""PCG file reader and parser."""

import struct
from pathlib import Path
from typing import BinaryIO
from .models import (
    PcgFile, PcgHeader, WorkstationModel, Bank, Program, Combi, 
    Category, Timbre, SetListSlot
)
from .pcg_parser import PcgBinaryParser


class PcgReader:
    """Read and parse PCG files."""
    
    # Product ID to model mapping
    PRODUCT_IDS = {
        0x68: WorkstationModel.KRONOS,
        0x6A: WorkstationModel.OASYS,
        0x50: WorkstationModel.TRITON,  # Also Studio, Extreme
        0x5D: WorkstationModel.KARMA,
        0x75: WorkstationModel.M3,
        0x76: WorkstationModel.M50,
        0x7C: WorkstationModel.KROME,
    }
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = b''
        
    def read(self) -> PcgFile:
        """Read and parse the PCG file."""
        with open(self.filepath, 'rb') as f:
            self.data = f.read()
        
        if len(self.data) < 16:
            raise ValueError("File too small to be a valid PCG file")
        
        header = self._parse_header()
        pcg = PcgFile(header=header, raw_data=self.data)
        
        # Use proper binary parser
        parser = PcgBinaryParser(self.data)
        parser.parse_prg1_chunk(pcg)
        parser.parse_cmb1_chunk(pcg)
        parser.parse_sls1_chunk(pcg)
        
        return pcg
    
    def _parse_header(self) -> PcgHeader:
        """Parse PCG file header."""
        magic = self.data[0:4]
        if magic != b'KORG':
            raise ValueError(f"Invalid PCG file: magic bytes are {magic}, expected b'KORG'")
        
        product_id = self.data[4]
        file_type = self.data[5]
        major_version = self.data[6]
        minor_version = self.data[7]
        
        model = self.PRODUCT_IDS.get(product_id, WorkstationModel.KRONOS)
        
        return PcgHeader(
            magic=magic,
            product_id=product_id,
            file_type=file_type,
            major_version=major_version,
            minor_version=minor_version,
            model=model
        )
    

    
    @staticmethod
    def read_string(data: bytes, offset: int, length: int) -> str:
        """Read a null-terminated or fixed-length string."""
        string_data = data[offset:offset+length]
        # Find null terminator
        null_pos = string_data.find(b'\x00')
        if null_pos >= 0:
            string_data = string_data[:null_pos]
        try:
            return string_data.decode('ascii', errors='ignore')
        except:
            return ""


def read_pcg_file(filepath: str) -> PcgFile:
    """Convenience function to read a PCG file."""
    reader = PcgReader(filepath)
    return reader.read()
