"""
Cubase instrument definition export.

Based on C# implementation:
- ViewModels/PcgViewModel.cs - ExportToCubase(), ExportProgramToCubase(), 
  AddProgramInfoToCubase(), AddHeaderToCubase(), AddNonGmProgramHeaderToCubase()

Generates a Cubase-compatible instrument definition file (.txt) containing
all programs from a PCG file, organized by category and subcategory.
"""

from typing import List, Optional
from pathlib import Path

from .models import PcgFile, Program, Bank


def export_to_cubase(pcg: PcgFile, output_path: Optional[str] = None, 
                     filename: Optional[str] = None) -> str:
    """
    Export PCG programs to Cubase instrument definition format.
    
    Based on C# PcgViewModel.ExportToCubase().
    
    Args:
        pcg: The PCG file to export
        output_path: Optional output file path. If None, returns the content as string.
        filename: Optional filename for the script name header
        
    Returns:
        The generated Cubase instrument definition content
    """
    lines = []
    
    # Get model name from header
    model_name = pcg.header.model.name if pcg.header and pcg.header.model else "KRONOS"
    
    # Header - based on C# ExportToCubase()
    lines.append("[cubase parse file]")
    lines.append("[parser version 0001]")
    lines.append("")
    lines.append("[creators first name]PCG Tools Python")
    lines.append("[creators last name]")
    lines.append("[device manufacturer]Korg")
    lines.append(f"[device name] {model_name.upper()}(KORG)")
    lines.append(f"[script name] {Path(filename).name if filename else 'Unknown'}")
    lines.append("[script version]version 1.00")
    lines.append("")
    lines.append("[define patchnames]")
    lines.append("")
    lines.append(f"[mode]{model_name}")
    
    # Collect all non-empty programs
    programs = []
    for bank in pcg.program_banks:
        for prog in bank.patches:
            if prog.name and prog.name.strip() and not _is_init_program(prog):
                programs.append((bank, prog))
    
    # Sort by category, then subcategory, then name
    programs.sort(key=lambda x: (
        x[1].category.main_category if x[1].category else 0,
        x[1].category.sub_category if x[1].category else 0,
        x[1].name
    ))
    
    current_category = -1
    current_subcategory = -1
    gm_reached = False
    
    for bank, prog in programs:
        is_gm = _is_gm_bank(bank)
        
        # Add headers as needed
        if is_gm:
            if not gm_reached:
                lines.append("[g1] GM Bank")
                gm_reached = True
        else:
            # Check if category changed
            cat = prog.category.main_category if prog.category else 0
            subcat = prog.category.sub_category if prog.category else 0
            
            if current_category != cat:
                cat_name = prog.category.main_category if prog.category else f"Category{cat}"
                lines.append(f"[g1] {cat_name}")
                current_category = cat
                current_subcategory = -1  # Reset subcategory
            
            # Check if subcategory changed (if supported)
            if current_subcategory != subcat:
                subcat_name = prog.category.sub_category if prog.category else f"Sub Category{subcat}"
                lines.append(f"[g2] {subcat_name}")
                current_subcategory = subcat
        
        # Add program info
        _add_program_info(lines, bank, prog, is_gm)
    
    lines.append("[end]")
    
    content = '\n'.join(lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return content


def _is_init_program(prog: Program) -> bool:
    """Check if a program is an init/empty program."""
    if not prog.name:
        return True
    name = prog.name.strip().lower()
    return name in ('', 'init program', 'init', 'initialized')


def _is_gm_bank(bank: Bank) -> bool:
    """Check if a bank is a GM bank."""
    bank_id = bank.bank_id.upper() if bank.bank_id else ""
    return bank_id.startswith("GM") or bank_id.startswith("G(")


def _get_bank_pcg_id(bank: Bank) -> int:
    """
    Get the PCG ID for a bank.
    
    Based on C# bank.PcgId values.
    """
    bank_id = bank.bank_id.upper() if bank.bank_id else ""
    
    # Internal banks: I-A=0, I-B=1, ..., I-F=5
    if bank_id.startswith("I-"):
        letter = bank_id[2] if len(bank_id) > 2 else 'A'
        return ord(letter) - ord('A')
    
    # GM banks: GM=6, g(1)=7, ..., g(9)=15, g(d)=16
    if bank_id == "GM":
        return 6
    if bank_id.startswith("G("):
        suffix = bank_id[2] if len(bank_id) > 2 else '1'
        if suffix == 'D':
            return 16
        return 6 + int(suffix)
    
    # User banks: U-A=17, U-B=18, ..., U-G=23, U-AA=24, ...
    if bank_id.startswith("U-"):
        suffix = bank_id[2:] if len(bank_id) > 2 else 'A'
        if len(suffix) == 1:
            return 17 + (ord(suffix) - ord('A'))
        elif len(suffix) == 2:
            # U-AA=24, U-BB=25, etc.
            return 24 + (ord(suffix[0]) - ord('A'))
    
    return 0


def _add_program_info(lines: List[str], bank: Bank, prog: Program, is_gm: bool):
    """
    Add program info line to the export.
    
    Based on C# AddProgramInfoToCubase().
    """
    pcg_id = _get_bank_pcg_id(bank)
    prog_index = prog.index if hasattr(prog, 'index') else 0
    
    if is_gm:
        # GM format: [p2,program_index,121,bank_offset]
        bank_offset = pcg_id - 6  # Offset from first GM bank
        patch_id = f"[p2,{prog_index},121,{bank_offset}]"
        lines.append(f"{patch_id} {prog.id}")
    else:
        # Non-GM format: [p3,program_index,0,bank_id] or [p2,...] without subcategories
        has_subcategories = prog.category and prog.category.sub_category is not None
        
        bank_id = bank.bank_id.upper() if bank.bank_id else ""
        if bank_id.startswith("U-"):
            # User bank offset
            bank_offset = pcg_id - 9
        else:
            # Internal bank
            bank_offset = pcg_id
        
        p_type = 3 if has_subcategories else 2
        patch_id = f"[p{p_type},{prog_index},0,{bank_offset}]"
        lines.append(f"{patch_id} {prog.id} {prog.name}")
