import pytest

from ..site import AdminSite, AdminSiteInvalidNodeError, Node


def test_admin_site_validate_nodes_raises_error_if_node_has_invalid_parent():
    site = AdminSite()

    site.add_node(
        name="Test",
        icon="test",
        namespace="test",
        parent="invalid",
    )

    with pytest.raises(AdminSiteInvalidNodeError) as exc_info:
        site.validate_nodes()

    assert str(exc_info.value) == (
        "Misago Admin node 'misago:admin:invalid:test:index' has "
        "an invalid parent 'misago:admin:invalid'."
    )


def test_admin_site_validate_nodes_raises_error_if_node_has_invalid_after():
    site = AdminSite()

    site.add_node(
        name="Test",
        icon="test",
        namespace="parent",
    )
    site.add_node(
        name="Test",
        icon="test",
        parent="parent",
        namespace="second",
        after="invalid",
    )
    site.add_node(
        name="Test",
        icon="test",
        parent="parent",
        namespace="first",
    )

    with pytest.raises(AdminSiteInvalidNodeError) as exc_info:
        site.validate_nodes()

    assert str(exc_info.value) == (
        "Misago Admin node 'misago:admin:parent:second:index' has "
        "an invalid after node 'misago:admin:parent:invalid'."
    )


def test_admin_site_validate_nodes_raises_error_if_node_has_invalid_before():
    site = AdminSite()

    site.add_node(
        name="Test",
        icon="test",
        namespace="parent",
    )
    site.add_node(
        name="Test",
        icon="test",
        parent="parent",
        namespace="second",
        before="invalid",
    )
    site.add_node(
        name="Test",
        icon="test",
        parent="parent",
        namespace="first",
    )

    with pytest.raises(AdminSiteInvalidNodeError) as exc_info:
        site.validate_nodes()

    assert str(exc_info.value) == (
        "Misago Admin node 'misago:admin:parent:second:index' has "
        "an invalid before node 'misago:admin:parent:invalid'."
    )


def test_node_is_added_at_end_of_parent_children():
    parent = Node(name="Apples", link="misago:index")
    child = Node(name="Oranges", link="misago:index")
    parent.add_node(child)

    assert parent.children()[-1].name == child.name


def test_add_node_after():
    """add_node added node after specific node"""
    parent = Node(name="Apples", link="misago:index")

    child = Node(name="Oranges", link="misago:index")
    parent.add_node(child)

    test = Node(name="Potatoes", link="misago:index")
    parent.add_node(test, after="misago:index")

    all_nodes = parent.children()
    for i, node in enumerate(all_nodes):
        if node.name == test.name:
            assert all_nodes[i - 1].name == child.name


def test_add_node_before():
    """add_node added node  before specific node"""
    parent = Node(name="Apples", link="misago:index")

    child = Node(name="Oranges", link="misago:index")
    parent.add_node(child)

    test = Node(name="Potatoes", link="misago:index")
    parent.add_node(test, before="misago:index")

    all_nodes = parent.children()
    for i, node in enumerate(all_nodes):
        if node.name == test.name:
            assert all_nodes[i + 1].name == child.name
