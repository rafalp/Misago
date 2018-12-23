import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import migrations, models

from ...acl.models import permissions_default


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("misago_acl", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "special_role",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.CharField(max_length=255)),
                ("description", models.TextField(null=True, blank=True)),
                ("is_closed", models.BooleanField(default=False)),
                ("threads", models.PositiveIntegerField(default=0)),
                ("posts", models.PositiveIntegerField(default=0)),
                (
                    "last_thread_title",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "last_thread_slug",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "last_poster_name",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "last_poster_slug",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("last_post_on", models.DateTimeField(null=True, blank=True)),
                ("prune_started_after", models.PositiveIntegerField(default=0)),
                ("prune_replied_after", models.PositiveIntegerField(default=0)),
                ("css_class", models.CharField(max_length=255, null=True, blank=True)),
                ("lft", models.PositiveIntegerField(editable=False, db_index=True)),
                ("rght", models.PositiveIntegerField(editable=False, db_index=True)),
                ("tree_id", models.PositiveIntegerField(editable=False, db_index=True)),
                ("level", models.PositiveIntegerField(editable=False, db_index=True)),
                (
                    "archive_pruned_in",
                    models.ForeignKey(
                        related_name="pruned_archive",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="misago_categories.Category",
                        null=True,
                    ),
                ),
                (
                    "last_poster",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        related_name="children",
                        on_delete=django.db.models.deletion.CASCADE,
                        blank=True,
                        to="misago_categories.Category",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="CategoryRole",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "special_role",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("permissions", JSONField(default=permissions_default)),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="RoleCategoryACL",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        related_name="category_role_set",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "category_role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.CategoryRole",
                        to_field="id",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        related_name="categories_acls",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_acl.Role",
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
