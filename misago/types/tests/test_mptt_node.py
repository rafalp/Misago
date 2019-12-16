from dataclasses import dataclass
from typing import Optional

from ..mptt import MPTTNode


@dataclass
class Node(MPTTNode):
    id: int
    left: int = 0
    right: int = 0
    depth: int = 0
    parent_id: Optional[int] = None


def test_node_is_not_its_own_parent_or_child():
    node = Node(id=1, left=1, right=2)

    assert not node.is_parent(node)
    assert not node.is_child(node)


def test_node_is_child_of_parent():
    parent = Node(id=1, left=1, right=4)
    child = Node(id=2, left=2, right=3)

    assert parent.is_parent(child)
    assert not parent.is_child(child)

    assert not child.is_parent(parent)
    assert child.is_child(parent)


def test_sibling_node_is_not_child_or_parent():
    node = Node(id=1, left=1, right=2)
    sibling = Node(id=2, left=3, right=4)

    assert not node.is_parent(sibling)
    assert not node.is_child(sibling)
    assert not sibling.is_parent(node)
    assert not sibling.is_child(node)


def test_leaf_node_has_no_children():
    node = Node(id=1, left=1, right=2)
    assert not node.has_children()


def test_parent_node_has_children():
    parent = Node(id=1, left=1, right=4)
    assert parent.has_children()
