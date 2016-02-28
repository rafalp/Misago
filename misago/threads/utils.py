def add_categories_to_threads(categories, threads):
    categories_dict = {}
    for category in categories:
        categories_dict[category.pk] = category

    top_categories_map = {}

    for thread in threads:
        thread.category = categories_dict[thread.category_id]

        if thread.category == categories[0]:
            thread.top_category = None
        elif thread.category.parent_id == categories[0].pk:
            thread.top_category = thread.category
        elif thread.category_id in top_categories_map:
            thread.top_category = top_categories_map[thread.category_id]
        else:
            for category in categories:
                if (category.parent_id == categories[0].pk and
                        category.has_child(thread.category)):
                    top_categories_map[thread.category_id] = category
                    thread.top_category = category
