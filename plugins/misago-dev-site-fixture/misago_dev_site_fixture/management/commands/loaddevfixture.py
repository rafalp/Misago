from datetime import timedelta
from random import randint
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone
from misago.cache.enums import CacheName
from misago.cache.versions import get_cache_versions, invalidate_cache
from misago.categories.models import Category
from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.models import Setting
from misago.permissions.enums import CategoryPermission
from misago.permissions.models import CategoryGroupPermission
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post, Thread
from misago.users.enums import DefaultGroupId
from misago.users.models import Ban, Group, Rank
from misago.users.setupnewuser import setup_new_user

User = get_user_model()


class Command(BaseCommand):
    help = "Populates the database with test data."

    def handle(self, *args, **options):
        Setting.objects.change_setting("forum_address", "http://localhost:8000")

        invalidate_cache(CacheName.SETTINGS)

        root = Category.objects.root_category()

        Category.objects.filter(slug="first-category").update(color="#0ea5e9")

        second_category = Category(
            name="Second category",
            slug="second-category",
            color="#a855f7",
        )
        second_category.insert_at(root, position="last-child", save=True)

        third_category = Category(
            name="Third category",
            slug="third-category",
            color="#84cc16",
        )
        third_category.insert_at(root, position="last-child", save=True)

        child_category = Category(
            name="Child category",
            slug="child-category",
            color="#fbbf24",
        )
        child_category.insert_at(third_category, position="last-child", save=True)

        deep_category = Category(
            name="Deep child",
            slug="deep-child",
            color="#f43f5e",
        )
        deep_category.insert_at(child_category, position="last-child", save=True)

        second_child_category = Category(
            name="Second child",
            slug="second-child",
            color="#818cf8",
        )
        second_child_category.insert_at(
            third_category, position="last-child", save=True
        )

        vanilla_category = Category(
            name="Vanilla category",
            slug="vanilla-category",
            is_vanilla=True,
            color="#e879f9",
        )
        vanilla_category.insert_at(root, position="last-child", save=True)

        vanilla_child_category = Category(
            name="Vanilla child",
            slug="vanilla-category",
            color="#2dd4bf",
        )
        vanilla_child_category.insert_at(
            vanilla_category, position="last-child", save=True
        )

        new_categories = (
            second_category,
            third_category,
            child_category,
            second_child_category,
            deep_category,
            vanilla_category,
            vanilla_child_category,
        )

        for category in new_categories:
            for group in Group.objects.all():
                for permission in CategoryPermission:
                    CategoryGroupPermission.objects.create(
                        category=category,
                        group=group,
                        permission=permission,
                    )

        invalidate_cache(CacheName.CATEGORIES)
        invalidate_cache(CacheName.PERMISSIONS)

        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)
        default_rank = Rank.objects.get_default()
        members_group = Group.objects.get(id=DefaultGroupId.MEMBERS)

        moderator = User.objects.create_user(
            "Moderator",
            "moderator@example.com",
            "password",
            group=Group.objects.get(id=DefaultGroupId.MODERATORS),
            title="Moderator",
            rank=default_rank,
        )

        moderator.update_acl_key()
        setup_new_user(settings, moderator)

        user = User.objects.create_user(
            "User",
            "user@example.com",
            "password",
            group=members_group,
            rank=default_rank,
        )

        user.update_acl_key()
        setup_new_user(settings, user)

        other_user = User.objects.create_user(
            "OtherUser",
            "other@example.com",
            "password",
            group=members_group,
            rank=default_rank,
        )

        other_user.update_acl_key()
        setup_new_user(settings, other_user)

        banned_user = User.objects.create_user(
            "Banned",
            "banned@example.com",
            "password",
            group=members_group,
            rank=default_rank,
        )

        banned_user.update_acl_key()
        setup_new_user(settings, banned_user)

        Ban.objects.create(check_type=Ban.USERNAME, banned_value="Banned")

        invalidate_cache(CacheName.BANS)

        timestamp = timezone.now()

        first_category = (
            Category.objects.filter(tree_id=root.tree_id, level__gt=root.level)
            .order_by("lft")
            .first()
        )

        previous_year_timestamp = timestamp.replace(
            year=timestamp.year - 1,
            month=randint(1, 10),
            day=randint(1, 28),
            hour=randint(0, 23),
            minute=randint(0, 59),
            second=randint(0, 59),
        )

        previous_year_thread = Thread.objects.create(
            category=first_category,
            title="Thread with last activity from previous year",
            slug="thread-with-last-activity-from-previous-year",
            started_on=previous_year_timestamp,
            last_post_on=previous_year_timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )
        previous_year_post = Post.objects.create(
            category=first_category,
            thread=previous_year_thread,
            poster=None,
            poster_name="Misago",
            posted_on=previous_year_timestamp,
            updated_on=previous_year_timestamp,
        )

        previous_year_thread.first_post = previous_year_thread.last_post = previous_year_post
        previous_year_thread.save()

        previous_year_post.original = (
            "This thread shows timestamps for content from another year."
        )

        previous_year_post.parsed = (
            "<p>This thread shows timestamps for content from another year.</p>"
        )

        previous_year_post.search_document = previous_year_post.original

        update_post_checksum(previous_year_post)
        previous_year_post.update_search_vector()
        previous_year_post.save()

        current_year_timestamp = timestamp.replace(
            month=randint(1, timestamp.month),
            day=randint(1, 28),
            hour=randint(0, 23),
            minute=randint(0, 59),
            second=randint(0, 59),
        )

        current_year_thread = Thread.objects.create(
            category=first_category,
            title="Thread with last activity from current year",
            slug="thread-with-last-activity-from-current-year",
            started_on=current_year_timestamp,
            last_post_on=current_year_timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )
        current_year_post = Post.objects.create(
            category=first_category,
            thread=current_year_thread,
            poster=None,
            poster_name="Misago",
            posted_on=current_year_timestamp,
            updated_on=current_year_timestamp,
        )

        current_year_thread.first_post = current_year_thread.last_post = current_year_post
        current_year_thread.save()

        current_year_post.original = (
            "This thread shows timestamps for content from current year."
        )

        current_year_post.parsed = (
            "<p>This thread shows timestamps for content from current year.</p>"
        )

        current_year_post.search_document = current_year_post.original

        update_post_checksum(current_year_post)
        current_year_post.update_search_vector()
        current_year_post.save()

        current_week_timestamp = timestamp.replace(
            hour=randint(0, 23),
            minute=randint(0, 59),
            second=randint(0, 59),
        ) - timedelta(days=3)

        current_week_thread = Thread.objects.create(
            category=first_category,
            title="Thread with last activity from current week",
            slug="thread-with-last-activity-from-current-week",
            started_on=current_week_timestamp,
            last_post_on=current_week_timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )
        current_week_post = Post.objects.create(
            category=first_category,
            thread=current_week_thread,
            poster=None,
            poster_name="Misago",
            posted_on=current_week_timestamp,
            updated_on=current_week_timestamp,
        )

        current_week_thread.first_post = current_week_thread.last_post = current_week_post
        current_week_thread.save()

        current_week_post.original = (
            "This thread shows timestamps for content from current week."
        )

        current_week_post.parsed = (
            "<p>This thread shows timestamps for content from current week.</p>"
        )

        current_week_post.search_document = current_week_post.original

        update_post_checksum(current_week_post)
        current_week_post.update_search_vector()
        current_week_post.save()

        yesterday_timestamp = timestamp.replace(
            hour=randint(0, 15),
            minute=randint(0, 59),
            second=randint(0, 59),
        ) - timedelta(days=1)

        yesterday_thread = Thread.objects.create(
            category=first_category,
            title="Thread with last activity from yesterday",
            slug="thread-with-last-activity-from-yesterday-week",
            started_on=yesterday_timestamp,
            last_post_on=yesterday_timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )
        yesterday_post = Post.objects.create(
            category=first_category,
            thread=yesterday_thread,
            poster=None,
            poster_name="Misago",
            posted_on=yesterday_timestamp,
            updated_on=yesterday_timestamp,
        )

        yesterday_thread.first_post = yesterday_thread.last_post = yesterday_post
        yesterday_thread.save()

        yesterday_post.original = (
            "This thread shows timestamps for content from yesterday."
        )

        yesterday_post.parsed = (
            "<p>This thread shows timestamps for content from yesterday.</p>"
        )

        yesterday_post.search_document = yesterday_post.original

        update_post_checksum(yesterday_post)
        yesterday_post.update_search_vector()
        yesterday_post.save()

        readme_thread = Thread.objects.create(
            category=first_category,
            title="Welcome to the Misago Dev Fixture! Read me first!",
            slug="welcome-to-the-misago-dev-fixture-read-me-first",
            started_on=timestamp,
            last_post_on=timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )
        readme_post = Post.objects.create(
            category=first_category,
            thread=readme_thread,
            poster=None,
            poster_name="Misago",
            posted_on=timestamp,
            updated_on=timestamp,
        )

        readme_thread.first_post = readme_thread.last_post = readme_post
        readme_thread.save()

        readme_post.original = dedent(
            """
            This Misago site was pre-populated with some initial data to make starting development easier:

            - Example categories hierarchy
            - Threads with activity from different times
            - Moderator account
            - Two regular user accounts
            - Banned user account

            ## Extra user accounts

            In addition to the default "Admin" account, the following accounts are available:

            ### Moderator

            Global moderator.

            - Username: `Moderator`
            - Email: `moderator@example.com`
            - Password: `password`

            ### User

            Regular user.

            - Username: `User`
            - Email: `user@example.com`
            - Password: `password`

            ### Other user

            Another regular user.

            - Username: `OtherUser`
            - Email: `other@example.com`
            - Password: `password`

            ### Banned user

            Permanently banned user.

            - Username: `Banned`
            - Email: `banned@example.com`
            - Password: `password`
            """
        ).strip()

        readme_post.parsed = (
            "<p>This Misago site was pre-populated with some initial data to make starting development easier:</p>"
            "<ul>"
            "<li>Example categories hierarchy</li>"
            "<li>Threads with activity from different times</li>"
            "<li>Moderator account</li>"
            "<li>Two regular user accounts</li>"
            "<li>Banned user account</li>"
            "</ul>"
            "<h2>Extra user accounts</h2>"
            "<p>In addition to the default &quot;Admin&quot; account, the following accounts are available:</p>"
            "<h3>Moderator</h3>"
            "<p>Global moderator.</p>"
            "<ul>"
            "<li>Username: <code>Moderator</code></li>"
            "<li>Email: <code>moderator@example.com</code></li>"
            "<li>Password: <code>password</code></li>"
            "</ul>"
            "<h3>User</h3>"
            "<p>Regular user.</p>"
            "<ul>"
            "<li>Username: <code>User</code></li>"
            "<li>Email: <code>user@example.com</code></li>"
            "<li>Password: <code>password</code></li>"
            "</ul>"
            "<h3>Other user</h3>"
            "<p>Another regular user.</p>"
            "<ul>"
            "<li>Username: <code>OtherUser</code></li>"
            "<li>Email: <code>other@example.com</code></li>"
            "<li>Password: <code>password</code></li>"
            "</ul>"
            "<h3>Banned user</h3>"
            "<p>Permanently banned user.</p>"
            "<ul>"
            "<li>Username: <code>Banned</code></li>"
            "<li>Email: <code>banned@example.com</code></li>"
            "<li>Password: <code>password</code></li>"
            "</ul>"
        ).strip()

        readme_post.search_document = (
            "This Misago site was pre-populated with some initial data to make starting development easier: "
            "- Example categories hierarchy "
            "- Threads with activity from different times "
            "- Moderator account "
            "- Two regular user accounts "
            "- Banned user account "
            "## Extra user accounts "
            'In addition to the default "Admin" account, the following accounts are available: '
            "### Moderator "
            "Global moderator. "
            "- Username: `Moderator` "
            "- Email: `moderator@example.com` "
            "- Password: `password` "
            "### User "
            "Regular user. "
            "- Username: `User` "
            "- Email: `user@example.com` "
            "- Password: `password` "
            "### Other user "
            "Another regular user. "
            "- Username: `OtherUser` "
            "- Email: `other@example.com` "
            "- Password: `password` "
            "### Banned user "
            "Permanently banned user. "
            "- Username: `Banned` "
            "- Email: `banned@example.com` "
            "- Password: `password`"
        ).strip()

        update_post_checksum(readme_post)
        readme_post.update_search_vector()
        readme_post.save()

        first_category.threads = models.F("threads") + 4
        first_category.posts = models.F("posts") + 4
        first_category.set_last_thread(readme_thread)
        first_category.save()

        self.stdout.write(
            self.style.SUCCESS("Database has been populated with additional data.")
        )
