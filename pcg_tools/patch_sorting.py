"""Patch sorting utilities for PCG Tools.

Based on C# PatchSorting/PatchSorter.cs, TitleComparer.cs, ArtistComparer.cs.

Provides advanced sorting by title/artist extracted from patch names using
a configurable split character.
"""

from enum import IntEnum
from typing import List, Optional, Callable, Any


class SortOrder(IntEnum):
    """Sort order options matching C# PatchSorter.SortOrder."""
    NAME_CATEGORY = 0           # ESortOrderNameCategory
    TITLE_ARTIST_CATEGORY = 1   # ESortOrderTitleArtistCategory
    ARTIST_TITLE_CATEGORY = 2   # ESortOrderArtistTitleCategory
    CATEGORY_NAME = 3           # ESortOrderCategoryName
    CATEGORY_TITLE_ARTIST = 4   # ESortOrderCategoryTitleArtist
    CATEGORY_ARTIST_TITLE = 5   # ESortOrderCategoryArtistTitle


def count_chars_around_index(s: str, index: int, char: str) -> int:
    """Count occurrences of char around the given index.
    
    Based on C# Common.Extensions.CountCharsAroundIndex().
    
    Args:
        s: String to search
        index: Index position to check around
        char: Character to count
        
    Returns:
        Count of char occurrences immediately before and after index
    """
    count = 0
    
    # Count before
    i = index - 1
    while i >= 0 and s[i] == char:
        count += 1
        i -= 1
    
    # Count after
    i = index + 1
    while i < len(s) and s[i] == char:
        count += 1
        i += 1
    
    return count


def find_split_index(name: str, split_char: str = '-') -> int:
    """Find the index of the split character in a patch name.
    
    Based on C# PatchSorter.SplitIndex().
    
    If multiple split characters are found, the one with the most spaces
    around it is selected; otherwise the last one.
    
    E.g. "Good For You - MC-Joe" returns 13 (the ' - ' not the '-' in MC-Joe)
    
    Args:
        name: Patch name to search
        split_char: Character to split on (default '-')
        
    Returns:
        Index of split character, or -1 if not found
    """
    if not split_char or len(split_char) != 1:
        return -1
    
    split_index = -1
    max_spaces_around = 0
    
    for index, char in enumerate(name):
        if char == split_char:
            spaces_around = count_chars_around_index(name, index, ' ')
            if spaces_around >= max_spaces_around:
                split_index = index
                max_spaces_around = spaces_around
    
    return split_index


def get_title(name: str, split_char: str = '-', artist_title_order: bool = True) -> str:
    """Extract title from patch name.
    
    Based on C# PatchSorter.GetTitle().
    
    Args:
        name: Patch name
        split_char: Character to split on (default '-')
        artist_title_order: If True, title is after split char; if False, before
        
    Returns:
        Title portion of the name, or full name if no split char found
    """
    split_index = find_split_index(name, split_char)
    
    if split_index == -1:
        return name
    
    if artist_title_order:
        # Title is after the split character
        title = name[split_index + 1:].strip()
    else:
        # Title is before the split character
        title = name[:split_index].strip()
    
    return title


def get_artist(name: str, split_char: str = '-', artist_title_order: bool = True) -> str:
    """Extract artist from patch name.
    
    Based on C# PatchSorter.GetArtist().
    
    Args:
        name: Patch name
        split_char: Character to split on (default '-')
        artist_title_order: If True, artist is before split char; if False, after
        
    Returns:
        Artist portion of the name, or full name if no split char found
    """
    split_index = find_split_index(name, split_char)
    
    if split_index == -1:
        return name
    
    if artist_title_order:
        # Artist is before the split character
        artist = name[:split_index].strip()
    else:
        # Artist is after the split character
        artist = name[split_index + 1:].strip()
    
    return artist


def is_empty_or_init(patch) -> bool:
    """Check if a patch is empty or an init patch.
    
    Based on C# EmptyOrInitComparer.
    
    Args:
        patch: Patch object with name attribute
        
    Returns:
        True if patch is empty or init
    """
    if not patch:
        return True
    
    name = getattr(patch, 'name', None)
    if not name or not name.strip():
        return True
    
    # Check for common init names
    name_lower = name.lower().strip()
    init_names = ['init', 'init program', 'init combi', 'initialized', '---']
    return name_lower in init_names


def compare_by_name(p1, p2) -> int:
    """Compare patches by name.
    
    Based on C# NameComparer.
    """
    name1 = getattr(p1, 'name', '') or ''
    name2 = getattr(p2, 'name', '') or ''
    
    if name1 < name2:
        return -1
    elif name1 > name2:
        return 1
    return 0


def compare_by_category(p1, p2) -> int:
    """Compare patches by category.
    
    Based on C# CategoricalComparer.
    """
    cat1 = getattr(p1, 'category', 0) or 0
    cat2 = getattr(p2, 'category', 0) or 0
    
    if cat1 < cat2:
        return -1
    elif cat1 > cat2:
        return 1
    
    # If categories equal, compare subcategories
    subcat1 = getattr(p1, 'subcategory', 0) or 0
    subcat2 = getattr(p2, 'subcategory', 0) or 0
    
    if subcat1 < subcat2:
        return -1
    elif subcat1 > subcat2:
        return 1
    
    return 0


def compare_by_title(p1, p2, split_char: str = '-', artist_title_order: bool = True) -> int:
    """Compare patches by title.
    
    Based on C# TitleComparer.
    """
    name1 = getattr(p1, 'name', '') or ''
    name2 = getattr(p2, 'name', '') or ''
    
    title1 = get_title(name1, split_char, artist_title_order)
    title2 = get_title(name2, split_char, artist_title_order)
    
    if title1 < title2:
        return -1
    elif title1 > title2:
        return 1
    return 0


def compare_by_artist(p1, p2, split_char: str = '-', artist_title_order: bool = True) -> int:
    """Compare patches by artist.
    
    Based on C# ArtistComparer.
    """
    name1 = getattr(p1, 'name', '') or ''
    name2 = getattr(p2, 'name', '') or ''
    
    artist1 = get_artist(name1, split_char, artist_title_order)
    artist2 = get_artist(name2, split_char, artist_title_order)
    
    if artist1 < artist2:
        return -1
    elif artist1 > artist2:
        return 1
    return 0


def compare_empty_or_init(p1, p2) -> int:
    """Compare patches, putting empty/init patches at the end.
    
    Based on C# EmptyOrInitComparer.
    """
    empty1 = is_empty_or_init(p1)
    empty2 = is_empty_or_init(p2)
    
    if empty1 and not empty2:
        return 1  # p1 goes after p2
    elif not empty1 and empty2:
        return -1  # p1 goes before p2
    return 0  # Both same (both empty or both not empty)


def create_composite_comparer(comparers: List[Callable]) -> Callable:
    """Create a composite comparer from multiple comparers.
    
    Based on C# CompositeComparer.
    
    Args:
        comparers: List of comparison functions
        
    Returns:
        A comparison function that applies comparers in order
    """
    def composite_compare(p1, p2) -> int:
        for comparer in comparers:
            result = comparer(p1, p2)
            if result != 0:
                return result
        return 0
    
    return composite_compare


def sort_patches(patches: List, sort_order: SortOrder, 
                split_char: str = '-', artist_title_order: bool = True) -> List:
    """Sort patches by the specified order.
    
    Based on C# PatchSorter.SortBy().
    
    Args:
        patches: List of patch objects
        sort_order: Sort order to use
        split_char: Character to split artist/title (default '-')
        artist_title_order: If True, format is "Artist - Title"; if False, "Title - Artist"
        
    Returns:
        Sorted list of patches (sorted in place and returned)
    """
    from functools import cmp_to_key
    
    # Build list of comparers based on sort order
    comparers = [compare_empty_or_init]  # Always put empty/init at end
    
    # Create closures for title/artist comparers with settings
    def title_cmp(p1, p2):
        return compare_by_title(p1, p2, split_char, artist_title_order)
    
    def artist_cmp(p1, p2):
        return compare_by_artist(p1, p2, split_char, artist_title_order)
    
    if sort_order == SortOrder.NAME_CATEGORY:
        comparers.extend([compare_by_name, compare_by_category])
    
    elif sort_order == SortOrder.TITLE_ARTIST_CATEGORY:
        comparers.extend([title_cmp, artist_cmp, compare_by_category])
    
    elif sort_order == SortOrder.ARTIST_TITLE_CATEGORY:
        comparers.extend([artist_cmp, title_cmp, compare_by_category])
    
    elif sort_order == SortOrder.CATEGORY_NAME:
        comparers.extend([compare_by_category, compare_by_name])
    
    elif sort_order == SortOrder.CATEGORY_TITLE_ARTIST:
        comparers.extend([compare_by_category, title_cmp, artist_cmp])
    
    elif sort_order == SortOrder.CATEGORY_ARTIST_TITLE:
        comparers.extend([compare_by_category, artist_cmp, title_cmp])
    
    # Create composite comparer and sort
    composite = create_composite_comparer(comparers)
    patches.sort(key=cmp_to_key(composite))
    
    return patches
