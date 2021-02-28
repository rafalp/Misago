from dataclasses import replace
from typing import Dict, List, Optional, Sequence, Union

from ..types import Category
from .update import update_category


class CategoryTreeNode:
    _root: Category
    _children: List["CategoryTreeNode"]

    def __init__(self, root: Category):
        self._root = root
        self._children = []

    def insert_node(self, node: Category):
        node = replace(node, parent_id=self._root.id)
        self._children.append(CategoryTreeNode(node))

    def get_category(self, category_id: int) -> Optional[Category]:
        if self._root and self._root.id == category_id:
            return self._root

        for node in self._children:
            category = node.get_category(category_id)
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

    def flatten_node(
        self, depth: int = 0, left: int = 0, parent_id: Optional[int] = None
    ) -> List[Category]:
        nodes_list: List[Category] = []
        root_node = replace(
            self._root, left=left, right=left + 1, depth=depth, parent_id=parent_id
        )
        nodes_list.append(root_node)
        if self._children:
            for i, node in enumerate(self._children):
                nodes_list += node.flatten_node(
                    depth=depth + 1, left=left + (i * 2) + 1, parent_id=root_node.id
                )
            root_node.right = nodes_list[-1].right + 1
        return nodes_list


class CategoryTree(CategoryTreeNode):
    _map: Dict[int, Category]

    def __init__(self, categories: Sequence[Category]):
        self._children = []
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

    def get_category(self, category_id: int) -> Optional[Category]:
        return self._map.get(category_id)


async def insert_category(
    categories: Sequence[Category],
    category: Category,
    parent: Optional[Category] = None,
) -> Category:
    tree = CategoryTree(categories)
    tree.insert_node(category, parent)

    categories_map = {c.id: c for c in categories}
    categories_map[category.id] = category

    validate_categories(categories_map, category, parent=parent)

    if parent and parent.id not in categories_map:
        raise ValueError(f"Parent category '{parent}' doesn't exist.")

    updated_categories: Dict[int, Category] = {}
    for updated_category in tree.get_list():
        old_category = categories_map[updated_category.id]
        if updated_category == old_category:
            updated_categories[old_category.id] = old_category
            continue

        parent_category: Union[Category, bool] = False
        if updated_category.parent_id:
            parent_category = categories_map[updated_category.parent_id]

        updated_categories[old_category.id] = await update_category(
            old_category,
            parent=parent_category,
            depth=updated_category.depth,
            left=updated_category.left,
            right=updated_category.right,
        )

    return updated_categories[category.id]


async def move_category(
    categories: Sequence[Category],
    category: Category,
    *,
    parent: Optional[Category] = None,
    before: Optional[Category] = None,
) -> Category:
    categories_map = {c.id: c for c in categories}
    categories_map[category.id] = category

    category_children = [c for c in categories if c.is_child(category)]

    validate_categories(categories_map, category, parent=parent, before=before)

    tree = CategoryTree([])
    for c in categories:
        if before and before.id == c.id:
            tree.insert_node(category, parent)
            for child in category_children:
                tree.insert_node(child, category)

        if c.id != category.id and not c.is_child(category):
            if c.parent_id:
                tree.insert_node(c, categories_map[c.parent_id])
            else:
                tree.insert_node(c)

    if not before:
        tree.insert_node(category, parent)
        for child in category_children:
            tree.insert_node(child, category)

    updated_categories: Dict[int, Category] = {}
    for updated_category in tree.get_list():
        old_category = categories_map[updated_category.id]
        if updated_category == old_category:
            updated_categories[old_category.id] = old_category
            continue

        parent_category: Union[Category, bool] = False
        if updated_category.parent_id:
            parent_category = categories_map[updated_category.parent_id]

        updated_categories[old_category.id] = await update_category(
            old_category,
            parent=parent_category,
            depth=updated_category.depth,
            left=updated_category.left,
            right=updated_category.right,
        )

    return updated_categories[category.id]


class CategoryTreeValidationError(ValueError):
    pass


def validate_categories(
    categories_map: Dict[int, Category],
    category: Category,
    *,
    parent: Optional[Category] = None,
    before: Optional[Category] = None,
):
    if parent:
        if parent.id not in categories_map:
            raise CategoryTreeValidationError(
                f"Parent category '{parent}' doesn't exist."
            )
        if parent.id == category.id:
            raise CategoryTreeValidationError(
                f"Category '{category}' can't be its own parent."
            )
        if parent.is_child(category):
            raise CategoryTreeValidationError(
                f"Category '{category}' can't use its own child as parent."
            )

    if before:
        if before.id not in categories_map:
            raise CategoryTreeValidationError(
                f"Before category '{before}' doesn't exist."
            )
        if before.id == category.id:
            raise CategoryTreeValidationError(
                f"Category '{category}' can't be moved before itself."
            )
        if (parent and before.parent_id != parent.id) or (
            not parent and before.parent_id
        ):
            raise CategoryTreeValidationError(
                f"Category '{category}' be moved before {before} "
                "because both have different parents."
            )
