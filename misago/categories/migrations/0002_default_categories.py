from django.db import migrations

from ...core.utils import slugify
from ..enums import CategoryTreeDeprecated

_ = lambda s: s


def create_default_categories_tree(apps, schema_editor):
    Category = apps.get_model("misago_categories", "Category")

    Category.objects.create(
        special_role="private_threads",
        name="Private",
        slug="private",
        lft=1,
        rght=2,
        tree_id=CategoryTreeDeprecated.PRIVATE_THREADS,
        level=0,
    )

    root = Category.objects.create(
        special_role="root_category",
        name="Root",
        slug="root",
        lft=3,
        rght=6,
        tree_id=CategoryTreeDeprecated.THREADS,
        level=0,
    )

    category_name = _("First category")

    Category.objects.create(
        parent=root,
        lft=4,
        rght=5,
        tree_id=1,
        level=CategoryTreeDeprecated.THREADS,
        name=category_name,
        slug=slugify(category_name),
    )


class Migration(migrations.Migration):
    dependencies = [("misago_categories", "0001_initial")]

    operations = [migrations.RunPython(create_default_categories_tree)]
