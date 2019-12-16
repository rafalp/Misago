from ..category import Category


def test_category_is_not_its_own_parent_or_child():
    category = Category(
        id=1, type=1, depth=1, left=1, right=2, name="Test", slug="test",
    )

    assert not category.is_parent(category)
    assert not category.is_child(category)


def test_category_is_child_of_parent():
    parent = Category(id=1, type=1, depth=1, left=1, right=4, name="Test", slug="test",)
    child = Category(id=2, type=1, depth=2, left=2, right=3, name="Test", slug="test",)

    assert parent.is_parent(child)
    assert not parent.is_child(child)

    assert not child.is_parent(parent)
    assert child.is_child(parent)


def test_sibling_category_is_not_child_or_parent():
    category = Category(
        id=1, type=1, depth=1, left=1, right=2, name="Test", slug="test",
    )
    sibling = Category(
        id=2, type=1, depth=1, left=3, right=4, name="Test", slug="test",
    )

    assert not category.is_parent(sibling)
    assert not category.is_child(sibling)
    assert not sibling.is_parent(category)
    assert not sibling.is_child(category)
