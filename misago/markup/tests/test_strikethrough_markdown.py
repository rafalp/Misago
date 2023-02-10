from ..parser import parse


def test_strikethrough_markdown(request_mock, user, snapshot):
    text = "Lorem ~~ipsum~~ dolor met!"
    result = parse(text, request_mock, user)
    snapshot.assert_match(result["parsed_text"])
