"""Command-line interface for PCG Tools."""

import click
import sys
from pathlib import Path
from .reader import read_pcg_file
from .writer import write_pcg_file


@click.group()
@click.version_option()
def cli():
    """PCG Tools - Cross-platform Korg PCG file editor."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def info(input_file):
    """Display information about a PCG file."""
    try:
        pcg = read_pcg_file(input_file)
        
        click.echo(f"\n{'='*60}")
        click.echo(f"PCG File: {Path(input_file).name}")
        click.echo(f"{'='*60}")
        click.echo(f"Model: {pcg.header.model.value}")
        click.echo(f"Version: {pcg.header.major_version}.{pcg.header.minor_version}")
        click.echo(f"Product ID: 0x{pcg.header.product_id:02X}")
        click.echo(f"\nProgram Banks: {len(pcg.program_banks)}")
        click.echo(f"Combi Banks: {len(pcg.combi_banks)}")
        click.echo(f"Set Lists: {len(pcg.set_lists)}")
        click.echo(f"Has Global: {pcg.has_global}")
        
        total_programs = sum(len(bank) for bank in pcg.program_banks)
        total_combis = sum(len(bank) for bank in pcg.combi_banks)
        
        click.echo(f"\nTotal Programs: {total_programs}")
        click.echo(f"Total Combis: {total_combis}")
        click.echo(f"{'='*60}\n")
        
    except Exception as e:
        click.echo(f"Error reading PCG file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def list_patches(input_file):
    """List all patches in a PCG file."""
    try:
        pcg = read_pcg_file(input_file)
        
        click.echo(f"\nPrograms in {Path(input_file).name}:")
        click.echo("-" * 60)
        
        for bank in pcg.program_banks:
            if bank.patches:
                click.echo(f"\nBank {bank.bank_id}:")
                for prog in bank.patches:
                    fav = " [FAV]" if prog.favorite else ""
                    click.echo(f"  {prog.id}: {prog.name}{fav}")
        
        if pcg.combi_banks:
            click.echo(f"\nCombis:")
            click.echo("-" * 60)
            for bank in pcg.combi_banks:
                if bank.patches:
                    click.echo(f"\nBank {bank.bank_id}:")
                    for combi in bank.patches:
                        fav = " [FAV]" if combi.favorite else ""
                        click.echo(f"  {combi.id}: {combi.name}{fav}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', type=click.Choice(['csv', 'txt', 'xml']), default='csv')
def export(input_file, output_file, format):
    """Export patch list to a file."""
    try:
        pcg = read_pcg_file(input_file)
        
        if format == 'csv':
            _export_csv(pcg, output_file)
        elif format == 'txt':
            _export_txt(pcg, output_file)
        else:
            click.echo("XML export not yet implemented", err=True)
            sys.exit(1)
        
        click.echo(f"Exported to {output_file}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--qt', is_flag=True, help='Use Qt GUI (recommended for macOS)')
def gui(qt):
    """Launch the graphical user interface."""
    try:
        import sys
        import platform
        
        # Try Qt GUI first if requested or on macOS
        if qt or platform.system() == 'Darwin':
            try:
                click.echo("Using Qt GUI")
                from .gui_qt import main as qt_main
                qt_main()
                return
            except ImportError:
                if qt:
                    click.echo("Qt GUI not available. Install with: pip install PySide6", err=True)
                    sys.exit(1)
                click.echo("Qt not available, falling back to tkinter GUI")
        
        # Fall back to tkinter GUI
        if platform.system() == 'Darwin':
            click.echo("Using macOS tkinter GUI")
            from .gui_macos import launch_gui
        else:
            from .gui import launch_gui
        
        launch_gui()
    except ImportError as e:
        click.echo(f"Error: GUI dependencies not available: {e}", err=True)
        sys.exit(1)


def _export_csv(pcg, output_file):
    """Export to CSV format."""
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Type', 'Bank', 'Index', 'ID', 'Name', 'Category', 'Favorite'])
        
        for bank in pcg.program_banks:
            for prog in bank.patches:
                cat = prog.category.name if prog.category else ""
                writer.writerow(['Program', prog.bank, prog.index, prog.id, prog.name, cat, prog.favorite])
        
        for bank in pcg.combi_banks:
            for combi in bank.patches:
                cat = combi.category.name if combi.category else ""
                writer.writerow(['Combi', combi.bank, combi.index, combi.id, combi.name, cat, combi.favorite])


def _export_txt(pcg, output_file):
    """Export to text format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"PCG File: {pcg.header.model.value}\n")
        f.write(f"Version: {pcg.header.major_version}.{pcg.header.minor_version}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("PROGRAMS\n")
        f.write("-" * 80 + "\n")
        for bank in pcg.program_banks:
            if bank.patches:
                f.write(f"\nBank {bank.bank_id}:\n")
                for prog in bank.patches:
                    fav = " [FAV]" if prog.favorite else ""
                    f.write(f"  {prog.id}: {prog.name}{fav}\n")
        
        if pcg.combi_banks:
            f.write("\n\nCOMBIS\n")
            f.write("-" * 80 + "\n")
            for bank in pcg.combi_banks:
                if bank.patches:
                    f.write(f"\nBank {bank.bank_id}:\n")
                    for combi in bank.patches:
                        fav = " [FAV]" if combi.favorite else ""
                        f.write(f"  {combi.id}: {combi.name}{fav}\n")




@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', type=click.Choice(['csv', 'txt']), default='csv')
def program_usage(input_file, output_file, format):
    """Generate program usage list."""
    try:
        from .list_generators import ListGenerator
        pcg = read_pcg_file(input_file)
        gen = ListGenerator(pcg)
        gen.generate_program_usage_list(output_file, format)
        click.echo(f"Program usage list saved to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', type=click.Choice(['csv', 'txt']), default='csv')
@click.option('--style', type=click.Choice(['short', 'long']), default='short')
def combi_content(input_file, output_file, format, style):
    """Generate combi content list."""
    try:
        from .list_generators import ListGenerator
        pcg = read_pcg_file(input_file)
        gen = ListGenerator(pcg)
        gen.generate_combi_content_list(output_file, format, style)
        click.echo(f"Combi content list saved to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', type=click.Choice(['csv', 'txt']), default='csv')
def differences(file1, file2, output_file, format):
    """Generate differences list between two PCG files."""
    try:
        from .list_generators import ListGenerator
        pcg1 = read_pcg_file(file1)
        pcg2 = read_pcg_file(file2)
        gen = ListGenerator(pcg1)
        gen.generate_differences_list(pcg2, output_file, format)
        click.echo(f"Differences list saved to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
