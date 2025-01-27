def test_unordered_list(parse_markup):
    result = parse_markup("- Lorem")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_unordered_list_with_multiple_items(parse_markup):
    result = parse_markup("- Lorem\n- Ipsum\n- Dolor")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Dolor",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_unordered_list_with_asterisk(parse_markup):
    result = parse_markup("* Lorem\n* Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "*",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_unordered_list_with_plus(parse_markup):
    result = parse_markup("+ Lorem\n+ Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "+",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_unordered_list_with_indent(parse_markup):
    result = parse_markup("  - Lorem\n  - Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_ordered_list(parse_markup):
    result = parse_markup("1. Lorem\n2) Ipsum\n4. Dolor")
    assert result == [
        {
            "type": "list",
            "ordered": True,
            "sign": None,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Dolor",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_separating_blank_lines(parse_markup):
    result = parse_markup("  - Lorem\n\n\n  - Ipsum")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_multiple_lists_separated_by_marker(parse_markup):
    result = parse_markup("- Lorem\n- Ipsum\n* Dolor\n* Met\n+ Sit\n1. Amet")
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
            ],
        },
        {
            "type": "list",
            "ordered": False,
            "sign": "*",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Dolor",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [],
                },
            ],
        },
        {
            "type": "list",
            "ordered": False,
            "sign": "+",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Sit",
                        },
                    ],
                    "lists": [],
                },
            ],
        },
        {
            "type": "list",
            "ordered": True,
            "sign": None,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Amet",
                        },
                    ],
                    "lists": [],
                },
            ],
        },
    ]


def test_list_with_first_item_subitems(parse_markup):
    result = parse_markup(
        """
        - Lorem
          - Ipsum
          - Dolor
        - Met
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [
                        {
                            "type": "list",
                            "ordered": False,
                            "sign": "-",
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Ipsum",
                                        },
                                    ],
                                    "lists": [],
                                },
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Dolor",
                                        },
                                    ],
                                    "lists": [],
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_second_item_subitems(parse_markup):
    result = parse_markup(
        """
        - Lorem
        - Met
          - Ipsum
          - Dolor
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [
                        {
                            "type": "list",
                            "ordered": False,
                            "sign": "-",
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Ipsum",
                                        },
                                    ],
                                    "lists": [],
                                },
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Dolor",
                                        },
                                    ],
                                    "lists": [],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
    ]


def test_list_with_first_item_subitems_two_levels_deep(parse_markup):
    result = parse_markup(
        """
        - Met
          - Ipsum
            - Dolor
          - Elit
        - Lorem
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [
                        {
                            "type": "list",
                            "ordered": False,
                            "sign": "-",
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Ipsum",
                                        },
                                    ],
                                    "lists": [
                                        {
                                            "type": "list",
                                            "ordered": False,
                                            "sign": "-",
                                            "children": [
                                                {
                                                    "type": "list-item",
                                                    "children": [
                                                        {
                                                            "type": "text",
                                                            "text": "Dolor",
                                                        },
                                                    ],
                                                    "lists": [],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Elit",
                                        },
                                    ],
                                    "lists": [],
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_first_item_children_three_levels_deep(parse_markup):
    result = parse_markup(
        """
        - Met
          - Ipsum
            - Dolor
              - Pacem
          - Elit
        - Lorem
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [
                        {
                            "type": "list",
                            "ordered": False,
                            "sign": "-",
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Ipsum",
                                        },
                                    ],
                                    "lists": [
                                        {
                                            "type": "list",
                                            "ordered": False,
                                            "sign": "-",
                                            "children": [
                                                {
                                                    "type": "list-item",
                                                    "children": [
                                                        {
                                                            "type": "text",
                                                            "text": "Dolor",
                                                        },
                                                    ],
                                                    "lists": [
                                                        {
                                                            "type": "list",
                                                            "ordered": False,
                                                            "sign": "-",
                                                            "children": [
                                                                {
                                                                    "type": "list-item",
                                                                    "children": [
                                                                        {
                                                                            "type": "text",
                                                                            "text": "Pacem",
                                                                        },
                                                                    ],
                                                                    "lists": [],
                                                                },
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Elit",
                                        },
                                    ],
                                    "lists": [],
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_empty_first_item(parse_markup):
    result = parse_markup(
        """
        -
        - Met
        - Ipsum
        - Lorem
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_empty_middle_item(parse_markup):
    result = parse_markup(
        """
        - Met
        - Ipsum
        -
        - Lorem
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Ipsum",
                        },
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_with_empty_nested_item(parse_markup):
    result = parse_markup(
        """
        - Met
          - Ipsum
          -
        - Lorem
        """
    )
    assert result == [
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Met",
                        },
                    ],
                    "lists": [
                        {
                            "type": "list",
                            "ordered": False,
                            "sign": "-",
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "text",
                                            "text": "Ipsum",
                                        },
                                    ],
                                    "lists": [],
                                },
                                {
                                    "type": "list-item",
                                    "children": [],
                                    "lists": [],
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "text",
                            "text": "Lorem",
                        },
                    ],
                    "lists": [],
                },
            ],
        }
    ]


def test_list_items_with_too_deep_levels_are_fixed(parse_markup):
    result = parse_markup(
        """
        - Met
            - Ipsum
            - Dolor
          - Sit
        - Lorem
        """
    )
    expected_result = parse_markup(
        """
        - Met
          - Ipsum
          - Dolor
          - Sit
        - Lorem
        """
    )
    assert result == expected_result


def test_list_with_too_deep_item_followed_by_deep_item_is_fixed(parse_markup):
    result = parse_markup(
        """
        - Met
                - Ipsum
            - Dolor
          - Sit
        - Lorem
        """
    )
    expected_result = parse_markup(
        """
        - Met
          - Ipsum
          - Dolor
          - Sit
        - Lorem
        """
    )
    assert result == expected_result


def test_list_with_too_deep_item_followed_by_two_too_deep_items_is_fixed(parse_markup):
    result = parse_markup(
        """
        - Met
                - Ipsum
              - Dolor
          - Sit
        - Lorem
        """
    )
    expected_result = parse_markup(
        """
        - Met
          - Ipsum
          - Dolor
          - Sit
        - Lorem
        """
    )
    assert result == expected_result


def test_list_with_first_item_indented_is_fixed(parse_markup):
    result = parse_markup(
        """
        Lorem ipsum

              - Met
              - Ipsum
            - Dolor
            - Sit
            - Lorem
        """
    )
    expected_result = parse_markup(
        """
        Lorem ipsum

        - Met
          - Ipsum
        - Dolor
        - Sit
        - Lorem
        """
    )
    assert result == expected_result


def test_list_items_with_not_deep_levels_are_fixed(parse_markup):
    result = parse_markup(
        """
        - Met
         - Ipsum
          - Dolor
           - Sit
        - Lorem
        """
    )
    expected_result = parse_markup(
        """
        - Met
        - Ipsum
        - Dolor
        - Sit
        - Lorem
        """
    )
    assert result == expected_result
