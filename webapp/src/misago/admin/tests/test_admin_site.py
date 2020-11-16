from ..site import Node


def test_node_is_added_at_end_of_parent_children():
    master = Node(name="Apples", link="misago:index")
    child = Node(name="Oranges", link="misago:index")
    master.add_node(child)

    assert master.children()[-1].name == child.name


def test_add_node_after():
    """add_node added node after specific node"""
    master = Node(name="Apples", link="misago:index")

    child = Node(name="Oranges", link="misago:index")
    master.add_node(child)

    test = Node(name="Potatoes", link="misago:index")
    master.add_node(test, after="misago:index")

    all_nodes = master.children()
    for i, node in enumerate(all_nodes):
        if node.name == test.name:
            assert all_nodes[i - 1].name == child.name


def test_add_node_before():
    """add_node added node  before specific node"""
    master = Node(name="Apples", link="misago:index")

    child = Node(name="Oranges", link="misago:index")
    master.add_node(child)

    test = Node(name="Potatoes", link="misago:index")
    master.add_node(test, before="misago:index")

    all_nodes = master.children()
    for i, node in enumerate(all_nodes):
        if node.name == test.name:
            assert all_nodes[i + 1].name == child.name
