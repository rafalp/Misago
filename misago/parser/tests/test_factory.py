from ..factory import create_parser


def test_create_parser_returns_parser_instance():
    parser = create_parser()
    assert parser.parse("Hello *world*!")
