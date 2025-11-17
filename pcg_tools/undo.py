"""Undo/redo support for PCG Tools."""

from typing import List, Any, Callable, Optional
from dataclasses import dataclass
import copy


@dataclass
class Action:
    """Represents an undoable action."""
    description: str
    undo_func: Callable
    redo_func: Callable
    undo_data: Any = None
    redo_data: Any = None


class UndoManager:
    """Manages undo/redo operations."""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.undo_stack: List[Action] = []
        self.redo_stack: List[Action] = []
        self.callbacks: List[Callable] = []
    
    def add_action(self, action: Action):
        """Add an action to the undo stack."""
        self.undo_stack.append(action)
        
        # Limit stack size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        
        # Clear redo stack when new action is added
        self.redo_stack.clear()
        
        # Notify callbacks
        self._notify_callbacks()
    
    def undo(self) -> bool:
        """Undo the last action."""
        if not self.can_undo():
            return False
        
        action = self.undo_stack.pop()
        
        try:
            # Execute undo
            action.undo_func(action.undo_data)
            
            # Move to redo stack
            self.redo_stack.append(action)
            
            # Notify callbacks
            self._notify_callbacks()
            
            return True
        except Exception as e:
            # If undo fails, put action back
            self.undo_stack.append(action)
            raise e
    
    def redo(self) -> bool:
        """Redo the last undone action."""
        if not self.can_redo():
            return False
        
        action = self.redo_stack.pop()
        
        try:
            # Execute redo
            action.redo_func(action.redo_data)
            
            # Move back to undo stack
            self.undo_stack.append(action)
            
            # Notify callbacks
            self._notify_callbacks()
            
            return True
        except Exception as e:
            # If redo fails, put action back
            self.redo_stack.append(action)
            raise e
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0
    
    def get_undo_description(self) -> Optional[str]:
        """Get description of next undo action."""
        if self.can_undo():
            return self.undo_stack[-1].description
        return None
    
    def get_redo_description(self) -> Optional[str]:
        """Get description of next redo action."""
        if self.can_redo():
            return self.redo_stack[-1].description
        return None
    
    def clear(self):
        """Clear all undo/redo history."""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self._notify_callbacks()
    
    def add_callback(self, callback: Callable):
        """Add a callback to be notified when undo/redo state changes."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self):
        """Notify all callbacks of state change."""
        for callback in self.callbacks:
            try:
                callback()
            except:
                pass


class UndoableEdit:
    """Helper class for creating undoable edits."""
    
    @staticmethod
    def create_patch_edit(patch, old_name, old_category, old_favorite, 
                         new_name, new_category, new_favorite):
        """Create an undoable patch edit action."""
        def undo(data):
            patch.name = data['old_name']
            patch.category = data['old_category']
            patch.favorite = data['old_favorite']
        
        def redo(data):
            patch.name = data['new_name']
            patch.category = data['new_category']
            patch.favorite = data['new_favorite']
        
        return Action(
            description=f"Edit {patch.id}",
            undo_func=undo,
            redo_func=redo,
            undo_data={
                'old_name': old_name,
                'old_category': old_category,
                'old_favorite': old_favorite
            },
            redo_data={
                'new_name': new_name,
                'new_category': new_category,
                'new_favorite': new_favorite
            }
        )
    
    @staticmethod
    def create_paste_action(bank, start_index, patches, old_patches):
        """Create an undoable paste action."""
        def undo(data):
            # Restore old patches
            for i, old_patch in enumerate(data['old_patches']):
                idx = data['start_index'] + i
                if idx < len(bank.patches):
                    bank.patches[idx] = old_patch
        
        def redo(data):
            # Paste new patches
            for i, new_patch in enumerate(data['new_patches']):
                idx = data['start_index'] + i
                if idx < len(bank.patches):
                    bank.patches[idx] = copy.deepcopy(new_patch)
        
        return Action(
            description=f"Paste {len(patches)} patch(es)",
            undo_func=undo,
            redo_func=redo,
            undo_data={
                'start_index': start_index,
                'old_patches': [copy.deepcopy(p) for p in old_patches]
            },
            redo_data={
                'start_index': start_index,
                'new_patches': [copy.deepcopy(p) for p in patches]
            }
        )
    
    @staticmethod
    def create_move_action(bank, from_index, to_index):
        """Create an undoable move action."""
        def undo(data):
            # Move back
            patch = bank.patches.pop(data['to_index'])
            bank.patches.insert(data['from_index'], patch)
        
        def redo(data):
            # Move forward
            patch = bank.patches.pop(data['from_index'])
            bank.patches.insert(data['to_index'], patch)
        
        return Action(
            description=f"Move patch",
            undo_func=undo,
            redo_func=redo,
            undo_data={'from_index': to_index, 'to_index': from_index},
            redo_data={'from_index': from_index, 'to_index': to_index}
        )
    
    @staticmethod
    def create_sort_action(bank, old_order):
        """Create an undoable sort action."""
        new_order = [copy.deepcopy(p) for p in bank.patches]
        
        def undo(data):
            bank.patches = [copy.deepcopy(p) for p in data['old_order']]
        
        def redo(data):
            bank.patches = [copy.deepcopy(p) for p in data['new_order']]
        
        return Action(
            description="Sort patches",
            undo_func=undo,
            redo_func=redo,
            undo_data={'old_order': old_order},
            redo_data={'new_order': new_order}
        )
    
    @staticmethod
    def create_clear_action(patch, old_data):
        """Create an undoable clear action."""
        new_data = copy.deepcopy(patch)
        
        def undo(data):
            patch.name = data['old'].name
            patch.category = data['old'].category
            patch.favorite = data['old'].favorite
            patch.raw_data = data['old'].raw_data
        
        def redo(data):
            patch.name = data['new'].name
            patch.category = data['new'].category
            patch.favorite = data['new'].favorite
            patch.raw_data = data['new'].raw_data
        
        return Action(
            description=f"Clear {patch.id}",
            undo_func=undo,
            redo_func=redo,
            undo_data={'old': old_data},
            redo_data={'new': new_data}
        )
