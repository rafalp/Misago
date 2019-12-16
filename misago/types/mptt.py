from dataclasses import replace
from typing import List, Optional, Protocol


class MPTTNode(Protocol):
    id: int
    left: int = 0
    right: int = 0
    depth: int = 0
    parent_id: Optional[int] = None

    def has_children(self) -> bool:
        return (self.left + 1) < self.right

    def is_parent(self, node: "MPTTNode") -> bool:
        return self.left < node.left and self.right > node.right

    def is_child(self, node: "MPTTNode") -> bool:
        return self.left > node.left and self.right < node.right


class MPTT:
    _root: Optional[MPTTNode] = None
    _children: List["MPTT"]

    def __init__(self, root: Optional[MPTTNode] = None):
        self._root = root
        self._children = []

    def insert_node(self, node: MPTTNode, parent: Optional[MPTTNode] = None):
        if parent and not self._children:
            raise ValueError("'parent' argument is not allowed because MPTT is empty")

        if parent:
            parent_node = self._get_node(parent)
            if not parent_node:
                raise ValueError(f"node with id '{parent.id}' doesn't exist")
            parent_node.insert_node(node)
        else:
            if self._root:
                node = replace(node, parent_id=self._root.id)
            self._children.append(MPTT(node))

    def _get_node(self, parent: MPTTNode) -> Optional["MPTT"]:
        for node in self._children:
            if node._root and node._root.id == parent.id:
                return node
            child_node = node._get_node(parent)
            if child_node:
                return child_node
        return None

    def nodes(self) -> List[MPTTNode]:
        nodes_list: List[MPTTNode] = []
        left = 1
        for node in self._children:
            child_nodes = node._flatten_nodes(left=left)
            nodes_list += child_nodes
            left = child_nodes[0].right + 1
        return nodes_list

    def _flatten_nodes(self, depth: int = 0, left: int = 0) -> List[MPTTNode]:
        if not self._root:
            raise TypeError("'_flatten_nodes' can't be called on root MPTT instance")

        nodes_list: List[MPTTNode] = []
        root_node = replace(self._root, left=left, right=left + 1, depth=depth)
        nodes_list.append(root_node)
        if self._children:
            for node in self._children:
                nodes_list += node._flatten_nodes(depth=depth + 1, left=left + 1)
            root_node.right = nodes_list[-1].right + 1
        return nodes_list
