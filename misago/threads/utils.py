def add_categories_to_threads(root_category, categories, threads):
    categories_dict = {}
    for category in categories:
        categories_dict[category.pk] = category

    top_categories_map = {}

    for thread in threads:
        thread.top_category = None
        thread.category = categories_dict[thread.category_id]

        if thread.category == root_category:
            continue
        elif thread.category.parent_id == root_category.pk:
            thread.top_category = thread.category
        elif thread.category_id in top_categories_map:
            thread.top_category = top_categories_map[thread.category_id]
        elif root_category.has_child(thread.category):
            # thread in subcategory resolution
            for category in categories:
                if (category.parent_id == root_category.pk and
                        category.has_child(thread.category)):
                    top_categories_map[thread.category_id] = category
                    thread.top_category = category
        else:
            # global thread in other category resolution
            for category in categories:
                if category.level == 1 and (
                        category == thread.category or
                        category.has_child(thread.category)):
                    top_categories_map[thread.category_id] = category
                    thread.top_category = category
