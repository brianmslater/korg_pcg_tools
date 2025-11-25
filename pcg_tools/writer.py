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
        # Update raw_data with any modified patch data before writing
        if self.pcg.raw_data:
            self._update_raw_data()
            with open(filepath, 'wb') as f:
                f.write(self.pcg.raw_data)
        else:
            raise NotImplementedError("Creating new PCG files from scratch not yet implemented")
    
    def _update_raw_data(self):
        """Update the PCG raw_data with modified patch data.
        
        This ensures that any changes made to patch names or properties
        are reflected in the raw binary data before writing to disk.
        """
        if not self.pcg.raw_data:
            return
        
        raw_data = bytearray(self.pcg.raw_data)
        
        # Update program data
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                if prog.raw_data and hasattr(prog, '_raw_offset'):
                    # If we tracked the offset, update it in place
                    offset = prog._raw_offset
                    if offset + len(prog.raw_data) <= len(raw_data):
                        raw_data[offset:offset+len(prog.raw_data)] = prog.raw_data
        
        # Update combi data
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if combi.raw_data and hasattr(combi, '_raw_offset'):
                    # If we tracked the offset, update it in place
                    offset = combi._raw_offset
                    if offset + len(combi.raw_data) <= len(raw_data):
                        raw_data[offset:offset+len(combi.raw_data)] = combi.raw_data
        
        # Update setlist data (names only - patch data format not yet fully understood)
        self._update_setlist_data(raw_data)
        
        # Update STL1/SBK1 data (color, text_size, and complete slot data)
        self._update_stl1_data(raw_data)
        
        self.pcg.raw_data = bytes(raw_data)
    
    def _update_setlist_data(self, raw_data: bytearray):
        """Update setlist and slot data in the SLS1 chunk.
        
        NEW format structure:
        - Marker: 0x1E 0x02 0x00 0x00
        - Setlist name (24 bytes)
        - Separator: 0x28 0x0F 0x01 0x00
        - First slot name (24 bytes, no marker)
        - Remaining 127 slots with marker + name (28 bytes each)
        """
        if not self.pcg.set_lists:
            return
        
        # Find SLS1 chunk
        sls1_offset = raw_data.find(b'SLS1')
        if sls1_offset < 0:
            return
        
        # Get SLS1 chunk size
        sls1_size = struct.unpack('<I', raw_data[sls1_offset+4:sls1_offset+8])[0]
        sls1_end = sls1_offset + 8 + sls1_size
        
        # Find all setlists by looking for separators
        separator = b'\x28\x0F\x01\x00'
        marker = b'\x1E\x02\x00\x00'
        
        setlist_offsets = []
        pos = sls1_offset + 8
        while pos < sls1_end:
            pos = raw_data.find(separator, pos)
            if pos == -1 or pos >= sls1_end:
                break
            
            # Check if there's a marker before the name (24 bytes before separator)
            name_offset = pos - 24
            marker_offset = name_offset - 4
            if marker_offset >= sls1_offset:
                check_marker = raw_data[marker_offset:marker_offset+4]
                if check_marker == marker:
                    setlist_offsets.append(marker_offset)
            
            pos += 4
        
        if len(setlist_offsets) == 0:
            return
        
        # Limit to 16 setlists
        setlist_offsets = setlist_offsets[:16]
        
        # Update each setlist
        for sl_idx, setlist_start in enumerate(setlist_offsets):
            if sl_idx >= len(self.pcg.set_lists):
                break
            
            setlist = self.pcg.set_lists[sl_idx]
            
            # Update setlist name (skip marker, write 24 bytes)
            name_offset = setlist_start + 4
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[name_offset:name_offset+24] = name_bytes
            
            # Update slots
            # After name + separator, slots begin
            slots_start = name_offset + 24 + 4  # name + separator
            
            # Create a map of slot_index -> slot for quick lookup
            slot_map = {slot.slot_index: slot for slot in setlist.slots}
            
            # Update first slot (no marker)
            if 0 in slot_map:
                slot = slot_map[0]
                name_bytes = slot.name.encode('ascii', errors='ignore')[:24]
                name_bytes = name_bytes.ljust(24, b'\x00')
                raw_data[slots_start:slots_start+24] = name_bytes
            
            # Update remaining slots (with markers)
            current_pos = slots_start + 24
            for slot_idx in range(1, 128):
                # Check if marker exists
                if current_pos + 28 > len(raw_data):
                    break
                
                check_marker = raw_data[current_pos:current_pos+4]
                if check_marker != marker:
                    break
                
                # Update slot name if it exists in our data
                if slot_idx in slot_map:
                    slot = slot_map[slot_idx]
                    name_bytes = slot.name.encode('ascii', errors='ignore')[:24]
                    name_bytes = name_bytes.ljust(24, b'\x00')
                    raw_data[current_pos+4:current_pos+28] = name_bytes
                
                current_pos += 28
    
    def _update_stl1_data(self, raw_data: bytearray):
        """Update STL1/SBK1 chunk with color and text_size metadata.
        
        STL1/SBK1 structure:
        - SBK1 data start + 16: Setlist name (24 bytes)
        - SBK1 data start + 40: First slot
        - Each slot: ~542 bytes
          - +0: Slot name (24 bytes)
          - +24: Color (1 byte)
          - +29: Text size (1 byte)
          - Rest: Notes/description
        """
        if not self.pcg.set_lists:
            return
        
        # Find STL1 chunk
        stl1_offset = raw_data.find(b'STL1')
        if stl1_offset < 0:
            # No STL1 chunk - file may not have full setlist data
            return
        
        # Find SBK1 within STL1
        sbk1_offset = raw_data.find(b'SBK1', stl1_offset)
        if sbk1_offset < 0:
            return
        
        # SBK1 data starts at +8
        sbk1_data_start = sbk1_offset + 8
        
        # Update setlist name at +16
        if len(self.pcg.set_lists) > 0:
            setlist = self.pcg.set_lists[0]  # Currently only handling first setlist
            setlist_name_offset = sbk1_data_start + 16
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[setlist_name_offset:setlist_name_offset+24] = name_bytes
            
            # Update slots starting at +40
            current_offset = sbk1_data_start + 40
            APPROX_SLOT_SIZE = 542
            
            # Create slot map for quick lookup
            slot_map = {slot.slot_index: slot for slot in setlist.slots}
            
            # Update each slot
            for slot_idx in range(128):
                if current_offset + 100 > len(raw_data):
                    break
                
                if slot_idx in slot_map:
                    slot = slot_map[slot_idx]
                    
                    # Update slot name (24 bytes)
                    name_bytes = slot.name.encode('ascii', errors='ignore')[:24]
                    name_bytes = name_bytes.ljust(24, b'\x00')
                    raw_data[current_offset:current_offset+24] = name_bytes
                    
                    # Update color at +24
                    if current_offset + 24 < len(raw_data):
                        raw_data[current_offset + 24] = slot.color & 0xFF
                    
                    # Update text_size at +29
                    if current_offset + 29 < len(raw_data):
                        raw_data[current_offset + 29] = slot.text_size & 0xFF
                
                # Move to next slot
                current_offset += APPROX_SLOT_SIZE
    
    def _encode_bank_id(self, bank_id: str) -> int:
        """Encode bank ID string to byte value.
        
        Format: I-A to I-H = 0x00 to 0x07
                U-A to U-G = 0x20 to 0x26
        """
        if not bank_id or len(bank_id) < 3:
            return 0x00
        
        bank_type = bank_id[0]  # 'I' or 'U'
        bank_letter = bank_id[2]  # 'A', 'B', 'C', etc.
        
        if bank_type == 'I':
            # Internal banks: I-A = 0x00, I-B = 0x01, etc.
            return ord(bank_letter) - ord('A')
        elif bank_type == 'U':
            # User banks: U-A = 0x20, U-B = 0x21, etc.
            return 0x20 + (ord(bank_letter) - ord('A'))
        
        return 0x00
    
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
