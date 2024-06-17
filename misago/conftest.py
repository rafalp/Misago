import pytest
from django.utils import timezone

from .acl import ACL_CACHE, useracl
from .admin.auth import authorize_admin
from .cache.enums import CacheName
from .categories.models import Category
from .conf import SETTINGS_CACHE
from .conf.dynamicsettings import DynamicSettings
from .conf.staticsettings import StaticSettings
from .menus import MENU_ITEMS_CACHE
from .notifications.models import WatchedThread
from .socialauth import SOCIALAUTH_CACHE
from .test import MisagoClient
from .themes import THEME_CACHE
from .threads.models import Thread
from .threads.test import post_thread, reply_thread
from .users import BANS_CACHE
from .users.enums import DefaultGroupId
from .users.models import AnonymousUser, Group, GroupDescription
from .users.test import create_test_superuser, create_test_user


def get_cache_versions():
    return {
        CacheName.CATEGORIES: "abcdefgh",
        CacheName.GROUPS: "abcdefgh",
        CacheName.MODERATORS: "abcdefgh",
        CacheName.PERMISSIONS: "abcdefgh",
        ACL_CACHE: "abcdefgh",
        BANS_CACHE: "abcdefgh",
        SETTINGS_CACHE: "abcdefgh",
        SOCIALAUTH_CACHE: "abcdefgh",
        THEME_CACHE: "abcdefgh",
        MENU_ITEMS_CACHE: "abcdefgh",
    }


@pytest.fixture
def cache_versions():
    return get_cache_versions()


@pytest.fixture
def dynamic_settings(db, cache_versions):
    return DynamicSettings(cache_versions)


@pytest.fixture
def settings():
    return StaticSettings()


@pytest.fixture
def user_password():
    return "p4ssw0rd!"


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def anonymous_user_acl(anonymous_user, cache_versions):
    return useracl.get_user_acl(anonymous_user, cache_versions)


@pytest.fixture
def user(db, user_password):
    return create_test_user("User", "user@example.com", user_password)


@pytest.fixture
def user_acl(user, cache_versions):
    return useracl.get_user_acl(user, cache_versions)


@pytest.fixture
def other_user(db, user_password):
    return create_test_user("Other_User", "otheruser@example.com", user_password)


@pytest.fixture
def other_user_acl(other_user, cache_versions):
    return useracl.get_user_acl(other_user, cache_versions)


@pytest.fixture
def staffuser(db, user_password):
    return create_test_user(
        "Staff_User", "staffuser@example.com", user_password, is_staff=True
    )


@pytest.fixture
def staffuser_acl(staffuser, cache_versions):
    return useracl.get_user_acl(staffuser, cache_versions)


@pytest.fixture
def other_staffuser(db, user_password):
    return create_test_user(
        "Other_Staff_User", "otherstaffuser@example.com", user_password, is_staff=False
    )


@pytest.fixture
def superuser(db, user_password):
    return create_test_user(
        "Super_User",
        "superuser@example.com",
        user_password,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin(db, user_password):
    user = create_test_superuser("Admin_User", "adminuser@example.com", user_password)
    user.is_staff = False
    user.is_superuser = False
    user.is_misago_root = False
    user.save()
    return user


@pytest.fixture
def other_admin(db, user_password):
    user = create_test_superuser("Other_Admin", "otheradmin@example.com", user_password)
    user.is_staff = False
    user.is_superuser = False
    user.is_misago_root = False
    user.save()
    return user


@pytest.fixture
def secondary_admin(db, user_password, admins_group, members_group):
    user = create_test_user("Second_Admin", "secondary@example.com", user_password)
    user.set_groups(members_group, [admins_group])
    user.save()
    return user


@pytest.fixture
def root_admin(db, user_password):
    user = create_test_superuser("Root_Admin", "rootadmin@example.com", user_password)
    user.is_staff = False
    user.is_superuser = False
    user.save()
    return user


@pytest.fixture
def other_root_admin(db, user_password):
    user = create_test_superuser("Other_Root", "otherroot@example.com", user_password)
    user.is_staff = False
    user.is_superuser = False
    user.save()
    return user


@pytest.fixture
def inactive_user(db, user_password):
    return create_test_user(
        "Inactive_User", "inactiveuser@example.com", user_password, is_active=False
    )


@pytest.fixture
def admins_group(db):
    return Group.objects.get(id=DefaultGroupId.ADMINS)


@pytest.fixture
def moderators_group(db):
    return Group.objects.get(id=DefaultGroupId.MODERATORS)


@pytest.fixture
def members_group(db):
    return Group.objects.get(id=DefaultGroupId.MEMBERS)


@pytest.fixture
def guests_group(db):
    return Group.objects.get(id=DefaultGroupId.GUESTS)


@pytest.fixture
def custom_group(db):
    group = Group.objects.create(
        name="Custom Group",
        slug="custom-group",
        ordering=4,
    )
    group.description = GroupDescription.objects.create(group=group)
    return group


@pytest.fixture
def client():
    return MisagoClient()


@pytest.fixture
def user_client(client, user):
    client.force_login(user)
    session = client.session
    session.save()
    return client


@pytest.fixture
def admin_client(mocker, client, admin):
    client.force_login(admin)
    session = client.session
    authorize_admin(mocker.Mock(session=session, user=admin))
    session.save()
    return client


@pytest.fixture
def root_admin_client(mocker, client, root_admin):
    client.force_login(root_admin)
    session = client.session
    authorize_admin(mocker.Mock(session=session, user=root_admin))
    session.save()
    return client


@pytest.fixture
def staff_client(mocker, client, staffuser):
    client.force_login(staffuser)
    session = client.session
    authorize_admin(mocker.Mock(session=session, user=staffuser))
    session.save()
    return client


@pytest.fixture
def root_category(db):
    return Category.objects.root_category()


@pytest.fixture
def private_threads_category(db):
    return Category.objects.private_threads()


@pytest.fixture
def default_category(db):
    return Category.objects.get(slug="first-category")


@pytest.fixture
def thread(default_category):
    return post_thread(default_category)


@pytest.fixture
def other_thread(default_category):
    return post_thread(default_category)


@pytest.fixture
def hidden_thread(default_category):
    return post_thread(default_category, is_hidden=True)


@pytest.fixture
def unapproved_thread(default_category):
    return post_thread(default_category, is_unapproved=True)


@pytest.fixture
def post(thread):
    return thread.first_post


@pytest.fixture
def reply(thread):
    return reply_thread(thread, poster="Ghost", posted_on=timezone.now())


@pytest.fixture
def user_reply(thread, user):
    return reply_thread(thread, poster=user, posted_on=timezone.now())


@pytest.fixture
def other_user_reply(thread, other_user):
    return reply_thread(thread, poster=other_user, posted_on=timezone.now())


@pytest.fixture
def user_thread(default_category, user):
    return post_thread(default_category, poster=user)


@pytest.fixture
def user_hidden_thread(default_category, user):
    return post_thread(default_category, poster=user, is_hidden=True)


@pytest.fixture
def user_unapproved_thread(default_category, user):
    return post_thread(default_category, poster=user, is_unapproved=True)


@pytest.fixture
def other_user_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user)


@pytest.fixture
def other_user_hidden_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user, is_hidden=True)


@pytest.fixture
def other_user_unapproved_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user, is_unapproved=True)


@pytest.fixture
def private_thread(private_threads_category):
    return post_thread(private_threads_category)


@pytest.fixture
def private_thread_reply(private_thread):
    return reply_thread(private_thread, poster="Ghost", posted_on=timezone.now())


@pytest.fixture
def private_thread_user_reply(private_thread, user):
    return reply_thread(private_thread, poster=user, posted_on=timezone.now())


@pytest.fixture
def user_private_thread(user, private_threads_category):
    return post_thread(private_threads_category, poster=user)


@pytest.fixture
def categories_tree(root_category):
    sibling_category = Category(
        name="Sibling Category",
        slug="sibling-category",
    )

    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(
        name="Child Category",
        slug="child-category",
        color="#FF0000",
    )

    child_category.insert_at(sibling_category, position="last-child", save=True)

    other_category = Category(
        name="Other Category",
        slug="other-category",
        short_name="Other",
    )

    other_category.insert_at(root_category, position="last-child", save=True)


@pytest.fixture
def sibling_category(categories_tree):
    return Category.objects.get(slug="sibling-category")


@pytest.fixture
def child_category(categories_tree):
    return Category.objects.get(slug="child-category")


@pytest.fixture
def other_category(categories_tree):
    return Category.objects.get(slug="other-category")


@pytest.fixture
def watched_thread_factory():
    def create_watched_thread(user: "User", thread: "Thread", send_emails: bool):
        return WatchedThread.objects.create(
            user=user,
            category_id=thread.category_id,
            thread=thread,
            send_emails=send_emails,
        )

    return create_watched_thread
