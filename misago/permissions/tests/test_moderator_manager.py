from ..models import Moderator


def test_moderator_manager_get_moderator_data_returns_empty_data_for_user_if_none_exist(
    user,
):
    data = Moderator.objects.get_moderator_data(user)
    assert not data.is_global
    assert not data.categories_ids


def test_moderator_manager_get_moderator_data_returns_categories_ids_for_user(
    root_category, child_category, user
):
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[root_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_data(user)
    assert not data.is_global
    assert data.categories_ids == set([root_category.id, child_category.id])


def test_moderator_manager_get_moderator_data_sums_categories_ids_for_user(
    root_category, child_category, user
):
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[root_category.id],
    )
    Moderator.objects.create(
        is_global=False,
        user=user,
        categories=[root_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_data(user)
    assert not data.is_global
    assert data.categories_ids == set([root_category.id, child_category.id])


def test_moderator_manager_get_moderator_data_returns_global_flag_for_user(user):
    Moderator.objects.create(is_global=True, user=user)

    data = Moderator.objects.get_moderator_data(user)
    assert data.is_global
    assert not data.categories_ids


def test_moderator_manager_get_moderator_data_returns_categories_ids_for_user_group(
    root_category, child_category, user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[root_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_data(user)
    assert not data.is_global
    assert data.categories_ids == set([root_category.id, child_category.id])


def test_moderator_manager_get_moderator_data_sums_categories_ids_for_user_group(
    root_category, child_category, user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[root_category.id],
    )
    Moderator.objects.create(
        is_global=False,
        group=custom_group,
        categories=[root_category.id, child_category.id],
    )

    data = Moderator.objects.get_moderator_data(user)
    assert not data.is_global
    assert data.categories_ids == set([root_category.id, child_category.id])


def test_moderator_manager_get_moderator_data_returns_global_flag_for_user_group(
    user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    Moderator.objects.create(is_global=True, group=custom_group)

    data = Moderator.objects.get_moderator_data(user)
    assert data.is_global
    assert not data.categories_ids
