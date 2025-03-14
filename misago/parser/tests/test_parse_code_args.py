from ..patterns.code import parse_code_args


def test_parse_code_args_extracts_prefixed_syntax(parser):
    args = parse_code_args(parser, "syntax:custom")
    assert args == {"info": None, "syntax": "custom"}


def test_parse_code_args_strips_prefixed_syntax(parser):
    args = parse_code_args(parser, "syntax:     custom     ")
    assert args == {"info": None, "syntax": "custom"}


def test_parse_code_args_detects_known_syntax(parser):
    args = parse_code_args(parser, "python")
    assert args == {"info": None, "syntax": "python"}


def test_parse_code_args_reads_info(parser):
    args = parse_code_args(parser, "Lorem ipsum dolor met")
    assert args == {"info": "Lorem ipsum dolor met", "syntax": None}


def test_parse_code_args_strips_info_whitespace(parser):
    args = parse_code_args(parser, "        Lorem ipsum dolor met     ")
    assert args == {"info": "Lorem ipsum dolor met", "syntax": None}


def test_parse_code_args_parses_info_and_syntax(parser):
    args = parse_code_args(parser, "Lorem ipsum dolor met,syntax=custom")
    assert args == {"info": "Lorem ipsum dolor met", "syntax": "custom"}


def test_parse_code_args_strips_info_and_syntax(parser):
    args = parse_code_args(
        parser, "        Lorem ipsum dolor met     ; syntax=   php   "
    )
    assert args == {"info": "Lorem ipsum dolor met", "syntax": "php"}


def test_parse_code_args_parses_empty_info_and_syntax(parser):
    args = parse_code_args(parser, "   , syntax=   ")
    assert args == {"info": ", syntax=", "syntax": None}
