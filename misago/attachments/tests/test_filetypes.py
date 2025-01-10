import pytest

from ..enums import AllowedAttachments
from ..filetypes import filetypes


def test_filetypes_get_filetype_returns_filetype_by_name():
    filetype = filetypes.get_filetype("JPEG")

    assert filetype.name == "JPEG"
    assert filetype.extensions == ("jpeg", "jpg")


def test_filetypes_get_filetype_raises_value_error_for_unsupported_type():
    with pytest.raises(ValueError) as exc_info:
        filetypes.get_filetype("UNSUPPORTED")

    assert isinstance(exc_info.value, ValueError)
    assert str(exc_info.value) == "'UNSUPPORTED' filetype is not supported"


def test_filetypes_match_filetype_returns_filetype_by_file_name():
    filetype = filetypes.match_filetype("LOREMIPSUM.JPG")
    assert filetype.name == "JPEG"


def test_filetypes_match_filetype_returns_filetype_by_file_name_and_content_type():
    filetype = filetypes.match_filetype("LOREMIPSUM.Mp4", "vIdEo/mP4")
    assert filetype.name == "MP4"


def test_filetypes_match_filetype_returns_none_for_file_with_unsupported_extension():
    filetype = filetypes.match_filetype("LOREMIPSUM.derp", "vIdEo/mP4")
    assert filetype is None


def test_filetypes_match_filetype_returns_none_for_file_with_invalid_content_type():
    filetype = filetypes.match_filetype("LOREMIPSUM.mp4", "invalid/mP4")
    assert filetype is None


def test_filetypes_match_filetype_returns_none_for_file_without_extension():
    filetype = filetypes.match_filetype("LOREMIPSUM", "invalid/mP4")
    assert filetype is None


def test_filetypes_get_accept_attr_str_returns_all_filetypes():
    value = filetypes.get_accept_attr_str(AllowedAttachments.ALL)
    assert ".jpeg, .jpg" in value
    assert ".mp4" in value
    assert ".pdf" in value
    assert ".zip" in value


def test_filetypes_get_accept_attr_str_returns_only_media_filetypes():
    value = filetypes.get_accept_attr_str(AllowedAttachments.MEDIA)
    assert ".jpeg, .jpg" in value
    assert ".mp4" in value
    assert ".pdf" not in value
    assert ".zip" not in value


def test_filetypes_get_accept_attr_str_returns_only_image_filetypes():
    value = filetypes.get_accept_attr_str(AllowedAttachments.IMAGES)
    assert ".jpeg, .jpg" in value
    assert ".mp4" not in value
    assert ".pdf" not in value
    assert ".zip" not in value


def test_filetypes_get_accept_attr_str_returns_empty_string():
    value = filetypes.get_accept_attr_str(AllowedAttachments.NONE)
    assert value == ""
