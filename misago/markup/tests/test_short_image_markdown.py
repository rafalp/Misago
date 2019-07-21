from ..parser import parse


def test_short_image_markdown(request_mock, user, snapshot):
    text = "!(http://somewhere.com/image.jpg)"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])
