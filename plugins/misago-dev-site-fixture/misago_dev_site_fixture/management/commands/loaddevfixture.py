from dataclasses import dataclass
from datetime import datetime, timedelta
from random import choice, randint
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.cache.enums import CacheName
from misago.cache.versions import get_cache_versions, invalidate_cache
from misago.categories.models import Category
from misago.categories.synchronize import synchronize_category
from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.models import Setting
from misago.core.utils import slugify
from misago.permissions.enums import CategoryPermission
from misago.permissions.models import CategoryGroupPermission
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post, Thread
from misago.threads.synchronize import synchronize_thread
from misago.users.enums import DefaultGroupId
from misago.users.models import Ban, Group, Rank
from misago.users.setupnewuser import setup_new_user

User = get_user_model()


@dataclass
class ThreadData:
    category: Category
    title: str
    posts: list["PostData"]
    weight: int = 0
    is_hidden: bool = False
    is_unapproved: bool = False
    is_locked: bool = False


@dataclass
class PostData:
    poster: str
    posted_at: datetime
    original: str
    parsed: str
    is_locked: bool = False
    is_hidden: bool = False
    is_unapproved: bool = False
    hidden_by: str | None = None


DELETED_USER_NAMES = (
    "DeletedUser",
    "Ghost",
    "Mokujin",
    "Bob",
    "Alice",
    "Daniel",
    "Christoph",
    "Ava",
    "Eve",
    "Cloud",
    "032MedicantBias",
)


def random_deleted_user() -> str:
    return choice(DELETED_USER_NAMES)


class Command(BaseCommand):
    help = "Populates the database with test data."

    def handle(self, *args, **options):
        Setting.objects.change_setting("forum_address", "http://localhost:8000")

        invalidate_cache(CacheName.SETTINGS)

        root = Category.objects.root_category()

        first_category = Category.objects.get(slug="first-category")

        first_category.color = "#0ea5e9"
        first_category.save()

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

        def random_registered_user():
            return choice((moderator, user, other_user))

        def random_user():
            return choice([moderator, user, other_user] + list(DELETED_USER_NAMES))

        Ban.objects.create(check_type=Ban.USERNAME, banned_value="Banned")

        invalidate_cache(CacheName.BANS)

        self.stdout.write("Created user accounts.")

        timestamp = timezone.now()

        threads = [
            ThreadData(
                category=first_category,
                title="Thread with last activity from previous year",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now().replace(
                            year=timestamp.year - 1,
                            month=randint(1, 10),
                            day=randint(1, 28),
                            hour=randint(0, 23),
                            minute=randint(0, 59),
                            second=randint(0, 59),
                        ),
                        original="This thread shows timestamps for content from another year.",
                        parsed=(
                            "<p>This thread shows timestamps for content from another year.</p>"
                        ),
                    )
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread with last activity from current year",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now().replace(
                            month=randint(1, timestamp.month),
                            day=randint(1, 28),
                            hour=randint(0, 23),
                            minute=randint(0, 59),
                            second=randint(0, 59),
                        ),
                        original="This thread shows timestamps for content from current year.",
                        parsed=(
                            "<p>This thread shows timestamps for content from current year.</p>"
                        ),
                    )
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread with last activity from current week",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=(
                            timezone.now().replace(
                                hour=randint(0, 23),
                                minute=randint(0, 59),
                                second=randint(0, 59),
                            )
                            - timedelta(days=3)
                        ),
                        original="This thread shows timestamps for content from current week.",
                        parsed=(
                            "<p>This thread shows timestamps for content from current week.</p>"
                        ),
                    )
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread with last activity from yesterday",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now() - timedelta(hours=24),
                        original="This thread shows timestamps for content from yesterday.",
                        parsed=(
                            "<p>This thread shows timestamps for content from yesterday.</p>"
                        ),
                    )
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread with activity by different users",
                posts=[
                    PostData(
                        poster=moderator,
                        posted_at=timezone.now()
                        - timedelta(minutes=(60 * 3) + randint(0, 59)),
                        original="Post by a moderator.",
                        parsed="<p>Post by a moderator.</p>",
                    ),
                    PostData(
                        poster=user,
                        posted_at=timezone.now()
                        - timedelta(minutes=(60 * 2) + randint(0, 59)),
                        original="Post by a registered user.",
                        parsed="<p>Post by a registered user.</p>",
                    ),
                    PostData(
                        poster=banned_user,
                        posted_at=timezone.now()
                        - timedelta(minutes=60 + randint(0, 59)),
                        original="Post by a banned user.",
                        parsed="<p>Post by a banned user.</p>",
                    ),
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 59)),
                        original="Post by a deleted user.",
                        parsed="<p>Post by a deleted user.</p>",
                    ),
                    PostData(
                        poster=other_user,
                        posted_at=timezone.now()
                        - timedelta(minutes=(60 * 2) + randint(0, 59)),
                        original="Post by an other registered user.",
                        parsed="<p>Post by an other registered user.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Pinned thread",
                weight=2,
                posts=[
                    PostData(
                        poster=moderator,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 600)),
                        original="This thread is globally pinned.",
                        parsed="<p>This thread is globally pinned.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread pinned in a category",
                weight=1,
                posts=[
                    PostData(
                        poster=moderator,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 600)),
                        original="This thread is pinned in a category.",
                        parsed="<p>This thread is pinned in a category.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Hidden thread",
                is_hidden=True,
                posts=[
                    PostData(
                        poster=user,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 600)),
                        original="This thread is hidden.",
                        parsed="<p>This thread is hidden.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Unapproved thread",
                is_unapproved=True,
                posts=[
                    PostData(
                        poster=user,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 600)),
                        original="This thread is unapproved.",
                        parsed="<p>This thread is unapproved.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Locked thread",
                is_locked=True,
                posts=[
                    PostData(
                        poster=user,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 600)),
                        original="This thread is locked.",
                        parsed="<p>This thread is locked.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread with different posts states",
                posts=[
                    PostData(
                        poster=user,
                        posted_at=timezone.now()
                        - timedelta(minutes=400 - randint(0, 59)),
                        original="This post is locked.",
                        parsed="<p>This post is locked.</p>",
                        is_locked=True,
                    ),
                    PostData(
                        poster="JohnDoe",
                        posted_at=timezone.now()
                        - timedelta(minutes=300 - randint(0, 59)),
                        original="This post is hidden by deleted user.",
                        parsed="<p>This post is hidden by deleted user.</p>",
                        is_hidden=True,
                        hidden_by="JohnDoe",
                    ),
                    PostData(
                        poster=other_user,
                        posted_at=timezone.now()
                        - timedelta(minutes=200 - randint(0, 59)),
                        original="This post is hidden by the moderator.",
                        parsed="<p>This post is hidden by the moderator.</p>",
                        is_hidden=True,
                        hidden_by=moderator,
                    ),
                    PostData(
                        poster=user,
                        posted_at=timezone.now() - timedelta(minutes=randint(0, 59)),
                        original="This post is unapproved.",
                        parsed="<p>This post is unapproved.</p>",
                        is_unapproved=True,
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Deleted users discussion",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=300 + randint(0, 60)),
                        original="Thread by a deleted user.",
                        parsed="<p>Thread by a deleted user.</p>",
                    ),
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=100 + randint(0, 60)),
                        original="Reply by a deleted user.",
                        parsed="<p>Reply by a deleted user.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread replied by a deleted user",
                posts=[
                    PostData(
                        poster=random_registered_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=300 + randint(0, 60)),
                        original="Thread by a registered user.",
                        parsed="<p>Thread by a registered user.</p>",
                    ),
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=100 + randint(0, 60)),
                        original="Reply by a deleted user.",
                        parsed="<p>Reply by a deleted user.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Thread started by a deleted user",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=300 + randint(0, 60)),
                        original="Thread by a deleted user.",
                        parsed="<p>Thread by a deleted user.</p>",
                    ),
                    PostData(
                        poster=random_registered_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=100 + randint(0, 60)),
                        original="Reply by a registered user.",
                        parsed="<p>Reply by a registered user.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Users thread",
                posts=[
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=300 + randint(0, 60)),
                        original="Original post.",
                        parsed="<p>Original post.</p>",
                    ),
                    PostData(
                        poster=random_deleted_user(),
                        posted_at=timezone.now()
                        - timedelta(minutes=100 + randint(0, 60)),
                        original="Example reply.",
                        parsed="<p>Example reply.</p>",
                    ),
                ],
            ),
            ThreadData(
                category=first_category,
                title="Welcome to the Misago Dev Fixture! Read me first!",
                weight=2,
                posts=[
                    PostData(
                        poster="Misago",
                        posted_at=timezone.now(),
                        original=dedent(
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
                        ).strip(),
                        parsed=(
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
                        ).strip(),
                    ),
                ],
            ),
        ]

        def create_thread_with_specified_length(thread_length: int, title: str):
            timestamps = sorted(
                timezone.now() - timedelta(minutes=randint(0, 600))
                for _ in range(thread_length)
            )

            thread_data = ThreadData(
                category=first_category,
                title=title,
                posts=[],
            )
            threads.append(thread_data)

            for i, timestamp in enumerate(timestamps, 1):
                thread_data.posts.append(
                    PostData(
                        poster=random_user(),
                        posted_at=timestamp,
                        original=f"Post no. {i}",
                        parsed=f"<p>Post no. {i}</p>",
                    )
                )

        create_thread_with_specified_length(
            settings.posts_per_page + settings.posts_per_page_orphans,
            "Thread with max-length single page",
        )
        create_thread_with_specified_length(
            settings.posts_per_page + settings.posts_per_page_orphans + 1,
            "Thread with two pages",
        )
        create_thread_with_specified_length(
            (settings.posts_per_page * 2) + settings.posts_per_page_orphans + 1,
            "Thread with three pages",
        )
        create_thread_with_specified_length(
            (settings.posts_per_page * 4) + settings.posts_per_page_orphans + 1,
            "Thread with five pages",
        )

        # Order threads posts
        for thread in threads:
            thread.posts = sorted(thread.posts, key=lambda p: p.posted_at)

        # Order threads
        threads = sorted(threads, key=lambda t: t.posts[0].posted_at)

        # Create threads
        threads_posts = []
        for thread_data in threads:
            thread = Thread.objects.create(
                category=thread_data.category,
                title=thread_data.title,
                slug=slugify(thread_data.title),
                started_at=thread_data.posts[0].posted_at,
                last_posted_at=thread_data.posts[-1].posted_at,
                starter=None,
                starter_name="Misago",
                starter_slug="misago",
                last_poster=None,
                last_poster_name="Misago",
                last_poster_slug="misago",
                weight=thread_data.weight,
                is_hidden=thread_data.is_hidden,
                is_unapproved=thread_data.is_unapproved,
                is_locked=thread_data.is_locked,
            )

            for post_data in thread_data.posts:
                threads_posts.append((post_data, thread))

        # Order posts
        posts_and_threads = sorted(threads_posts, key=lambda i: i[0].posted_at)

        # Create threads posts
        for post_data, thread in posts_and_threads:
            if isinstance(post_data.poster, str):
                poster = None
                poster_name = post_data.poster
            else:
                poster = post_data.poster
                poster_name = poster.username

            hidden_at = None
            hidden_by = None
            hidden_by_name = None
            hidden_by_slug = None

            if post_data.is_hidden:
                hidden_at = min(
                    post_data.posted_at + timedelta(minutes=randint(10, 80)),
                    timezone.now(),
                )

                if isinstance(post_data.hidden_by, str):
                    hidden_by = None
                    hidden_by_name = post_data.hidden_by
                    hidden_by_slug = slugify(post_data.hidden_by)
                else:
                    hidden_by = post_data.hidden_by
                    hidden_by_name = hidden_by.username
                    hidden_by_slug = hidden_by.slug

            post = Post.objects.create(
                category=thread.category,
                thread=thread,
                poster=poster,
                poster_name=poster_name,
                posted_at=post_data.posted_at,
                original=post_data.original,
                parsed=post_data.parsed,
                is_locked=post_data.is_locked,
                is_hidden=post_data.is_hidden,
                is_unapproved=post_data.is_unapproved,
                hidden_at=hidden_at,
                hidden_by=hidden_by,
                hidden_by_name=hidden_by_name,
                hidden_by_slug=hidden_by_slug,
            )

            post.set_search_document(thread, post_data.original)
            post.set_search_vector()
            post.save()

        for thread in Thread.objects.iterator():
            synchronize_thread(thread)

        for category in Category.objects.iterator():
            synchronize_category(category)

        self.stdout.write("Created demo threads.")

        for user in User.objects.order_by("id").iterator():
            user.threads = user.thread_set.count()
            user.posts = user.post_set.count()
            user.save()

        self.stdout.write("Synchronized user accounts.")

        self.stdout.write(
            self.style.SUCCESS("Database has been populated with development data.")
        )
