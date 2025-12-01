"""Batch operations for programs, combis, and setlists."""

from typing import List, Callable
from .models import Program, Combi, Bank, SetList


class BatchOperations:
    """Batch operations for PCG files."""
    
    @staticmethod
    def sort_programs(bank: Bank, key: str = "name", reverse: bool = False):
        """Sort programs in a bank.
        
        Args:
            bank: Program bank to sort
            key: Sort key - "name", "category", "favorite", "engine"
            reverse: If True, sort in descending order
        """
        if key == "name":
            bank.patches.sort(key=lambda p: p.name.lower(), reverse=reverse)
        elif key == "category":
            bank.patches.sort(key=lambda p: (p.category.main_category if p.category else 0, 
                                            p.category.sub_category if p.category else 0), 
                            reverse=reverse)
        elif key == "favorite":
            bank.patches.sort(key=lambda p: p.favorite, reverse=not reverse)  # Favorites first
        elif key == "engine":
            bank.patches.sort(key=lambda p: p.engine or "", reverse=reverse)
        
        # IDs are derived from position, no need to update
    
    @staticmethod
    def sort_combis(bank: Bank, key: str = "name", reverse: bool = False):
        """Sort combis in a bank.
        
        Args:
            bank: Combi bank to sort
            key: Sort key - "name", "category", "favorite", "tempo"
            reverse: If True, sort in descending order
        """
        if key == "name":
            bank.patches.sort(key=lambda c: c.name.lower(), reverse=reverse)
        elif key == "category":
            bank.patches.sort(key=lambda c: (c.category.main_category if c.category else 0,
                                            c.category.sub_category if c.category else 0),
                            reverse=reverse)
        elif key == "favorite":
            bank.patches.sort(key=lambda c: c.favorite, reverse=not reverse)
        elif key == "tempo":
            bank.patches.sort(key=lambda c: c.tempo or 0, reverse=reverse)
        
        # IDs are derived from position, no need to update
    
    @staticmethod
    def compact_bank(bank: Bank, empty_names: List[str] = None):
        """Remove empty patches and compact bank.
        
        Args:
            bank: Bank to compact
            empty_names: List of names considered "empty" (default: ["Init", "[Empty"])
        """
        if empty_names is None:
            empty_names = ["Init", "[Empty", ""]
        
        # Filter out empty patches
        non_empty = []
        for patch in bank.patches:
            is_empty = False
            for empty_name in empty_names:
                if patch.name.startswith(empty_name) or patch.name.strip() == "":
                    is_empty = True
                    break
            if not is_empty:
                non_empty.append(patch)
        
        # Replace patches with compacted list
        bank.patches = non_empty
    
    @staticmethod
    def remove_duplicates(bank: Bank, by: str = "name"):
        """Remove duplicate patches from bank.
        
        Args:
            bank: Bank to process
            by: Comparison key - "name" or "exact" (compares all properties)
        """
        seen = set()
        unique = []
        
        for patch in bank.patches:
            if by == "name":
                key = patch.name.lower().strip()
            elif by == "exact":
                # Compare name, category, and favorite
                key = (patch.name.lower().strip(),
                      patch.category.main_category if patch.category else 0,
                      patch.category.sub_category if patch.category else 0,
                      patch.favorite)
            else:
                key = patch.name.lower().strip()
            
            if key not in seen:
                seen.add(key)
                unique.append(patch)
        
        # Replace with unique patches
        bank.patches = unique
    
    @staticmethod
    def capitalize_names(bank: Bank, style: str = "title"):
        """Capitalize patch names in bank.
        
        Args:
            bank: Bank to process
            style: Capitalization style - "title", "upper", "lower", "sentence"
        """
        for patch in bank.patches:
            if style == "title":
                patch.name = patch.name.title()
            elif style == "upper":
                patch.name = patch.name.upper()
            elif style == "lower":
                patch.name = patch.name.lower()
            elif style == "sentence":
                patch.name = patch.name.capitalize()
    
    @staticmethod
    def move_favorites_to_top(bank: Bank):
        """Move all favorite patches to the top of the bank."""
        favorites = [p for p in bank.patches if p.favorite]
        non_favorites = [p for p in bank.patches if not p.favorite]
        
        bank.patches = favorites + non_favorites
    
    @staticmethod
    def clear_empty_slots(setlist: SetList):
        """Remove empty slots from setlist.
        
        Args:
            setlist: Setlist to process
        """
        non_empty = []
        for slot in setlist.slots:
            if slot.name.strip() or slot.patch_type:
                non_empty.append(slot)
        
        setlist.slots = non_empty
        
        # Update slot indices
        for i, slot in enumerate(setlist.slots):
            slot.slot_index = i
    
    @staticmethod
    def fill_empty_names(bank: Bank, prefix: str = "Patch"):
        """Fill empty patch names with default names.
        
        Args:
            bank: Bank to process
            prefix: Prefix for generated names (e.g., "Patch 001")
        """
        for i, patch in enumerate(bank.patches):
            if not patch.name.strip() or patch.name.startswith("Init") or patch.name.startswith("[Empty"):
                patch.name = f"{prefix} {i+1:03d}"
    
    @staticmethod
    def move_patch_up(bank: Bank, index: int) -> bool:
        """Move patch up one position in bank.
        
        Args:
            bank: Bank containing the patch
            index: Current index of patch to move
        
        Returns:
            True if moved, False if already at top
        """
        if index <= 0 or index >= len(bank.patches):
            return False
        
        # Swap with previous
        bank.patches[index], bank.patches[index-1] = bank.patches[index-1], bank.patches[index]
        return True
    
    @staticmethod
    def move_patch_down(bank: Bank, index: int) -> bool:
        """Move patch down one position in bank.
        
        Args:
            bank: Bank containing the patch
            index: Current index of patch to move
        
        Returns:
            True if moved, False if already at bottom
        """
        if index < 0 or index >= len(bank.patches) - 1:
            return False
        
        # Swap with next
        bank.patches[index], bank.patches[index+1] = bank.patches[index+1], bank.patches[index]
        return True
    
    @staticmethod
    def move_slot_up(setlist: SetList, index: int) -> bool:
        """Move slot up one position in setlist.
        
        Args:
            setlist: Setlist containing the slot
            index: Current index of slot to move
        
        Returns:
            True if moved, False if already at top
        """
        if index <= 0 or index >= len(setlist.slots):
            return False
        
        # Swap with previous
        setlist.slots[index], setlist.slots[index-1] = setlist.slots[index-1], setlist.slots[index]
        
        # Update slot indices
        setlist.slots[index].slot_index = index
        setlist.slots[index-1].slot_index = index - 1
        
        return True
    
    @staticmethod
    def sort_slots(setlist: SetList, key: str = "name", reverse: bool = False):
        """Sort slots in a setlist.
        
        Args:
            setlist: Setlist to sort
            key: Sort key - "name", "patch"
            reverse: If True, sort in descending order
        """
        if key == "name":
            setlist.slots.sort(key=lambda s: s.name.lower(), reverse=reverse)
        elif key == "patch":
            setlist.slots.sort(key=lambda s: s.patch_id, reverse=reverse)
        
        # Update slot indices after sorting
        for i, slot in enumerate(setlist.slots):
            slot.slot_index = i
    
    @staticmethod
    def move_slot_down(setlist: SetList, index: int) -> bool:
        """Move slot down one position in setlist.
        
        Args:
            setlist: Setlist containing the slot
            index: Current index of slot to move
        
        Returns:
            True if moved, False if already at bottom
        """
        if index < 0 or index >= len(setlist.slots) - 1:
            return False
        
        # Swap with next
        setlist.slots[index], setlist.slots[index+1] = setlist.slots[index+1], setlist.slots[index]
        
        # Update slot indices
        setlist.slots[index].slot_index = index
        setlist.slots[index+1].slot_index = index + 1
        
        return True
