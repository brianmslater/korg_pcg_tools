"""Track program references in combis and set lists."""

from typing import Dict, List, Set, Tuple
from .models import PcgFile, Program, Combi, Bank


class ReferenceTracker:
    """Track which programs are referenced by combis."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self._program_usage: Dict[str, List[str]] = {}  # program_id -> [combi_ids]
        self._combi_programs: Dict[str, Set[str]] = {}  # combi_id -> {program_ids}
        self._build_references()
    
    def _build_references(self):
        """Build the reference maps."""
        self._program_usage.clear()
        self._combi_programs.clear()
        
        # Scan all combis
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if not combi.name or combi.name.strip() == "":
                    continue
                
                combi_id = combi.id
                self._combi_programs[combi_id] = set()
                
                # Check each timbre
                for timbre in combi.timbres:
                    # Only count timbres that are ON (status != "OFF")
                    if timbre.status == "OFF":
                        continue
                    
                    prog_id = timbre.program_id
                    if prog_id:
                        # Add to combi's program list
                        self._combi_programs[combi_id].add(prog_id)
                        
                        # Add to program's usage list
                        if prog_id not in self._program_usage:
                            self._program_usage[prog_id] = []
                        self._program_usage[prog_id].append(combi_id)
    
    def get_program_usage(self, program_id: str) -> List[str]:
        """Get list of combi IDs that use this program."""
        return self._program_usage.get(program_id, [])
    
    def get_combi_programs(self, combi_id: str) -> Set[str]:
        """Get set of program IDs used by this combi."""
        return self._combi_programs.get(combi_id, set())
    
    def is_program_used(self, program_id: str) -> bool:
        """Check if a program is used by any combi."""
        return program_id in self._program_usage
    
    def get_all_referenced_programs(self, combi_ids: List[str]) -> Set[str]:
        """Get all programs referenced by a list of combis."""
        all_progs = set()
        for combi_id in combi_ids:
            all_progs.update(self.get_combi_programs(combi_id))
        return all_progs
    
    def get_usage_count(self, program_id: str) -> int:
        """Get number of combis using this program."""
        return len(self.get_program_usage(program_id))
    
    def refresh(self):
        """Rebuild the reference maps."""
        self._build_references()


class ProgramRemapper:
    """Handle program reference remapping when copying/pasting."""
    
    def __init__(self):
        self.remap_table: Dict[str, str] = {}  # old_prog_id -> new_prog_id
    
    def add_mapping(self, old_id: str, new_id: str):
        """Add a program ID mapping."""
        self.remap_table[old_id] = new_id
    
    def get_mapped_id(self, old_id: str) -> str:
        """Get the new ID for an old program ID."""
        return self.remap_table.get(old_id, old_id)
    
    def remap_combi(self, combi: Combi) -> Combi:
        """Remap all program references in a combi."""
        # Create a copy
        new_combi = Combi(
            bank=combi.bank,
            index=combi.index,
            name=combi.name,
            category=combi.category,
            favorite=combi.favorite,
            timbres=combi.timbres.copy(),
            raw_data=combi.raw_data
        )
        
        # Remap each timbre's program reference
        for timbre in new_combi.timbres:
            if timbre.program_id in self.remap_table:
                old_id = timbre.program_id
                new_id = self.remap_table[old_id]
                
                # Parse new bank and index
                new_bank = new_id[:-3]
                new_index = int(new_id[-3:])
                
                timbre.program_bank = new_bank
                timbre.program_index = new_index
                timbre.program_id = new_id
        
        return new_combi
    
    def clear(self):
        """Clear all mappings."""
        self.remap_table.clear()
