"""Proper PCG binary format parser based on original C# implementation."""

import struct
from typing import List, Tuple, Optional
from .models import PcgFile, Program, Combi, Bank, Category


# Enable debug output
DEBUG = False

def debug_print(msg):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(msg)


class PcgBinaryParser:
    """Parse PCG binary format properly."""
    
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0
    
    def get_int(self, offset: int, size: int) -> int:
        """Read integer from data (big-endian - Korg format)."""
        if offset + size > len(self.data):
            return 0
        
        # Korg files use big-endian for all integers
        if size == 4:
            return struct.unpack('>I', self.data[offset:offset+4])[0]
        elif size == 2:
            return struct.unpack('>H', self.data[offset:offset+2])[0]
        
        # For other sizes, use big-endian
        value = 0
        for i in range(size):
            value += self.data[offset + i] * (256 ** (size - i - 1))
        return value
    
    def get_string(self, offset: int, length: int) -> str:
        """Read null-terminated ASCII string."""
        string_data = self.data[offset:offset+length]
        # Find null terminator
        null_pos = string_data.find(b'\x00')
        if null_pos >= 0:
            string_data = string_data[:null_pos]
        return string_data.decode('ascii', errors='ignore').strip()
    
    def find_chunk(self, chunk_id: bytes, start_offset: int = 16, search_inside_pcg1: bool = True) -> Optional[Tuple[int, int]]:
        """Find a chunk by ID, returns (offset, size) or None."""
        offset = start_offset
        while offset < len(self.data) - 8:
            current_id = self.data[offset:offset+4]
            if current_id == chunk_id:
                size = self.get_int(offset + 4, 4)
                return (offset, size)
            
            # If looking for PRG1/CMB1 and we found PCG1, search inside it
            if search_inside_pcg1 and current_id == b'PCG1' and chunk_id in [b'PRG1', b'CMB1']:
                size = self.get_int(offset + 4, 4)
                # Search inside PCG1 chunk
                result = self.find_chunk(chunk_id, offset + 8, search_inside_pcg1=False)
                if result:
                    return result
            
            # Skip this chunk
            if len(current_id) == 4:
                try:
                    size = self.get_int(offset + 4, 4)
                    offset += 8 + size
                    # Align to 4 bytes
                    if offset % 4:
                        offset += 4 - (offset % 4)
                except:
                    break
            else:
                break
        
        return None
    
    def parse_prg1_chunk(self, pcg: PcgFile):
        """Parse PRG1 chunk containing program banks."""
        # Search for PRG1 anywhere in the file
        prg1_offset = self.data.find(b'PRG1')
        if prg1_offset < 0:
            debug_print("PRG1 chunk not found")
            return
        
        offset = prg1_offset
        chunk_size = self.get_int(offset + 4, 4)
        debug_print(f"Found PRG1 at offset {offset:08X}, size {chunk_size:08X}")
        
        chunk_end = offset + 8 + chunk_size
        offset += 12  # Skip chunk header (8) + gap (4)
        
        while offset < chunk_end - 8 and offset < len(self.data) - 8:
            sub_id = self.data[offset:offset+4]
            debug_print(f"At offset {offset:08X}, found sub-chunk: {sub_id}")
            
            if sub_id == b'PBK1':
                offset = self._parse_pbk1_chunk(pcg, offset)
            elif sub_id == b'MBK1':
                offset = self._parse_mbk1_chunk(pcg, offset)
            else:
                # Skip unknown chunk
                try:
                    size = self.get_int(offset + 4, 4)
                    debug_print(f"Skipping unknown chunk {sub_id}, size {size}")
                    offset += 8 + size + 12
                except:
                    break
    
    def _parse_pbk1_chunk(self, pcg: PcgFile, offset: int) -> int:
        """Parse a PBK1 (Program Bank) chunk."""
        chunk_size = self.get_int(offset + 4, 4)
        start_offset = offset
        
        debug_print(f"Parsing PBK1 at {offset:08X}, size {chunk_size:08X}")
        
        # Read bank info
        offset += 12  # Skip to number of programs
        num_programs = self.get_int(offset, 4)
        offset += 4
        program_size = self.get_int(offset, 4)
        offset += 4
        bank_id_raw = self.get_int(offset, 4)
        offset += 4
        
        debug_print(f"  Bank ID raw: {bank_id_raw:08X}, Programs: {num_programs}, Size: {program_size}")
        
        # Decode bank ID
        bank_name = self._decode_bank_id(bank_id_raw, is_combi=False)
        debug_print(f"  Decoded bank name: {bank_name}")
        
        # Create bank
        # Mark GM bank as read-only (ROM bank)
        is_read_only = (bank_name == "GM")
        bank = Bank(bank_id=bank_name, bank_type='Program', is_read_only=is_read_only)
        
        # Read programs
        for i in range(min(num_programs, 128)):  # Max 128 per bank
            if offset + program_size > len(self.data):
                debug_print(f"  Reached end of data at program {i}")
                break
            
            # Program name is typically at offset 0 within the program data, 24 bytes
            name = self.get_string(offset, 24)
            if not name or len(name) < 2:
                name = f"[Empty {i:03d}]"
            
            if i < 3:  # Debug first 3 programs
                debug_print(f"  Program {i}: {name}")
            
            # Extract engine information
            engine = self._extract_engine(self.data[offset:offset+program_size])
            
            # Extract additional parameters
            osc_mode, category, favorite = self._extract_program_params(self.data[offset:offset+program_size])
            
            program = Program(
                bank=bank_name,
                index=i,
                name=name,
                engine=engine,
                osc_mode=osc_mode,
                category=category,
                favorite=favorite,
                raw_data=self.data[offset:offset+program_size]
            )
            
            # Track offset for writing back
            program._raw_offset = offset
            
            bank.patches.append(program)
            offset += program_size
        
        if bank.patches:  # Only add if we found programs
            pcg.program_banks.append(bank)
            debug_print(f"  Added bank {bank_name} with {len(bank.patches)} programs")
        
        # Next chunk starts after: chunk ID (4) + size (4) + chunk data (chunk_size) + gap (4)
        return start_offset + 8 + chunk_size + 4
    
    def _parse_mbk1_chunk(self, pcg: PcgFile, offset: int) -> int:
        """Parse an MBK1 (Model Bank - for special synthesis types) chunk."""
        chunk_size = self.get_int(offset + 4, 4)
        start_offset = offset
        
        debug_print(f"Parsing MBK1 at {offset:08X}, size {chunk_size:08X}")
        
        # MBK1 structure (based on C# ReadMbk1Chunk):
        # +0: 'MBK1' (4 bytes)
        # +4: chunk size (4 bytes, big-endian)
        # +8: gap/header data
        # +12: number of programs (4 bytes, big-endian)
        # +16: size of program (4 bytes, big-endian)
        # +20: bank ID (4 bytes, big-endian)
        # +24: programs start
        
        num_programs = self.get_int(offset + 12, 4)
        program_size = self.get_int(offset + 16, 4)
        bank_id_raw = self.get_int(offset + 20, 4)
        
        debug_print(f"  Number of programs: {num_programs}")
        debug_print(f"  Program size: {program_size}")
        debug_print(f"  Bank ID raw: 0x{bank_id_raw:08X}")
        
        bank_id = self._decode_bank_id(bank_id_raw, is_combi=False)
        debug_print(f"  Decoded bank ID: {bank_id}")
        
        # Programs start at offset +24
        programs = []
        scan_offset = offset + 24
        
        for i in range(min(num_programs, 128)):
            if scan_offset + 24 > len(self.data):
                break
            name = self.get_string(scan_offset, 24)
            if not name or len(name) < 2:
                name = f"[Empty {i:03d}]"
            
            programs.append((i, name, scan_offset))
            if i < 3:
                debug_print(f"  Program {i}: {name}")
            scan_offset += program_size
        
        if programs:
            
            # Create bank
            # Mark GM bank as read-only (ROM bank)
            is_read_only = (bank_id == "GM")
            bank = Bank(bank_id=bank_id, bank_type='Program', is_read_only=is_read_only)
            
            for idx, name, prog_offset in programs:
                # Extract engine information
                engine = self._extract_engine(self.data[prog_offset:prog_offset+program_size])
                
                # Extract additional parameters
                osc_mode, category, favorite = self._extract_program_params(self.data[prog_offset:prog_offset+program_size])
                
                program = Program(
                    bank=bank_id,
                    index=idx,
                    name=name,
                    engine=engine,
                    osc_mode=osc_mode,
                    category=category,
                    favorite=favorite,
                    raw_data=self.data[prog_offset:prog_offset+program_size]
                )
                
                # Track offset for writing back
                program._raw_offset = prog_offset
                
                bank.patches.append(program)
            
            pcg.program_banks.append(bank)
            debug_print(f"  Added bank {bank_id} with {len(programs)} programs")
        
        # Next chunk starts after: chunk ID (4) + size (4) + chunk data (chunk_size) + gap (4)
        next_offset = start_offset + 8 + chunk_size + 4
        debug_print(f"  Next offset: 0x{next_offset:08X} (start=0x{start_offset:08X}, size=0x{chunk_size:08X})")
        return next_offset
    
    def _extract_program_params(self, program_data: bytes) -> Tuple[str, Optional[Category], bool]:
        """Extract program parameters: OSC Mode, Category, and Favorite flag.
        
        Based on C# KronosProgram.cs:
        - OSC Mode: offset 2558, 2 bytes (enum: Single, Double, Drums, -, -, Double Drums)
        - Category: offset 2568, bits 4-0 (5 bits)
        - SubCategory: offset 2568, bits 7-5 (3 bits)
        - Favorite: offset 2558, bit 5
        
        Returns:
            Tuple of (osc_mode, category, favorite)
        """
        if len(program_data) < 2570:
            return ("", None, False)
        
        try:
            # OSC Mode (2 bytes at offset 2558, little-endian)
            # Extract bits 0-2 from the 2-byte value
            osc_mode_raw = struct.unpack('<H', program_data[2558:2560])[0]
            osc_mode_value = osc_mode_raw & 0x07  # Extract lower 3 bits
            osc_modes = ["Single", "Double", "Drums", "- (EXi)", "- (Unused)", "Double Drums"]
            osc_mode = osc_modes[osc_mode_value] if osc_mode_value < len(osc_modes) else f"Unknown({osc_mode_value})"
            
            # Favorite flag (bit 5 of byte 2558)
            favorite = bool(program_data[2558] & 0x20)
            
            # Category and SubCategory (byte 2568)
            cat_byte = program_data[2568]
            main_category = cat_byte & 0x1F  # Bits 4-0
            sub_category = (cat_byte >> 5) & 0x07  # Bits 7-5
            
            category = Category(
                main_category=main_category,
                sub_category=sub_category
            )
            
            return (osc_mode, category, favorite)
        except:
            return ("", None, False)
    
    def _extract_engine(self, program_data: bytes) -> str:
        """Extract engine type from program data.
        
        Based on C# KronosProgram.cs:
        - OSC Mode at offset 2558, bits 0-2 determines the synthesis type
        - OSC Mode value 3 = "- (EXI)" means EXi engine
        - Other values (Single, Double, Drums, Double Drums) mean HD-1 engine
        
        The C# code uses BankSynthesisType to track HD-1 vs EXi, but the actual
        determination comes from the OSC Mode parameter.
        
        Reference: C# KronosProgram.cs GetParam(OscMode) and KronosProgramBank.cs
        """
        if len(program_data) < 2560:
            return ""
        
        try:
            # OSC Mode at offset 2558, bits 0-2
            # Values: 0=Single, 1=Double, 2=Drums, 3=EXi, 4=Unused, 5=Double Drums
            osc_mode_raw = struct.unpack('<H', program_data[2558:2560])[0]
            osc_mode_value = osc_mode_raw & 0x07  # Extract lower 3 bits
            
            # OSC Mode 3 = "- (EXI)" indicates EXi engine
            if osc_mode_value == 3:
                return "EXi"
            else:
                # All other modes (Single, Double, Drums, Double Drums) are HD-1
                return "HD-1"
        except:
            return ""
    
    def _decode_slot_bank_id(self, bank_id: int, is_combi: bool) -> str:
        """Decode bank ID from setlist slot data (5-bit value).
        
        This is different from _decode_bank_id which decodes from bank chunks.
        Slot bank IDs are simpler: 0-7 for internal banks, 0x20+ for user banks.
        
        Args:
            bank_id: 5-bit bank ID from slot data (0-31)
            is_combi: True if this is a combi bank
        
        Returns:
            Bank ID string like "I-A", "U-A", etc.
        """
        if bank_id < 8:
            # Internal banks: 0-7 = I-A through I-H
            return f"I-{chr(65 + bank_id)}"
        elif bank_id >= 0x17:  # 23 decimal
            # User banks start at 23 (0x17)
            user_idx = bank_id - 0x17
            if user_idx < 7:
                return f"U-{chr(65 + user_idx)}"
            else:
                # Extended user banks (U-AA, U-BB, etc.)
                double_idx = user_idx - 7
                if double_idx < 7:
                    letter = chr(65 + double_idx)
                    return f"U-{letter}{letter}"
                else:
                    return f"U-{user_idx}"
        else:
            return f"?-{bank_id}"
    
    def _decode_bank_id(self, bank_id_raw: int, is_combi: bool) -> str:
        """Decode raw bank ID to human-readable format.
        
        Based on C# PcgFileReader.cs ProgramBankId2ProgramIndex:
        - id == 0x8000: I-F (bank index 5)
        - id < 0x8000: I-A through I-E (bank index 0-4), plus GM (bank index 6)
        - id >= 0x20000: User banks (U-A through U-GG)
        
        For combis, the mapping is simpler (0-6 for I-A through I-G, 0x20000+ for user).
        """
        if is_combi:
            # Combi bank ID format: (bank_type << 16) | sub_index
            # bank_type: 0 = Internal, 2 = User
            # sub_index: 0-6 for A-G
            bank_type = (bank_id_raw >> 16) & 0xFFFF
            sub_index = bank_id_raw & 0xFFFF
            
            if bank_type == 0:
                # Internal banks: I-A through I-G
                if sub_index < 7:
                    return f"I-{chr(65 + sub_index)}"
                else:
                    return f"I-?{sub_index}"
            elif bank_type == 2:
                # User banks: U-A through U-G
                if sub_index < 7:
                    return f"U-{chr(65 + sub_index)}"
                else:
                    return f"U-?{sub_index}"
            else:
                return f"?-{bank_id_raw:08X}"
        else:
            # Program banks: I-A through I-F, GM, U-A through U-GG
            if bank_id_raw == 6:
                # GM bank (special case)
                return "GM"
            elif bank_id_raw == 0x8000:
                # Special case: I-F
                return "I-F"
            elif bank_id_raw < 0x8000:
                # I-A through I-E (0-4)
                if bank_id_raw < 6:
                    return f"I-{chr(65 + bank_id_raw)}"
                else:
                    return f"?-{bank_id_raw:08X}"
            else:
                # User banks (>= 0x20000)
                if bank_id_raw >= 0x20000:
                    user_idx = bank_id_raw - 0x20000
                    if user_idx < 7:
                        # U-A through U-G
                        return f"U-{chr(65 + user_idx)}"
                    elif user_idx < 14:
                        # U-AA through U-GG
                        double_idx = user_idx - 7
                        letter = chr(65 + double_idx)
                        return f"U-{letter}{letter}"
                    else:
                        return f"U-{user_idx}"
                else:
                    return f"?-{bank_id_raw:08X}"
    
    def parse_cmb1_chunk(self, pcg: PcgFile):
        """Parse CMB1 chunk containing combi banks."""
        # Search for CMB1 anywhere in the file
        cmb1_offset = self.data.find(b'CMB1')
        if cmb1_offset < 0:
            debug_print("CMB1 chunk not found")
            return
        
        offset = cmb1_offset
        chunk_size = self.get_int(offset + 4, 4)
        debug_print(f"Found CMB1 at offset {offset:08X}, size {chunk_size:08X}")
        
        chunk_end = offset + 8 + chunk_size
        offset += 12  # Skip chunk header (8) + gap (4)
        
        while offset < chunk_end - 8 and offset < len(self.data) - 8:
            sub_id = self.data[offset:offset+4]
            debug_print(f"At offset {offset:08X}, found sub-chunk: {sub_id}")
            
            if sub_id == b'CBK1':
                offset = self._parse_cbk1_chunk(pcg, offset)
            else:
                # Skip unknown chunk
                try:
                    size = self.get_int(offset + 4, 4)
                    debug_print(f"Skipping unknown chunk {sub_id}, size {size}")
                    offset += 8 + size + 12
                except:
                    break
    
    def parse_sls1_chunk(self, pcg: PcgFile):
        """Parse SLS1 chunk containing set lists.
        
        Kronos has TWO setlist formats in the file:
        1. OLD format: Marker-based with slot 111 as display name
        2. NEW format: Direct slot names with 0x28 0x0F 0x01 0x00 separator
        
        The Kronos uses the NEW format for display. This parser reads that format.
        """
        from .models import SetList, SetListSlot
        
        # Try to parse the NEW format first (what Kronos actually uses)
        if self._parse_new_setlist_format(pcg):
            debug_print("Parsed setlists using NEW format")
            # Now parse SLD1 to get actual slot names
            self._parse_sld1_slot_data(pcg)
            return
        
        # Fallback to OLD format if NEW format not found
        debug_print("NEW format not found, trying OLD format")
        self._parse_old_setlist_format(pcg)
    
    def _parse_new_setlist_format(self, pcg: PcgFile):
        """Parse the NEW setlist format that Kronos actually uses.
        
        Structure:
        - Marker: 0x1E 0x02 0x00 0x00
        - Setlist name (24 bytes, null-terminated)
        - Separator: 0x28 0x0F 0x01 0x00
        - First slot name (24 bytes, no marker)
        - Remaining 127 slots, each with:
          * Marker: 0x1E 0x02 0x00 0x00
          * Slot name (24 bytes, null-terminated)
        
        Note: SLS1 format only contains slot names, not color/text size.
        Those are stored in SLD1 combi data or not available.
        """
        from .models import SetList, SetListSlot
        
        # Find SLS1 chunk first
        sls1_offset = self.data.find(b'SLS1')
        if sls1_offset < 0:
            return False
        
        # Get SLS1 chunk size
        sls1_size = self.get_int(sls1_offset + 4, 4)
        sls1_end = sls1_offset + 8 + sls1_size
        
        # Search for the separator pattern within SLS1 chunk only
        separator = b'\x28\x0F\x01\x00'
        marker = b'\x1E\x02\x00\x00'
        
        # Find all setlists by looking for the separator
        setlist_offsets = []
        first_setlist_offset = None
        
        pos = sls1_offset + 8  # Start after SLS1 header
        while pos < sls1_end:
            pos = self.data.find(separator, pos)
            if pos == -1 or pos >= sls1_end:
                break
            
            # Check if there's a setlist name before this separator
            # Setlist name should be 24 bytes before the separator
            name_offset = pos - 24
            if name_offset >= sls1_offset:
                # Check if there's a marker before the name
                marker_offset = name_offset - 4
                if marker_offset >= sls1_offset:
                    check_marker = self.data[marker_offset:marker_offset+4]
                    if check_marker == marker:
                        # Standard setlist with marker
                        setlist_offsets.append(marker_offset)
                    elif first_setlist_offset is None:
                        # First setlist without marker (e.g., "Preload Set List")
                        # Store it separately to add at the beginning
                        first_setlist_offset = name_offset
            
            pos += 4
        
        # If we found a first setlist without marker, add it at the beginning
        if first_setlist_offset is not None:
            setlist_offsets.insert(0, first_setlist_offset)
        
        if len(setlist_offsets) == 0:
            return False
        
        # Limit to 128 setlists (Kronos supports up to 128 setlists)
        setlist_offsets = setlist_offsets[:128]
        
        debug_print(f"Found {len(setlist_offsets)} setlists in NEW format")
        
        # Parse each setlist
        for sl_idx, setlist_start in enumerate(setlist_offsets):
            # Check if this offset has a marker or not
            has_marker = self.data[setlist_start:setlist_start+4] == marker
            
            # Read setlist name
            if has_marker:
                # Skip marker, read 24 bytes
                name_offset = setlist_start + 4
            else:
                # No marker, start directly at name
                name_offset = setlist_start
            
            sl_name = self.get_string(name_offset, 24)
            
            if not sl_name:
                sl_name = f"Set List {sl_idx + 1}"
            
            setlist = SetList(
                index=sl_idx,
                name=sl_name,
                description="",
                color=0
            )
            
            # After name + separator, read 128 slots
            # First slot has NO marker, just the name
            # Subsequent slots have marker + name
            slots_start = name_offset + 24 + 4  # name + separator
            
            # Read all 128 slots
            # First slot (index 0) has NO marker, just the name
            slot_name = self.get_string(slots_start, 24)
            slot = SetListSlot(
                set_list_index=sl_idx,
                slot_index=0,
                name=slot_name if slot_name else "",
                notes="",
                patch_type="Combi",  # SLS1 slots are combis
                patch_bank="",
                patch_index=0,
                color=0  # Not available in SLS1 format
            )
            # Set properties after creation (C# pattern)
            slot._transpose = 0
            slot._volume = 127
            slot._text_size = 2  # Medium
            setlist.slots.append(slot)
            
            # Read remaining 127 slots (with markers)
            # After first slot name (24 bytes), we expect marker + name pattern
            current_pos = slots_start + 24  # After first slot name
            
            for slot_idx in range(1, 128):
                # Check if there's enough data
                if current_pos + 28 > len(self.data):
                    break
                
                slot_marker = self.data[current_pos:current_pos+4]
                if slot_marker == marker:
                    # Read slot name
                    slot_name = self.get_string(current_pos + 4, 24)
                    
                    # Add ALL slots, even if empty (to maintain proper indices)
                    slot = SetListSlot(
                        set_list_index=sl_idx,
                        slot_index=slot_idx,
                        name=slot_name if slot_name else "",
                        notes="",
                        patch_type="Combi",  # SLS1 slots are combis
                        patch_bank="",
                        patch_index=0,
                        color=0  # Not available in SLS1 format
                    )
                    # Set properties after creation (C# pattern)
                    slot._transpose = 0
                    slot._volume = 127
                    slot._text_size = 2  # Medium
                    setlist.slots.append(slot)
                    
                    current_pos += 28  # marker + name
                else:
                    # No marker found - this might be the end of this setlist
                    # or the start of the next setlist
                    break
            
            pcg.set_lists.append(setlist)
            debug_print(f"Set list {sl_idx}: {sl_name}, {len(setlist.slots)} slots")
        
        pcg.has_set_lists = len(pcg.set_lists) > 0
        return True
    
    def _parse_old_setlist_format(self, pcg: PcgFile):
        """Parse the OLD setlist format (fallback).
        
        This is the original format we were parsing before.
        """
        from .models import SetList, SetListSlot
        
        # Search for SLS1 anywhere in the file
        sls1_offset = self.data.find(b'SLS1')
        if sls1_offset < 0:
            debug_print("SLS1 chunk not found")
            return
        
        pcg.has_set_lists = True
        
        # Search for the marker pattern that precedes names: 1E 02 00 00
        marker = b'\x1E\x02\x00\x00'
        
        # Find all occurrences of the marker after SLS1
        name_offsets = []
        search_start = sls1_offset + 8
        pos = search_start
        
        while pos < len(self.data) - 32:
            pos = self.data.find(marker, pos)
            if pos == -1:
                break
            # Check if this is within reasonable range (first 100KB after SLS1)
            if pos - sls1_offset > 100000:
                break
            name_offsets.append(pos + 4)  # Skip marker, point to name
            pos += 4
        
        if not name_offsets:
            debug_print("No setlist names found")
            pcg.has_set_lists = False
            return
        
        debug_print(f"Found {len(name_offsets)} potential name entries")
        
        # Validate: We need at least 16 entries for setlist names
        # If we have fewer than 16, this probably isn't a real setlist section
        if len(name_offsets) < 16:
            debug_print(f"Too few entries ({len(name_offsets)}) for valid setlists, skipping")
            pcg.has_set_lists = False
            return
        
        # Parse up to 128 setlists with 128 slots each
        # Structure: First N marker entries are setlist names
        # Then 128 slot names for each setlist
        # Determine how many setlists we have based on the data
        max_setlists = min(128, len(name_offsets) // 129)  # 1 name + 128 slots per setlist
        num_setlists = max_setlists if max_setlists > 0 else 16  # Default to 16 if calculation fails
        slots_per_setlist = 128
        
        # Validate the first few names to ensure they're reasonable
        valid_count = 0
        for i in range(min(5, len(name_offsets))):
            name = self.get_string(name_offsets[i], 24)
            if name and len(name) >= 2 and name.isprintable():
                valid_count += 1
        
        if valid_count < 3:
            debug_print(f"Names don't look valid (only {valid_count}/5 printable), skipping setlists")
            pcg.has_set_lists = False
            return
        
        # Parse each setlist
        for sl_idx in range(num_setlists):
            if sl_idx >= len(name_offsets):
                break
            
            offset = name_offsets[sl_idx]
            sl_name = self.get_string(offset, 24)
            if not sl_name:
                sl_name = f"Set List {sl_idx + 1}"
            
            setlist = SetList(
                index=sl_idx,
                name=sl_name,
                description="",
                color=0
            )
            
            # Slot names start after the 16 setlist names
            slot_start_idx = num_setlists + (sl_idx * slots_per_setlist)
            
            for slot_idx in range(slots_per_setlist):
                name_idx = slot_start_idx + slot_idx
                if name_idx >= len(name_offsets):
                    break
                
                offset = name_offsets[name_idx]
                slot_name = self.get_string(offset, 24)
                
                # Skip empty slots
                if not slot_name or len(slot_name) < 2:
                    continue
                
                # Parse patch reference data (8 bytes after the 24-byte name)
                patch_data_offset = offset + 24
                patch_type = "Combi"
                patch_bank = "I-A"
                patch_index = 0
                transpose = 0
                volume = 127
                
                if patch_data_offset + 8 <= len(self.data):
                    try:
                        # Read patch reference bytes
                        patch_idx_low = self.data[patch_data_offset]
                        patch_idx_high = self.data[patch_data_offset + 1]
                        patch_index = patch_idx_low + (patch_idx_high << 8)
                        
                        bank_byte = self.data[patch_data_offset + 2]
                        type_byte = self.data[patch_data_offset + 3]
                        
                        # Decode patch type
                        if type_byte == 0x30:
                            patch_type = "Combi"
                        elif type_byte == 0x20:
                            patch_type = "Program"
                        
                        # Decode bank ID
                        # Bank byte format: 0x00-0x07 = I-A to I-H, 0x20+ = User banks
                        if bank_byte < 0x08:
                            patch_bank = f"I-{chr(65 + bank_byte)}"
                        elif bank_byte >= 0x20:
                            user_idx = bank_byte - 0x20
                            if user_idx < 8:
                                patch_bank = f"U-{chr(65 + user_idx)}"
                            else:
                                patch_bank = f"U-{user_idx}"
                        else:
                            # EXi or other special banks
                            patch_bank = f"I-{chr(65 + (bank_byte & 0x0F))}"
                        
                        # Transpose and volume
                        if patch_data_offset + 5 < len(self.data):
                            transpose_byte = self.data[patch_data_offset + 4]
                            # Transpose is signed, centered at 0x40 (64)
                            transpose = transpose_byte - 0x40 if transpose_byte < 0x80 else transpose_byte - 0x40
                            
                            volume = self.data[patch_data_offset + 5]
                        
                        # Validate patch index (should be 0-127)
                        if patch_index > 127:
                            patch_index = patch_index & 0x7F  # Take lower 7 bits
                        
                    except Exception as e:
                        debug_print(f"Error parsing patch data for slot {slot_idx}: {e}")
                
                slot = SetListSlot(
                    set_list_index=sl_idx,
                    slot_index=slot_idx,
                    name=slot_name,
                    notes="",
                    patch_type=patch_type,
                    patch_bank=patch_bank,
                    patch_index=patch_index
                )
                # Set properties after creation (C# pattern)
                slot._transpose = transpose
                slot._volume = volume
                slot._text_size = 2  # Medium default
                
                setlist.slots.append(slot)
            
            # Kronos convention: Slot 111 contains the user-visible setlist name
            # Use it as the display name if it exists
            slot_111_name = None
            for slot in setlist.slots:
                if slot.slot_index == 111:
                    slot_111_name = slot.name
                    break
            
            if slot_111_name and slot_111_name.strip():
                setlist.name = slot_111_name
                debug_print(f"Set list {sl_idx}: Using slot 111 name: {slot_111_name}")
            
            # Add setlist even if empty (to maintain indices)
            pcg.set_lists.append(setlist)
            debug_print(f"Set list {sl_idx}: {setlist.name}, {len(setlist.slots)} slots")
    
    def _parse_cbk1_chunk(self, pcg: PcgFile, offset: int) -> int:
        """Parse a CBK1 (Combi Bank) chunk."""
        chunk_size = self.get_int(offset + 4, 4)
        start_offset = offset
        
        debug_print(f"Parsing CBK1 at {offset:08X}, size {chunk_size:08X}")
        
        # CBK1 structure (similar to MBK1):
        # +0: 'CBK1' (4 bytes)
        # +4: chunk size (4 bytes, big-endian)
        # +8: gap/header data
        # +12: number of combis (4 bytes, big-endian)
        # +16: size of combi (4 bytes, big-endian)
        # +20: bank ID (4 bytes, big-endian)
        # +24: combis start
        
        num_combis = self.get_int(offset + 12, 4)
        combi_size = self.get_int(offset + 16, 4)
        bank_id_raw = self.get_int(offset + 20, 4)
        
        debug_print(f"  Number of combis: {num_combis}")
        debug_print(f"  Combi size: {combi_size}")
        debug_print(f"  Bank ID raw: 0x{bank_id_raw:08X}")
        
        bank_id = self._decode_bank_id(bank_id_raw, is_combi=True)
        debug_print(f"  Decoded bank ID: {bank_id}")
        
        # Combis start at offset +24
        combis = []
        scan_offset = offset + 24
        
        for i in range(min(num_combis, 128)):
            if scan_offset + 24 > len(self.data):
                break
            name = self.get_string(scan_offset, 24)
            if not name or len(name) < 2:
                name = f"[Empty {i:03d}]"
            
            combis.append((i, name, scan_offset))
            if i < 3:
                debug_print(f"  Combi {i}: {name}")
            scan_offset += combi_size
        
        if combis:
            
            bank = Bank(bank_id=bank_id, bank_type='Combi')
            
            for idx, name, combi_offset in combis:
                # Parse timbres from combi data
                timbres = self._parse_timbres(combi_offset)
                
                # Extract combi parameters
                category, favorite, tempo = self._extract_combi_params(self.data[combi_offset:combi_offset+7810])
                
                combi = Combi(
                    bank=bank_id,
                    index=idx,
                    name=name,
                    category=category,
                    favorite=favorite,
                    tempo=tempo,
                    timbres=timbres,
                    raw_data=self.data[combi_offset:combi_offset+7810]
                )
                
                # Track offset for writing back
                combi._raw_offset = combi_offset
                
                bank.patches.append(combi)
                debug_print(f"  Combi {idx}: {name} with {len(timbres)} timbres")
            
            pcg.combi_banks.append(bank)
            debug_print(f"  Added bank {bank_id} with {len(combis)} combis")
        
        # Return next offset: chunk header (8) + chunk data + padding (4)
        return start_offset + 8 + chunk_size + 4
    
    def _extract_combi_params(self, combi_data: bytes) -> Tuple[Optional[Category], bool, float]:
        """Extract combi parameters: Category, Favorite flag, and Tempo.
        
        Based on C# KronosCombi.cs:
        - Category: offset 4790, bits 4-0 (5 bits)
        - SubCategory: offset 4790, bits 7-5 (3 bits)
        - Favorite: offset 4791, bit 0
        - Tempo: offset 1304, 2 bytes (word, little-endian, divide by 100 for BPM)
        
        Returns:
            Tuple of (category, favorite, tempo)
        """
        if len(combi_data) < 4792:
            return (None, False, 120.0)
        
        try:
            # Category and SubCategory (byte 4790)
            cat_byte = combi_data[4790]
            main_category = cat_byte & 0x1F  # Bits 4-0
            sub_category = (cat_byte >> 5) & 0x07  # Bits 7-5
            
            category = Category(
                main_category=main_category,
                sub_category=sub_category
            )
            
            # Favorite flag (bit 0 of byte 4791)
            favorite = bool(combi_data[4791] & 0x01)
            
            # Tempo (2 bytes at offset 1304, little-endian, divide by 100)
            tempo_raw = struct.unpack('<H', combi_data[1304:1306])[0]
            tempo = tempo_raw / 100.0
            
            return (category, favorite, tempo)
        except:
            return (None, False, 120.0)
    
    def _parse_timbres(self, combi_offset: int) -> List:
        """Parse timbres from combi data.
        
        Kronos combi structure (simplified):
        - Offset 0-23: Name
        - Offset 24-25: Category
        - Offset ~1024+: Timbre data (16 timbres, each ~400 bytes)
        
        Each timbre contains:
        - Status (INT/OFF/EXi)
        - Program bank/number reference
        - MIDI channel, volume, pan, etc.
        """
        from .models import Timbre
        
        timbres = []
        
        # Timbre data starts at offset 4802 in Kronos combis (from C# KronosTimbres.cs: TimbresOffsetConstant)
        # Each timbre is 188 bytes (from C# KronosTimbre.cs: TimbresSizeConstant)
        timbre_base = combi_offset + 4802
        timbre_size = 188
        
        for i in range(16):  # 16 timbres per combi
            timbre_offset = timbre_base + (i * timbre_size)
            
            if timbre_offset + 20 > len(self.data):
                break
            
            try:
                # Parse program reference (offset +0 and +1 per C# code)
                # Program number at +0, Bank ID at +1
                prog_num_byte = self.data[timbre_offset + 0] if timbre_offset + 0 < len(self.data) else 0
                prog_bank_byte = self.data[timbre_offset + 1] if timbre_offset + 1 < len(self.data) else 0
                
                # Convert bank byte (PcgId) to bank ID
                # Based on C# KronosProgramBanks.cs:
                # I-A through I-F: 0-5
                # GM: 6
                # g(1) through g(9): 7-15 (GM2 sub-banks)
                # g(d): 16 (GM2 drums)
                # U-A through U-G: 17-23
                # U-AA through U-GG: 24-30
                # Virtual banks: 48+ (0x30+)
                prog_bank = "I-A"
                if prog_bank_byte <= 5:  # I-A through I-F (0-5)
                    prog_bank = f"I-{chr(65 + prog_bank_byte)}"
                elif prog_bank_byte == 6:  # GM bank
                    prog_bank = "GM"
                elif 7 <= prog_bank_byte <= 15:  # g(1) through g(9) (GM2 sub-banks)
                    prog_bank = f"g({prog_bank_byte - 6})"
                elif prog_bank_byte == 16:  # g(d) (GM2 drums)
                    prog_bank = "g(d)"
                elif 17 <= prog_bank_byte <= 23:  # U-A through U-G (17-23)
                    user_idx = prog_bank_byte - 17
                    prog_bank = f"U-{chr(65 + user_idx)}"
                elif 24 <= prog_bank_byte <= 30:  # U-AA through U-GG (24-30)
                    user_idx = prog_bank_byte - 24
                    prog_bank = f"U-{chr(65 + user_idx)}{chr(65 + user_idx)}"
                elif prog_bank_byte >= 48:  # Virtual banks (0x30+)
                    vbank_idx = prog_bank_byte - 48
                    group = vbank_idx // 8
                    bank_letter = chr(65 + (vbank_idx % 8))
                    prog_bank = f"V{group}-{bank_letter}"
                else:
                    prog_bank = f"?-{prog_bank_byte}"  # Unknown bank
                
                # Status (offset +2, bits 7-5) - from C# KronosOasysTimbre.cs
                # 0=Off, 1=Int, 2=Both, 3=Ext, 4=Ex2
                status_byte = self.data[timbre_offset + 2] if timbre_offset + 2 < len(self.data) else 0
                status_value = (status_byte >> 5) & 0x07
                status_names = ["Off", "Int", "Both", "Ext", "Ex2"]
                status = status_names[status_value] if status_value < len(status_names) else "Off"
                
                # MIDI channel (offset +2, bits 4-0)
                midi_channel = status_byte & 0x1F  # Extract bits 4-0
                
                # Volume (offset +5, bits 7-0)
                volume = self.data[timbre_offset + 5] if timbre_offset + 5 < len(self.data) else 127
                
                # Bend Range (offset +6, bits 7-0, signed) - from C# Timbre.cs
                bend_range = 0
                if timbre_offset + 6 < len(self.data):
                    bend_range_byte = self.data[timbre_offset + 6]
                    # Convert unsigned byte to signed (-128 to +127)
                    bend_range = bend_range_byte if bend_range_byte < 128 else bend_range_byte - 256
                
                # Pan - not a timbre parameter (stored in program)
                pan = 64
                
                # Transpose (offset +7, bits 7-0, signed)
                transpose = 0
                if timbre_offset + 7 < len(self.data):
                    transpose_byte = self.data[timbre_offset + 7]
                    # Convert unsigned byte to signed (-128 to +127)
                    transpose = transpose_byte if transpose_byte < 128 else transpose_byte - 256
                
                # Detune (offset +8, 2 bytes, signed, little-endian)
                detune = 0
                if timbre_offset + 10 <= len(self.data):
                    detune = struct.unpack('<h', self.data[timbre_offset + 8:timbre_offset + 10])[0]
                
                # Mute (offset +34, bit 7) - from C# KronosOasysTimbre.cs
                mute = False
                if timbre_offset + 34 < len(self.data):
                    mute = bool(self.data[timbre_offset + 34] & 0x80)
                
                # Priority (offset +35, bit 4) - from C# KronosOasysTimbre.cs
                priority = False
                if timbre_offset + 35 < len(self.data):
                    priority = bool(self.data[timbre_offset + 35] & 0x10)
                
                # Osc Mode (offset +35, bits 1-0) - from C# KronosOasysTimbre.cs
                # 0=Prg, 1=Poly, 2=Mono, 3=Legato
                osc_mode = "Prg"
                if timbre_offset + 35 < len(self.data):
                    osc_mode_value = self.data[timbre_offset + 35] & 0x03
                    osc_mode_names = ["Prg", "Poly", "Mono", "Legato"]
                    osc_mode = osc_mode_names[osc_mode_value] if osc_mode_value < len(osc_mode_names) else "Prg"
                
                # Osc Select (offset +35, bits 3-2) - from C# KronosOasysTimbre.cs
                # 0=Both, 1=Osc1, 2=Osc2
                osc_select = "Both"
                if timbre_offset + 35 < len(self.data):
                    osc_select_value = (self.data[timbre_offset + 35] >> 2) & 0x03
                    osc_select_names = ["Both", "Osc1", "Osc2"]
                    osc_select = osc_select_names[osc_select_value] if osc_select_value < len(osc_select_names) else "Both"
                
                # Portamento (offset +36, bits 7-0, signed) - from C# KronosOasysTimbre.cs
                portamento = 0
                if timbre_offset + 36 < len(self.data):
                    portamento_byte = self.data[timbre_offset + 36]
                    portamento = portamento_byte if portamento_byte < 128 else portamento_byte - 256
                
                # Key zones (offset +37/+38) - from C# KronosOasysTimbre.cs
                top_key = self.data[timbre_offset + 37] if timbre_offset + 37 < len(self.data) else 127
                bottom_key = self.data[timbre_offset + 38] if timbre_offset + 38 < len(self.data) else 0
                
                # Velocity zones (offset +40/+41) - from C# KronosOasysTimbre.cs
                top_velocity = self.data[timbre_offset + 40] if timbre_offset + 40 < len(self.data) else 127
                bottom_velocity = self.data[timbre_offset + 41] if timbre_offset + 41 < len(self.data) else 1
                
                timbre = Timbre(
                    program_bank=prog_bank,
                    program_index=prog_num_byte,
                    midi_channel=midi_channel,
                    status=status,
                    volume=volume,
                    pan=pan,
                    mute=mute,
                    priority=priority,
                    bend_range=bend_range,
                    detune=detune,
                    transpose=transpose,
                    portamento=portamento,
                    osc_mode=osc_mode,
                    osc_select=osc_select,
                    bottom_key=bottom_key,
                    top_key=top_key,
                    bottom_velocity=bottom_velocity,
                    top_velocity=top_velocity
                )
                
                timbres.append(timbre)
                
            except Exception as e:
                debug_print(f"Error parsing timbre {i}: {e}")
                continue
        
        return timbres
    
    def _bank_id_to_name(self, bank_id: int, is_combi: bool) -> str:
        """Convert bank ID to bank name (I-A, I-B, U-A, etc.)."""
        # Handle invalid bank IDs
        if bank_id < 0 or bank_id > 0x30000:
            debug_print(f"Invalid bank ID: {bank_id:08X}, using default")
            return "I-A"
        
        if bank_id < 0x20000:
            # Internal banks (I-A through I-G)
            if bank_id < 26:  # A-Z
                return f"I-{chr(65 + bank_id)}"  # 65 is 'A'
            else:
                return f"I-{bank_id}"
        else:
            # User banks (U-A through U-GG)
            user_index = bank_id - 0x20000
            if user_index < 7:
                return f"U-{chr(65 + user_index)}"
            elif user_index < 56:  # 7 + 7*7
                # Extended banks (U-AA through U-GG)
                first_letter = chr(65 + ((user_index - 7) // 7))
                second_letter = chr(65 + ((user_index - 7) % 7))
                return f"U-{first_letter}{second_letter}"
            else:
                return f"U-{user_index}"
    
    def _parse_sld1_slot_data(self, pcg: PcgFile):
        """Parse SLD1 chunk to get actual slot names and data.
        
        SLD1 contains the real slot data with actual names, patch references, etc.
        Each slot entry is 7810 bytes (0x1E82) - a full combi structure.
        
        Structure:
        - Each setlist starts with CBK1 marker
        - Each setlist has 128 slots of 7810 bytes each
        - 24-byte gap between setlists
        - Slot name at +24 from slot start (combi name position)
        """
        if not pcg.set_lists:
            return
        
        # Find SLD1 chunk (it's inside SLS1)
        sld1_offset = self.data.find(b'SLD1')
        if sld1_offset < 0:
            debug_print("SLD1 chunk not found")
            return
        
        debug_print(f"Found SLD1 at offset {sld1_offset:08X}")
        
        # Find all CBK1 markers (one per setlist)
        cbk1_positions = []
        search_pos = sld1_offset
        while len(cbk1_positions) < 128:  # Max 128 setlists
            cbk1_pos = self.data.find(b'CBK1', search_pos)
            if cbk1_pos < 0:
                break
            cbk1_positions.append(cbk1_pos)
            search_pos = cbk1_pos + 4
        
        if not cbk1_positions:
            debug_print("No CBK1 markers found in SLD1")
            return
        
        debug_print(f"Found {len(cbk1_positions)} CBK1 markers (setlists)")
        
        # Each slot is 7810 bytes (0x1E82) - a full combi
        SLOT_SIZE = 0x1E82
        
        # Parse slots for each setlist
        for sl_idx, setlist in enumerate(pcg.set_lists):
            if sl_idx >= len(cbk1_positions):
                break
            
            # This setlist starts at its CBK1 marker
            setlist_start = cbk1_positions[sl_idx]
            debug_print(f"Parsing setlist {sl_idx} at 0x{setlist_start:08X}")
            
            # Update each slot with data from SLD1
            for slot_idx in range(128):
                slot_offset = setlist_start + (slot_idx * SLOT_SIZE)
                
                # Name is always at +24 from slot start (combi name position)
                name_offset = slot_offset + 24
                
                # Check if we're still within the file
                if name_offset + 60 > len(self.data):
                    break
                
                # Read combi name from SLD1
                sld1_name = self.get_string(name_offset, 24)
                
                # Skip empty slots
                if not sld1_name or len(sld1_name) < 2:
                    continue
                
                # Find the existing slot from SLS1 to get its name
                slot = None
                for s in setlist.slots:
                    if s.slot_index == slot_idx:
                        slot = s
                        break
                
                # Determine patch type from SLS1 slot name
                # 
                # Note: The authoritative patch type is stored in STL1/SBK1 data at
                # byte +24 bits 1-0, but STL1 only contains data for ONE setlist per file.
                # For setlists without STL1 data, we use the slot name as a heuristic:
                # - If slot name is "Combi" → Combi reference
                # - Otherwise → Program reference
                # 
                # This works well when users follow the naming convention of explicitly
                # naming combi slots as "Combi", but may not work for all setlists.
                sls1_name = slot.name if slot else ""
                if sls1_name.strip().lower() == "combi":
                    patch_type = "Combi"
                    patch_bank = "I-A"  # Combis default to I-A
                    patch_index = slot_idx
                else:
                    patch_type = "Program"
                    patch_bank = "I-A"  # Programs default to I-A
                    patch_index = slot_idx
                
                # Color and text size are not available in SLD1 format
                color = 0
                text_size = 0
                
                if not slot:
                    # Create new slot
                    from .models import SetListSlot
                    slot = SetListSlot(
                        set_list_index=sl_idx,
                        slot_index=slot_idx,
                        name=sld1_name,
                        color=color,
                        patch_type=patch_type,
                        patch_bank=patch_bank,
                        patch_index=patch_index
                    )
                    # Set properties after creation (C# pattern)
                    slot._text_size = text_size
                    slot._transpose = 0
                    slot._volume = 127
                    setlist.slots.append(slot)
                else:
                    # Update existing slot with SLD1 data
                    # KEEP the SLS1 name (it's the user's custom label like "SGX-2", "Combi")
                    # The SLD1 name is the actual patch name, store it in description
                    if sld1_name and sld1_name != slot.name:
                        slot.description = sld1_name  # Actual patch name from SLD1
                    
                    # Update patch reference but keep the slot name from SLS1
                    slot.patch_type = patch_type
                    slot.patch_bank = patch_bank
                    slot.patch_index = patch_index
                
                if slot_idx < 5:  # Debug first 5 slots
                    debug_print(f"  Slot {slot_idx}: '{sld1_name}'")
        
        debug_print(f"Finished parsing SLD1 slot data")

    def parse_stl1_chunk(self, pcg: PcgFile):
        """Parse STL1 chunk to get complete setlist data including color and text size.
        
        STL1/SBK1 contains the authoritative setlist data with:
        - Setlist names
        - Slot names  
        - Color (byte +24 from slot name)
        - Text size (byte +29 from slot name)
        - Notes/descriptions
        
        This should be called AFTER parse_sls1_chunk to override with complete data.
        
        SBK1 structure (from C# PcgFileReader.cs ReadSetList method):
        - 'SBK1' marker (4 bytes)
        - Chunk size (4 bytes)
        - Unknown (4 bytes)
        - Number of setlists (4 bytes)
        - Chunk size for slots (4 bytes) - total size of all slot data
        - Unknown (8 bytes)
        - For each setlist:
          - Name (24 bytes)
          - 128 slots × slot_size
          - Gap (16 bytes)
        
        Slot size = chunk_size / number_of_setlists
        """
        from .models import SetList, SetListSlot
        
        # Find STL1 chunk
        stl1_offset = self.data.find(b'STL1')
        if stl1_offset < 0:
            debug_print("STL1 chunk not found - file may not have full setlist data")
            return
        
        debug_print(f"Found STL1 at offset {stl1_offset:08X}")
        
        # Find SBK1 within STL1
        sbk1_offset = self.data.find(b'SBK1', stl1_offset)
        if sbk1_offset < 0:
            debug_print("No SBK1 marker found in STL1")
            return
        
        debug_print(f"Found SBK1 at offset {sbk1_offset:08X}")
        
        # Read SBK1 header values (matching C# ReadSetList method)
        # C# code flow:
        #   Index += 4;  // Skip 'SBK1'
        #   sbk1ChunkSize = GetInt(Index, 4);  // at +4
        #   Index += 8;  // Skip size + unknown -> at +12
        #   numberOfSetLists = GetInt(Index, 4);  // at +12
        #   Index += 4;  // -> at +16
        #   chunkSize = GetInt(Index, 4);  // at +16
        #   Index += 8;  // Skip chunkSize + unknown -> at +24
        #   // Now at +24, setlist data starts
        
        num_setlists = self.get_int(sbk1_offset + 12, 4)
        chunk_size = self.get_int(sbk1_offset + 16, 4)
        
        # Calculate slot size from chunk data (C#: sizeOfASetListSlot = chunkSize/numberOfSetLists)
        if num_setlists > 0:
            SLOT_SIZE = chunk_size // num_setlists
        else:
            SLOT_SIZE = 542  # Fallback to default
        
        debug_print(f"SBK1 header: num_setlists={num_setlists}, chunk_size={chunk_size}, slot_size={SLOT_SIZE}")
        
        # Data starts at SBK1 + 24 (after header)
        data_start = sbk1_offset + 24
        
        debug_print(f"Parsing all setlists from STL1 (up to {num_setlists})")
        
        # Calculate setlist size: 24 (name) + 128 * slot_size + 16 (gap)
        SETLIST_SIZE = 24 + (128 * SLOT_SIZE) + 16
        
        # Parse setlists
        setlists_parsed = 0
        for setlist_idx in range(num_setlists):
            setlist_start = data_start + (setlist_idx * SETLIST_SIZE)
            
            # Check if we have enough data for this setlist
            if setlist_start + SETLIST_SIZE > len(self.data):
                debug_print(f"Reached end of data at setlist {setlist_idx}")
                break
            
            # Read setlist name (24 bytes at start of setlist)
            setlist_name = self.get_string(setlist_start, 24)
            
            # Skip empty setlists
            if not setlist_name:
                continue
            
            # Find existing setlist from SLS1 parsing
            existing_setlist = None
            for sl in pcg.set_lists:
                if sl.name == setlist_name or sl.index == setlist_idx:
                    existing_setlist = sl
                    break
            
            # If not found, create new setlist
            if not existing_setlist:
                debug_print(f"Creating new setlist {setlist_idx}: '{setlist_name}'")
                existing_setlist = SetList(index=setlist_idx, name=setlist_name)
                pcg.set_lists.append(existing_setlist)
            else:
                debug_print(f"Updating setlist {setlist_idx}: '{setlist_name}'")
            
            # Parse 128 slots for this setlist
            # Slots start after the 24-byte name
            first_slot_offset = setlist_start + 24
            for slot_idx in range(128):
                slot_offset = first_slot_offset + (slot_idx * SLOT_SIZE)
                
                # Check if we have enough data
                if slot_offset + 30 > len(self.data):
                    break
                
                # Read slot name (24 bytes)
                slot_name = self.get_string(slot_offset, 24)
                
                # Color is stored in bits 5-2 of byte +24 (4 bits = 0-15 color index)
                # Then we need to map the index to the actual color value
                color = 0
                if slot_offset + 24 < len(self.data):
                    from .bit_utils import get_bits
                    color_index = get_bits(self.data, slot_offset + 24, 5, 2)
                    # Map color index (0-15) to color value
                    # Based on Kronos color mapping: index * 4 + 136, with 0 = Default
                    if color_index == 0:
                        color = 0  # Default
                    else:
                        color = (color_index - 1) * 4 + 136
                
                # Text size is split across two bytes:
                # MSB (1 bit) -> byte +29, bit 4
                # LSB (2 bits) -> byte +24, bits 7-6
                text_size = 2  # Default to Medium
                if slot_offset + 29 < len(self.data):
                    from .bit_utils import get_bits
                    msb = get_bits(self.data, slot_offset + 29, 4, 4)
                    lsb = get_bits(self.data, slot_offset + 24, 7, 6)
                    text_size_value = (msb << 2) | lsb
                    # Validate it's in range 0-4 (XS, S, M, L, XL)
                    if 0 <= text_size_value <= 4:
                        text_size = text_size_value
                    else:
                        text_size = 2  # Default to Medium if invalid
                
                # Patch reference at +24 (type), +25 (bank) and +26 (index) from name start
                patch_bank = ""
                patch_index = 0
                patch_type = ""
                volume = 127
                
                if slot_offset + 28 < len(self.data):
                    # Read patch type from byte +24, bits 1-0
                    # C# enum: Program = 1, Combi = 0, Song = 2
                    type_byte = self.data[slot_offset + 24]
                    type_value = type_byte & 0x03  # Get bits 1-0
                    type_map = {0: 'Combi', 1: 'Program', 2: 'Song'}
                    patch_type = type_map.get(type_value, 'Program')
                    
                    bank_byte = self.data[slot_offset + 25]
                    index_byte = self.data[slot_offset + 26]
                    volume = self.data[slot_offset + 28]
                    
                    # Decode bank ID from bits 4-0 of byte 25
                    bank_id = bank_byte & 0x1F  # Extract bits 4-0
                    
                    # Bank mapping differs between Programs and Combis:
                    # 
                    # For PROGRAMS (patch_type == 'Program'), bank_id is a PcgId:
                    #   PcgId 0-5: I-A through I-F
                    #   PcgId 6: GM
                    #   PcgId 7-16: g(1) through g(9), g(d) (GM2 variation banks)
                    #   PcgId 17-23: U-A through U-G
                    #   PcgId 24-30: U-AA through U-GG
                    #
                    # For COMBIS (patch_type == 'Combi'), bank_id is a direct array index:
                    #   Index 0-6: I-A through I-G
                    #   Index 7-13: U-A through U-G
                    #   Index 14+: Virtual banks
                    
                    if patch_type == 'Program':
                        # Program bank mapping (PcgId)
                        if bank_id <= 5:
                            patch_bank = f"I-{chr(65 + bank_id)}"  # I-A to I-F (PcgId 0-5)
                        elif bank_id == 6:
                            patch_bank = "GM"
                        elif 7 <= bank_id <= 16:
                            # GM2 variation banks g(1) through g(9), g(d)
                            if bank_id <= 15:
                                patch_bank = f"g({bank_id - 6})"  # g(1) to g(9)
                            else:
                                patch_bank = "g(d)"  # g(d) = drums
                        elif 17 <= bank_id <= 23:
                            patch_bank = f"U-{chr(65 + (bank_id - 17))}"  # U-A to U-G (PcgId 17-23)
                        elif 24 <= bank_id <= 30:
                            # U-AA through U-GG (extended user banks, PcgId 24-30)
                            letter = chr(65 + (bank_id - 24))  # A-G
                            patch_bank = f"U-{letter}{letter}"  # U-AA, U-BB, etc.
                        else:
                            patch_bank = f"?{bank_id}"
                    else:
                        # Combi bank mapping (direct array index)
                        if bank_id <= 6:
                            patch_bank = f"I-{chr(65 + bank_id)}"  # I-A to I-G (index 0-6)
                        elif 7 <= bank_id <= 13:
                            patch_bank = f"U-{chr(65 + (bank_id - 7))}"  # U-A to U-G (index 7-13)
                        else:
                            patch_bank = f"?{bank_id}"
                    
                    patch_index = index_byte
                    
                    # Note: The C# code trusts the type bits from the file without verification.
                    # We should do the same - the type bits are authoritative.
                
                # Find or create slot
                slot = None
                for s in existing_setlist.slots:
                    if s.slot_index == slot_idx:
                        slot = s
                        break
                
                if not slot and slot_name:
                    # Create new slot
                    slot = SetListSlot(
                        set_list_index=existing_setlist.index,
                        slot_index=slot_idx,
                        name=slot_name,
                        color=color,
                        patch_type=patch_type,
                        patch_bank=patch_bank,
                        patch_index=patch_index
                    )
                    # Set properties after creation (C# pattern)
                    slot._text_size = text_size
                    slot._volume = volume
                    slot._transpose = 0
                    existing_setlist.slots.append(slot)
                elif slot:
                    # Update existing slot with STL1 data
                    # STL1 is the authoritative source - always override with its data
                    if slot_name:
                        slot.name = slot_name
                    slot.color = color
                    slot._text_size = text_size
                    
                    # Always update patch reference from STL1 (it's the correct source)
                    if patch_type:
                        slot.patch_type = patch_type
                    if patch_bank:
                        slot.patch_bank = patch_bank
                    if patch_index is not None:
                        slot.patch_index = patch_index
                    if volume:
                        slot.volume = volume
            
            setlists_parsed += 1
        
        debug_print(f"Finished parsing STL1: {setlists_parsed} setlists")
        pcg.has_set_lists = len(pcg.set_lists) > 0

    def parse_slot_notes(self, pcg: PcgFile):
        """Parse slot notes/comments from SLS1 chunk.
        
        Notes are stored in a separate section of the SLS1 chunk with the structure:
        - Setlist name (24 bytes, mostly padding)
        - Slot name (24 bytes)
        - Metadata (12 bytes)
        - Notes text (variable length, null-terminated)
        
        This section appears to be after the main setlist/slot name data.
        """
        if not pcg.set_lists:
            return
        
        # Find SLS1 chunk
        sls1_offset = self.data.find(b'SLS1')
        if sls1_offset < 0:
            debug_print("SLS1 chunk not found for notes parsing")
            return
        
        sls1_size = self.get_int(sls1_offset + 4, 4)
        sls1_end = sls1_offset + 8 + sls1_size
        
        debug_print(f"Parsing slot notes from SLS1 at {sls1_offset:08X}")
        
        # Search for setlist names in the notes section
        # The notes section seems to start around offset 0xA0000+ in the test file
        # But we'll search for setlist names to find the notes
        
        notes_found = 0
        for setlist in pcg.set_lists:
            # Search for this setlist's name in the SLS1 chunk
            # The notes section has a specific structure with padding before the setlist name
            search_start = sls1_offset + 0x2000  # Skip the main setlist data
            
            while search_start < sls1_end:
                # Look for setlist name, but check for the structure:
                # Usually there's padding (nulls) before the setlist name
                setlist_name_bytes = setlist.name.encode('ascii')[:24]
                name_offset = self.data.find(setlist_name_bytes, search_start, sls1_end)
                
                if name_offset < 0:
                    break
                
                # Verify this looks like a notes entry by checking for nulls before it
                # and that it's followed by a slot name
                if name_offset >= 10:
                    # Check if there are some null bytes before (indicating padding)
                    has_padding = any(self.data[name_offset - i] == 0 for i in range(1, min(10, name_offset)))
                    if not has_padding:
                        search_start = name_offset + 1
                        continue
                
                # Check if this looks like a notes entry (should have slot name after it)
                slot_name_offset = name_offset + 24
                if slot_name_offset + 24 > len(self.data):
                    search_start = name_offset + 1
                    continue
                
                # Read potential slot name
                potential_slot_name = self.get_string(slot_name_offset, 24)
                
                # Check if this slot exists in our setlist
                matching_slot = None
                for slot in setlist.slots:
                    if slot.name and potential_slot_name and slot.name.strip() == potential_slot_name.strip():
                        matching_slot = slot
                        break
                
                if matching_slot:
                    # Found a notes entry! Parse the notes
                    # Notes start after: slot name field (24 bytes) + metadata (12 bytes)
                    # Important: slot_name_offset is the START of the 24-byte field, not where text begins
                    notes_offset = slot_name_offset + 24 + 12
                    
                    # Read notes until null terminator or end of reasonable length
                    notes_bytes = bytearray()
                    max_notes_length = 4096  # Reasonable max
                    for i in range(max_notes_length):
                        if notes_offset + i >= len(self.data):
                            break
                        byte = self.data[notes_offset + i]
                        if byte == 0:
                            break
                        notes_bytes.append(byte)
                    
                    if notes_bytes:
                        try:
                            notes_text = notes_bytes.decode('ascii', errors='replace')
                            matching_slot.notes = notes_text
                            notes_found += 1
                            debug_print(f"Found notes for {setlist.name} slot {matching_slot.slot_index}: {len(notes_text)} chars")
                        except Exception as e:
                            debug_print(f"Error decoding notes: {e}")
                
                # Continue searching
                search_start = name_offset + 1
        
        debug_print(f"Parsed {notes_found} slot notes")


    def parse_dkt1_chunk(self, pcg: PcgFile):
        """Parse DKT1 chunk containing drum kit banks.
        
        Based on C# PcgFileReader.ReadDkt1Chunk().
        """
        from .models import DrumKit, DrumKitBank
        
        # Search for DKT1 anywhere in the file
        dkt1_offset = self.data.find(b'DKT1')
        if dkt1_offset < 0:
            debug_print("DKT1 chunk not found")
            return
        
        offset = dkt1_offset
        chunk_size = self.get_int(offset + 4, 4)
        debug_print(f"Found DKT1 at offset {offset:08X}, size {chunk_size:08X}")
        
        chunk_end = offset + 8 + chunk_size
        offset += 12  # Skip chunk header (8) + gap (4)
        
        while offset < chunk_end - 8 and offset < len(self.data) - 8:
            sub_id = self.data[offset:offset+4]
            
            if sub_id != b'DBK1':
                break
            
            bank_info = self._parse_dbk1_chunk(offset)
            if bank_info:
                pcg.drum_kit_banks.append(bank_info)
                # Move to next chunk
                sub_size = self.get_int(offset + 4, 4)
                offset += 12 + sub_size
            else:
                break
        
        pcg.has_drum_kits = len(pcg.drum_kit_banks) > 0
        debug_print(f"Parsed {len(pcg.drum_kit_banks)} drum kit banks")
    
    def _parse_dbk1_chunk(self, dbk1_offset: int):
        """Parse DBK1 (drum kit bank) chunk.
        
        Based on C# PcgFileReader.ReadDbk1Chunk().
        
        DBK1 structure (Kronos/Oasys):
        - +0: 'DBK1' (4 bytes)
        - +4: chunk size (4 bytes)
        - +8: header (4 bytes)
        - +12: num_drum_kits (4 bytes)
        - +16: drum_kit_size (4 bytes)
        - +20: bank_id (4 bytes)
        - +24: drum kit data starts
        """
        from .models import DrumKit, DrumKitBank
        
        if len(self.data) < dbk1_offset + 24:
            return None
        
        # Verify DBK1 chunk
        if self.data[dbk1_offset:dbk1_offset+4] != b'DBK1':
            return None
        
        chunk_size = self.get_int(dbk1_offset + 4, 4)
        
        # Read bank info
        num_drum_kits = self.get_int(dbk1_offset + 12, 4)
        drum_kit_size = self.get_int(dbk1_offset + 16, 4)
        bank_id = self.get_int(dbk1_offset + 20, 4)
        
        # Convert bank ID to name
        if bank_id == 0:
            bank_name = 'INT'
        elif bank_id >= 0x20000:
            user_idx = bank_id - 0x20000
            if user_idx < 7:
                bank_name = f'USER-{chr(65 + user_idx)}'
            elif user_idx < 14:
                letter = chr(65 + (user_idx - 7))
                bank_name = f'USER-{letter}{letter}'
            else:
                bank_name = f'UNKNOWN-{bank_id:X}'
        else:
            bank_name = f'UNKNOWN-{bank_id:X}'
        
        # Parse drum kit names
        drum_kits = []
        kit_offset = dbk1_offset + 24
        
        for i in range(num_drum_kits):
            if kit_offset + 24 > len(self.data):
                break
            
            # Drum kit name is at the start of each drum kit (24 bytes)
            name = self.get_string(kit_offset, 24)
            
            drum_kit = DrumKit(
                bank=bank_name,
                index=i,
                name=name,
                raw_data=self.data[kit_offset:kit_offset+drum_kit_size],
                _raw_offset=kit_offset
            )
            drum_kits.append(drum_kit)
            kit_offset += drum_kit_size
        
        return DrumKitBank(
            bank_id=bank_name,
            drum_kits=drum_kits,
            byte_offset=dbk1_offset,
            patch_size=drum_kit_size,
            is_writable=(bank_id >= 0x20000),  # User banks are writable
            is_loaded=True
        )
    
    def parse_wsq1_chunk(self, pcg: PcgFile):
        """Parse WSQ1 chunk containing wave sequence banks.
        
        Based on C# PcgFileReader.ReadWsq1Chunk().
        """
        from .models import WaveSequence, WaveSequenceBank
        
        # Search for WSQ1 anywhere in the file
        wsq1_offset = self.data.find(b'WSQ1')
        if wsq1_offset < 0:
            debug_print("WSQ1 chunk not found")
            return
        
        offset = wsq1_offset
        chunk_size = self.get_int(offset + 4, 4)
        debug_print(f"Found WSQ1 at offset {offset:08X}, size {chunk_size:08X}")
        
        chunk_end = offset + 8 + chunk_size
        offset += 12  # Skip chunk header (8) + gap (4)
        
        while offset < chunk_end - 8 and offset < len(self.data) - 8:
            sub_id = self.data[offset:offset+4]
            
            if sub_id != b'WBK1':
                break
            
            bank_info = self._parse_wbk1_chunk(offset)
            if bank_info:
                pcg.wave_sequence_banks.append(bank_info)
                # Move to next chunk
                sub_size = self.get_int(offset + 4, 4)
                offset += 12 + sub_size
            else:
                break
        
        pcg.has_wave_sequences = len(pcg.wave_sequence_banks) > 0
        debug_print(f"Parsed {len(pcg.wave_sequence_banks)} wave sequence banks")
    
    def _parse_wbk1_chunk(self, wbk1_offset: int):
        """Parse WBK1 (wave sequence bank) chunk.
        
        Based on C# PcgFileReader.ReadWbk1Chunk().
        
        WBK1 structure:
        - +0: 'WBK1' (4 bytes)
        - +4: chunk size (4 bytes)
        - +8: header (4 bytes)
        - +12: num_wave_seqs (4 bytes)
        - +16: wave_seq_size (4 bytes)
        - +20: bank_id (4 bytes)
        - +24: wave sequence data starts
        """
        from .models import WaveSequence, WaveSequenceBank
        
        if len(self.data) < wbk1_offset + 24:
            return None
        
        # Verify WBK1 chunk
        if self.data[wbk1_offset:wbk1_offset+4] != b'WBK1':
            return None
        
        chunk_size = self.get_int(wbk1_offset + 4, 4)
        
        # Read bank info
        num_wave_seqs = self.get_int(wbk1_offset + 12, 4)
        wave_seq_size = self.get_int(wbk1_offset + 16, 4)
        bank_id = self.get_int(wbk1_offset + 20, 4)
        
        # Convert bank ID to name
        if bank_id == 0:
            bank_name = 'INT'
        elif bank_id >= 0x20000:
            user_idx = bank_id - 0x20000
            if user_idx < 7:
                bank_name = f'USER-{chr(65 + user_idx)}'
            elif user_idx < 14:
                letter = chr(65 + (user_idx - 7))
                bank_name = f'USER-{letter}{letter}'
            else:
                bank_name = f'UNKNOWN-{bank_id:X}'
        else:
            bank_name = f'UNKNOWN-{bank_id:X}'
        
        # Parse wave sequence names
        wave_sequences = []
        ws_offset = wbk1_offset + 24
        
        for i in range(num_wave_seqs):
            if ws_offset + 24 > len(self.data):
                break
            
            # Wave sequence name is at the start (24 bytes)
            name = self.get_string(ws_offset, 24)
            
            wave_seq = WaveSequence(
                bank=bank_name,
                index=i,
                name=name,
                raw_data=self.data[ws_offset:ws_offset+wave_seq_size],
                _raw_offset=ws_offset
            )
            wave_sequences.append(wave_seq)
            ws_offset += wave_seq_size
        
        return WaveSequenceBank(
            bank_id=bank_name,
            wave_sequences=wave_sequences,
            byte_offset=wbk1_offset,
            patch_size=wave_seq_size,
            is_writable=(bank_id >= 0x20000),  # User banks are writable
            is_loaded=True
        )
