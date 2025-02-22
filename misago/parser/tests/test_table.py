from itertools import product

import pytest


@pytest.mark.parametrize(
    "prepend",
    (
        ("", None),
        (
            "paragraph1",
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "paragraph1"},
                ],
            },
        ),
        (
            "# heading1",
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "heading1"},
                ],
            },
        ),
    ),
)
@pytest.mark.parametrize(
    "append",
    (
        ("", None),
        (
            "paragraph2",
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "paragraph2"},
                ],
            },
        ),
        (
            "# heading2",
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "heading2"},
                ],
            },
        ),
    ),
)
@pytest.mark.parametrize("separator", ("\n", "\n\n\n"))
@pytest.mark.parametrize(
    "case",
    (
        (
            "|Col1\n|-",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [],
            },
        ),
        (
            "|Col1|\n|-|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [],
            },
        ),
        (
            "|Col1\n|-\n|Cell1",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    }
                ],
            },
        ),
        (
            "|Col1\n|-\n|Cell1\n|Cell2",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            }
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|\n|-|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [],
            },
        ),
        (
            "|Col1\n|-\n|Cell1",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    }
                ],
            },
        ),
        (
            "|Col1|\n|-|\n|Cell1|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    }
                ],
            },
        ),
        (
            "|Col1\n|-\n|Cell1\n|Cell2",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            }
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|\n|-|\n|Cell1|\n|Cell2|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    }
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            }
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            }
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|*Col2*|Col3\n|-|-|-",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [],
            },
        ),
        (
            "|Col1|*Col2*|Col3|\n|-|-|-|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [],
            },
        ),
        (
            "|Col1|*Col2*|Col3\n|-|-|-\n|Cell1|Cell2|Cell3",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell3"}],
                            },
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|*Col2*|Col3|\n|-|-|-|\n|Cell1|Cell2|Cell3|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell3"}],
                            },
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|*Col2*|Col3\n|-|-|-\n|Cell1|Cell2|Cell3\n|Cell4|Cell5|Cell6",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell3"}],
                            },
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell4"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell5"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell6"}],
                            },
                        ],
                    },
                ],
            },
        ),
        (
            "|Col1|*Col2*|Col3|\n|-|-|-|\n|Cell1|Cell2|Cell3\n|Cell4|Cell5|Cell6|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col1"}],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {
                                "type": "emphasis",
                                "children": [
                                    {"type": "text", "text": "Col2"},
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [{"type": "text", "text": "Col3"}],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell1"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell2"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell3"}],
                            },
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell4"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell5"}],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [{"type": "text", "text": "Cell6"}],
                            },
                        ],
                    },
                ],
            },
        ),
    ),
)
def test_markdown_table(parse_markup, prepend, append, separator, case):
    markup = []
    expected = []

    prepend_markup, prepend_result = prepend
    if prepend_markup:
        markup.append(prepend_markup)
    if prepend_result:
        expected.append(prepend_result)

    case_markup, case_result = case
    markup.append(case_markup)
    expected.append(case_result)

    append_markup, append_result = append
    if append_markup:
        markup.append(append_markup)
    if append_result:
        expected.append(append_result)

    result = parse_markup(separator.join(markup))
    assert result == expected


@pytest.mark.parametrize(
    "case",
    (
        (
            "| Col |\n| - |",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n|:-|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n|-:|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "right",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n|:-:|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "center",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n| :-: |",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "center",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n|  :----:  |",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "center",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "| Col |\n|:-:",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "center",
                        "children": [
                            {"type": "text", "text": "Col"},
                        ],
                    }
                ],
                "children": [],
            },
        ),
        (
            "|Col1|Col2|Col3\n|:-:|-:|:-|\n|Cell1|Cell2|Cell3|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "center",
                        "children": [
                            {"type": "text", "text": "Col1"},
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "right",
                        "children": [
                            {"type": "text", "text": "Col2"},
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {"type": "text", "text": "Col3"},
                        ],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "center",
                                "children": [
                                    {"type": "text", "text": "Cell1"},
                                ],
                            },
                            {
                                "type": "table-cell",
                                "align": "right",
                                "children": [
                                    {"type": "text", "text": "Cell2"},
                                ],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {"type": "text", "text": "Cell3"},
                                ],
                            },
                        ],
                    }
                ],
            },
        ),
        (
            "|Col1|Col2|\n|-|-|\n|Strong|**Strong**|\n|Link|example.com|\n|Empty|",
            {
                "type": "table",
                "header": [
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {"type": "text", "text": "Col1"},
                        ],
                    },
                    {
                        "type": "table-header",
                        "align": "left",
                        "children": [
                            {"type": "text", "text": "Col2"},
                        ],
                    },
                ],
                "children": [
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {"type": "text", "text": "Strong"},
                                ],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {
                                        "type": "strong",
                                        "children": [
                                            {"type": "text", "text": "Strong"},
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {"type": "text", "text": "Link"},
                                ],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {
                                        "type": "auto-url",
                                        "href": "example.com",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "type": "table-row",
                        "children": [
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [
                                    {"type": "text", "text": "Empty"},
                                ],
                            },
                            {
                                "type": "table-cell",
                                "align": "left",
                                "children": [],
                            },
                        ],
                    },
                ],
            },
        ),
    ),
)
def test_markdown_table_contents(parse_markup, case):
    markup, expected = case
    result = parse_markup(markup)
    assert result == [expected]
