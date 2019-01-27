from ..categories import (
    fake_category,
    fake_category_description,
    fake_category_name,
    fake_closed_category,
)


def test_fake_category_can_be_created(fake, root_category):
    assert fake_category(fake, root_category)


def test_fake_category_is_created_with_specified_parent(fake, default_category):
    category = fake_category(fake, default_category)
    assert category.parent == default_category


def test_fake_category_can_be_created_with_copy_of_other_category_acls(
    fake, root_category, default_category
):
    category = fake_category(fake, root_category, copy_acl_from=default_category)
    for acl in default_category.category_role_set.all():
        category.category_role_set.get(role=acl.role, category_role=acl.category_role)


def test_fake_closed_category_can_be_created(fake, root_category):
    category = fake_closed_category(fake, root_category)
    assert category.is_closed


def test_fake_category_name_can_be_created(fake):
    assert fake_category_name(fake)


def test_different_fake_category_name_is_created_every_time(fake):
    fake_names = [fake_category_name(fake) for i in range(5)]
    assert len(fake_names) == len(set(fake_names))


def test_fake_category_description_can_be_created(fake):
    assert fake_category_description(fake)


def test_different_fake_category_description_is_created_every_time(fake):
    fake_descriptions = [fake_category_description(fake) for i in range(5)]
    assert len(fake_descriptions) == len(set(fake_descriptions))
