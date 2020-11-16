import random

from ..categories.models import Category, RoleCategoryACL


def fake_category(fake, parent, copy_acl_from=None):
    category = Category()
    category.set_name(fake_category_name(fake))

    if random.randint(1, 100) > 50:
        category.description = fake_category_description(fake)

    category.insert_at(parent, position="last-child", save=True)

    if copy_acl_from:
        copy_acl_to_fake_category(copy_acl_from, category)

    return category


def fake_closed_category(fake, parent, copy_acl_from=None):
    category = fake_category(fake, parent, copy_acl_from)
    category.is_closed = True
    category.save(update_fields=["is_closed"])

    return category


def copy_acl_to_fake_category(source, category):
    copied_acls = []
    for acl in source.category_role_set.all():
        copied_acls.append(
            RoleCategoryACL(
                role_id=acl.role_id,
                category=category,
                category_role_id=acl.category_role_id,
            )
        )

    if copied_acls:
        RoleCategoryACL.objects.bulk_create(copied_acls)


def fake_category_name(fake):
    if random.randint(1, 100) > 75:
        return fake.catch_phrase().title()
    return fake.street_name()


def fake_category_description(fake):
    if random.randint(1, 100) > 80:
        return "\r\n".join(fake.paragraphs())
    return fake.paragraph()
