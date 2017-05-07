from misago.acl import add_acl
from misago.readtracker import categoriestracker

from .models import Category


def get_categories_tree(user, parent=None, join_posters=False):
    if not user.acl_cache['visible_categories']:
        return []

    if parent:
        queryset = parent.get_descendants().order_by('lft')
    else:
        queryset = Category.objects.all_categories()

    queryset_with_acl = queryset.filter(id__in=user.acl_cache['visible_categories'])
    if join_posters:
        queryset_with_acl = queryset_with_acl.select_related('last_poster')

    visible_categories = list(queryset_with_acl)

    categories_dict = {}
    categories_list = []

    parent_level = parent.level + 1 if parent else 1

    for category in visible_categories:
        category.subcategories = []
        categories_dict[category.pk] = category
        categories_list.append(category)

        if category.parent_id and category.level > parent_level:
            categories_dict[category.parent_id].subcategories.append(category)

    add_acl(user, categories_list)
    categoriestracker.make_read_aware(user, categories_list)

    for category in reversed(visible_categories):
        if category.acl['can_browse']:
            category.parent = categories_dict.get(category.parent_id)
            if category.parent:
                category.parent.threads += category.threads
                category.parent.posts += category.posts

                if category.parent.last_post_on and category.last_post_on:
                    parent_last_post = category.parent.last_post_on
                    category_last_post = category.last_post_on
                    update_last_thead = parent_last_post < category_last_post
                elif not category.parent.last_post_on and category.last_post_on:
                    update_last_thead = True
                else:
                    update_last_thead = False

                if update_last_thead:
                    category.parent.last_post_on = category.last_post_on
                    category.parent.last_thread_id = category.last_thread_id
                    category.parent.last_thread_title = category.last_thread_title
                    category.parent.last_thread_slug = category.last_thread_slug
                    category.parent.last_poster_name = category.last_poster_name
                    category.parent.last_poster_slug = category.last_poster_slug

                if not category.is_read:
                    category.parent.is_read = False

    flat_list = []
    for category in categories_list:
        if category.level == parent_level:
            flat_list.append(category)
    return flat_list


def get_category_path(category):
    if category.special_role:
        return [category]

    category_path = []
    while category and category.level > 0:
        category_path.append(category)
        category = category.parent
    return [f for f in reversed(category_path)]
