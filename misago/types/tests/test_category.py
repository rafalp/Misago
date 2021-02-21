from ..category import Category


def category_factory(*, id, left, right):
    return Category(name="T", slug="t", type=0, id=id, left=left, right=right, extra={})


def test_category_is_not_its_own_parent_or_child():
    category = category_factory(id=1, left=1, right=2)

    assert not category.is_parent(category)
    assert not category.is_child(category)


def test_category_is_child_of_parent():
    parent = category_factory(id=1, left=1, right=4)
    child = category_factory(id=2, left=2, right=3)

    assert parent.is_parent(child)
    assert not parent.is_child(child)

    assert not child.is_parent(parent)
    assert child.is_child(parent)


def test_sibling_category_is_not_child_or_parent():
    category = category_factory(id=1, left=1, right=2)
    sibling = category_factory(id=2, left=3, right=4)

    assert not category.is_parent(sibling)
    assert not category.is_child(sibling)
    assert not sibling.is_parent(category)
    assert not sibling.is_child(category)


def test_leaf_category_has_no_children():
    category = category_factory(id=1, left=1, right=2)
    assert not category.has_children()


def test_parent_category_has_children():
    parent = category_factory(id=1, left=1, right=4)
    assert parent.has_children()
