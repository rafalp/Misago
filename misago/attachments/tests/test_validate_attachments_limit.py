import pytest
from django.core.exceptions import ValidationError

from ..validators import validate_post_attachments_limit


def test_validate_post_attachments_limit_passes_zero_attachments():
    validate_post_attachments_limit(0, 5)


def test_validate_post_attachments_limit_passes_attachments_within_limit():
    validate_post_attachments_limit(5, 5)


def test_validate_post_attachments_limit_fails_too_many_attachments():
    with pytest.raises(ValidationError) as exc_info:
        validate_post_attachments_limit(6, 5)

    assert exc_info.value.message == (
        "Posted message cannot have more than %(limit_value)s attachments "
        "(it has %(show_value)s)."
    )
    assert exc_info.value.code == "attachments_limit"
    assert exc_info.value.params == {"limit_value": 5, "show_value": 6}
