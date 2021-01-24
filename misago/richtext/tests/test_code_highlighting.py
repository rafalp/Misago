from ..highlight import highlight_code


def test_empty_lines_are_trimmed_from_beginning_and_end_of_code():
    code = highlight_code('\n\n    hello_world("2021")\n\n')
    assert code == "hello_world(&quot;2021&quot;)"


def test_code_indentation_is_reduced():
    code = highlight_code("    a\n  b\n    c")
    assert code == "  a\nb\n  c"


def test_code_without_specified_syntax_is_not_highlighted():
    code = highlight_code('hello_world("2021")')
    assert code == "hello_world(&quot;2021&quot;)"


def test_code_without_unknown_syntax_is_not_highlighted():
    code = highlight_code('hello_world("2021")', "yolo")
    assert code == "hello_world(&quot;2021&quot;)"


def test_code_with_valid_syntax_is_highlighted():
    code = highlight_code('hello_world("2021")', "python")
    assert code == (
        '<span class="hl-n">hello_world</span>'
        '<span class="hl-p">(</span>'
        '<span class="hl-s2">&quot;2021&quot;</span>'
        '<span class="hl-p">)</span>'
    )
