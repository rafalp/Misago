from datetime import timedelta
from random import randint
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
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

        self.stdout.write("Created new categories hierarchy.")

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

        self.stdout.write("Created user accounts.")

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

        previous_year_thread.first_post = previous_year_thread.last_post = (
            previous_year_post
        )
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

        current_year_thread.first_post = current_year_thread.last_post = (
            current_year_post
        )
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

        current_week_thread.first_post = current_week_thread.last_post = (
            current_week_post
        )
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

        timestamp = timezone.now() - timedelta(minutes=randint(50, 60))

        thread_with_states = Thread.objects.create(
            category=first_category,
            title="Different post states",
            slug="different-post-states",
            started_on=timestamp,
            last_post_on=timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )

        default_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=user,
            poster_name=user.username,
            posted_on=timestamp,
            updated_on=timestamp,
        )

        default_post.original = "Post in a default state."
        default_post.parsed = "<p>Post in a default state.</p>"
        default_post.search_document = default_post.original

        update_post_checksum(default_post)
        default_post.update_search_vector()
        default_post.save()

        timestamp = timezone.now() - timedelta(minutes=randint(40, 50))

        guest_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=None,
            poster_name="DeletedUser",
            posted_on=timestamp,
            updated_on=timestamp,
        )

        guest_post.original = "Post by a deleted user."
        guest_post.parsed = "<p>Post by a deleted user.</p>"
        guest_post.search_document = guest_post.original

        update_post_checksum(guest_post)
        guest_post.update_search_vector()
        guest_post.save()

        timestamp = timezone.now() - timedelta(minutes=randint(30, 40))

        hidden_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=other_user,
            poster_name=other_user.username,
            posted_on=timestamp,
            updated_on=timestamp,
            is_hidden=True,
        )

        hidden_post.original = "Hidden post."
        hidden_post.parsed = "<p>Hidden post.</p>"
        hidden_post.search_document = hidden_post.original

        update_post_checksum(hidden_post)
        hidden_post.update_search_vector()
        hidden_post.save()

        timestamp = timezone.now() - timedelta(minutes=randint(20, 30))

        unapproved_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=user,
            poster_name=user.username,
            posted_on=timestamp,
            updated_on=timestamp,
            is_hidden=True,
        )

        unapproved_post.original = "Unapproved post."
        unapproved_post.parsed = "<p>Unapproved post.</p>"
        unapproved_post.search_document = unapproved_post.original

        update_post_checksum(unapproved_post)
        unapproved_post.update_search_vector()
        unapproved_post.save()

        timestamp = timezone.now() - timedelta(minutes=randint(10, 20))

        locked_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=banned_user,
            poster_name=banned_user.username,
            posted_on=timestamp,
            updated_on=timestamp,
            is_protected=True,
        )

        locked_post.original = "Locked post by a banned user."
        locked_post.parsed = "<p>Locked post by a banned user.</p>"
        locked_post.search_document = locked_post.original

        update_post_checksum(locked_post)
        locked_post.update_search_vector()
        locked_post.save()

        edited_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=user,
            poster_name=user.username,
            posted_on=timezone.now() - timedelta(minutes=randint(5, 10)),
            updated_on=timezone.now() - timedelta(minutes=randint(1, 5)),
            edits=42,
            last_editor=moderator,
            last_editor_name=moderator.username,
            last_editor_slug=moderator.slug,
        )

        edited_post.original = "Edited post."
        edited_post.parsed = "<p>Edited post.</p>"
        edited_post.search_document = edited_post.original

        update_post_checksum(edited_post)
        edited_post.update_search_vector()
        edited_post.save()

        timestamp = timezone.now() - timedelta(minutes=randint(1, 5))

        moderator_post = Post.objects.create(
            category=first_category,
            thread=thread_with_states,
            poster=moderator,
            poster_name=moderator.username,
            posted_on=timestamp,
            updated_on=timestamp,
        )

        moderator_post.original = "Post by a moderator."
        moderator_post.parsed = "<p>Post by a moderator.</p>"
        moderator_post.search_document = moderator_post.original

        update_post_checksum(moderator_post)
        moderator_post.update_search_vector()
        moderator_post.save()

        thread_with_states.synchronize()
        thread_with_states.save()

        thread_length = settings.posts_per_page + settings.posts_per_page_orphans
        timestamp = timezone.now() - timedelta(minutes=50)

        thread_one_page = Thread.objects.create(
            category=first_category,
            title="Thread with max-length single page",
            slug="thread-with-max-length-single-page",
            started_on=timestamp,
            last_post_on=timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )

        for i in range(thread_length):
            timestamp += timedelta(minutes=randint(0, 3))

            post = Post.objects.create(
                category=first_category,
                thread=thread_one_page,
                poster=None,
                poster_name="Poster",
                posted_on=timestamp,
                updated_on=timestamp,
            )

            post.original = f"Post no. {i + 1}"
            post.parsed = f"<p>Post no. {i + 1}</p>"
            post.search_document = post.original

            update_post_checksum(post)
            post.update_search_vector()
            post.save()

        thread_one_page.synchronize()
        thread_one_page.save()

        thread_length = settings.posts_per_page + settings.posts_per_page_orphans + 1

        thread_two_pages = Thread.objects.create(
            category=first_category,
            title="Thread with two pages",
            slug="thread-with-two-pages",
            started_on=timestamp,
            last_post_on=timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )

        for i in range(thread_length):
            timestamp += timedelta(minutes=randint(0, 3))

            post = Post.objects.create(
                category=first_category,
                thread=thread_two_pages,
                poster=None,
                poster_name="Poster",
                posted_on=timestamp,
                updated_on=timestamp,
            )

            post.original = f"Post no. {i + 1}"
            post.parsed = f"<p>Post no. {i + 1}</p>"
            post.search_document = post.original

            update_post_checksum(post)
            post.update_search_vector()
            post.save()

        thread_two_pages.synchronize()
        thread_two_pages.save()

        thread_length = (
            (settings.posts_per_page * 2) + settings.posts_per_page_orphans + 1
        )

        thread_three_pages = Thread.objects.create(
            category=first_category,
            title="Thread with three pages",
            slug="thread-with-three-pages",
            started_on=timestamp,
            last_post_on=timestamp,
            starter=None,
            starter_name="Misago",
            starter_slug="misago",
            last_poster=None,
            last_poster_name="Misago",
            last_poster_slug="misago",
        )

        for i in range(thread_length):
            timestamp += timedelta(minutes=randint(0, 3))

            post = Post.objects.create(
                category=first_category,
                thread=thread_three_pages,
                poster=None,
                poster_name="Poster",
                posted_on=timestamp,
                updated_on=timestamp,
            )

            post.original = f"Post no. {i + 1}"
            post.parsed = f"<p>Post no. {i + 1}</p>"
            post.search_document = post.original

            update_post_checksum(post)
            post.update_search_vector()
            post.save()

        thread_three_pages.synchronize()
        thread_three_pages.save()

        timestamp = timezone.now()
        posts_to_update = Post.objects.filter(id__gt=yesterday_post.id).order_by("-id")
        for post in posts_to_update.iterator():
            if post.updated_on == post.posted_on:
                post.posted_on = timestamp
                post.updated_on = post.posted_on
            else:
                post.posted_on = timestamp
                post.updated_on = timestamp + timedelta(minutes=randint(1, 10))

            post.save()

            timestamp -= timedelta(minutes=randint(1, 10))

        for thread in Thread.objects.iterator():
            thread.synchronize()
            thread.save()

        timestamp = timezone.now()

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
            - Threads with activity from different dates
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
            "<li>Threads with activity from different dates</li>"
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
            "- Threads with activity from different dates "
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

        first_category.synchronize()
        first_category.save()

        self.stdout.write("Created demo threads.")

        for user in User.objects.order_by("id").iterator():
            user.threads = user.thread_set.count()
            user.posts = user.post_set.count()
            user.save()

        self.stdout.write("Synchronized user accounts.")

        self.stdout.write(
            self.style.SUCCESS("Database has been populated with development data.")
        )
