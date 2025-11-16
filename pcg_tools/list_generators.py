"""List generators for various reports."""

from typing import List, TextIO
import csv
from .models import PcgFile, Program, Combi


class ListGenerator:
    """Generate various lists and reports from PCG files."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
    
    def generate_program_usage_list(self, output_file: str, format: str = 'csv'):
        """Generate program usage list showing which combis use each program."""
        usage_map = {}
        
        # Count usage
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                for timbre in combi.timbres:
                    prog_id = timbre.program_id
                    if prog_id not in usage_map:
                        usage_map[prog_id] = []
                    usage_map[prog_id].append(combi.id)
        
        # Write output
        if format == 'csv':
            self._write_program_usage_csv(output_file, usage_map)
        else:
            self._write_program_usage_txt(output_file, usage_map)
    
    def _write_program_usage_csv(self, output_file: str, usage_map: dict):
        """Write program usage to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Program ID', 'Program Name', 'Usage Count', 'Used By'])
            
            for bank in self.pcg.program_banks:
                for program in bank.patches:
                    prog_id = program.id
                    usage = usage_map.get(prog_id, [])
                    used_by = ', '.join(usage) if usage else 'Not used'
                    writer.writerow([prog_id, program.name, len(usage), used_by])
    
    def _write_program_usage_txt(self, output_file: str, usage_map: dict):
        """Write program usage to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PROGRAM USAGE LIST\n")
            f.write("=" * 80 + "\n\n")
            
            for bank in self.pcg.program_banks:
                f.write(f"\nBank {bank.bank_id}:\n")
                f.write("-" * 80 + "\n")
                
                for program in bank.patches:
                    prog_id = program.id
                    usage = usage_map.get(prog_id, [])
                    f.write(f"{prog_id}: {program.name}\n")
                    if usage:
                        f.write(f"  Used by: {', '.join(usage)}\n")
                    else:
                        f.write(f"  Not used\n")
    
    def generate_combi_content_list(self, output_file: str, format: str = 'csv', style: str = 'short'):
        """Generate combi content list showing what's in each combi."""
        if format == 'csv':
            self._write_combi_content_csv(output_file, style)
        else:
            self._write_combi_content_txt(output_file, style)
    
    def _write_combi_content_csv(self, output_file: str, style: str):
        """Write combi content to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if style == 'short':
                writer.writerow(['Combi ID', 'Combi Name', 'Timbre Count', 'Programs Used'])
                
                for bank in self.pcg.combi_banks:
                    for combi in bank.patches:
                        programs = [t.program_id for t in combi.timbres]
                        writer.writerow([
                            combi.id,
                            combi.name,
                            len(combi.timbres),
                            ', '.join(programs) if programs else 'None'
                        ])
            else:
                # Long format with timbre details
                writer.writerow(['Combi ID', 'Combi Name', 'Timbre #', 'Program', 'Status', 'Volume', 'Pan'])
                
                for bank in self.pcg.combi_banks:
                    for combi in bank.patches:
                        for i, timbre in enumerate(combi.timbres, 1):
                            writer.writerow([
                                combi.id,
                                combi.name,
                                i,
                                timbre.program_id,
                                timbre.status,
                                timbre.volume,
                                timbre.pan
                            ])
    
    def _write_combi_content_txt(self, output_file: str, style: str):
        """Write combi content to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("COMBI CONTENT LIST\n")
            f.write("=" * 80 + "\n\n")
            
            for bank in self.pcg.combi_banks:
                f.write(f"\nBank {bank.bank_id}:\n")
                f.write("-" * 80 + "\n")
                
                for combi in bank.patches:
                    f.write(f"\n{combi.id}: {combi.name}\n")
                    
                    if style == 'short':
                        programs = [t.program_id for t in combi.timbres]
                        f.write(f"  Timbres: {len(combi.timbres)}\n")
                        f.write(f"  Programs: {', '.join(programs) if programs else 'None'}\n")
                    else:
                        # Long format
                        for i, timbre in enumerate(combi.timbres, 1):
                            f.write(f"  Timbre {i}: {timbre.program_id} "
                                  f"(Status: {timbre.status}, Vol: {timbre.volume}, Pan: {timbre.pan})\n")
    
    def generate_differences_list(self, other_pcg: PcgFile, output_file: str, format: str = 'csv'):
        """Generate differences list comparing two PCG files."""
        if format == 'csv':
            self._write_differences_csv(other_pcg, output_file)
        else:
            self._write_differences_txt(other_pcg, output_file)
    
    def _write_differences_csv(self, other_pcg: PcgFile, output_file: str):
        """Write differences to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'ID', 'File 1 Name', 'File 2 Name', 'Status'])
            
            # Compare programs
            for bank in self.pcg.program_banks:
                for program in bank.patches:
                    other_prog = other_pcg.find_program(program.bank, program.index)
                    if other_prog:
                        if program.name != other_prog.name:
                            writer.writerow(['Program', program.id, program.name, other_prog.name, 'Different'])
                    else:
                        writer.writerow(['Program', program.id, program.name, '', 'Only in File 1'])
            
            # Compare combis
            for bank in self.pcg.combi_banks:
                for combi in bank.patches:
                    other_combi = other_pcg.find_combi(combi.bank, combi.index)
                    if other_combi:
                        if combi.name != other_combi.name:
                            writer.writerow(['Combi', combi.id, combi.name, other_combi.name, 'Different'])
                    else:
                        writer.writerow(['Combi', combi.id, combi.name, '', 'Only in File 1'])
    
    def _write_differences_txt(self, other_pcg: PcgFile, output_file: str):
        """Write differences to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("DIFFERENCES LIST\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("Programs:\n")
            f.write("-" * 80 + "\n")
            
            for bank in self.pcg.program_banks:
                for program in bank.patches:
                    other_prog = other_pcg.find_program(program.bank, program.index)
                    if other_prog:
                        if program.name != other_prog.name:
                            f.write(f"{program.id}: '{program.name}' vs '{other_prog.name}'\n")
                    else:
                        f.write(f"{program.id}: '{program.name}' (only in file 1)\n")
            
            f.write("\nCombis:\n")
            f.write("-" * 80 + "\n")
            
            for bank in self.pcg.combi_banks:
                for combi in bank.patches:
                    other_combi = other_pcg.find_combi(combi.bank, combi.index)
                    if other_combi:
                        if combi.name != other_combi.name:
                            f.write(f"{combi.id}: '{combi.name}' vs '{other_combi.name}'\n")
                    else:
                        f.write(f"{combi.id}: '{combi.name}' (only in file 1)\n")
    
    def generate_file_content_list(self, output_file: str, format: str = 'csv'):
        """Generate file content summary."""
        if format == 'csv':
            self._write_file_content_csv(output_file)
        else:
            self._write_file_content_txt(output_file)
    
    def _write_file_content_csv(self, output_file: str):
        """Write file content to CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Bank Type', 'Bank ID', 'Total Slots', 'Filled', 'Empty'])
            
            for bank in self.pcg.program_banks:
                filled = sum(1 for p in bank.patches if p.name and 'init' not in p.name.lower())
                empty = len(bank.patches) - filled
                writer.writerow(['Program', bank.bank_id, len(bank.patches), filled, empty])
            
            for bank in self.pcg.combi_banks:
                filled = sum(1 for c in bank.patches if c.name and 'init' not in c.name.lower())
                empty = len(bank.patches) - filled
                writer.writerow(['Combi', bank.bank_id, len(bank.patches), filled, empty])
    
    def _write_file_content_txt(self, output_file: str):
        """Write file content to text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("FILE CONTENT SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Model: {self.pcg.header.model.value}\n")
            f.write(f"Version: {self.pcg.header.major_version}.{self.pcg.header.minor_version}\n\n")
            
            f.write("Program Banks:\n")
            f.write("-" * 80 + "\n")
            for bank in self.pcg.program_banks:
                filled = sum(1 for p in bank.patches if p.name and 'init' not in p.name.lower())
                empty = len(bank.patches) - filled
                f.write(f"  {bank.bank_id}: {filled}/{len(bank.patches)} filled, {empty} empty\n")
            
            f.write("\nCombi Banks:\n")
            f.write("-" * 80 + "\n")
            for bank in self.pcg.combi_banks:
                filled = sum(1 for c in bank.patches if c.name and 'init' not in c.name.lower())
                empty = len(bank.patches) - filled
                f.write(f"  {bank.bank_id}: {filled}/{len(bank.patches)} filled, {empty} empty\n")
