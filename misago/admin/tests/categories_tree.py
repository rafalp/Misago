from ...categories.models import Category


def assert_valid_categories_tree(expected_tree: list[tuple]):
    root = Category.objects.root_category()
    queryset = Category.objects.filter(tree_id=root.tree_id).order_by("lft")

    current_tree = []
    for category in queryset:
        current_tree.append(
            (
                category,
                category.level,
                category.lft - root.lft + 1,
                category.rght - root.lft + 1,
            )
        )

    c_len, e_len = len(current_tree), len(expected_tree)
    assert c_len == e_len, (
        "categories trees lengths don't match: " f"found {c_len}, expected {e_len}"
    )

    for i, current in enumerate(current_tree):
        expected = expected_tree[i]

        assert current[0] == expected[0], (
            f"category #{i} is wrong: " f"'{current[0].name}' != '{expected[0].name}'"
        )

        c_level, e_level = current[1], expected[1]
        assert (
            c_level == e_level
        ), f"category #{i} level is invalid: {c_level} != {e_level}"

        c_lft, e_lft = current[2], expected[2]
        assert c_lft == e_lft, f"category #{i} left edge is invalid: {c_lft} != {e_lft}"

        c_rght, e_rght = current[3], expected[3]
        assert (
            c_rght == e_rght
        ), f"category #{i} right edge is invalid: {c_rght} != {e_rght}"
