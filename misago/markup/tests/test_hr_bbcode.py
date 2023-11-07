from ..parser import parse


def test_hr_bbcode_is_replaced_if_its_alone_in_paragraph(request_mock, user, snapshot):
    text = """
Lorem ipsum dolor met.
[hr]
Sit amet elit.
"""
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_hr_bbcode_is_skipped_if_its_part_of_paragraph(request_mock, user, snapshot):
    text = "Lorem ipsum[hr]dolor met."
    result = parse(text, request_mock, user)
    assert result["parsed_text"] == "<p>Lorem ipsum[hr]dolor met.</p>"
