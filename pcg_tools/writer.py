"""PCG file writer."""

import struct
import shutil
from pathlib import Path
from .models import PcgFile
from .checksum import fix_all_checksums


class PcgWriter:
    """Write PCG files."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
    
    def write(self, filepath: str, create_backup: bool = True):
        """Write PCG file to disk.
        
        Args:
            filepath: Path to write the file
            create_backup: If True and file exists, create .backup file first
        """
        # Update raw_data with any modified patch data before writing
        if self.pcg.raw_data:
            # Validate file before writing
            if not self._validate_pcg_data():
                raise ValueError("PCG data validation failed - file may be corrupted")
            
            # Create backup if file exists
            if create_backup and Path(filepath).exists():
                backup_path = f"{filepath}.backup"
                shutil.copy2(filepath, backup_path)
            
            self._update_raw_data()
            
            # Fix checksums before writing (CRITICAL!)
            raw_data = bytearray(self.pcg.raw_data)
            fix_all_checksums(raw_data)
            self.pcg.raw_data = bytes(raw_data)
            
            with open(filepath, 'wb') as f:
                f.write(self.pcg.raw_data)
        else:
            raise NotImplementedError("Creating new PCG files from scratch not yet implemented")
    
    def _validate_pcg_data(self) -> bool:
        """Validate PCG data before writing.
        
        Returns:
            True if data appears valid
        """
        if not self.pcg.raw_data:
            return False
        
        # Check minimum file size (PCG files are typically > 100KB)
        if len(self.pcg.raw_data) < 10000:
            return False
        
        # Check for KORG magic number at start
        if self.pcg.raw_data[:4] != b'KORG':
            return False
        
        # Check for PCG1 chunk
        if b'PCG1' not in self.pcg.raw_data[:1000]:
            return False
        
        return True
    
    def _update_raw_data(self):
        """Update the PCG raw_data with modified patch data.
        
        This ensures that any changes made to patch names or properties
        are reflected in the raw binary data before writing to disk.
        """
        if not self.pcg.raw_data:
            return
        
        raw_data = bytearray(self.pcg.raw_data)
        
        # Update program names directly in raw_data
        for bank in self.pcg.program_banks:
            for prog in bank.patches:
                if hasattr(prog, '_raw_offset') and prog._raw_offset > 0:
                    # Program name is at offset 0 in the program data (first 24 bytes)
                    offset = prog._raw_offset
                    name_bytes = prog.name.encode('ascii', errors='ignore')[:24]
                    name_bytes = name_bytes.ljust(24, b'\x00')
                    raw_data[offset:offset+24] = name_bytes
        
        # Update combi names and timbres directly in raw_data
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if hasattr(combi, '_raw_offset') and combi._raw_offset > 0:
                    # Combi name is at offset 0 in the combi data (first 24 bytes)
                    offset = combi._raw_offset
                    name_bytes = combi.name.encode('ascii', errors='ignore')[:24]
                    name_bytes = name_bytes.ljust(24, b'\x00')
                    raw_data[offset:offset+24] = name_bytes
                    
                    # Update timbre data
                    self._update_timbre_data(raw_data, combi)
        
        # Update ALL chunks to keep them in sync
        self._update_all_setlist_chunks(raw_data)
        
        self.pcg.raw_data = bytes(raw_data)
    
    def _update_timbre_data(self, raw_data: bytearray, combi):
        """Update timbre properties in combi raw data.
        
        Timbre structure (from C# KronosTimbres.cs and Timbre.cs):
        - Timbre base offset: 4802 (from C# KronosTimbres.cs: TimbresOffsetConstant)
        - Timbre size: 188 bytes (from C# KronosTimbre.cs: TimbresSizeConstant)
        - Offset +2: Status (bits 7-5) and MIDI channel (bits 4-0)
        - Offset +5: Volume (bits 7-0)
        - Offset +7: Transpose (bits 7-0, signed)
        - Offset +8: Detune (2 bytes, signed, little-endian)
        - Offset +34: Mute (bit 7)
        - Offset +37: Top Key
        - Offset +38: Bottom Key
        - Offset +40: Top Velocity
        - Offset +41: Bottom Velocity
        """
        if not hasattr(combi, '_raw_offset') or combi._raw_offset <= 0:
            return
        
        # CRITICAL FIX: Timbre data starts at offset 4802 (not 1024!)
        # From C# KronosTimbres.cs: TimbresOffsetConstant => 4802
        timbre_base = combi._raw_offset + 4802
        timbre_size = 188  # From C# KronosTimbre.cs: TimbresSizeConstant
        
        for i, timbre in enumerate(combi.timbres):
            if i >= 16:  # Max 16 timbres
                break
            
            timbre_offset = timbre_base + (i * timbre_size)
            
            # Verify we're in bounds
            if timbre_offset + 42 > len(raw_data):
                break
            
            # Update Status (offset +2, bits 7-5) and MIDI channel (offset +2, bits 4-0)
            status_value = ["Off", "Int", "Both", "Ext", "Ex2"].index(timbre.status) if timbre.status in ["Off", "Int", "Both", "Ext", "Ex2"] else 1
            byte_2 = (status_value << 5) | (timbre.midi_channel & 0x1F)
            raw_data[timbre_offset + 2] = byte_2
            
            # Update volume (offset +5, bits 7-0)
            raw_data[timbre_offset + 5] = timbre.volume & 0xFF
            
            # Update transpose (offset +7, bits 7-0, signed)
            transpose_byte = timbre.transpose if timbre.transpose >= 0 else (256 + timbre.transpose)
            raw_data[timbre_offset + 7] = transpose_byte & 0xFF
            
            # Update detune (offset +8, 2 bytes, signed, little-endian)
            detune_bytes = struct.pack('<h', timbre.detune)
            raw_data[timbre_offset + 8:timbre_offset + 10] = detune_bytes
            
            # Update mute (offset +34, bit 7)
            if timbre.mute:
                raw_data[timbre_offset + 34] |= 0x80
            else:
                raw_data[timbre_offset + 34] &= 0x7F
            
            # Update key zones (offset +37/+38)
            raw_data[timbre_offset + 37] = timbre.top_key & 0xFF
            raw_data[timbre_offset + 38] = timbre.bottom_key & 0xFF
            
            # Update velocity zones (offset +40/+41)
            raw_data[timbre_offset + 40] = timbre.top_velocity & 0xFF
            raw_data[timbre_offset + 41] = timbre.bottom_velocity & 0xFF
    
    def _update_all_setlist_chunks(self, raw_data: bytearray):
        """Update setlist names in both SLS1 and STL1 chunks.
        
        CRITICAL FINDING (Nov 27, 2025):
        - Must update BOTH SLS1 and STL1 for names to change on hardware
        - Must recalculate checksums after editing (done in write() method)
        - Without checksums, file becomes corrupted
        
        With checksum fixing, both updates work correctly!
        """
        if not self.pcg.set_lists:
            return
        
        # Update SLS1 (for parser consistency)
        self._update_sls1_names(raw_data)
        
        # Update STL1/SBK1 (what Kronos actually reads)
        self._update_stl1_data(raw_data)
    
    def _update_sls1_names(self, raw_data: bytearray):
        """Update setlist names in SLS1 chunk (new format).
        
        Structure: marker (1e020000) + name (24 bytes) + separator (280f0100)
        Spacing: ~3612 bytes between setlists
        
        This is the format the parser reads from, so it MUST be updated!
        """
        sls1_offset = raw_data.find(b'SLS1')
        if sls1_offset < 0:
            return
        
        # Find setlist positions by looking for the marker pattern
        marker = b'\x1e\x02\x00\x00'
        separator = b'\x28\x0f\x01\x00'
        
        sls1_data_start = sls1_offset + 8
        sls1_size = struct.unpack('<I', raw_data[sls1_offset+4:sls1_offset+8])[0]
        sls1_end = sls1_data_start + sls1_size
        
        # Find all setlist name positions
        positions = []
        pos = sls1_data_start
        while pos < sls1_end:
            # Look for marker
            pos = raw_data.find(marker, pos, sls1_end)
            if pos == -1:
                break
            
            # Check if separator follows after 24 bytes
            name_start = pos + 4
            sep_pos = name_start + 24
            if sep_pos + 4 <= sls1_end:
                if raw_data[sep_pos:sep_pos+4] == separator:
                    positions.append(name_start)
            
            pos += 1
        
        # Update names for setlists we have
        for sl_idx, setlist in enumerate(self.pcg.set_lists):
            if sl_idx >= len(positions):
                break
            
            name_pos = positions[sl_idx]
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[name_pos:name_pos+24] = name_bytes
    
    def _update_sbk1_names(self, raw_data: bytearray):
        """Update setlist names in SBK1 chunk (old format).
        
        Structure: name (24 bytes) directly, no markers
        Spacing: 69,416 bytes between setlists
        First setlist at: SBK1_data + 69,432
        """
        sbk1_offset = raw_data.find(b'SBK1')
        if sbk1_offset < 0:
            return
        
        sbk1_data_start = sbk1_offset + 8
        
        SETLIST_SPACING = 69416
        FIRST_SETLIST_OFFSET = 69432
        
        # Update each setlist
        for sl_idx, setlist in enumerate(self.pcg.set_lists):
            if sl_idx == 0:
                name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET
            else:
                name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET + (sl_idx * SETLIST_SPACING)
            
            if name_pos + 24 > len(raw_data):
                break
            
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[name_pos:name_pos+24] = name_bytes
    
    def _update_setlist_data(self, raw_data: bytearray):
        """Update setlist and slot data in the SLS1 chunk.
        
        NEW format structure:
        - Marker: 0x1E 0x02 0x00 0x00
        - Setlist name (24 bytes)
        - Separator: 0x28 0x0F 0x01 0x00
        - First slot name (24 bytes, no marker)
        - Remaining 127 slots with marker + name (28 bytes each)
        
        IMPORTANT: Only updates setlists that exist in self.pcg.set_lists.
        Does NOT touch empty setlist positions to avoid corruption.
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
        
        # Find all setlist positions by looking for separators
        separator = b'\x28\x0F\x01\x00'
        marker = b'\x1E\x02\x00\x00'
        
        all_setlist_offsets = []
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
                    all_setlist_offsets.append(marker_offset)
            
            pos += 4
        
        if len(all_setlist_offsets) == 0:
            return
        
        # CRITICAL FIX: Only update the first N positions where N = number of actual setlists
        # This prevents corrupting empty setlist positions with data from setlist 0
        num_setlists_to_update = min(len(self.pcg.set_lists), len(all_setlist_offsets))
        
        # Update only the setlists we have data for
        for sl_idx in range(num_setlists_to_update):
            setlist = self.pcg.set_lists[sl_idx]
            setlist_start = all_setlist_offsets[sl_idx]
            
            # Update setlist name (skip marker, write 24 bytes)
            name_offset = setlist_start + 4
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[name_offset:name_offset+24] = name_bytes
            
            # TODO: Update slots
            # Slot writing is currently disabled because it's corrupting data
            # Need to investigate why slot data from setlist 0 is being written to all positions
            pass
            
            # # Update slots
            # # After name + separator, slots begin
            # slots_start = name_offset + 24 + 4  # name + separator
            #
            # # Create a map of slot_index -> slot for quick lookup
            # slot_map = {slot.slot_index: slot for slot in setlist.slots}
            #
            # # Update first slot (no marker)
            # if 0 in slot_map:
            #     slot = slot_map[0]
            #     name_bytes = slot.name.encode('ascii', errors='ignore')[:24]
            #     name_bytes = name_bytes.ljust(24, b'\x00')
            #     raw_data[slots_start:slots_start+24] = name_bytes
            #
            # # Update remaining slots (with markers)
            # current_pos = slots_start + 24
            # for slot_idx in range(1, 128):
            #     # Check if marker exists
            #     if current_pos + 28 > len(raw_data):
            #         break
            #
            #     check_marker = raw_data[current_pos:current_pos+4]
            #     if check_marker != marker:
            #         break
            #
            #     # Update slot name if it exists in our data
            #     if slot_idx in slot_map:
            #         slot = slot_map[slot_idx]
            #         name_bytes = slot.name.encode('ascii', errors='ignore')[:24]
            #         name_bytes = name_bytes.ljust(24, b'\x00')
            #         raw_data[current_pos+4:current_pos+28] = name_bytes
            #
            #     current_pos += 28
    
    def _update_stl1_data(self, raw_data: bytearray):
        """Update STL1/SBK1 chunk with setlist data.
        
        SBK1 structure (discovered through analysis):
        - Each setlist is 69,416 bytes
        - Setlist N starts at: SBK1_data_start + (N * 69416) + 69432
        - Within each setlist:
          - Offset +0: Setlist name (24 bytes) - but actually at -16 from first occurrence
          - Slots follow after
        
        This is the chunk the Kronos actually reads for display!
        """
        if not self.pcg.set_lists:
            return
        
        # Find STL1 chunk
        stl1_offset = raw_data.find(b'STL1')
        if stl1_offset < 0:
            return
        
        # Find SBK1 within STL1
        sbk1_offset = raw_data.find(b'SBK1', stl1_offset)
        if sbk1_offset < 0:
            return
        
        # SBK1 data starts at +8
        sbk1_data_start = sbk1_offset + 8
        
        # Constants from analysis
        SETLIST_SPACING = 69416  # Bytes between setlists
        FIRST_SETLIST_OFFSET = 69432  # Offset to first setlist name
        NAME_OFFSET_FROM_FOUND = -16  # Setlist name is 16 bytes before where we find it
        
        # Update each setlist we have data for
        for sl_idx, setlist in enumerate(self.pcg.set_lists):
            # Calculate where this setlist's name should be
            # First setlist is at +69432, then every 69416 bytes
            if sl_idx == 0:
                name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET
            else:
                name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET + (sl_idx * SETLIST_SPACING)
            
            # Verify we're in bounds
            if name_pos + 24 > len(raw_data):
                break
            
            # Update setlist name
            name_bytes = setlist.name.encode('ascii', errors='ignore')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[name_pos:name_pos+24] = name_bytes
            
            # TODO: Update slot names and metadata
            # For now, just updating setlist names to avoid corruption
    
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


def write_pcg_file(pcg: PcgFile, filepath: str, create_backup: bool = True):
    """Convenience function to write a PCG file.
    
    Args:
        pcg: PCG file object to write
        filepath: Path to write the file
        create_backup: If True, create .backup file before overwriting (default: True)
    """
    writer = PcgWriter(pcg)
    writer.write(filepath, create_backup=create_backup)


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
