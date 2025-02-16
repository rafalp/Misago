import pytest

from ..enums import AllowedAttachments
from ..filetypes import filetypes


def test_filetypes_get_all_filetypes_returns_list_of_filetypes():
    assert len(filetypes.get_all_filetypes()) > 10


def test_filetypes_get_filetype_returns_filetype_by_name():
    filetype = filetypes.get_filetype("jpeg")

    assert filetype.id == "jpeg"
    assert filetype.extensions == ("jpg", "jpeg")


def test_filetypes_get_filetype_raises_value_error_for_unsupported_type():
    with pytest.raises(ValueError) as exc_info:
        filetypes.get_filetype("UNSUPPORTED")

    assert isinstance(exc_info.value, ValueError)
    assert str(exc_info.value) == "'UNSUPPORTED' file type is not supported"


def test_filetypes_match_filetype_returns_filetype_by_file_name():
    filetype = filetypes.match_filetype("LOREMIPSUM.JPG")
    assert filetype.id == "jpeg"


def test_filetypes_match_filetype_returns_filetype_by_file_name_and_content_type():
    filetype = filetypes.match_filetype("LOREMIPSUM.Mp4", "vIdEo/mP4")
    assert filetype.id == "mp4"


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
    assert ".jpg, .jpeg" in value
    assert ".mp4" in value
    assert ".pdf" in value
    assert ".zip" in value


def test_filetypes_get_accept_attr_str_returns_only_media_filetypes():
    value = filetypes.get_accept_attr_str(AllowedAttachments.MEDIA)
    assert ".jpg, .jpeg" in value
    assert ".mp4" in value
    assert ".pdf" not in value
    assert ".zip" not in value


def test_filetypes_get_accept_attr_str_returns_only_image_filetypes():
    value = filetypes.get_accept_attr_str(AllowedAttachments.IMAGES)
    assert ".jpg, .jpeg" in value
    assert ".mp4" not in value
    assert ".pdf" not in value
    assert ".zip" not in value


def test_filetypes_get_accept_attr_str_returns_empty_string():
    value = filetypes.get_accept_attr_str(AllowedAttachments.NONE)
    assert value == ""


def test_filetypes_get_accept_attr_str_limits_list_to_required_extensions():
    value = filetypes.get_accept_attr_str(
        AllowedAttachments.ALL,
        require_extensions=["jpg", "png"],
    )

    assert len(value) == len(".jpg, .png")
    assert ".jpg" in value
    assert ".png" in value


def test_filetypes_get_accept_attr_str_removes_disallow_extensions():
    value = filetypes.get_accept_attr_str(
        AllowedAttachments.ALL,
        disallow_extensions=["jpg", "png"],
    )

    assert ".jpg" not in value
    assert ".png" not in value


def test_attachment_filetype_is_media_is_true_for_image_type():
    filetype = filetypes.get_filetype("jpeg")
    assert filetype.is_media


def test_attachment_filetype_is_media_is_true_for_video_type():
    filetype = filetypes.get_filetype("mp4")
    assert filetype.is_media


def test_attachment_filetype_is_media_is_false_for_non_media_type():
    filetype = filetypes.get_filetype("pdf")
    assert not filetype.is_media


def test_attachment_filetype_split_name_returns_split_name():
    filetype = filetypes.get_filetype("jpeg")
    assert filetype.split_name("FILE.JPEG") == ("FILE", "JPEG")
    assert filetype.split_name("FilE.jpG") == ("FilE", "jpG")
