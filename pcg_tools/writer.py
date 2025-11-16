"""PCG file writer."""

import struct
from pathlib import Path
from .models import PcgFile


class PcgWriter:
    """Write PCG files."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
    
    def write(self, filepath: str):
        """Write PCG file to disk."""
        # For now, if we haven't modified the structure, write the raw data
        if self.pcg.raw_data:
            with open(filepath, 'wb') as f:
                f.write(self.pcg.raw_data)
        else:
            raise NotImplementedError("Creating new PCG files from scratch not yet implemented")
    
    def _build_header(self) -> bytes:
        """Build PCG file header."""
        header = bytearray(16)
        header[0:4] = b'KORG'
        header[4] = self.pcg.header.product_id
        header[5] = self.pcg.header.file_type
        header[6] = self.pcg.header.major_version
        header[7] = self.pcg.header.minor_version
        return bytes(header)


def write_pcg_file(pcg: PcgFile, filepath: str):
    """Convenience function to write a PCG file."""
    writer = PcgWriter(pcg)
    writer.write(filepath)


def create_blank_pcg(output_path: str, num_program_banks: int = 1, num_combi_banks: int = 1):
    """Create a blank PCG file with empty banks.
    
    Args:
        output_path: Path to save the blank PCG file
        num_program_banks: Number of program banks to create (default 1)
        num_combi_banks: Number of combi banks to create (default 1)
    
    Returns:
        PcgFile object
    """
    import struct
    from .models import PcgFile, PcgHeader, WorkstationModel, Bank, Program, Combi, Category
    
    # Create PCG header
    header = PcgHeader(
        magic=b'KORG',
        product_id=0x68,  # Kronos
        file_type=0x00,
        major_version=2,
        minor_version=2,
        model=WorkstationModel.KRONOS
    )
    
    # Create PCG file object
    pcg = PcgFile(header=header, program_banks=[], combi_banks=[], set_lists=[])
    
    # Create program banks
    for bank_idx in range(num_program_banks):
        bank_id = f"I-{chr(65 + bank_idx)}"  # I-A, I-B, I-C, etc.
        bank = Bank(bank_id=bank_id, bank_type='Program')
        
        for i in range(128):
            program = Program(
                bank=bank_id,
                index=i,
                name=f"Init Program {i:03d}",
                category=Category(0, 0),
                favorite=False,
                raw_data=b'\x00' * 4960  # Kronos program size
            )
            bank.patches.append(program)
        
        pcg.program_banks.append(bank)
    
    # Create combi banks
    for bank_idx in range(num_combi_banks):
        bank_id = f"I-{chr(65 + bank_idx)}"  # I-A, I-B, I-C, etc.
        bank = Bank(bank_id=bank_id, bank_type='Combi')
        
        for i in range(128):
            combi = Combi(
                bank=bank_id,
                index=i,
                name=f"Init Combi {i:03d}",
                category=Category(0, 0),
                favorite=False,
                timbres=[],
                raw_data=b'\x00' * 7810  # Kronos combi size
            )
            bank.patches.append(combi)
        
        pcg.combi_banks.append(bank)
    
    # Write to file
    write_pcg_file(pcg, output_path)
    
    return pcg
