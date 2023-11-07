import pytest

from ..parser import parse


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("!(http://somewhere.com/image.jpg)", id="base"),
        pytest.param("! (space)", id="space-one-word"),
        pytest.param("! (space with other words)", id="space-multiple-words"),
        pytest.param(
            "Text before exclamation mark!(http://somewhere.com/image.jpg)",
            id="text-before-mark",
        ),
        pytest.param(
            "Text before with space in between! (sometext)", id="text-before-with-space"
        ),
    ],
)
def test_short_image_markdown(request_mock, user, snapshot, text):
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]
