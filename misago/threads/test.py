from misago.acl.test import patch_user_acl
from misago.categories.models import Category

default_category_acl = {
    'can_see': 1,
    'can_browse': 1,
    'can_see_all_threads': 1,
    'can_see_own_threads': 0,
    'can_hide_threads': 0,
    'can_approve_content': 0,
    'can_edit_posts': 0,
    'can_hide_posts': 0,
    'can_hide_own_posts': 0,
    'can_merge_threads': 0,
    'can_close_threads': 0,
}


def patch_category_acl(acl_patch):
    def patch_acl(_, user_acl):
        category = Category.objects.get(slug="first-category")
        category_acl = user_acl['categories'][category.id]
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)

    return patch_user_acl(patch_acl)


def patch_other_category_acl(acl_patch):
    def patch_acl(_, user_acl):
        src_category = Category.objects.get(slug="first-category")
        category_acl = user_acl['categories'][src_category.id].copy()

        dst_category = Category.objects.get(slug="other-category")
        user_acl['categories'][dst_category.id] = category_acl

        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)

        cleanup_patched_acl(user_acl, category_acl, dst_category)

    return patch_user_acl(patch_acl)


def create_category_acl_patch(category_slug, acl_patch):
    def created_category_acl_patch(_, user_acl):
        category = Category.objects.get(slug=category_slug)
        category_acl = user_acl['categories'].get(category.id, {})
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)
    
    return created_category_acl_patch


def cleanup_patched_acl(user_acl, category_acl, category):
    visible_categories = user_acl['visible_categories']
    browseable_categories = user_acl['browseable_categories']

    if not category_acl['can_see'] and category.id in visible_categories:
        visible_categories.remove(category.id)

    if not category_acl['can_see'] and category.id in browseable_categories:
        browseable_categories.remove(category.id)

    if not category_acl['can_browse'] and category.id in browseable_categories:
        browseable_categories.remove(category.id)

    if category_acl['can_see'] and category.id not in visible_categories:
        visible_categories.append(category.id)

    if category_acl['can_browse'] and category.id not in browseable_categories:
        browseable_categories.append(category.id)
