#!/usr/bin/env python3
"""Test patch sorting module for PCG Tools.

Tests the advanced sorting functionality based on C# PatchSorter.
"""

from pcg_tools.patch_sorting import (
    SortOrder, find_split_index, get_title, get_artist,
    count_chars_around_index, is_empty_or_init, sort_patches,
    compare_by_name, compare_by_category, compare_by_title, compare_by_artist
)


class MockPatch:
    """Mock patch for testing."""
    def __init__(self, name: str, category: int = 0, subcategory: int = 0):
        self.name = name
        self.category = category
        self.subcategory = subcategory


def test_count_chars_around_index():
    """Test counting characters around an index."""
    # Test with spaces around hyphen
    s = "Good For You - MC-Joe"
    
    # Index 13 is the ' - ' hyphen (has spaces around it)
    assert count_chars_around_index(s, 13, ' ') == 2  # One space before, one after
    
    # Index 17 is the '-' in MC-Joe (no spaces)
    assert count_chars_around_index(s, 17, ' ') == 0
    
    print("✓ count_chars_around_index works correctly")


def test_find_split_index():
    """Test finding the split index in patch names.
    
    Based on C# PatchSorter.SplitIndex() behavior.
    """
    # Test with spaces around hyphen - should prefer the one with spaces
    assert find_split_index("Good For You - MC-Joe", '-') == 13
    
    # Test with single hyphen
    assert find_split_index("Artist-Title", '-') == 6
    
    # Test with no hyphen
    assert find_split_index("No Split Here", '-') == -1
    
    # Test with multiple hyphens, no spaces - should return last one
    assert find_split_index("A-B-C", '-') == 3
    
    # Test with different split character
    assert find_split_index("Artist/Title", '/') == 6
    
    print("✓ find_split_index works correctly")


def test_get_title():
    """Test extracting title from patch name.
    
    Based on C# PatchSorter.GetTitle().
    """
    # Default: artist_title_order=True means "Artist - Title" format
    # Title is after the split character
    assert get_title("MC-Joe - Good For You", '-', True) == "Good For You"
    assert get_title("Artist - Title", '-', True) == "Title"
    
    # With artist_title_order=False, title is before split
    assert get_title("Title - Artist", '-', False) == "Title"
    
    # No split character - return full name
    assert get_title("No Split", '-', True) == "No Split"
    
    print("✓ get_title works correctly")


def test_get_artist():
    """Test extracting artist from patch name.
    
    Based on C# PatchSorter.GetArtist().
    """
    # Default: artist_title_order=True means "Artist - Title" format
    # Artist is before the split character
    assert get_artist("MC-Joe - Good For You", '-', True) == "MC-Joe"
    assert get_artist("Artist - Title", '-', True) == "Artist"
    
    # With artist_title_order=False, artist is after split
    assert get_artist("Title - Artist", '-', False) == "Artist"
    
    # No split character - return full name
    assert get_artist("No Split", '-', True) == "No Split"
    
    print("✓ get_artist works correctly")


def test_is_empty_or_init():
    """Test empty/init patch detection."""
    # Empty patches
    assert is_empty_or_init(None) == True
    assert is_empty_or_init(MockPatch("")) == True
    assert is_empty_or_init(MockPatch("   ")) == True
    
    # Init patches
    assert is_empty_or_init(MockPatch("Init")) == True
    assert is_empty_or_init(MockPatch("init")) == True
    assert is_empty_or_init(MockPatch("Init Program")) == True
    assert is_empty_or_init(MockPatch("---")) == True
    
    # Normal patches
    assert is_empty_or_init(MockPatch("My Patch")) == False
    assert is_empty_or_init(MockPatch("Piano")) == False
    
    print("✓ is_empty_or_init works correctly")


def test_compare_by_name():
    """Test name comparison."""
    p1 = MockPatch("Alpha")
    p2 = MockPatch("Beta")
    p3 = MockPatch("Alpha")
    
    assert compare_by_name(p1, p2) < 0  # Alpha < Beta
    assert compare_by_name(p2, p1) > 0  # Beta > Alpha
    assert compare_by_name(p1, p3) == 0  # Alpha == Alpha
    
    print("✓ compare_by_name works correctly")


def test_compare_by_category():
    """Test category comparison."""
    p1 = MockPatch("A", category=1, subcategory=0)
    p2 = MockPatch("B", category=2, subcategory=0)
    p3 = MockPatch("C", category=1, subcategory=1)
    p4 = MockPatch("D", category=1, subcategory=0)
    
    assert compare_by_category(p1, p2) < 0  # Cat 1 < Cat 2
    assert compare_by_category(p2, p1) > 0  # Cat 2 > Cat 1
    assert compare_by_category(p1, p3) < 0  # Same cat, subcat 0 < subcat 1
    assert compare_by_category(p1, p4) == 0  # Same cat and subcat
    
    print("✓ compare_by_category works correctly")


def test_compare_by_title():
    """Test title comparison."""
    p1 = MockPatch("Artist1 - Alpha")
    p2 = MockPatch("Artist2 - Beta")
    p3 = MockPatch("Artist3 - Alpha")
    
    # Titles are Alpha, Beta, Alpha
    assert compare_by_title(p1, p2) < 0  # Alpha < Beta
    assert compare_by_title(p2, p1) > 0  # Beta > Alpha
    assert compare_by_title(p1, p3) == 0  # Alpha == Alpha
    
    print("✓ compare_by_title works correctly")


def test_compare_by_artist():
    """Test artist comparison."""
    p1 = MockPatch("Alpha - Title1")
    p2 = MockPatch("Beta - Title2")
    p3 = MockPatch("Alpha - Title3")
    
    # Artists are Alpha, Beta, Alpha
    assert compare_by_artist(p1, p2) < 0  # Alpha < Beta
    assert compare_by_artist(p2, p1) > 0  # Beta > Alpha
    assert compare_by_artist(p1, p3) == 0  # Alpha == Alpha
    
    print("✓ compare_by_artist works correctly")


def test_sort_patches_by_name():
    """Test sorting patches by name."""
    patches = [
        MockPatch("Zebra"),
        MockPatch("Alpha"),
        MockPatch("Init"),  # Should go to end
        MockPatch("Beta"),
    ]
    
    sorted_patches = sort_patches(patches, SortOrder.NAME_CATEGORY)
    
    # Init should be at end, others sorted alphabetically
    assert sorted_patches[0].name == "Alpha"
    assert sorted_patches[1].name == "Beta"
    assert sorted_patches[2].name == "Zebra"
    assert sorted_patches[3].name == "Init"
    
    print("✓ sort_patches by name works correctly")


def test_sort_patches_by_title_artist():
    """Test sorting patches by title then artist."""
    patches = [
        MockPatch("Artist2 - Zebra"),
        MockPatch("Artist1 - Alpha"),
        MockPatch("Artist3 - Alpha"),  # Same title as above
        MockPatch("Init"),
    ]
    
    sorted_patches = sort_patches(patches, SortOrder.TITLE_ARTIST_CATEGORY)
    
    # Should be sorted by title first, then artist
    # Alpha (Artist1), Alpha (Artist3), Zebra (Artist2), Init
    assert sorted_patches[0].name == "Artist1 - Alpha"
    assert sorted_patches[1].name == "Artist3 - Alpha"
    assert sorted_patches[2].name == "Artist2 - Zebra"
    assert sorted_patches[3].name == "Init"
    
    print("✓ sort_patches by title/artist works correctly")


def test_sort_patches_by_artist_title():
    """Test sorting patches by artist then title."""
    patches = [
        MockPatch("Beta - Title2"),
        MockPatch("Alpha - Title1"),
        MockPatch("Alpha - Title2"),  # Same artist as above
        MockPatch("Init"),
    ]
    
    sorted_patches = sort_patches(patches, SortOrder.ARTIST_TITLE_CATEGORY)
    
    # Should be sorted by artist first, then title
    # Alpha-Title1, Alpha-Title2, Beta-Title2, Init
    assert sorted_patches[0].name == "Alpha - Title1"
    assert sorted_patches[1].name == "Alpha - Title2"
    assert sorted_patches[2].name == "Beta - Title2"
    assert sorted_patches[3].name == "Init"
    
    print("✓ sort_patches by artist/title works correctly")


def test_sort_patches_by_category_name():
    """Test sorting patches by category then name."""
    patches = [
        MockPatch("Zebra", category=1),
        MockPatch("Alpha", category=2),
        MockPatch("Beta", category=1),
        MockPatch("Init", category=0),
    ]
    
    sorted_patches = sort_patches(patches, SortOrder.CATEGORY_NAME)
    
    # Should be sorted by category first, then name
    # Cat 1: Beta, Zebra; Cat 2: Alpha; Init at end
    assert sorted_patches[0].name == "Beta"
    assert sorted_patches[1].name == "Zebra"
    assert sorted_patches[2].name == "Alpha"
    assert sorted_patches[3].name == "Init"
    
    print("✓ sort_patches by category/name works correctly")


def test_sort_order_enum():
    """Test SortOrder enum values match C#."""
    assert SortOrder.NAME_CATEGORY == 0
    assert SortOrder.TITLE_ARTIST_CATEGORY == 1
    assert SortOrder.ARTIST_TITLE_CATEGORY == 2
    assert SortOrder.CATEGORY_NAME == 3
    assert SortOrder.CATEGORY_TITLE_ARTIST == 4
    assert SortOrder.CATEGORY_ARTIST_TITLE == 5
    
    print("✓ SortOrder enum values match C#")


if __name__ == '__main__':
    print("Testing PCG Tools Patch Sorting Module")
    print("=" * 50)
    
    test_count_chars_around_index()
    test_find_split_index()
    test_get_title()
    test_get_artist()
    test_is_empty_or_init()
    test_compare_by_name()
    test_compare_by_category()
    test_compare_by_title()
    test_compare_by_artist()
    test_sort_patches_by_name()
    test_sort_patches_by_title_artist()
    test_sort_patches_by_artist_title()
    test_sort_patches_by_category_name()
    test_sort_order_enum()
    
    print("=" * 50)
    print("All patch sorting tests passed!")
