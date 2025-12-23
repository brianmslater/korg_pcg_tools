"""List generators for various reports.

Based on C# ListGenerator classes:
- ListGenerator.cs (base class)
- ListGeneratorPatchList.cs
- ListGeneratorProgramUsageList.cs
- ListGeneratorCombiContentList.cs
- ListGeneratorDifferencesList.cs
- ListGeneratorFileContentList.cs
"""

from typing import List, Optional, Dict, Any, TextIO, Set
from enum import Enum
import csv
import os
from .models import PcgFile, Program, Combi, Bank, SetList, SetListSlot
from .virtual_banks import (
    is_virtual_bank_id, 
    create_virtual_program_banks, 
    create_virtual_combi_banks,
    VirtualBank
)


class OutputFormat(Enum):
    """Output format options matching C# ListGenerator.OutputFormat."""
    TEXT = "text"
    CSV = "csv"
    ASCII_TABLE = "ascii_table"
    XML = "xml"


class SortMethod(Enum):
    """Sort method options matching C# ListGenerator.Sort."""
    TYPE_BANK_INDEX = "type_bank_index"
    ALPHABETICAL = "alphabetical"
    CATEGORICAL = "categorical"


class ListSubType(Enum):
    """List sub-type options matching C# ListGenerator.SubType."""
    COMPACT = "compact"  # Combi content list
    SHORT = "short"      # Combi content list
    LONG = "long"        # Combi content list
    INCLUDING_PATCH_NAME = "including_patch_name"  # Differences list
    EXCLUDING_PATCH_NAME = "excluding_patch_name"  # Differences list


class FilterOnFavorites(Enum):
    """Favorites filter options matching C# ListGenerator.FilterOnFavorites."""
    ALL = "all"
    NO = "no"
    YES = "yes"


class ListGenerator:
    """Generate various lists and reports from PCG files.
    
    Based on C# ListGenerator base class.
    """
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        
        # Output options
        self.output_format: OutputFormat = OutputFormat.TEXT
        self.sort_method: SortMethod = SortMethod.TYPE_BANK_INDEX
        
        # Optional columns
        self.optional_crc_including_name: bool = False
        self.optional_crc_excluding_name: bool = False
        self.optional_setlist_slot_reference_id: bool = True
        self.optional_setlist_slot_reference_name: bool = True
        
        # Filter options
        self.filter_on_text: bool = False
        self.filter_text: str = ""
        self.filter_case_sensitive: bool = False
        self.filter_on_favorites: FilterOnFavorites = FilterOnFavorites.ALL
        
        # Bank selection (None means all banks)
        self.selected_program_banks: Optional[List[str]] = None
        self.selected_combi_banks: Optional[List[str]] = None
        
        # Virtual banks support (based on C# ListGeneratorWindow.SetGeneratorProgramParameters)
        # When enabled, all virtual banks are added to selected banks
        self.include_virtual_program_banks: bool = False
        self.include_virtual_combi_banks: bool = False
        
        # Ignore options
        self.ignore_init_programs: bool = True
        self.ignore_init_combis: bool = True
        self.ignore_init_setlist_slots: bool = True
        self.ignore_first_program: bool = False
        self.ignore_muted_off_timbres: bool = True
        
        # Set list options
        self.setlists_enabled: bool = True
        self.setlists_range_from: int = 0
        self.setlists_range_to: int = 15
    
    def _is_init_patch(self, patch) -> bool:
        """Check if a patch is an init/empty patch."""
        if not patch.name:
            return True
        name_lower = patch.name.lower().strip()
        return name_lower in ('', 'init program', 'init combi', 'init', '---')
    
    def _matches_text_filter(self, name: str) -> bool:
        """Check if name matches text filter."""
        if not self.filter_on_text or not self.filter_text:
            return True
        if self.filter_case_sensitive:
            return self.filter_text in name
        return self.filter_text.lower() in name.lower()
    
    def _matches_favorite_filter(self, patch) -> bool:
        """Check if patch matches favorite filter."""
        if self.filter_on_favorites == FilterOnFavorites.ALL:
            return True
        is_favorite = getattr(patch, 'favorite', False)
        if self.filter_on_favorites == FilterOnFavorites.YES:
            return is_favorite
        return not is_favorite
    
    def _should_include_patch(self, patch, ignore_init: bool = True) -> bool:
        """Check if patch should be included in list."""
        if ignore_init and self._is_init_patch(patch):
            return False
        if not self._matches_text_filter(patch.name):
            return False
        if not self._matches_favorite_filter(patch):
            return False
        return True
    
    def _get_selected_program_banks(self) -> List[Bank]:
        """Get list of selected program banks.
        
        Based on C# ListGeneratorWindow.SetGeneratorProgramParameters().
        When include_virtual_program_banks is True, all virtual banks are included.
        """
        banks = []
        
        if self.selected_program_banks is None:
            # All banks selected
            banks = list(self.pcg.program_banks)
        else:
            # Only selected banks
            banks = [b for b in self.pcg.program_banks if b.bank_id in self.selected_program_banks]
        
        # Add virtual banks if enabled (per C# behavior)
        # Virtual banks are added when the "Virtual Banks" checkbox is checked
        if self.include_virtual_program_banks:
            # Virtual banks are not stored in PCG files, they're logical aggregations
            # For now, we include any banks that match virtual bank IDs
            for bank in self.pcg.program_banks:
                if is_virtual_bank_id(bank.bank_id) and bank not in banks:
                    banks.append(bank)
        
        return banks
    
    def _get_selected_combi_banks(self) -> List[Bank]:
        """Get list of selected combi banks.
        
        Based on C# ListGeneratorWindow.SetGeneratorCombiParameters().
        When include_virtual_combi_banks is True, all virtual banks are included.
        """
        banks = []
        
        if self.selected_combi_banks is None:
            # All banks selected
            banks = list(self.pcg.combi_banks)
        else:
            # Only selected banks
            banks = [b for b in self.pcg.combi_banks if b.bank_id in self.selected_combi_banks]
        
        # Add virtual banks if enabled (per C# behavior)
        if self.include_virtual_combi_banks:
            for bank in self.pcg.combi_banks:
                if is_virtual_bank_id(bank.bank_id) and bank not in banks:
                    banks.append(bank)
        
        return banks
    
    def _write_xsl_file(self, output_file: str, list_type: str, columns: List[str]):
        """Write XSL stylesheet for XML output.
        
        Based on C# WriteXslFile() methods.
        """
        xsl_file = os.path.splitext(output_file)[0] + '.xsl'
        
        with open(xsl_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0"?>\n')
            f.write('<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n\n')
            f.write('<xsl:template match="/">\n')
            f.write('  <html>\n')
            f.write('  <body>\n')
            f.write(f'    <h2>{list_type}</h2>\n')
            f.write('    <table border="1">\n')
            f.write('      <tr bgcolor="#80a0ff">\n')
            for col in columns:
                f.write(f'        <th>{col}</th>\n')
            f.write('      </tr>\n')
            f.write(f'      <xsl:for-each select="{list_type.lower().replace(" ", "_")}/item">\n')
            f.write('        <tr>\n')
            for col in columns:
                tag = col.lower().replace(' ', '_').replace('#', 'nr_')
                f.write(f'          <td><xsl:value-of select="{tag}"/></td>\n')
            f.write('        </tr>\n')
            f.write('      </xsl:for-each>\n')
            f.write('    </table>\n')
            f.write('  </body>\n')
            f.write('  </html>\n')
            f.write('</xsl:template>\n\n')
            f.write('</xsl:stylesheet>\n')

    # =========================================================================
    # Patch List Generator
    # Based on C# ListGeneratorPatchList.cs
    # =========================================================================
    
    def generate_patch_list(self, output_file: str, 
                           include_crc_incl_name: bool = False,
                           include_crc_excl_name: bool = False):
        """Generate patch list with optional CRC columns.
        
        Based on C# ListGeneratorPatchList.
        
        Args:
            output_file: Output file path
            include_crc_incl_name: Include CRC including name column
            include_crc_excl_name: Include CRC excluding name column
        """
        self.optional_crc_including_name = include_crc_incl_name
        self.optional_crc_excluding_name = include_crc_excl_name
        
        # Build patch list
        patches = []
        
        # Programs
        for bank in self._get_selected_program_banks():
            for program in bank.patches:
                if self._should_include_patch(program, self.ignore_init_programs):
                    patches.append(('Program', program))
        
        # Combis
        for bank in self._get_selected_combi_banks():
            for combi in bank.patches:
                if self._should_include_patch(combi, self.ignore_init_combis):
                    patches.append(('Combi', combi))
        
        # Set list slots
        if self.setlists_enabled and self.pcg.set_lists:
            for i, setlist in enumerate(self.pcg.set_lists):
                if self.setlists_range_from <= i <= self.setlists_range_to:
                    for slot in setlist.slots:
                        if self._should_include_patch(slot, self.ignore_init_setlist_slots):
                            patches.append(('SetListSlot', slot))
        
        # Sort
        if self.sort_method == SortMethod.ALPHABETICAL:
            patches.sort(key=lambda x: (x[1].name or '').lower())
        elif self.sort_method == SortMethod.CATEGORICAL:
            def get_category(patch):
                if hasattr(patch, 'category') and patch.category:
                    cat = getattr(patch.category, 'main_category', '')
                    return str(cat) if cat else ''
                return ''
            patches.sort(key=lambda x: (get_category(x[1]), (x[1].name or '').lower()))
        
        # Write output
        if self.output_format == OutputFormat.CSV:
            self._write_patch_list_csv(output_file, patches)
        elif self.output_format == OutputFormat.ASCII_TABLE:
            self._write_patch_list_ascii(output_file, patches)
        elif self.output_format == OutputFormat.XML:
            self._write_patch_list_xml(output_file, patches)
        else:
            self._write_patch_list_txt(output_file, patches)
    
    def _write_patch_list_csv(self, output_file: str, patches: List):
        """Write patch list to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Build header
            header = ['Type', 'ID', 'Name', 'Category']
            if self.optional_crc_including_name:
                header.append('CRC Inc')
            if self.optional_crc_excluding_name:
                header.append('CRC Exc')
            writer.writerow(header)
            
            for patch_type, patch in patches:
                category = ''
                if hasattr(patch, 'category') and patch.category:
                    category = patch.category.main_category
                row = [patch_type, patch.id, patch.name, category]
                if self.optional_crc_including_name:
                    row.append(patch.calc_crc(True) if hasattr(patch, 'calc_crc') else '')
                if self.optional_crc_excluding_name:
                    row.append(patch.calc_crc(False) if hasattr(patch, 'calc_crc') else '')
                writer.writerow(row)
    
    def _write_patch_list_txt(self, output_file: str, patches: List):
        """Write patch list to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PATCH LIST\n")
            f.write("=" * 80 + "\n\n")
            
            current_type = None
            for patch_type, patch in patches:
                if patch_type != current_type:
                    f.write(f"\n{patch_type}s:\n")
                    f.write("-" * 80 + "\n")
                    current_type = patch_type
                
                patch_id = patch.id if hasattr(patch, 'id') else str(patch)
                line = f"  {patch_id}: {patch.name}"
                if self.optional_crc_including_name and hasattr(patch, 'calc_crc'):
                    line += f"  CRC Inc: {patch.calc_crc(True):5d}"
                if self.optional_crc_excluding_name and hasattr(patch, 'calc_crc'):
                    line += f"  CRC Exc: {patch.calc_crc(False):5d}"
                f.write(line + "\n")
    
    def _write_patch_list_ascii(self, output_file: str, patches: List):
        """Write patch list to ASCII table format.
        
        Based on C# WriteAsciiTablePatch methods.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            # Build header line
            header_line = "+------------------------+------------+-----------+"
            header_text = "|Patch Name              |Patch Type  |Patch ID   |"
            
            if self.pcg.header and hasattr(self.pcg.header, 'model'):
                header_line += "----------------+"
                header_text += "Category        |"
            
            if self.optional_crc_including_name:
                header_line += "-------+"
                header_text += "CRC Inc|"
            if self.optional_crc_excluding_name:
                header_line += "-------+"
                header_text += "CRC Exc|"
            
            f.write(header_line + "\n")
            f.write(header_text + "\n")
            f.write(header_line + "\n")
            
            for patch_type, patch in patches:
                category = ''
                if hasattr(patch, 'category') and patch.category:
                    category = patch.category.main_category
                patch_id = patch.id if hasattr(patch, 'id') else str(patch)
                line = f"|{patch.name:<24}|{patch_type:<12}|{patch_id:<11}|"
                
                if self.pcg.header and hasattr(self.pcg.header, 'model'):
                    line += f"{category:<16}|"
                
                if self.optional_crc_including_name:
                    crc = patch.calc_crc(True) if hasattr(patch, 'calc_crc') else 0
                    line += f"{crc:6d} |"
                if self.optional_crc_excluding_name:
                    crc = patch.calc_crc(False) if hasattr(patch, 'calc_crc') else 0
                    line += f"{crc:6d} |"
                
                f.write(line + "\n")
            
            f.write(header_line + "\n")
    
    def _write_patch_list_xml(self, output_file: str, patches: List):
        """Write patch list to XML format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xsl_file = os.path.basename(os.path.splitext(output_file)[0] + '.xsl')
            f.write(f'<?xml-stylesheet type="text/xsl" href="{xsl_file}"?>\n')
            f.write('<patch_list xml:lang="en">\n')
            
            for patch_type, patch in patches:
                patch_id = patch.id if hasattr(patch, 'id') else str(patch)
                category = ''
                if hasattr(patch, 'category') and patch.category:
                    category = patch.category.main_category
                f.write('  <item>\n')
                f.write(f'    <type>{patch_type}</type>\n')
                f.write(f'    <id>{patch_id}</id>\n')
                f.write(f'    <name>{patch.name}</name>\n')
                f.write(f'    <category>{category}</category>\n')
                if self.optional_crc_including_name and hasattr(patch, 'calc_crc'):
                    f.write(f'    <crc_inc>{patch.calc_crc(True)}</crc_inc>\n')
                if self.optional_crc_excluding_name and hasattr(patch, 'calc_crc'):
                    f.write(f'    <crc_exc>{patch.calc_crc(False)}</crc_exc>\n')
                f.write('  </item>\n')
            
            f.write('</patch_list>\n')
        
        # Write XSL file
        columns = ['Type', 'ID', 'Name', 'Category']
        if self.optional_crc_including_name:
            columns.append('CRC Inc')
        if self.optional_crc_excluding_name:
            columns.append('CRC Exc')
        self._write_xsl_file(output_file, 'Patch List', columns)

    # =========================================================================
    # Program Usage List Generator
    # Based on C# ListGeneratorProgramUsageList.cs
    # =========================================================================

    def generate_program_usage_list(self, output_file: str):
        """Generate program usage list showing which combis use each program.
        
        Based on C# ListGeneratorProgramUsageList.
        """
        # Build usage map: program_id -> list of (combi_id, timbre_index)
        usage_map: Dict[str, List[tuple]] = {}
        
        for bank in self._get_selected_combi_banks():
            for combi in bank.patches:
                if self.ignore_init_combis and self._is_init_patch(combi):
                    continue
                for i, timbre in enumerate(combi.timbres):
                    if self.ignore_muted_off_timbres:
                        status = getattr(timbre, 'status', 'INT')
                        if status in ('OFF', 'Mute'):
                            continue
                    if self.ignore_first_program and i == 0:
                        continue
                    prog_id = timbre.program_id
                    if prog_id not in usage_map:
                        usage_map[prog_id] = []
                    usage_map[prog_id].append((combi.id, i + 1))
        
        # Also check set list slots
        if self.setlists_enabled and self.pcg.set_lists:
            for i, setlist in enumerate(self.pcg.set_lists):
                if self.setlists_range_from <= i <= self.setlists_range_to:
                    for slot in setlist.slots:
                        if self.ignore_init_setlist_slots and self._is_init_patch(slot):
                            continue
                        ref_type = getattr(slot, 'reference_type', 'Program')
                        if ref_type == 'Program':
                            prog_id = getattr(slot, 'program_id', None)
                            if prog_id:
                                if prog_id not in usage_map:
                                    usage_map[prog_id] = []
                                usage_map[prog_id].append((f"SL{i+1}:{slot.index}", 0))
        
        # Write output
        if self.output_format == OutputFormat.CSV:
            self._write_program_usage_csv(output_file, usage_map)
        elif self.output_format == OutputFormat.ASCII_TABLE:
            self._write_program_usage_ascii(output_file, usage_map)
        elif self.output_format == OutputFormat.XML:
            self._write_program_usage_xml(output_file, usage_map)
        else:
            self._write_program_usage_txt(output_file, usage_map)
    
    def _write_program_usage_csv(self, output_file: str, usage_map: dict):
        """Write program usage to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Program ID', 'Program Name', 'Usage Count', 'Used By'])
            
            for bank in self._get_selected_program_banks():
                for program in bank.patches:
                    if self.ignore_init_programs and self._is_init_patch(program):
                        continue
                    prog_id = program.id
                    usage = usage_map.get(prog_id, [])
                    used_by = ', '.join(f"{u[0]}" for u in usage) if usage else 'Not used'
                    writer.writerow([prog_id, program.name, len(usage), used_by])
    
    def _write_program_usage_txt(self, output_file: str, usage_map: dict):
        """Write program usage to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PROGRAM USAGE LIST\n")
            f.write("=" * 80 + "\n\n")
            
            for bank in self._get_selected_program_banks():
                f.write(f"\nBank {bank.bank_id}:\n")
                f.write("-" * 80 + "\n")
                
                for program in bank.patches:
                    if self.ignore_init_programs and self._is_init_patch(program):
                        continue
                    prog_id = program.id
                    usage = usage_map.get(prog_id, [])
                    f.write(f"{prog_id}: {program.name}\n")
                    if usage:
                        f.write(f"  Used by: {', '.join(f'{u[0]}' for u in usage)}\n")
                    else:
                        f.write(f"  Not used\n")
    
    def _write_program_usage_ascii(self, output_file: str, usage_map: dict):
        """Write program usage to ASCII table."""
        lines = []
        lines.append("+-----------+------------------------+-------+----------------------------------------+")
        lines.append("|Program ID |Program Name            | Count |Used By                                 |")
        lines.append("+-----------+------------------------+-------+----------------------------------------+")
        
        for bank in self._get_selected_program_banks():
            for program in bank.patches:
                if self.ignore_init_programs and self._is_init_patch(program):
                    continue
                prog_id = program.id
                usage = usage_map.get(prog_id, [])
                used_by = ', '.join(f"{u[0]}" for u in usage)[:40] if usage else 'Not used'
                lines.append(f"|{prog_id:<11}|{program.name:<24}|{len(usage):5}  |{used_by:<40}|")
        
        lines.append("+-----------+------------------------+-------+----------------------------------------+")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
    
    def _write_program_usage_xml(self, output_file: str, usage_map: dict):
        """Write program usage to XML."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xsl_file = os.path.basename(os.path.splitext(output_file)[0] + '.xsl')
            f.write(f'<?xml-stylesheet type="text/xsl" href="{xsl_file}"?>\n')
            f.write('<program_usage_list xml:lang="en">\n')
            
            for bank in self._get_selected_program_banks():
                for program in bank.patches:
                    if self.ignore_init_programs and self._is_init_patch(program):
                        continue
                    prog_id = program.id
                    usage = usage_map.get(prog_id, [])
                    f.write('  <item>\n')
                    f.write(f'    <program_id>{prog_id}</program_id>\n')
                    f.write(f'    <program_name>{program.name}</program_name>\n')
                    f.write(f'    <usage_count>{len(usage)}</usage_count>\n')
                    used_by = ', '.join(f"{u[0]}" for u in usage) if usage else 'Not used'
                    f.write(f'    <used_by>{used_by}</used_by>\n')
                    f.write('  </item>\n')
            
            f.write('</program_usage_list>\n')
        
        self._write_xsl_file(output_file, 'Program Usage List', 
                            ['Program ID', 'Program Name', 'Usage Count', 'Used By'])

    # =========================================================================
    # Combi Content List Generator
    # Based on C# ListGeneratorCombiContentList.cs
    # =========================================================================
    
    def generate_combi_content_list(self, output_file: str, style: str = 'short'):
        """Generate combi content list showing what's in each combi.
        
        Based on C# ListGeneratorCombiContentList.
        
        Args:
            output_file: Output file path
            style: 'compact', 'short', or 'long'
        """
        if self.output_format == OutputFormat.CSV:
            self._write_combi_content_csv(output_file, style)
        elif self.output_format == OutputFormat.ASCII_TABLE:
            self._write_combi_content_ascii(output_file, style)
        elif self.output_format == OutputFormat.XML:
            self._write_combi_content_xml(output_file, style)
        else:
            self._write_combi_content_txt(output_file, style)
    
    def _write_combi_content_csv(self, output_file: str, style: str):
        """Write combi content to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if style == 'compact':
                writer.writerow(['Combi ID', 'Combi Name', 'Programs'])
                for bank in self._get_selected_combi_banks():
                    for combi in bank.patches:
                        if self.ignore_init_combis and self._is_init_patch(combi):
                            continue
                        programs = self._get_combi_programs(combi)
                        writer.writerow([combi.id, combi.name, ' '.join(programs)])
            
            elif style == 'short':
                writer.writerow(['Combi ID', 'Combi Name', 'Timbre Count', 'Programs Used'])
                for bank in self._get_selected_combi_banks():
                    for combi in bank.patches:
                        if self.ignore_init_combis and self._is_init_patch(combi):
                            continue
                        programs = self._get_combi_programs(combi)
                        writer.writerow([
                            combi.id, combi.name, len(programs),
                            ', '.join(programs) if programs else 'None'
                        ])
            
            else:  # long
                writer.writerow(['Combi ID', 'Combi Name', 'Timbre #', 'Program', 
                               'Status', 'Volume', 'Pan', 'Channel'])
                for bank in self._get_selected_combi_banks():
                    for combi in bank.patches:
                        if self.ignore_init_combis and self._is_init_patch(combi):
                            continue
                        for i, timbre in enumerate(combi.timbres, 1):
                            if self.ignore_muted_off_timbres:
                                status = getattr(timbre, 'status', 'INT')
                                if status in ('OFF', 'Mute'):
                                    continue
                            writer.writerow([
                                combi.id, combi.name, i, timbre.program_id,
                                getattr(timbre, 'status', ''),
                                getattr(timbre, 'volume', ''),
                                getattr(timbre, 'pan', ''),
                                getattr(timbre, 'midi_channel', '')
                            ])
    
    def _get_combi_programs(self, combi) -> List[str]:
        """Get list of program IDs used in combi."""
        programs = []
        for timbre in combi.timbres:
            if self.ignore_muted_off_timbres:
                status = getattr(timbre, 'status', 'INT')
                if status in ('OFF', 'Mute'):
                    continue
            prog_id = timbre.program_id
            if prog_id and prog_id not in programs:
                programs.append(prog_id)
        return programs
    
    def _write_combi_content_txt(self, output_file: str, style: str):
        """Write combi content to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("COMBI CONTENT LIST\n")
            f.write("=" * 80 + "\n\n")
            
            for bank in self._get_selected_combi_banks():
                f.write(f"\nBank {bank.bank_id}:\n")
                f.write("-" * 80 + "\n")
                
                for combi in bank.patches:
                    if self.ignore_init_combis and self._is_init_patch(combi):
                        continue
                    f.write(f"\n{combi.id}: {combi.name}\n")
                    
                    if style == 'compact':
                        programs = self._get_combi_programs(combi)
                        f.write(f"  Programs: {' '.join(programs) if programs else 'None'}\n")
                    elif style == 'short':
                        programs = self._get_combi_programs(combi)
                        f.write(f"  Timbres: {len(programs)}\n")
                        f.write(f"  Programs: {', '.join(programs) if programs else 'None'}\n")
                    else:  # long
                        for i, timbre in enumerate(combi.timbres, 1):
                            if self.ignore_muted_off_timbres:
                                status = getattr(timbre, 'status', 'INT')
                                if status in ('OFF', 'Mute'):
                                    continue
                            f.write(f"  Timbre {i}: {timbre.program_id} "
                                  f"(Status: {getattr(timbre, 'status', '')}, "
                                  f"Vol: {getattr(timbre, 'volume', '')}, "
                                  f"Pan: {getattr(timbre, 'pan', '')})\n")
    
    def _write_combi_content_ascii(self, output_file: str, style: str):
        """Write combi content to ASCII table."""
        lines = []
        
        if style in ('compact', 'short'):
            lines.append("+-----------+------------------------+-------+----------------------------------------+")
            lines.append("|Combi ID   |Combi Name              |Timbres|Programs                                |")
            lines.append("+-----------+------------------------+-------+----------------------------------------+")
            
            for bank in self._get_selected_combi_banks():
                for combi in bank.patches:
                    if self.ignore_init_combis and self._is_init_patch(combi):
                        continue
                    programs = self._get_combi_programs(combi)
                    prog_str = ', '.join(programs)[:40] if programs else 'None'
                    lines.append(f"|{combi.id:<11}|{combi.name:<24}|{len(programs):5}  |{prog_str:<40}|")
            
            lines.append("+-----------+------------------------+-------+----------------------------------------+")
        else:  # long
            lines.append("+-----------+------------------------+---+-----------+------+-----+-----+----+")
            lines.append("|Combi ID   |Combi Name              |T# |Program    |Status| Vol | Pan | Ch |")
            lines.append("+-----------+------------------------+---+-----------+------+-----+-----+----+")
            
            for bank in self._get_selected_combi_banks():
                for combi in bank.patches:
                    if self.ignore_init_combis and self._is_init_patch(combi):
                        continue
                    for i, timbre in enumerate(combi.timbres, 1):
                        if self.ignore_muted_off_timbres:
                            status = getattr(timbre, 'status', 'INT')
                            if status in ('OFF', 'Mute'):
                                continue
                        lines.append(
                            f"|{combi.id:<11}|{combi.name:<24}|{i:2} |{timbre.program_id:<11}|"
                            f"{getattr(timbre, 'status', ''):<6}|{getattr(timbre, 'volume', ''):4} |"
                            f"{getattr(timbre, 'pan', ''):4} |{getattr(timbre, 'midi_channel', ''):3} |"
                        )
            
            lines.append("+-----------+------------------------+---+-----------+------+-----+-----+----+")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
    
    def _write_combi_content_xml(self, output_file: str, style: str):
        """Write combi content to XML."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xsl_file = os.path.basename(os.path.splitext(output_file)[0] + '.xsl')
            f.write(f'<?xml-stylesheet type="text/xsl" href="{xsl_file}"?>\n')
            f.write('<combi_content_list xml:lang="en">\n')
            
            for bank in self._get_selected_combi_banks():
                for combi in bank.patches:
                    if self.ignore_init_combis and self._is_init_patch(combi):
                        continue
                    f.write('  <item>\n')
                    f.write(f'    <combi_id>{combi.id}</combi_id>\n')
                    f.write(f'    <combi_name>{combi.name}</combi_name>\n')
                    
                    if style in ('compact', 'short'):
                        programs = self._get_combi_programs(combi)
                        f.write(f'    <timbre_count>{len(programs)}</timbre_count>\n')
                        f.write(f'    <programs>{", ".join(programs)}</programs>\n')
                    else:  # long
                        f.write('    <timbres>\n')
                        for i, timbre in enumerate(combi.timbres, 1):
                            if self.ignore_muted_off_timbres:
                                status = getattr(timbre, 'status', 'INT')
                                if status in ('OFF', 'Mute'):
                                    continue
                            f.write('      <timbre>\n')
                            f.write(f'        <number>{i}</number>\n')
                            f.write(f'        <program>{timbre.program_id}</program>\n')
                            f.write(f'        <status>{getattr(timbre, "status", "")}</status>\n')
                            f.write(f'        <volume>{getattr(timbre, "volume", "")}</volume>\n')
                            f.write(f'        <pan>{getattr(timbre, "pan", "")}</pan>\n')
                            f.write('      </timbre>\n')
                        f.write('    </timbres>\n')
                    
                    f.write('  </item>\n')
            
            f.write('</combi_content_list>\n')
        
        if style in ('compact', 'short'):
            self._write_xsl_file(output_file, 'Combi Content List',
                                ['Combi ID', 'Combi Name', 'Timbre Count', 'Programs'])


    # =========================================================================
    # Differences List Generator
    # Based on C# ListGeneratorDifferencesList.cs
    # =========================================================================
    
    def generate_differences_list(self, other_pcg: PcgFile, output_file: str,
                                  max_differences: int = 500,
                                  ignore_patch_names: bool = True,
                                  ignore_setlist_descriptions: bool = True,
                                  search_both_directions: bool = False):
        """Generate differences list comparing two PCG files.
        
        Based on C# ListGeneratorDifferencesList.
        
        Args:
            other_pcg: Second PCG file to compare
            output_file: Output file path
            max_differences: Maximum number of differences to report
            ignore_patch_names: Don't report name-only differences
            ignore_setlist_descriptions: Don't report description-only differences
            search_both_directions: Also find items in other_pcg not in self.pcg
        """
        differences = []
        
        # Compare programs
        for bank in self._get_selected_program_banks():
            for program in bank.patches:
                if self.ignore_init_programs and self._is_init_patch(program):
                    continue
                other_prog = other_pcg.find_program(program.bank, program.index)
                if other_prog:
                    if not ignore_patch_names and program.name != other_prog.name:
                        differences.append({
                            'type': 'Program',
                            'id': program.id,
                            'name1': program.name,
                            'name2': other_prog.name,
                            'status': 'Name Different'
                        })
                    # Compare CRC to detect content differences
                    elif hasattr(program, 'calc_crc') and hasattr(other_prog, 'calc_crc'):
                        if program.calc_crc(False) != other_prog.calc_crc(False):
                            differences.append({
                                'type': 'Program',
                                'id': program.id,
                                'name1': program.name,
                                'name2': other_prog.name,
                                'status': 'Content Different'
                            })
                else:
                    differences.append({
                        'type': 'Program',
                        'id': program.id,
                        'name1': program.name,
                        'name2': '',
                        'status': 'Only in File 1'
                    })
                
                if len(differences) >= max_differences:
                    break
            if len(differences) >= max_differences:
                break
        
        # Compare combis
        if len(differences) < max_differences:
            for bank in self._get_selected_combi_banks():
                for combi in bank.patches:
                    if self.ignore_init_combis and self._is_init_patch(combi):
                        continue
                    other_combi = other_pcg.find_combi(combi.bank, combi.index)
                    if other_combi:
                        if not ignore_patch_names and combi.name != other_combi.name:
                            differences.append({
                                'type': 'Combi',
                                'id': combi.id,
                                'name1': combi.name,
                                'name2': other_combi.name,
                                'status': 'Name Different'
                            })
                        elif hasattr(combi, 'calc_crc') and hasattr(other_combi, 'calc_crc'):
                            if combi.calc_crc(False) != other_combi.calc_crc(False):
                                differences.append({
                                    'type': 'Combi',
                                    'id': combi.id,
                                    'name1': combi.name,
                                    'name2': other_combi.name,
                                    'status': 'Content Different'
                                })
                    else:
                        differences.append({
                            'type': 'Combi',
                            'id': combi.id,
                            'name1': combi.name,
                            'name2': '',
                            'status': 'Only in File 1'
                        })
                    
                    if len(differences) >= max_differences:
                        break
                if len(differences) >= max_differences:
                    break
        
        # Search other direction if requested
        if search_both_directions and len(differences) < max_differences:
            # Find programs in other_pcg not in self.pcg
            for bank in other_pcg.program_banks:
                for program in bank.patches:
                    if self._is_init_patch(program):
                        continue
                    my_prog = self.pcg.find_program(program.bank, program.index)
                    if not my_prog or self._is_init_patch(my_prog):
                        differences.append({
                            'type': 'Program',
                            'id': program.id,
                            'name1': '',
                            'name2': program.name,
                            'status': 'Only in File 2'
                        })
                    if len(differences) >= max_differences:
                        break
                if len(differences) >= max_differences:
                    break
        
        # Write output
        if self.output_format == OutputFormat.CSV:
            self._write_differences_csv(output_file, differences)
        elif self.output_format == OutputFormat.ASCII_TABLE:
            self._write_differences_ascii(output_file, differences)
        elif self.output_format == OutputFormat.XML:
            self._write_differences_xml(output_file, differences)
        else:
            self._write_differences_txt(output_file, differences)
    
    def _write_differences_csv(self, output_file: str, differences: List[dict]):
        """Write differences to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'ID', 'File 1 Name', 'File 2 Name', 'Status'])
            for diff in differences:
                writer.writerow([
                    diff['type'], diff['id'], diff['name1'], 
                    diff['name2'], diff['status']
                ])
    
    def _write_differences_txt(self, output_file: str, differences: List[dict]):
        """Write differences to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("DIFFERENCES LIST\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total differences found: {len(differences)}\n\n")
            
            current_type = None
            for diff in differences:
                if diff['type'] != current_type:
                    f.write(f"\n{diff['type']}s:\n")
                    f.write("-" * 80 + "\n")
                    current_type = diff['type']
                
                if diff['status'] == 'Only in File 1':
                    f.write(f"{diff['id']}: '{diff['name1']}' (only in file 1)\n")
                elif diff['status'] == 'Only in File 2':
                    f.write(f"{diff['id']}: '{diff['name2']}' (only in file 2)\n")
                else:
                    f.write(f"{diff['id']}: '{diff['name1']}' vs '{diff['name2']}' ({diff['status']})\n")
    
    def _write_differences_ascii(self, output_file: str, differences: List[dict]):
        """Write differences to ASCII table."""
        lines = []
        lines.append("+------------+-----------+------------------------+------------------------+------------------+")
        lines.append("|Type        |ID         |File 1 Name             |File 2 Name             |Status            |")
        lines.append("+------------+-----------+------------------------+------------------------+------------------+")
        
        for diff in differences:
            lines.append(
                f"|{diff['type']:<12}|{diff['id']:<11}|{diff['name1']:<24}|"
                f"{diff['name2']:<24}|{diff['status']:<18}|"
            )
        
        lines.append("+------------+-----------+------------------------+------------------------+------------------+")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
    
    def _write_differences_xml(self, output_file: str, differences: List[dict]):
        """Write differences to XML."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xsl_file = os.path.basename(os.path.splitext(output_file)[0] + '.xsl')
            f.write(f'<?xml-stylesheet type="text/xsl" href="{xsl_file}"?>\n')
            f.write('<differences_list xml:lang="en">\n')
            
            for diff in differences:
                f.write('  <item>\n')
                f.write(f'    <type>{diff["type"]}</type>\n')
                f.write(f'    <id>{diff["id"]}</id>\n')
                f.write(f'    <file1_name>{diff["name1"]}</file1_name>\n')
                f.write(f'    <file2_name>{diff["name2"]}</file2_name>\n')
                f.write(f'    <status>{diff["status"]}</status>\n')
                f.write('  </item>\n')
            
            f.write('</differences_list>\n')
        
        self._write_xsl_file(output_file, 'Differences List',
                            ['Type', 'ID', 'File 1 Name', 'File 2 Name', 'Status'])

    # =========================================================================
    # File Content List Generator
    # Based on C# ListGeneratorFileContentList.cs
    # =========================================================================
    
    def generate_file_content_list(self, output_file: str):
        """Generate file content summary showing bank usage.
        
        Based on C# ListGeneratorFileContentList.
        Shows bank type, content type, bank ID, writable/filled/empty counts.
        """
        # Build bank list
        banks = []
        
        # Program banks
        for bank in self.pcg.program_banks:
            if not bank.is_writable if hasattr(bank, 'is_writable') else True:
                continue
            filled = sum(1 for p in bank.patches if not self._is_init_patch(p))
            total = len(bank.patches)
            
            # Determine synthesis type if available
            synth_type = getattr(bank, 'synthesis_type', 'HD-1')
            content_type = f"{synth_type} Programs"
            
            # Get filled patch IDs
            filled_ids = [p.id for p in bank.patches if not self._is_init_patch(p)]
            
            banks.append({
                'bank_type': 'ProgramBank',
                'content_type': content_type,
                'bank_id': bank.bank_id,
                'writable': total,
                'filled': filled,
                'empty': total - filled,
                'patch_ids': self._compress_patch_ids(filled_ids)
            })
        
        # Combi banks
        for bank in self.pcg.combi_banks:
            filled = sum(1 for c in bank.patches if not self._is_init_patch(c))
            total = len(bank.patches)
            filled_ids = [c.id for c in bank.patches if not self._is_init_patch(c)]
            
            banks.append({
                'bank_type': 'CombiBank',
                'content_type': 'Combis',
                'bank_id': bank.bank_id,
                'writable': total,
                'filled': filled,
                'empty': total - filled,
                'patch_ids': self._compress_patch_ids(filled_ids)
            })
        
        # Set lists
        if self.pcg.set_lists:
            for i, setlist in enumerate(self.pcg.set_lists):
                filled = sum(1 for s in setlist.slots if not self._is_init_patch(s))
                total = len(setlist.slots)
                if filled > 0:  # Only include non-empty set lists
                    filled_ids = [f"SL{i+1}:{s.slot_index}" for s in setlist.slots if not self._is_init_patch(s)]
                    banks.append({
                        'bank_type': 'SetList',
                        'content_type': 'SetListSlots',
                        'bank_id': str(i + 1),
                        'writable': total,
                        'filled': filled,
                        'empty': total - filled,
                        'patch_ids': self._compress_patch_ids(filled_ids)
                    })
        
        # Write output
        if self.output_format == OutputFormat.CSV:
            self._write_file_content_csv(output_file, banks)
        elif self.output_format == OutputFormat.ASCII_TABLE:
            self._write_file_content_ascii(output_file, banks)
        elif self.output_format == OutputFormat.XML:
            self._write_file_content_xml(output_file, banks)
        else:
            self._write_file_content_txt(output_file, banks)
    
    def _compress_patch_ids(self, ids: List[str]) -> str:
        """Compress patch IDs into ranges where possible.
        
        Based on C# Util.GetPatchIdsString().
        Example: ['I-A000', 'I-A001', 'I-A002', 'I-A005'] -> 'I-A000~I-A002, I-A005'
        
        The algorithm groups consecutive patches and uses ~ for ranges.
        """
        if not ids:
            return ''
        
        result_parts = []
        range_start = None
        range_end = None
        prev_bank = None
        prev_index = -2
        
        def extract_bank_index(patch_id: str):
            """Extract bank prefix and numeric index from patch ID."""
            # Handle formats like 'I-A000', 'U-GG127', 'SL1:5'
            if ':' in patch_id:  # SetList slot format
                return patch_id, -1  # Don't compress setlist slots
            
            # Find where the number starts
            for i in range(len(patch_id) - 1, -1, -1):
                if not patch_id[i].isdigit():
                    bank = patch_id[:i+1]
                    try:
                        index = int(patch_id[i+1:])
                    except ValueError:
                        return patch_id, -1
                    return bank, index
            return patch_id, -1
        
        def flush_range():
            """Add current range to result."""
            nonlocal range_start, range_end
            if range_start is None:
                return
            if range_start != range_end:
                result_parts.append(f"{range_start}~{range_end}")
            else:
                result_parts.append(range_start)
        
        for patch_id in ids:
            bank, index = extract_bank_index(patch_id)
            
            if range_start is None:
                # First patch - start a new range
                range_start = patch_id
                range_end = patch_id
                prev_bank = bank
                prev_index = index
            elif bank != prev_bank or index < 0 or prev_index < 0:
                # Different bank or non-numeric - flush and start new
                flush_range()
                range_start = patch_id
                range_end = patch_id
                prev_bank = bank
                prev_index = index
            elif index == prev_index + 1:
                # Consecutive - extend range
                range_end = patch_id
                prev_index = index
            else:
                # Gap - flush and start new
                flush_range()
                range_start = patch_id
                range_end = patch_id
                prev_index = index
        
        # Flush final range
        flush_range()
        
        return ', '.join(result_parts)
    
    def _write_file_content_csv(self, output_file: str, banks: List[dict]):
        """Write file content to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Bank Type', 'Content Type', 'Bank ID', 
                           '# Writable', '# Filled', '# Empty', 'Patch IDs'])
            for bank in banks:
                writer.writerow([
                    bank['bank_type'], bank['content_type'], bank['bank_id'],
                    bank['writable'], bank['filled'], bank['empty'],
                    bank['patch_ids'].replace(',', ' ')  # Avoid CSV issues
                ])
    
    def _write_file_content_txt(self, output_file: str, banks: List[dict]):
        """Write file content to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("FILE CONTENT SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            if self.pcg.header:
                f.write(f"Model: {self.pcg.header.model.value if hasattr(self.pcg.header.model, 'value') else self.pcg.header.model}\n")
                f.write(f"Version: {self.pcg.header.major_version}.{self.pcg.header.minor_version}\n\n")
            
            for bank in banks:
                f.write(f"{bank['bank_type']} {bank['content_type']} {bank['bank_id']}: "
                       f"{bank['writable']}/{bank['filled']}/{bank['empty']}: "
                       f"{bank['patch_ids']}\n")
    
    def _write_file_content_ascii(self, output_file: str, banks: List[dict]):
        """Write file content to ASCII table.
        
        Based on C# WriteToFile() in ListGeneratorFileContentList.
        Uses dynamic right border based on longest line (matching C# CreateVerticalRightLine).
        """
        lines = []
        
        # Build header without right border initially (C# style)
        lines.append("+-----------+-----------------------+-------+----------+--------+-------+")
        lines.append("|Bank Type  |Content Type           |Bank ID|# Writable|# Filled|# Empty|Patch IDs of filled patches")
        lines.append("+-----------+-----------------------+-------+----------+--------+-------+")
        
        for bank in banks:
            lines.append(
                f"|{bank['bank_type']:<11}|{bank['content_type']:<23}| {bank['bank_id']:<6}|"
                f"{bank['writable']:5}     |{bank['filled']:5}   |{bank['empty']:5}  |{bank['patch_ids']}"
            )
        
        lines.append("+-----------+-----------------------+-------+----------+--------+-------+")
        
        # Create vertical right line (C# CreateVerticalRightLine)
        max_length = max(len(line) for line in lines) + 1  # +1 for right line |
        
        # Update header lines
        lines[0] = lines[0] + '-' * (max_length - len(lines[0])) + '+'
        lines[1] = lines[1] + ' ' * (max_length - len(lines[1])) + '|'
        lines[2] = lines[2] + '-' * (max_length - len(lines[2])) + '+'
        
        # Update data lines
        for i in range(3, len(lines) - 1):
            lines[i] = lines[i] + ' ' * (max_length - len(lines[i])) + '|'
        
        # Update footer line
        lines[-1] = lines[-1] + '-' * (max_length - len(lines[-1])) + '+'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
    
    def _write_file_content_xml(self, output_file: str, banks: List[dict]):
        """Write file content to XML."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xsl_file = os.path.basename(os.path.splitext(output_file)[0] + '.xsl')
            f.write(f'<?xml-stylesheet type="text/xsl" href="{xsl_file}"?>\n')
            f.write('<file_content_list xml:lang="en">\n')
            
            for bank in banks:
                f.write('  <bank>\n')
                f.write(f'    <type>{bank["bank_type"]}</type>\n')
                f.write(f'    <content_type>{bank["content_type"]}</content_type>\n')
                f.write(f'    <id>{bank["bank_id"]}</id>\n')
                f.write(f'    <nr_writable_patches>{bank["writable"]}</nr_writable_patches>\n')
                f.write(f'    <nr_filled_patches>{bank["filled"]}</nr_filled_patches>\n')
                f.write(f'    <nr_empty_patches>{bank["empty"]}</nr_empty_patches>\n')
                f.write(f'    <patch_ids>{bank["patch_ids"]}</patch_ids>\n')
                f.write('  </bank>\n')
            
            f.write('</file_content_list>\n')
        
        self._write_xsl_file(output_file, 'File Content List',
                            ['Bank Type', 'Content Type', 'Bank ID', 
                             '# Writable', '# Filled', '# Empty', 'Patch IDs'])
