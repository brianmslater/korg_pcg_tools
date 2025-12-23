"""
Hex export functionality for viewing raw patch data.

Based on C# implementation:
- ViewModels/PcgViewModel.cs - HexExport command
- HexExportDlg.xaml / HexExportDlg.xaml.cs

Displays raw hex data for selected patches, useful for debugging
and understanding patch structure.
"""

from typing import List, Union
from .models import Program, Combi, SetListSlot


def generate_hex_export(patches: List[Union[Program, Combi, SetListSlot]], 
                        content: bytes,
                        columns_per_line: int = 16) -> str:
    """
    Generate hex export text for selected patches.
    
    Based on C# PcgViewModel hex export implementation.
    
    Args:
        patches: List of patches to export (Program, Combi, or SetListSlot)
        content: The raw PCG file content bytes
        columns_per_line: Number of hex bytes per line (default 16)
        
    Returns:
        Formatted hex dump string
    """
    lines = []
    
    for patch in patches:
        # Get patch info
        patch_id = getattr(patch, 'id', 'Unknown')
        patch_name = getattr(patch, 'name', '')
        byte_offset = getattr(patch, 'byte_offset', 0)
        byte_length = getattr(patch, 'byte_length', 0)
        
        if byte_offset == 0 or byte_length == 0:
            continue
        
        lines.append(f"{patch_id}: {patch_name}")
        
        index = 0
        while index < byte_length:
            # Build the hex line
            chars_in_line = [' '] * columns_per_line
            offset = byte_offset + index
            
            # Line header: relative offset (decimal) absolute offset (hex)
            line_parts = [f"{index:08x} ({index:08d}) {offset:08x}: "]
            
            # Hex bytes
            hex_parts = []
            for column in range(columns_per_line):
                # Add space every 4 bytes for readability
                if column > 0 and column % 4 == 0:
                    hex_parts.append(' ')
                
                if index + column < byte_length and offset + column < len(content):
                    byte_val = content[offset + column]
                    hex_parts.append(f" {byte_val:02x}")
                    # Store printable character
                    char_val = chr(byte_val)
                    if char_val.isprintable() and not char_val.isspace():
                        chars_in_line[column] = char_val
                    else:
                        chars_in_line[column] = '.'
                else:
                    hex_parts.append("   ")  # Padding for incomplete lines
            
            line_parts.append(''.join(hex_parts))
            line_parts.append(": ")
            
            # ASCII representation
            ascii_parts = []
            for column in range(columns_per_line):
                if column > 0 and column % 4 == 0:
                    ascii_parts.append(' ')
                ascii_parts.append(chars_in_line[column])
            
            line_parts.append(''.join(ascii_parts))
            lines.append(''.join(line_parts))
            
            index += columns_per_line
        
        lines.append("")  # Blank line between patches
    
    return '\n'.join(lines)


def format_single_patch_hex(patch: Union[Program, Combi, SetListSlot],
                            content: bytes,
                            columns_per_line: int = 16) -> str:
    """
    Format hex dump for a single patch.
    
    Args:
        patch: The patch to export
        content: The raw PCG file content bytes
        columns_per_line: Number of hex bytes per line
        
    Returns:
        Formatted hex dump string
    """
    return generate_hex_export([patch], content, columns_per_line)
