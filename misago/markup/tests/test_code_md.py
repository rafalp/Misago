from ..parser import parse


def test_single_line_code_markdown(request_mock, user, snapshot):
    text = '```<script>alert("!")</script>```'
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_multi_line_code_markdown(request_mock, user, snapshot):
    text = """
```
<script>
alert("!")
</script>
```
    """
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_multi_line_code_markdown_with_language(request_mock, user, snapshot):
    text = """
```javascript
<script>
alert("!")
</script>
```
    """
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]
