from ..filename import clean_filename, trim_filename
from ..filetypes import filetypes


def test_clean_filename_passes_valid_filename():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("filename.png", filetype)
    assert filename == "filename.png"


def test_clean_filename_removes_invalid_characters():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("<hello>.png", filetype)
    assert filename == "hello.png"


def test_clean_filename_strips_whitespace_from_around_name():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("  <hello>  .png", filetype)
    assert filename == "hello.png"


def test_clean_filename_fallbacks_to_valid_filename_for_empty_name():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("   .png", filetype)
    assert filename == "file.png"


def test_clean_filename_fallbacks_to_valid_filename_for_invalid_name():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("######.png", filetype)
    assert filename == "file.png"


def test_trim_filename_leaves_short_filename_unchanged():
    filetype = filetypes.match_filetype("test.png")
    filename = trim_filename("test.png", filetype)
    assert filename == "test.png"


def test_trim_filename_cuts_short_too_long_filename():
    filetype = filetypes.match_filetype("screen-shot.png")
    filename = trim_filename("screen-shot.png", filetype, 10)
    assert filename == "screen.png"


def test_trim_filename_strips_spaces_from_filename():
    filetype = filetypes.match_filetype("screen .png")
    filename = trim_filename("screen .png", filetype, 10)
    assert filename == "screen.png"
