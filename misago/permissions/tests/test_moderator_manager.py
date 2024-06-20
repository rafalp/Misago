from ..models import Moderator


def test_moderator_manager_get_moderator_permissions_returns_empty_data_for_user_if_none_exist(
    user,
):
    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert not data.categories_ids


def test_moderator_manager_get_moderator_permissions_returns_categories_ids_for_user(
    sibling_category, child_category, user
):
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[sibling_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert data.categories_ids == set([sibling_category.id, child_category.id])


def test_moderator_manager_get_moderator_permissions_sums_categories_ids_for_user(
    sibling_category, child_category, user
):
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[sibling_category.id],
    )
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[sibling_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert data.categories_ids == set([sibling_category.id, child_category.id])


def test_moderator_manager_get_moderator_permissions_returns_global_flag_for_user(user):
    Moderator.objects.create(is_global=True, user=user)

    data = Moderator.objects.get_moderator_permissions(user)
    assert data.is_global
    assert not data.categories_ids


def test_moderator_manager_get_moderator_permissions_returns_categories_ids_for_user_group(
    sibling_category, child_category, user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[sibling_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert data.categories_ids == set([sibling_category.id, child_category.id])


def test_moderator_manager_get_moderator_permissions_sums_categories_ids_for_user_group(
    sibling_category, child_category, user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[sibling_category.id],
    )
    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[sibling_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert data.categories_ids == set([sibling_category.id, child_category.id])


def test_moderator_manager_get_moderator_permissions_returns_global_flag_for_user_group(
    user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(is_global=True, group=custom_group)

    data = Moderator.objects.get_moderator_permissions(user)
    assert data.is_global
    assert not data.categories_ids


def test_moderator_manager_get_moderator_permissions_returns_private_threads_flag_for_user(
    user,
):
    Moderator.objects.create(is_global=False, private_threads=True, user=user)

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert not data.categories_ids
    assert data.private_threads


def test_moderator_manager_get_moderator_permissions_returns_global_flag_for_user_group(
    user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(is_global=False, private_threads=True, group=custom_group)

    data = Moderator.objects.get_moderator_permissions(user)
    assert not data.is_global
    assert not data.categories_ids
    assert data.private_threads
