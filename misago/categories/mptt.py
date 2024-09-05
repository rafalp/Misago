from .models import Category

MPTTData = tuple[int, int, int]


def heal_category_trees() -> int:
    trees: set[int] = set()
    categories: dict[int, dict] = {}

    queryset = Category.objects.values(
        "id",
        "parent_id",
        "tree_id",
        "level",
        "lft",
        "rght",
    ).order_by("tree_id", "lft")

    for category in queryset:
        trees.add(category["tree_id"])
        categories[category["id"]] = category

    healthy_categories: list[dict] = []
    for tree_id in trees:
        healthy_categories += heal_tree(tree_id, categories)

    updates = 0
    for healed_category in healthy_categories:
        org_category = categories[healed_category["id"]]
        if org_category != healed_category:
            Category.objects.filter(id=healed_category["id"]).update(
                level=healed_category["level"],
                lft=healed_category["lft"],
                rght=healed_category["rght"],
            )
            updates += 1

    return updates


def heal_tree(tree_id: int, categories: dict[int, dict]) -> list[dict]:
    tree_categories = {
        c["id"]: c.copy() for c in categories.values() if c["tree_id"] == tree_id
    }
    tree_categories_list = list(tree_categories.values())

    cursor = 0
    for category in tree_categories_list:
        if category["parent_id"]:
            continue

        category["level"] = 0
        cursor += 1
        category["lft"] = cursor
        category["rght"] = cursor = heal_category(category, tree_categories_list) + 1

    return sorted(tree_categories_list, key=lambda i: i["lft"])


def heal_category(category: dict, tree_categories_list: list[dict]) -> int:
    cursor = category["lft"]
    for child in tree_categories_list:
        if child["parent_id"] != category["id"]:
            continue

        child["level"] = category["level"] + 1

        cursor += 1
        child["lft"] = cursor
        child["rght"] = cursor = heal_category(child, tree_categories_list) + 1

    return cursor
