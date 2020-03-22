from dataclasses import dataclass
from typing import Optional

import pytest

from ..mptt import MPTT, MPTTNode


@dataclass
class Node(MPTTNode):
    id: int
    left: int = 0
    right: int = 0
    depth: int = 0
    parent_id: Optional[int] = None


@pytest.fixture
def mptt():
    return MPTT()


def simplify_mptt(mptt):
    tree = []
    for node in mptt.nodes():
        tree.append((node.id, node.parent_id, node.left, node.right, node.depth))
    return tree


def test_node_is_added_to_empty_mptt(mptt):
    node = Node(id=1)
    mptt.insert_node(node)
    assert simplify_mptt(mptt) == [(1, None, 1, 2, 0)]


def test_mptt_raises_value_error_if_parent_arg_is_used_for_empty_tree(mptt):
    with pytest.raises(ValueError):
        mptt.insert_node(Node(id=1), Node(id=2))


def test_mptt_raises_value_error_if_parent_arg_is_not_already_present_in_tree(mptt):
    mptt.insert_node(Node(id=1))
    with pytest.raises(ValueError):
        mptt.insert_node(Node(id=3), Node(id=2))


def test_node_is_added_after_previous_one_in_mptt(mptt):
    mptt.insert_node(Node(id=1))
    mptt.insert_node(Node(id=2))
    assert simplify_mptt(mptt) == [(1, None, 1, 2, 0), (2, None, 3, 4, 0)]


def test_child_node_is_inserted_under_parent_one(mptt):
    parent = Node(id=1)
    mptt.insert_node(parent)
    mptt.insert_node(Node(id=2), parent)
    assert simplify_mptt(mptt) == [(1, None, 1, 4, 0), (2, 1, 2, 3, 1)]


def test_next_child_node_is_inserted_after_previous_one(mptt):
    parent = Node(id=1)
    mptt.insert_node(parent)
    mptt.insert_node(Node(id=2), parent)
    mptt.insert_node(Node(id=3), parent)
    assert simplify_mptt(mptt) == [(1, None, 1, 6, 0), (2, 1, 2, 3, 1), (3, 1, 4, 5, 1)]


def test_node_is_added_after_previous_root_node_in_mptt(mptt):
    parent = Node(id=1)
    mptt.insert_node(parent)
    mptt.insert_node(Node(id=2), parent)
    mptt.insert_node(Node(id=3))
    assert simplify_mptt(mptt) == [
        (1, None, 1, 4, 0),
        (2, 1, 2, 3, 1),
        (3, None, 5, 6, 0),
    ]


def test_inserting_child_node_updates_parent_siblings(mptt):
    parent = Node(id=1)
    mptt.insert_node(parent)
    mptt.insert_node(Node(id=2))
    mptt.insert_node(Node(id=3))
    mptt.insert_node(Node(id=4), parent)
    assert simplify_mptt(mptt) == [
        (1, None, 1, 4, 0),
        (4, 1, 2, 3, 1),
        (2, None, 5, 6, 0),
        (3, None, 7, 8, 0),
    ]


def test_mptt_raises_type_error_if_flatten_nodes_is_called_for_root_tree(mptt):
    with pytest.raises(TypeError):
        mptt._flatten_nodes()
