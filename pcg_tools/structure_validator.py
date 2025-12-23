"""PCG Structure Validator Module.

This module provides validation functions to verify that the PCG parser
correctly interprets the binary file structure according to the C# reference
implementation and Korg documentation.

Based on:
- C# PcgFileReader.cs: Chunk parsing and navigation
- C# KronosOasysPcgFileReader.cs: Kronos-specific offsets
- C# KronosTimbre.cs, KronosOasysTimbre.cs: Timbre structure
- C# KronosProgram.cs: Program structure
- Official Korg documentation (PCG Structure Kronos.txt)
"""

import struct
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Any
from enum import IntEnum

from .pcg_structure import (
    FileHeader, ProductId, ChunkId, ChunkStructure,
    KronosProgramOffsets, KronosCombiOffsets, KronosTimbreOffsets,
    KronosSetListSlotOffsets, Div1Offsets,
    PROGRAM_BANK_CHUNK_IDS, COMBI_BANK_CHUNK_IDS,
    TIMBRE_BANK_PCGIDS, PCGID_TO_TIMBRE_BANK
)


# =============================================================================
# VALIDATION RESULT CLASSES
# =============================================================================

@dataclass
class ValidationIssue:
    """Represents a single validation issue found during parsing."""
    severity: str  # 'error', 'warning', 'info'
    location: str  # e.g., "PBK1 chunk at 0x12345"
    expected: Any
    actual: Any
    message: str


@dataclass
class ChunkInfo:
    """Information about a parsed chunk."""
    chunk_id: bytes
    offset: int
    size: int
    data_offset: int  # offset + 8 (after header)
    
    @property
    def end_offset(self) -> int:
        return self.offset + 8 + self.size


@dataclass
class ValidationReport:
    """Complete validation report for a PCG file."""
    file_path: str = ""
    product_id: int = 0
    product_name: str = ""
    file_size: int = 0
    
    # Chunk information
    chunks: List[ChunkInfo] = field(default_factory=list)
    
    # Validation issues
    issues: List[ValidationIssue] = field(default_factory=list)
    
    # Statistics
    program_banks_found: int = 0
    combi_banks_found: int = 0
    setlists_found: int = 0
    
    @property
    def has_errors(self) -> bool:
        return any(i.severity == 'error' for i in self.issues)
    
    @property
    def has_warnings(self) -> bool:
        return any(i.severity == 'warning' for i in self.issues)
    
    def add_issue(self, severity: str, location: str, expected: Any, 
                  actual: Any, message: str):
        self.issues.append(ValidationIssue(
            severity=severity,
            location=location,
            expected=expected,
            actual=actual,
            message=message
        ))
    
    def summary(self) -> str:
        """Generate a summary of the validation report."""
        lines = [
            f"PCG Validation Report: {self.file_path}",
            f"Product: {self.product_name} (0x{self.product_id:02X})",
            f"File size: {self.file_size} bytes",
            f"Chunks found: {len(self.chunks)}",
            f"Program banks: {self.program_banks_found}",
            f"Combi banks: {self.combi_banks_found}",
            f"Set lists: {self.setlists_found}",
            "",
            f"Issues: {len(self.issues)} total",
            f"  Errors: {sum(1 for i in self.issues if i.severity == 'error')}",
            f"  Warnings: {sum(1 for i in self.issues if i.severity == 'warning')}",
            f"  Info: {sum(1 for i in self.issues if i.severity == 'info')}",
        ]
        
        if self.issues:
            lines.append("")
            lines.append("Issues:")
            for issue in self.issues:
                lines.append(f"  [{issue.severity.upper()}] {issue.location}: {issue.message}")
                if issue.expected != issue.actual:
                    lines.append(f"    Expected: {issue.expected}, Actual: {issue.actual}")
        
        return "\n".join(lines)


# =============================================================================
# KRONOS-SPECIFIC CONSTANTS (from C# KronosOasysPcgFileReader.cs)
# =============================================================================

class KronosParserConstants:
    """Constants from C# KronosOasysPcgFileReader.cs."""
    # Offset to DIV1 chunk from file start (after 16-byte header + PCG1 header)
    DIV1_OFFSET = 0x1C  # 28 decimal
    
    # Gap between chunks (includes 4-byte padding after chunk data)
    BETWEEN_CHUNK_GAP_SIZE = 12
    
    # PBK1 chunk: offset from chunk start to number of programs
    PBK1_NUMBER_OF_PROGRAMS_OFFSET = 12
    
    # MBK1 chunk: gap after chunk name before data
    GAP_SIZE_AFTER_MBK1_CHUNK_NAME = 4
    
    # CBK1 chunk: offset from chunk start to number of combis
    CBK1_NUMBER_OF_COMBIS_OFFSET = 12
    
    # Size between CMB1 and first CBK1
    SIZE_BETWEEN_CMB1_AND_CBK1 = 8
    
    # DBK1 chunk: offset from chunk start to number of drum kits
    DBK1_NUMBER_OF_DRUMKITS_OFFSET = 12


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

class PcgStructureValidator:
    """Validates PCG file structure against C# reference implementation."""
    
    def __init__(self, data: bytes):
        self.data = data
        self.report = ValidationReport(file_size=len(data))
    
    def get_int(self, offset: int, size: int) -> int:
        """Read big-endian integer (Korg format)."""
        if offset + size > len(self.data):
            return 0
        if size == 4:
            return struct.unpack('>I', self.data[offset:offset+4])[0]
        elif size == 2:
            return struct.unpack('>H', self.data[offset:offset+2])[0]
        elif size == 1:
            return self.data[offset]
        return 0
    
    def get_string(self, offset: int, length: int) -> str:
        """Read null-terminated ASCII string."""
        if offset + length > len(self.data):
            return ""
        string_data = self.data[offset:offset+length]
        null_pos = string_data.find(b'\x00')
        if null_pos >= 0:
            string_data = string_data[:null_pos]
        return string_data.decode('ascii', errors='ignore').strip()
    
    def validate_header(self) -> bool:
        """Validate PCG file header (16 bytes).
        
        Based on C# and Korg documentation:
        - Bytes 0-3: 'KORG' magic
        - Byte 4: Product ID
        - Byte 5: File type (0x00 = PCG)
        - Byte 6: Major version
        - Byte 7: Minor version
        - Byte 8: Checksum flag
        - Bytes 9-15: Reserved
        """
        if len(self.data) < FileHeader.HEADER_SIZE:
            self.report.add_issue(
                'error', 'File header', 
                f'>= {FileHeader.HEADER_SIZE} bytes', len(self.data),
                'File too small for PCG header'
            )
            return False
        
        # Check magic
        magic = self.data[FileHeader.MAGIC_OFFSET:FileHeader.MAGIC_OFFSET + FileHeader.MAGIC_SIZE]
        if magic != FileHeader.MAGIC:
            self.report.add_issue(
                'error', 'File header offset 0x00',
                FileHeader.MAGIC, magic,
                'Invalid magic bytes - not a Korg file'
            )
            return False
        
        # Get product ID
        product_id = self.data[FileHeader.PRODUCT_ID_OFFSET]
        self.report.product_id = product_id
        
        # Map product ID to name
        product_names = {
            ProductId.KRONOS: 'Kronos',
            ProductId.OASYS: 'Oasys',
            ProductId.TRITON: 'Triton',
            ProductId.M3: 'M3',
            ProductId.KROME: 'Krome',
            ProductId.KROSS: 'Kross',
            ProductId.KROSS_2: 'Kross 2',
            ProductId.KROME_EX: 'Krome EX',
        }
        self.report.product_name = product_names.get(product_id, f'Unknown (0x{product_id:02X})')
        
        # Check file type
        file_type = self.data[FileHeader.FILE_TYPE_OFFSET]
        if file_type != 0x00:
            self.report.add_issue(
                'warning', 'File header offset 0x05',
                0x00, file_type,
                f'Unexpected file type (expected PCG=0x00, got 0x{file_type:02X})'
            )
        
        return True
    
    def validate_pcg1_chunk(self) -> Optional[ChunkInfo]:
        """Validate PCG1 container chunk.
        
        PCG1 should be at offset 0x10 (after 16-byte header).
        """
        pcg1_offset = FileHeader.HEADER_SIZE  # 0x10
        
        if pcg1_offset + 8 > len(self.data):
            self.report.add_issue(
                'error', f'PCG1 chunk at 0x{pcg1_offset:04X}',
                'PCG1', 'missing',
                'File too small for PCG1 chunk'
            )
            return None
        
        chunk_id = self.data[pcg1_offset:pcg1_offset+4]
        if chunk_id != ChunkId.PCG1:
            self.report.add_issue(
                'error', f'Chunk at 0x{pcg1_offset:04X}',
                ChunkId.PCG1, chunk_id,
                'Expected PCG1 chunk after header'
            )
            return None
        
        chunk_size = self.get_int(pcg1_offset + 4, 4)
        chunk_info = ChunkInfo(
            chunk_id=chunk_id,
            offset=pcg1_offset,
            size=chunk_size,
            data_offset=pcg1_offset + 8
        )
        self.report.chunks.append(chunk_info)
        
        return chunk_info
    
    def iterate_chunks(self, start_offset: int = None, gap_size: int = 12) -> List[ChunkInfo]:
        """Iterate through all chunks in the file.
        
        Based on C# PcgFileReader.ReadContent():
        - Start at Div1Offset (0x1C for Kronos)
        - Read chunk ID (4 bytes) and size (4 bytes)
        - Skip to next chunk: offset + chunkSize + BetweenChunkGapSize
        
        Args:
            start_offset: Starting offset (default: DIV1_OFFSET for Kronos)
            gap_size: BetweenChunkGapSize (12 for Kronos/Oasys, 8 for Triton)
        """
        if start_offset is None:
            # For Kronos/Oasys, DIV1 is at offset 0x1C from file start
            start_offset = KronosParserConstants.DIV1_OFFSET
        
        chunks = []
        offset = start_offset
        
        while offset < len(self.data) - 8:
            chunk_id = self.data[offset:offset+4]
            
            # Check if this looks like a valid chunk ID (4 ASCII chars)
            if not all(32 <= b < 127 for b in chunk_id):
                break
            
            chunk_size = self.get_int(offset + 4, 4)
            
            # Sanity check on chunk size
            if chunk_size > len(self.data) - offset:
                self.report.add_issue(
                    'warning', f'Chunk at 0x{offset:08X}',
                    f'<= {len(self.data) - offset}', chunk_size,
                    f'Chunk size exceeds file bounds'
                )
                break
            
            chunk_info = ChunkInfo(
                chunk_id=chunk_id,
                offset=offset,
                size=chunk_size,
                data_offset=offset + 8
            )
            chunks.append(chunk_info)
            
            # Move to next chunk
            # C# uses: Index += chunkSize + BetweenChunkGapSize
            # BetweenChunkGapSize is 12 for Kronos/Oasys, 8 for Triton
            offset += chunk_size + gap_size
        
        return chunks
    
    def validate_pbk1_structure(self, chunk: ChunkInfo) -> Dict[str, Any]:
        """Validate PBK1 (HD-1 Program Bank) chunk structure.
        
        Based on C# PcgFileReader.ReadPbk1Chunk():
        - +0: 'PBK1' (4 bytes)
        - +4: chunk size (4 bytes)
        - +12: number of programs (4 bytes)
        - +16: size of program (4 bytes)
        - +20: bank ID (4 bytes)
        - +24: program data starts
        """
        result = {
            'valid': True,
            'num_programs': 0,
            'program_size': 0,
            'bank_id': 0,
            'bank_name': '',
        }
        
        offset = chunk.offset
        
        # Verify chunk ID
        if chunk.chunk_id != ChunkId.PBK1:
            self.report.add_issue(
                'error', f'PBK1 at 0x{offset:08X}',
                ChunkId.PBK1, chunk.chunk_id,
                'Invalid chunk ID'
            )
            result['valid'] = False
            return result
        
        # Read structure at expected offsets
        # C# uses: Index += Pbk1NumberOfProgramsOffset (12)
        num_programs = self.get_int(offset + 12, 4)
        program_size = self.get_int(offset + 16, 4)
        bank_id = self.get_int(offset + 20, 4)
        
        result['num_programs'] = num_programs
        result['program_size'] = program_size
        result['bank_id'] = bank_id
        
        # Decode bank ID using C# logic from ProgramBankId2ProgramIndex
        if bank_id == 0x8000:
            result['bank_name'] = 'I-F'
        elif bank_id == 6:
            result['bank_name'] = 'GM'
        elif bank_id < 0x8000:
            if bank_id < 6:
                result['bank_name'] = f'I-{chr(65 + bank_id)}'
            else:
                result['bank_name'] = f'?-{bank_id:08X}'
        elif bank_id >= 0x20000:
            user_idx = bank_id - 0x20000
            if user_idx < 7:
                result['bank_name'] = f'U-{chr(65 + user_idx)}'
            elif user_idx < 14:
                letter = chr(65 + (user_idx - 7))
                result['bank_name'] = f'U-{letter}{letter}'
            else:
                result['bank_name'] = f'U-{user_idx}'
        else:
            result['bank_name'] = f'?-{bank_id:08X}'
        
        # Validate program count
        if num_programs > 128:
            self.report.add_issue(
                'warning', f'PBK1 at 0x{offset:08X}',
                '<= 128', num_programs,
                'Unusual number of programs in bank'
            )
        
        # Validate program size (typical HD-1 is ~4200 bytes)
        if program_size < 100 or program_size > 10000:
            self.report.add_issue(
                'warning', f'PBK1 at 0x{offset:08X}',
                '100-10000', program_size,
                'Unusual program size'
            )
        
        return result
    
    def validate_cbk1_structure(self, chunk: ChunkInfo) -> Dict[str, Any]:
        """Validate CBK1 (Combi Bank) chunk structure.
        
        Based on C# PcgFileReader.ReadCbk1Chunk():
        - +0: 'CBK1' (4 bytes)
        - +4: chunk size (4 bytes)
        - +12: number of combis (4 bytes)
        - +16: size of combi (4 bytes)
        - +20: bank ID (4 bytes)
        - +24: combi data starts
        """
        result = {
            'valid': True,
            'num_combis': 0,
            'combi_size': 0,
            'bank_id': 0,
            'bank_name': '',
        }
        
        offset = chunk.offset
        
        # Read structure at expected offsets
        num_combis = self.get_int(offset + 12, 4)
        combi_size = self.get_int(offset + 16, 4)
        bank_id = self.get_int(offset + 20, 4)
        
        result['num_combis'] = num_combis
        result['combi_size'] = combi_size
        result['bank_id'] = bank_id
        
        # Decode bank ID using C# logic from CombiBankId2CombiIndex
        bank_type = (bank_id >> 16) & 0xFFFF
        sub_index = bank_id & 0xFFFF
        
        if bank_type == 0:
            if sub_index < 7:
                result['bank_name'] = f'I-{chr(65 + sub_index)}'
            else:
                result['bank_name'] = f'I-?{sub_index}'
        elif bank_type == 2:
            if sub_index < 7:
                result['bank_name'] = f'U-{chr(65 + sub_index)}'
            else:
                result['bank_name'] = f'U-?{sub_index}'
        else:
            result['bank_name'] = f'?-{bank_id:08X}'
        
        # Validate combi size (Kronos is 7810 bytes)
        expected_combi_size = KronosCombiOffsets.COMBI_SIZE
        if combi_size != expected_combi_size:
            self.report.add_issue(
                'info', f'CBK1 at 0x{offset:08X}',
                expected_combi_size, combi_size,
                f'Combi size differs from Kronos standard ({expected_combi_size})'
            )
        
        return result
    
    def validate_timbre_offsets(self, combi_offset: int, timbre_index: int) -> Dict[str, Any]:
        """Validate timbre data at expected offsets.
        
        Based on C# KronosTimbre.cs and KronosOasysTimbre.cs:
        - Timbres start at combi_offset + 4802
        - Each timbre is 188 bytes
        """
        result = {
            'valid': True,
            'program_index': 0,
            'program_bank': 0,
            'status': 0,
            'midi_channel': 0,
            'volume': 0,
            'transpose': 0,
            'detune': 0,
        }
        
        # Calculate timbre offset
        timbre_offset = (combi_offset + 
                        KronosCombiOffsets.TIMBRES_OFFSET + 
                        timbre_index * KronosTimbreOffsets.TIMBRE_SIZE)
        
        if timbre_offset + KronosTimbreOffsets.TIMBRE_SIZE > len(self.data):
            result['valid'] = False
            return result
        
        # Read values at C# documented offsets
        result['program_index'] = self.data[timbre_offset + KronosTimbreOffsets.PROGRAM_INDEX]
        result['program_bank'] = self.data[timbre_offset + KronosTimbreOffsets.PROGRAM_BANK]
        
        # Status and MIDI channel from byte +2
        status_byte = self.data[timbre_offset + KronosTimbreOffsets.STATUS_CHANNEL]
        result['status'] = (status_byte >> 5) & 0x07  # Bits 7-5
        result['midi_channel'] = status_byte & 0x1F   # Bits 4-0
        
        result['volume'] = self.data[timbre_offset + KronosTimbreOffsets.VOLUME]
        
        # Transpose (signed byte)
        transpose_byte = self.data[timbre_offset + KronosTimbreOffsets.TRANSPOSE]
        result['transpose'] = transpose_byte if transpose_byte < 128 else transpose_byte - 256
        
        # Detune (2 bytes, signed, little-endian for Kronos)
        detune_bytes = self.data[timbre_offset + KronosTimbreOffsets.DETUNE:
                                 timbre_offset + KronosTimbreOffsets.DETUNE + 2]
        result['detune'] = struct.unpack('<h', detune_bytes)[0]
        
        return result
    
    def validate_full(self) -> ValidationReport:
        """Perform full validation of PCG file structure."""
        # Validate header
        if not self.validate_header():
            return self.report
        
        # Validate PCG1 chunk
        pcg1 = self.validate_pcg1_chunk()
        if not pcg1:
            return self.report
        
        # Iterate through all chunks
        chunks = self.iterate_chunks()
        self.report.chunks.extend(chunks)
        
        # Validate specific chunk types
        for chunk in chunks:
            if chunk.chunk_id == ChunkId.PBK1:
                result = self.validate_pbk1_structure(chunk)
                if result['valid']:
                    self.report.program_banks_found += 1
            
            elif chunk.chunk_id == ChunkId.MBK1:
                # MBK1 has similar structure to PBK1
                self.report.program_banks_found += 1
            
            elif chunk.chunk_id == ChunkId.CBK1:
                result = self.validate_cbk1_structure(chunk)
                if result['valid']:
                    self.report.combi_banks_found += 1
            
            elif chunk.chunk_id == ChunkId.SBK1:
                self.report.setlists_found += 1
        
        return self.report


def validate_pcg_file(file_path: str) -> ValidationReport:
    """Validate a PCG file and return a report.
    
    Args:
        file_path: Path to the PCG file
    
    Returns:
        ValidationReport with all findings
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    
    validator = PcgStructureValidator(data)
    validator.report.file_path = file_path
    return validator.validate_full()


def validate_pcg_data(data: bytes) -> ValidationReport:
    """Validate PCG data and return a report.
    
    Args:
        data: Raw PCG file bytes
    
    Returns:
        ValidationReport with all findings
    """
    validator = PcgStructureValidator(data)
    return validator.validate_full()
