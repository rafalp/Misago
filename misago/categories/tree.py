from dataclasses import replace
from typing import Dict, List, Optional, Sequence, Tuple

from ..types import Category
from .update import update_category


class CategoryTreeNode:
    _root: Optional[Category] = None
    _children: List["CategoriesTree"]

    def __init__(self, root: Optional[Category] = None):
        self._root = root
        self._children = []

    def insert_node(self, node: Category):
        node = replace(node, parent_id=self._root.id)
        self._children.append(CategoryTreeNode(node))

    def get_category(self, id: int) -> Optional[Category]:
        if self._root and self._root.id == id:
            return self._root

        for node in self._children:
            category = node.get_category(id)
            if category:
                return category
        return None

    def get_node(self, category: Category) -> Optional["CategoryTreeNode"]:
        for node in self._children:
            if node._root and node._root.id == category.id:
                return node
            child_node = node.get_node(category)
            if child_node:
                return child_node
        return None

    def flatten_node(self, depth: int = 0, left: int = 0) -> List[Category]:
        nodes_list: List[Category] = []
        root_node = replace(self._root, left=left, right=left + 1, depth=depth)
        nodes_list.append(root_node)
        if self._children:
            for i, node in enumerate(self._children):
                nodes_list += node.flatten_node(
                    depth=depth + 1, left=left + (i * 2) + 1
                )
            root_node.right = nodes_list[-1].right + 1
        return nodes_list


class CategoryTree(CategoryTreeNode):
    _map: Dict[int, Category]

    def __init__(self, categories: Sequence[Category]):
        super().__init__()

        self._map = {}

        category_map = {c.id: c for c in categories}
        for category in categories:
            if category.parent_id:
                self.insert_node(category, category_map[category.parent_id])
            else:
                self.insert_node(category)

    def insert_node(self, node: Category, parent: Optional[Category] = None):
        if parent:
            parent_node = self.get_node(parent)
            if not parent_node:
                raise ValueError(f"node with id '{parent.id}' doesn't exist")
            parent_node.insert_node(node)
        else:
            self._children.append(CategoryTreeNode(node))

        self._map[node.id] = node

    def get_list(self) -> List[Category]:
        nodes_list: List[Category] = []
        left = 1
        for node in self._children:
            child_nodes = node.flatten_node(left=left)
            nodes_list += child_nodes
            left = child_nodes[0].right + 1
        return nodes_list

    def get_category(self, id: int) -> Optional[Category]:
        return self._map.get(id)


async def insert_category(
    categories: Sequence[Category],
    category: Category,
    parent: Optional[Category] = None,
) -> Category:
    tree = CategoryTree(categories)
    tree.insert_node(category, parent)

    categories_map = {c.id: c for c in categories}
    categories_map[category.id] = category

    result = None

    for updated_category in tree.get_list():
        old_category = categories_map[updated_category.id]
        if updated_category == old_category:
            continue

        if updated_category.parent_id:
            parent_category = categories_map.get(updated_category.parent_id)
        else:
            parent_category = None

        saved_category = await update_category(
            old_category,
            parent=parent_category,
            depth=updated_category.depth,
            left=updated_category.left,
            right=updated_category.right,
        )

        if saved_category.id == category.id:
            result = saved_category

    return result
