# Generated by Django 4.2.7 on 2023-12-19 18:07

from django.db import migrations

from ..enums import CategoryTree, CategoryTreeDeprecated


def change_default_categories_trees_ids(apps, schema_editor):
    # Swaps tree ids for threads and private threads around
    Category = apps.get_model("misago_categories", "Category")
    Category.objects.filter(tree_id=CategoryTreeDeprecated.THREADS).update(
        tree_id=CategoryTree.THREADS
    )
    Category.objects.filter(special_role="private_threads").update(
        tree_id=CategoryTree.PRIVATE_THREADS
    )


class Migration(migrations.Migration):
    dependencies = [
        ("misago_categories", "0011_plugin_data"),
    ]

    operations = [migrations.RunPython(change_default_categories_trees_ids)]
