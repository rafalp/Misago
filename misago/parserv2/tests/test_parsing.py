from ..factory import create_parser


def test_parsing():
    parser = create_parser(None)
    tokens = parser.parse("hello *world*, how's going?")