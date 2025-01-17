from ..filename import clean_filename, trim_filename
from ..filetypes import filetypes


def test_clean_filename_passes_valid_filename():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("filename.png", filetype)
    assert filename == "filename.png"


def test_clean_filename_slugifies_filename():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename("filename (fixed v2!)-some.png", filetype)
    assert filename == "filename-fixed-v2-some.png"


def test_clean_filename_cuts_long_filename():
    filetype = filetypes.match_filetype("test.png")
    filename = clean_filename(("long" * 20) + ".png", filetype)
    assert filename == "longlonglonglonglonglonglonglonglonglonglonglonglo.png"
