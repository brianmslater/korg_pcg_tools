"""Program Reference Changer - Change program references in combis and set lists.

Ported from C# PCG Tools:
- Tools/ReferenceChanger.cs - Core reference changing logic
- Tools/RuleParser.cs - Parse reference change rules
- Tools/ProgramPatchParser.cs - Parse program patches

Rule syntax:
    bank_name                           e.g. I-A (whole bank)
    bank_name start_index..end_index    e.g. I-A040..080 (range)
    bank_name index                     e.g. I-A040 (single program)
    
    From -> To syntax:
    I-A -> U-A                          (whole bank to whole bank)
    I-A040..080 -> U-A000..             (range to range, auto-calculate end)
    I-A040 -> U-A000                    (single to single)
    
    Arrows can be: -> or => or >
"""

from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
from .models import PcgFile, Program, Combi, Bank, SetListSlot


@dataclass
class ParseError:
    """Error information from parsing."""
    line_number: int
    message: str


@dataclass
class ReferenceChangeRule:
    """A single reference change rule."""
    from_bank: str
    from_start: int
    from_end: int
    to_bank: str
    to_start: int
    to_end: int
    
    def __str__(self) -> str:
        if self.from_start == self.from_end:
            from_str = f"{self.from_bank}{self.from_start:03d}"
        else:
            from_str = f"{self.from_bank}{self.from_start:03d}..{self.from_end:03d}"
        
        if self.to_start == self.to_end:
            to_str = f"{self.to_bank}{self.to_start:03d}"
        else:
            to_str = f"{self.to_bank}{self.to_start:03d}..{self.to_end:03d}"
        
        return f"{from_str} -> {to_str}"


class ProgramPatchParser:
    """Parse program patch references from rule strings.
    
    Based on C# Tools/ProgramPatchParser.cs.
    
    Syntax:
        bank_name                           e.g. I-A (whole bank)
        bank_name start_index..end_index    e.g. I-A040..080 (range)
        bank_name index                     e.g. I-A040 (single program)
        bank_name start_index..             e.g. I-A040.. (range with auto end)
    """
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
    
    def parse(self, part: str, from_patches: Optional[List[Tuple[str, int]]] = None) -> Optional[List[Tuple[str, int]]]:
        """Parse a patch reference string.
        
        Args:
            part: The string to parse (e.g., "I-A040..080")
            from_patches: If this is a "to" part, the from patches for auto-end calculation
            
        Returns:
            List of (bank_id, index) tuples, or None if parse failed
        """
        part = part.strip()
        
        # Parse indices
        result = self._parse_indices(part)
        if result is None:
            return None
        
        bank_name, start_index, end_index, auto_end = result
        
        # Find the bank
        bank = self.pcg.get_program_bank(bank_name)
        if bank is None:
            return None
        
        # Handle auto-end (e.g., "I-A040..")
        if auto_end and from_patches is not None:
            end_index = start_index + len(from_patches) - 1
        
        # If both indices are -1, use whole bank
        if start_index == -1 and end_index == -1:
            start_index = 0
            end_index = len(bank.patches) - 1
        
        # If only end_index is set (single program), start = end
        if start_index == -1:
            start_index = end_index
        
        # Validate indices
        if start_index < 0 or end_index < 0:
            return None
        if start_index > end_index:
            return None
        if end_index >= len(bank.patches):
            return None
        
        # Build list of patches
        patches = []
        for index in range(start_index, end_index + 1):
            patches.append((bank_name, index))
        
        return patches
    
    def _parse_indices(self, part: str) -> Optional[Tuple[str, int, int, bool]]:
        """Parse bank name and indices from a string.
        
        Returns:
            Tuple of (bank_name, start_index, end_index, auto_end) or None if failed
            auto_end is True if the syntax was "bank_name start.." (auto-calculate end)
        """
        auto_end = False
        start_index = -1
        end_index = -1
        
        # Check for range syntax with ".."
        if ".." in part:
            # Could be "I-A040..080" or "I-A040.."
            if part.endswith(".."):
                # Auto-end syntax: "I-A040.."
                auto_end = True
                part = part[:-2]  # Remove trailing ".."
                
                # Parse the start index (last 3 digits)
                if len(part) >= 3 and part[-3:].isdigit():
                    start_index = int(part[-3:])
                    part = part[:-3]
                else:
                    return None
            else:
                # Range syntax: "I-A040..080"
                parts = part.split("..")
                if len(parts) != 2:
                    return None
                
                # Parse end index
                if len(parts[1]) >= 3 and parts[1][-3:].isdigit():
                    end_index = int(parts[1][-3:])
                else:
                    return None
                
                # Parse start index
                if len(parts[0]) >= 3 and parts[0][-3:].isdigit():
                    start_index = int(parts[0][-3:])
                    part = parts[0][:-3]
                else:
                    return None
        else:
            # Single index or whole bank: "I-A040" or "I-A"
            if len(part) >= 3 and part[-3:].isdigit():
                end_index = int(part[-3:])
                part = part[:-3]
            # else: whole bank, indices stay -1
        
        # What remains should be the bank name
        bank_name = part.strip()
        if not bank_name:
            return None
        
        return (bank_name, start_index, end_index, auto_end)


class RuleParser:
    """Parse reference change rules.
    
    Based on C# Tools/RuleParser.cs.
    
    Rule format:
        from_spec -> to_spec
        from_spec => to_spec
        from_spec > to_spec
        
    Examples:
        I-A -> U-A                  (whole bank)
        I-A040..080 -> U-A000..     (range)
        I-A040 -> U-A000            (single)
    """
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self.parsed_rules: Dict[Tuple[str, int], Tuple[str, int]] = {}
        self.has_parsed_ok = False
        self.parse_error_line = -1
        self.parse_error_message = ""
    
    def parse(self, rules: str) -> bool:
        """Parse rules from a multi-line string.
        
        Args:
            rules: Multi-line string with one rule per line
            
        Returns:
            True if all rules parsed successfully
        """
        self.parsed_rules.clear()
        self.has_parsed_ok = False
        self.parse_error_line = -1
        self.parse_error_message = ""
        
        lines = rules.split('\n')
        line_number = 0
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                line_number += 1
                continue
            
            # Normalize arrow syntax
            line = line.replace("->", ">").replace("=>", ">")
            
            if not self._parse_line(line, line_number):
                return False
            
            line_number += 1
        
        self.has_parsed_ok = True
        return True
    
    def _parse_line(self, line: str, line_number: int) -> bool:
        """Parse a single rule line.
        
        Args:
            line: The line to parse (already normalized)
            line_number: Line number for error reporting
            
        Returns:
            True if parsed successfully
        """
        if ">" not in line:
            self.parse_error_line = line_number
            self.parse_error_message = "Missing arrow (-> or =>)"
            return False
        
        parts = line.split(">")
        if len(parts) != 2:
            self.parse_error_line = line_number
            self.parse_error_message = "Invalid rule format (multiple arrows?)"
            return False
        
        from_part = parts[0].strip()
        to_part = parts[1].strip()
        
        if not from_part or not to_part:
            self.parse_error_line = line_number
            self.parse_error_message = "Empty from or to specification"
            return False
        
        parser = ProgramPatchParser(self.pcg)
        
        # Parse "from" patches
        from_patches = parser.parse(from_part)
        if from_patches is None:
            self.parse_error_line = line_number
            self.parse_error_message = f"Invalid 'from' specification: {from_part}"
            return False
        
        # Parse "to" patches (with from_patches for auto-end calculation)
        to_patches = parser.parse(to_part, from_patches)
        if to_patches is None:
            self.parse_error_line = line_number
            self.parse_error_message = f"Invalid 'to' specification: {to_part}"
            return False
        
        # Verify same count
        if len(from_patches) != len(to_patches):
            self.parse_error_line = line_number
            self.parse_error_message = f"Patch count mismatch: {len(from_patches)} from vs {len(to_patches)} to"
            return False
        
        # Add to rules
        for i in range(len(from_patches)):
            self.parsed_rules[from_patches[i]] = to_patches[i]
        
        return True
    
    def get_rules_as_list(self) -> List[ReferenceChangeRule]:
        """Get parsed rules as a list of ReferenceChangeRule objects."""
        # Group consecutive rules into ranges
        rules = []
        
        # Sort by from bank and index
        sorted_items = sorted(self.parsed_rules.items(), key=lambda x: (x[0][0], x[0][1]))
        
        if not sorted_items:
            return rules
        
        # Group into ranges
        current_from_bank = sorted_items[0][0][0]
        current_to_bank = sorted_items[0][1][0]
        current_from_start = sorted_items[0][0][1]
        current_to_start = sorted_items[0][1][1]
        current_from_end = current_from_start
        current_to_end = current_to_start
        
        for i in range(1, len(sorted_items)):
            from_patch, to_patch = sorted_items[i]
            from_bank, from_idx = from_patch
            to_bank, to_idx = to_patch
            
            # Check if this continues the current range
            if (from_bank == current_from_bank and 
                to_bank == current_to_bank and
                from_idx == current_from_end + 1 and
                to_idx == current_to_end + 1):
                # Extend current range
                current_from_end = from_idx
                current_to_end = to_idx
            else:
                # Save current range and start new one
                rules.append(ReferenceChangeRule(
                    from_bank=current_from_bank,
                    from_start=current_from_start,
                    from_end=current_from_end,
                    to_bank=current_to_bank,
                    to_start=current_to_start,
                    to_end=current_to_end
                ))
                current_from_bank = from_bank
                current_to_bank = to_bank
                current_from_start = from_idx
                current_to_start = to_idx
                current_from_end = from_idx
                current_to_end = to_idx
        
        # Don't forget the last range
        rules.append(ReferenceChangeRule(
            from_bank=current_from_bank,
            from_start=current_from_start,
            from_end=current_from_end,
            to_bank=current_to_bank,
            to_start=current_to_start,
            to_end=current_to_end
        ))
        
        return rules


class ReferenceChanger:
    """Change program references in combis and set list slots.
    
    Based on C# Tools/ReferenceChanger.cs.
    """
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self._rule_parser: Optional[RuleParser] = None
        self._processed_slots: set = set()  # Track processed slots to avoid double-processing
        self._processed_timbres: set = set()  # Track processed timbres
        self._progress_callback: Optional[Callable[[int], None]] = None
        
        # Statistics
        self.slots_changed = 0
        self.timbres_changed = 0
    
    def set_progress_callback(self, callback: Callable[[int], None]):
        """Set a callback for progress updates (0-100)."""
        self._progress_callback = callback
    
    def parse_rules(self, rules: str) -> bool:
        """Parse reference change rules.
        
        Args:
            rules: Multi-line string with rules
            
        Returns:
            True if parsing succeeded
        """
        self._rule_parser = RuleParser(self.pcg)
        return self._rule_parser.parse(rules)
    
    @property
    def has_parsed_ok(self) -> bool:
        """Check if rules were parsed successfully."""
        return self._rule_parser is not None and self._rule_parser.has_parsed_ok
    
    @property
    def parse_error_line(self) -> int:
        """Get the line number where parsing failed (-1 if no error)."""
        if self._rule_parser is None:
            return -1
        return self._rule_parser.parse_error_line
    
    @property
    def parse_error_message(self) -> str:
        """Get the parse error message."""
        if self._rule_parser is None:
            return ""
        return self._rule_parser.parse_error_message
    
    @property
    def parsed_rules(self) -> Dict[Tuple[str, int], Tuple[str, int]]:
        """Get the parsed rules dictionary."""
        if self._rule_parser is None:
            return {}
        return self._rule_parser.parsed_rules
    
    def change_references(self) -> Tuple[int, int]:
        """Apply the parsed rules to change references.
        
        Returns:
            Tuple of (slots_changed, timbres_changed)
        """
        if not self.has_parsed_ok:
            return (0, 0)
        
        self._processed_slots.clear()
        self._processed_timbres.clear()
        self.slots_changed = 0
        self.timbres_changed = 0
        
        rules = self._rule_parser.parsed_rules
        total_rules = len(rules)
        current_percentage = 0
        
        for i, (from_patch, to_patch) in enumerate(rules.items()):
            # Progress update
            new_percentage = int((i + 1) * 100 / total_rules) if total_rules > 0 else 100
            if new_percentage != current_percentage:
                current_percentage = new_percentage
                if self._progress_callback:
                    self._progress_callback(current_percentage)
            
            # Change references in set list slots
            self._change_references_in_slots(from_patch, to_patch)
            
            # Change references in combis
            self._change_references_in_combis(from_patch, to_patch)
        
        return (self.slots_changed, self.timbres_changed)
    
    def _change_references_in_slots(self, from_patch: Tuple[str, int], to_patch: Tuple[str, int]):
        """Change program references in set list slots.
        
        Based on C# ReferenceChanger.ChangeReferencesInSetListSlots.
        """
        from_bank, from_index = from_patch
        to_bank, to_index = to_patch
        
        for setlist in self.pcg.set_lists:
            for slot in setlist.slots:
                # Only change program references (not combi references)
                if slot.patch_type != "Program":
                    continue
                
                # Check if this slot references the "from" program
                if slot.patch_bank != from_bank or slot.patch_index != from_index:
                    continue
                
                # Skip if already processed
                slot_id = (id(setlist), id(slot))
                if slot_id in self._processed_slots:
                    continue
                
                # Change the reference
                slot.patch_bank = to_bank
                slot.patch_index = to_index
                
                # Update raw_data if present
                if hasattr(slot, 'raw_data') and slot.raw_data:
                    self._update_slot_raw_data(slot, to_bank, to_index)
                
                self._processed_slots.add(slot_id)
                self.slots_changed += 1
    
    def _change_references_in_combis(self, from_patch: Tuple[str, int], to_patch: Tuple[str, int]):
        """Change program references in combi timbres.
        
        Based on C# ReferenceChanger.ChangeReferencesInCombis and ChangeReferencesInTimbres.
        """
        from_bank, from_index = from_patch
        to_bank, to_index = to_patch
        
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                for i, timbre in enumerate(combi.timbres):
                    # Only change timbres that are Off or Int (internal)
                    # Based on C# logic that checks Status == "Off" or "Int"
                    if timbre.status not in ("Off", "Int"):
                        continue
                    
                    # Check if this timbre references the "from" program
                    if timbre.program_bank != from_bank or timbre.program_index != from_index:
                        continue
                    
                    # Skip if already processed
                    timbre_id = (id(combi), i)
                    if timbre_id in self._processed_timbres:
                        continue
                    
                    # Change the reference
                    timbre.program_bank = to_bank
                    timbre.program_index = to_index
                    
                    # Update raw_data if present
                    if hasattr(combi, 'raw_data') and combi.raw_data:
                        self._update_timbre_raw_data(combi, i, to_bank, to_index)
                    
                    self._processed_timbres.add(timbre_id)
                    self.timbres_changed += 1
    
    def _update_slot_raw_data(self, slot: SetListSlot, new_bank: str, new_index: int):
        """Update the raw_data bytes for a slot's program reference.
        
        Based on KronosSetListSlot.cs structure:
        - Offset 2: Bank ID (1 byte)
        - Offset 4-5: Program index (2 bytes, little-endian)
        """
        from .pcg_structure import SLOT_BANK_IDS
        
        if not slot.raw_data or len(slot.raw_data) < 6:
            return
        
        # Convert to mutable bytearray
        data = bytearray(slot.raw_data)
        
        # Get bank ID for the new bank
        bank_id = SLOT_BANK_IDS.get(new_bank)
        if bank_id is not None:
            data[2] = bank_id
        
        # Set program index (little-endian 16-bit at offset 4)
        data[4] = new_index & 0xFF
        data[5] = (new_index >> 8) & 0xFF
        
        slot.raw_data = bytes(data)
    
    def _update_timbre_raw_data(self, combi: Combi, timbre_index: int, new_bank: str, new_index: int):
        """Update the raw_data bytes for a timbre's program reference.
        
        Based on KronosTimbre.cs structure:
        - Timbre offset: 4802 + (timbre_index * 188)
        - Within timbre:
          - Offset 0: Program bank ID (1 byte)
          - Offset 2-3: Program index (2 bytes, little-endian)
        """
        from .pcg_structure import TIMBRE_BANK_PCGIDS, KronosCombiOffsets, KronosTimbreOffsets
        
        if not combi.raw_data:
            return
        
        # Calculate timbre offset within combi
        timbre_offset = KronosCombiOffsets.TIMBRES_OFFSET + (timbre_index * KronosTimbreOffsets.TIMBRE_SIZE)
        
        if timbre_offset + 4 > len(combi.raw_data):
            return
        
        # Convert to mutable bytearray
        data = bytearray(combi.raw_data)
        
        # Get bank ID for the new bank
        bank_id = TIMBRE_BANK_PCGIDS.get(new_bank)
        if bank_id is not None:
            data[timbre_offset] = bank_id
        
        # Set program index (little-endian 16-bit at offset +2)
        data[timbre_offset + 2] = new_index & 0xFF
        data[timbre_offset + 3] = (new_index >> 8) & 0xFF
        
        combi.raw_data = bytes(data)


def change_references_from_rules(pcg: PcgFile, rules: str, 
                                  progress_callback: Optional[Callable[[int], None]] = None) -> Tuple[bool, str, int, int]:
    """Convenience function to parse rules and change references.
    
    Args:
        pcg: The PCG file to modify
        rules: Multi-line string with reference change rules
        progress_callback: Optional callback for progress updates (0-100)
        
    Returns:
        Tuple of (success, error_message, slots_changed, timbres_changed)
    """
    changer = ReferenceChanger(pcg)
    
    if progress_callback:
        changer.set_progress_callback(progress_callback)
    
    if not changer.parse_rules(rules):
        error_msg = f"Line {changer.parse_error_line + 1}: {changer.parse_error_message}"
        return (False, error_msg, 0, 0)
    
    slots_changed, timbres_changed = changer.change_references()
    return (True, "", slots_changed, timbres_changed)
