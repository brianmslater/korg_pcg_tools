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
        """Read integer from data (little-endian for size, big-endian for IDs)."""
        if offset + size > len(self.data):
            return 0
        
        # For 4-byte integers, use little-endian (Korg format)
        if size == 4:
            return struct.unpack('<I', self.data[offset:offset+4])[0]
        
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
        bank = Bank(bank_id=bank_name, bank_type='Program')
        
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
            
            program = Program(
                bank=bank_name,
                index=i,
                name=name,
                engine=engine,
                raw_data=self.data[offset:offset+program_size]
            )
            
            # Track offset for writing back
            program._raw_offset = offset
            
            bank.patches.append(program)
            offset += program_size
        
        if bank.patches:  # Only add if we found programs
            pcg.program_banks.append(bank)
            debug_print(f"  Added bank {bank_name} with {len(bank.patches)} programs")
        
        return start_offset + 8 + chunk_size + 12
    
    def _parse_mbk1_chunk(self, pcg: PcgFile, offset: int) -> int:
        """Parse an MBK1 (Model Bank - for special synthesis types) chunk."""
        chunk_size = self.get_int(offset + 4, 4)
        start_offset = offset
        
        debug_print(f"Parsing MBK1 at {offset:08X}, size {chunk_size:08X}")
        
        # MBK1 header structure varies - try both +24 and +32 offsets
        # Some files have programs at +24, others at +32
        program_size = 4960  # Kronos program size
        programs = []
        
        # Try offset +24 first (older format)
        scan_offset = offset + 24
        for i in range(128):
            if scan_offset + 24 > len(self.data):
                break
            name = self.get_string(scan_offset, 24)
            if name and len(name) >= 3 and name.isprintable():
                programs.append((i, name, scan_offset))
                if i < 3:
                    debug_print(f"  Found program {i} at +24: {name}")
                scan_offset += program_size
            else:
                break
        
        # If no programs found at +24, try +32 (newer format)
        if not programs:
            scan_offset = offset + 32
            for i in range(128):
                if scan_offset + 24 > len(self.data):
                    break
                name = self.get_string(scan_offset, 24)
                if name and len(name) >= 3 and name.isprintable():
                    programs.append((i, name, scan_offset))
                    if i < 3:
                        debug_print(f"  Found program {i} at +32: {name}")
                    scan_offset += program_size
                else:
                    break
        
        if programs:
            # Decode bank ID from the chunk data (at offset +20 from data start, after 8-byte header = +28 total)
            bank_id_raw = self.get_int(start_offset + 28, 4)
            bank_id = self._decode_bank_id(bank_id_raw, is_combi=False)
            debug_print(f"  Decoded bank ID: {bank_id} (raw: {bank_id_raw:08X})")
            
            # Create bank
            bank = Bank(bank_id=bank_id, bank_type='Program')
            
            for idx, name, prog_offset in programs:
                # Extract engine information
                engine = self._extract_engine(self.data[prog_offset:prog_offset+program_size])
                
                program = Program(
                    bank=bank_id,
                    index=idx,
                    name=name,
                    engine=engine,
                    raw_data=self.data[prog_offset:prog_offset+program_size]
                )
                
                # Track offset for writing back
                program._raw_offset = prog_offset
                
                bank.patches.append(program)
            
            pcg.program_banks.append(bank)
            debug_print(f"  Added bank {bank_id} with {len(programs)} programs")
        
        return start_offset + 8 + chunk_size + 12
    
    def _extract_engine(self, program_data: bytes) -> str:
        """Extract engine type from program data.
        
        For Kronos programs, the engine type is encoded in the program data.
        Common engines: HD-1, AL-1, CX-3, STR-1, EP-1, MS-20EX, PolysixEX, MOD-7, SGX-1, SGX-2
        """
        if len(program_data) < 100:
            return ""
        
        # Engine type is typically at offset 0x58 (88) for Kronos
        # It's a 2-byte value that maps to engine types
        try:
            engine_byte = program_data[0x58] if len(program_data) > 0x58 else 0
            
            # Kronos engine mapping (based on analysis of real PCG files)
            engine_map = {
                0x00: "HD-1",      # HD-1 Synthesizer (default)
                0x01: "HD-1",      # HD-1 (alternate)
                0x02: "HD-1",      # HD-1 (pads)
                0x04: "SGX-1",     # SGX-1 Piano
                0x05: "SGX-1",     # SGX-1 (harpsichord)
                0x08: "SGX-1",     # SGX-1 (alternate)
                0x0B: "SGX-1",     # SGX-1 Piano
                0x0C: "MS-20EX",   # MS-20EX Analog
                0x0D: "PolysixEX", # PolysixEX Analog
                0x0E: "MOD-7",     # MOD-7 VPM
                0x13: "SGX-2",     # SGX-2 Electric Piano (MK I, etc.)
                0x15: "SGX-2",     # SGX-2 Electric Piano (alternate)
                0x1B: "CX-3",      # CX-3 Organ
                0x1F: "STR-1",     # STR-1 Strings
                0x21: "HD-1",      # HD-1 (alternate)
                0x22: "HD-1",      # HD-1 (alternate)
                0x23: "AL-1",      # AL-1 Analog Synthesizer
                0x25: "AL-1",      # AL-1 Analog Synthesizer (vintage)
                0x27: "AL-1",      # AL-1 Analog Synthesizer (alternate)
                0x28: "HD-1",      # HD-1 Synthesizer
                0x29: "AL-1",      # AL-1 Analog Synthesizer  
                0x2A: "STR-1",     # STR-1 String Synthesizer
                0x2B: "SGX-2",     # SGX-2 Electric Piano
                0x2C: "MOD-7",     # MOD-7 Waveshaping VPM
                0x2D: "CX-3",      # CX-3 Tonewheel Organ
                0x2E: "MOD-7",     # MOD-7 (alternate)
                0x30: "MOD-7",     # MOD-7 (alternate)
                0x33: "STR-1",     # STR-1 (alternate)
                0x38: "SGX-1",     # SGX-1 Piano (alternate)
                0x39: "SGX-2",     # SGX-2 EP (alternate)
                0x40: "EXi",       # EXi sample-based
                0x4D: "EXi",       # EXi sample-based (alternate)
                0x52: "EXi",       # EXi sample-based (alternate)
                0x55: "EXi",       # EXi sample-based (alternate)
                0x5A: "EXi",       # EXi sample-based (alternate)
                0x5B: "EXi",       # EXi sample-based (alternate)
                0x5D: "AL-1",      # AL-1 (brass/lead)
                0x64: "EXi",       # EXi sample-based (guitar)
                0x69: "EXi",       # EXi sample-based (alternate)
                0x8D: "EXi",       # EXi sample-based (alternate)
                0x95: "EXi",       # EXi sample-based (alternate)
                0xC5: "EXi",       # EXi sample-based (alternate)
            }
            
            engine = engine_map.get(engine_byte, f"0x{engine_byte:02X}")
            
            # Fallback: search for engine name in ASCII data
            if engine.startswith("0x"):
                raw_str = program_data[:200].decode('ascii', errors='ignore')
                known_engines = ['HD-1', 'AL-1', 'CX-3', 'STR-1', 'EP-1', 'MS-20', 'Polysix', 'MOD-7', 'SGX-1', 'SGX-2']
                for eng in known_engines:
                    if eng in raw_str:
                        return eng
            
            return engine
        except:
            return ""
    
    def _decode_bank_id(self, bank_id_raw: int, is_combi: bool) -> str:
        """Decode raw bank ID to human-readable format.
        
        Bank ID format (4 bytes):
        - Byte 0: Bank type/engine (0x00=INT, 0x0C=EXi, etc.)
        - Byte 1: Sub-bank (0x00=A, 0x01=B, etc.)
        - Byte 2: Additional info
        - Byte 3: Flags
        
        Examples:
        - 0x00000000 = I-A (Internal bank A)
        - 0x0C000200 = I-AA (EXi bank AA)
        - 0x0C010200 = I-AB (EXi bank AB)
        """
        # Extract bytes
        byte0 = (bank_id_raw >> 24) & 0xFF
        byte1 = (bank_id_raw >> 16) & 0xFF
        byte2 = (bank_id_raw >> 8) & 0xFF
        byte3 = bank_id_raw & 0xFF
        
        # Determine prefix (always I- for internal)
        prefix = "I-"
        
        # Determine bank letter(s) - ALWAYS UPPERCASE
        if byte0 == 0x00:
            # Standard internal bank (A-G)
            bank_letter = chr(65 + byte1).upper()  # A, B, C, etc.
        elif byte0 == 0x0C:
            # EXi banks use double letters (AA, AB, AC, etc.)
            bank_letter = (chr(65 + byte1) + chr(65 + byte1)).upper()  # AA, BB, CC, etc.
            if byte2 > 0:
                # Sub-banks: AA, AB, AC, etc.
                bank_letter = (chr(65 + byte1) + chr(65 + byte2)).upper()
        else:
            # Other engine types - use simple letter
            bank_letter = chr(65 + byte1).upper()
        
        result = f"{prefix}{bank_letter}"
        debug_print(f"  _decode_bank_id: raw={bank_id_raw:08X}, is_combi={is_combi}, result='{result}'")
        return result
    
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
        
        Kronos SLS1 structure (discovered through binary analysis):
        - SLS1 header contains sub-chunks (SLD1, SDB1)
        - First entry: "Preload Set List" (skip)
        - Next 16 entries: Setlist names with marker (1E 02 00 00) + 24-byte name
        - Following entries: Slot names (128 per setlist × 16 setlists)
        - After each slot name (at +24): patch reference data (8 bytes)
          Byte 0-1: Patch index (little-endian)
          Byte 2: Bank ID
          Byte 3: Patch type (0x30=Combi, 0x20=Program)
          Byte 4-5: Transpose/Volume
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
            return
        
        debug_print(f"Found {len(name_offsets)} potential name entries")
        
        # Parse as 16 setlists with 128 slots each
        # Structure: First 16 marker entries are setlist names
        # Then 128 slot names for each setlist (16 × 128 = 2048 slots)
        num_setlists = 16
        slots_per_setlist = 128
        
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
                    patch_index=patch_index,
                    transpose=transpose,
                    volume=volume
                )
                
                setlist.slots.append(slot)
            
            # Add setlist even if empty (to maintain indices)
            pcg.set_lists.append(setlist)
            debug_print(f"Set list {sl_idx}: {sl_name}, {len(setlist.slots)} slots")
    
    def _parse_cbk1_chunk(self, pcg: PcgFile, offset: int) -> int:
        """Parse a CBK1 (Combi Bank) chunk."""
        chunk_size = self.get_int(offset + 4, 4)
        start_offset = offset
        
        debug_print(f"Parsing CBK1 at {offset:08X}, size {chunk_size:08X}")
        
        # CBK1 structure varies - try both +24 and +40 offsets
        # Some files have combis at +24, others at +40
        combi_size = 7810  # Kronos combi size
        combis = []
        
        # Try offset +24 first (older format)
        scan_offset = offset + 24
        for i in range(128):
            if scan_offset + 24 > len(self.data):
                break
            name = self.get_string(scan_offset, 24)
            if name and len(name) >= 3 and name.isprintable():
                combis.append((i, name, scan_offset))
                if i < 3:
                    debug_print(f"  Found combi {i} at +24: {name}")
                scan_offset += combi_size
            else:
                break
        
        # If no combis found at +24, try +40 (newer format)
        if not combis:
            scan_offset = offset + 40
            for i in range(128):
                if scan_offset + 24 > len(self.data):
                    break
                name = self.get_string(scan_offset, 24)
                if name and len(name) >= 3 and name.isprintable():
                    combis.append((i, name, scan_offset))
                    if i < 3:
                        debug_print(f"  Found combi {i} at +40: {name}")
                    scan_offset += combi_size
                else:
                    break
        
        if combis:
            # Decode bank ID - try both possible locations
            # Older format: +20, Newer format: +28
            bank_id_raw = self.get_int(start_offset + 20, 4)
            if bank_id_raw == 0 or bank_id_raw > 0x10000000:
                # Try newer format
                bank_id_raw = self.get_int(start_offset + 28, 4)
            
            bank_id = self._decode_bank_id(bank_id_raw, is_combi=True)
            debug_print(f"  Decoded bank ID: {bank_id} (raw: {bank_id_raw:08X})")
            
            bank = Bank(bank_id=bank_id, bank_type='Combi')
            
            for idx, name, combi_offset in combis:
                # Parse timbres from combi data
                timbres = self._parse_timbres(combi_offset)
                
                combi = Combi(
                    bank=bank_id,
                    index=idx,
                    name=name,
                    timbres=timbres,
                    raw_data=self.data[combi_offset:combi_offset+7810]
                )
                
                # Track offset for writing back
                combi._raw_offset = combi_offset
                
                bank.patches.append(combi)
                debug_print(f"  Combi {idx}: {name} with {len(timbres)} timbres")
            
            pcg.combi_banks.append(bank)
            debug_print(f"  Added bank {bank_id} with {len(combis)} combis")
        
        return start_offset + 8 + chunk_size + 12
    
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
        
        # Timbre data starts around offset 1024 in Kronos combis
        # Each timbre is approximately 400 bytes
        timbre_base = combi_offset + 1024
        timbre_size = 400
        
        for i in range(16):  # 16 timbres per combi
            timbre_offset = timbre_base + (i * timbre_size)
            
            if timbre_offset + 20 > len(self.data):
                break
            
            try:
                # Parse timbre status (offset +0)
                # 0 = OFF, 1 = INT, 2 = EXi, etc.
                status_byte = self.data[timbre_offset]
                status = "OFF"
                if status_byte == 1:
                    status = "INT"
                elif status_byte == 2:
                    status = "EXi"
                
                # Parse program reference (offset +4 and +5)
                # Bank ID is at +4 (1 byte), Program number at +5 (1 byte)
                prog_bank_byte = self.data[timbre_offset + 4] if timbre_offset + 4 < len(self.data) else 0
                prog_num_byte = self.data[timbre_offset + 5] if timbre_offset + 5 < len(self.data) else 0
                
                # Convert bank byte to bank ID
                prog_bank = "I-A"
                if prog_bank_byte < 7:  # I-A through I-G
                    prog_bank = f"I-{chr(65 + prog_bank_byte)}"
                elif prog_bank_byte >= 0x20:  # User banks
                    user_idx = prog_bank_byte - 0x20
                    if user_idx < 7:
                        prog_bank = f"U-{chr(65 + user_idx)}"
                
                # MIDI channel (offset +2)
                midi_channel = self.data[timbre_offset + 2] if timbre_offset + 2 < len(self.data) else 0
                
                # Volume (offset +8)
                volume = self.data[timbre_offset + 8] if timbre_offset + 8 < len(self.data) else 127
                
                # Pan (offset +9)
                pan = self.data[timbre_offset + 9] if timbre_offset + 9 < len(self.data) else 64
                
                timbre = Timbre(
                    program_bank=prog_bank,
                    program_index=prog_num_byte,
                    midi_channel=midi_channel,
                    status=status,
                    volume=volume,
                    pan=pan,
                    mute=False
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
