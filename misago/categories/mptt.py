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

    healed_categories: list[dict] = []
    for tree_id in trees:
        healed_categories += heal_tree(tree_id, categories)

    update_categories: list[Category] = []
    for healed_category in healed_categories:
        org_category = categories[healed_category["id"]]
        if org_category != healed_category:
            update_categories.append(Category(**healed_category))

    if not update_categories:
        return 0

    return Category.objects.bulk_update(
        update_categories,
        ("level", "lft", "rght"),
    )


def heal_tree(tree_id: int, categories: dict[int, dict]) -> list[dict]:
    healed_categories: list[dict] = []
    categories_branches: dict[int, list[dict]] = {0: []}
    for category in categories.values():
        if category["tree_id"] != tree_id:
            category_copy = category.copy()
            healed_categories.append(category_copy)
            categories_branches[category["parent_id"] or 0].append(category_copy)
            categories_branches[category["id"]] = []

    mptt_data = list(range(1, (len(categories) * 2) + 1))
    for category in categories_branches[0]:
        heal_category(category, categories_branches, mptt_data, level=0)

    return healed_categories


def heal_category(
    category: dict,
    categories_branches: dict[int, list[dict]],
    mptt_data: list[int],
    level: int,
):
    category["level"] = level
    category["lft"] = mptt_data.pop(0)
    for child in categories_branches[category["id"]]:
        heal_category(child, categories_branches, mptt_data, level + 1)
    category["rght"] = mptt_data.pop(0)
