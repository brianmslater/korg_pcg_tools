"""Basic usage examples for PCG Tools."""

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file


def example_read_file():
    """Example: Read and display PCG file info."""
    pcg = read_pcg_file("my_patches.pcg")
    
    print(f"Model: {pcg.header.model.value}")
    print(f"Version: {pcg.header.major_version}.{pcg.header.minor_version}")
    print(f"Program banks: {len(pcg.program_banks)}")
    print(f"Combi banks: {len(pcg.combi_banks)}")


def example_list_programs():
    """Example: List all programs."""
    pcg = read_pcg_file("my_patches.pcg")
    
    for bank in pcg.program_banks:
        print(f"\nBank {bank.bank_id}:")
        for program in bank.patches:
            fav = " [FAVORITE]" if program.favorite else ""
            print(f"  {program.id}: {program.name}{fav}")


def example_find_favorites():
    """Example: Find all favorite patches."""
    pcg = read_pcg_file("my_patches.pcg")
    
    print("Favorite Programs:")
    for program in pcg.get_all_programs():
        if program.favorite:
            print(f"  {program.id}: {program.name}")
    
    print("\nFavorite Combis:")
    for combi in pcg.get_all_combis():
        if combi.favorite:
            print(f"  {combi.id}: {combi.name}")


def example_modify_and_save():
    """Example: Modify patch names and save."""
    pcg = read_pcg_file("my_patches.pcg")
    
    # Modify program names (if patches exist)
    for bank in pcg.program_banks:
        for program in bank.patches:
            if "Piano" in program.name:
                program.name = program.name.replace("Piano", "Pno")
    
    # Save to new file
    write_pcg_file(pcg, "modified_patches.pcg")
    print("Saved modified file")


if __name__ == "__main__":
    # Run examples (uncomment as needed)
    # example_read_file()
    # example_list_programs()
    # example_find_favorites()
    # example_modify_and_save()
    pass
