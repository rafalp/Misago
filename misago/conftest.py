import random
import os
from datetime import timedelta

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from .acl import ACL_CACHE, useracl
from .admin.auth import authorize_admin
from .attachments.models import Attachment
from .attachments.filetypes import filetypes
from .cache.enums import CacheName
from .categories.models import Category
from .conf import SETTINGS_CACHE
from .conf.dynamicsettings import DynamicSettings
from .conf.staticsettings import StaticSettings
from .core.utils import slugify
from .menus import MENU_ITEMS_CACHE
from .notifications.models import WatchedThread
from .permissions.models import Moderator
from .privatethreads.models import PrivateThreadMember
from .socialauth import SOCIALAUTH_CACHE
from .socialauth.models import SocialAuthProvider
from .test import (
    IMAGE_INVALID,
    IMAGE_LARGE,
    IMAGE_SMALL,
    TEXT_FILE,
    MisagoClient,
    teardown_attachments,
)
from .test.categories import category_relations_factory
from .test.time import *
from .test.polls import *
from .test.posts import *
from .test.threads import thread_factory, thread_relations_factory
from .test.threadupdates import *
from .test.userpermissions import *
from .themes import THEME_CACHE
from .threads.models import Thread
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
def category_moderator(db, user_password, default_category):
    user = create_test_user("Moderator", "moderator@example.com", user_password)

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    return user


@pytest.fixture
def moderator(db, user_password, moderators_group):
    user = create_test_user("Moderator", "moderator@example.com", user_password)
    user.set_groups(moderators_group)
    user.save()
    return user


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
def other_user_client(client, other_user):
    client.force_login(other_user)
    session = client.session
    session.save()
    return client


@pytest.fixture
def moderator_client(client, moderator):
    client.force_login(moderator)
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
def thread(thread_factory, default_category):
    thread = thread_factory(default_category)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def other_thread(thread_factory, default_category):
    thread = thread_factory(default_category)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def hidden_thread(thread_factory, default_category):
    thread = thread_factory(default_category, is_hidden=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def unapproved_thread(thread_factory, default_category):
    thread = thread_factory(default_category, is_unapproved=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def post(thread):
    return thread.first_post


@pytest.fixture
def reply(thread_reply_factory, thread):
    reply = thread_reply_factory(
        thread,
        poster="Reply",
        original="I am reply",
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def hidden_reply(thread_reply_factory, thread):
    reply = thread_reply_factory(
        thread,
        poster="HiddenPoster",
        original="I am hidden reply",
        is_hidden=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def unapproved_reply(thread_reply_factory, thread):
    reply = thread_reply_factory(
        thread,
        poster="UnapprovedPoster",
        original="I am unapproved reply",
        is_unapproved=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def user_reply(thread_reply_factory, thread, user):
    reply = thread_reply_factory(
        thread,
        poster=user,
        original="I am user reply",
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def user_hidden_reply(thread_reply_factory, thread, user):
    reply = thread_reply_factory(
        thread,
        poster=user,
        original="I am user hidden reply",
        is_hidden=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def user_unapproved_reply(thread_reply_factory, thread, user):
    reply = thread_reply_factory(
        thread,
        poster=user,
        original="I am user unapproved reply",
        is_unapproved=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def other_user_reply(thread_reply_factory, thread, other_user):
    reply = thread_reply_factory(
        thread,
        poster=other_user,
        original="I am other user reply",
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def other_user_hidden_reply(thread_reply_factory, thread, other_user):
    reply = thread_reply_factory(
        thread,
        poster=other_user,
        original="I am user hidden reply",
        is_hidden=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def other_user_unapproved_reply(thread_reply_factory, thread, other_user):
    reply = thread_reply_factory(
        thread,
        poster=other_user,
        original="I am other user unapproved reply",
        is_unapproved=True,
    )

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def user_thread(thread_factory, default_category, user):
    thread = thread_factory(default_category, starter=user)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def user_hidden_thread(thread_factory, default_category, user):
    thread = thread_factory(default_category, starter=user, is_hidden=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def user_unapproved_thread(thread_factory, default_category, user):
    thread = thread_factory(default_category, starter=user, is_unapproved=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def other_user_thread(thread_factory, default_category, other_user):
    thread = thread_factory(default_category, starter=other_user)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def other_user_hidden_thread(thread_factory, default_category, other_user):
    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def other_user_unapproved_thread(thread_factory, default_category, other_user):
    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def old_thread(thread_factory, default_category):
    thread = thread_factory(default_category, started_at=-3600)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def old_user_thread(thread_factory, default_category, user):
    thread = thread_factory(default_category, started_at=-3600, starter=user)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def old_other_user_thread(thread_factory, default_category, other_user):
    thread = thread_factory(default_category, started_at=-3600, starter=other_user)

    default_category.synchronize()
    default_category.save()

    return thread


@pytest.fixture
def old_thread_reply(thread_reply_factory, old_thread):
    reply = thread_reply_factory(old_thread)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_thread_user_reply(thread_reply_factory, old_thread, user):
    reply = thread_reply_factory(old_thread, poster=user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_thread_other_user_reply(thread_reply_factory, old_thread, other_user):
    reply = thread_reply_factory(old_thread, poster=other_user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_user_thread_reply(thread_reply_factory, old_user_thread):
    reply = thread_reply_factory(old_user_thread)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_user_thread_user_reply(thread_reply_factory, old_user_thread, user):
    reply = thread_reply_factory(old_user_thread, poster=user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_user_thread_other_user_reply(thread_reply_factory, old_user_thread, other_user):
    reply = thread_reply_factory(old_user_thread, poster=other_user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_other_user_thread_reply(thread_reply_factory, old_other_user_thread):
    reply = thread_reply_factory(old_other_user_thread)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_other_user_thread_user_reply(thread_reply_factory, old_other_user_thread, user):
    reply = thread_reply_factory(old_other_user_thread, poster=user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def old_other_user_thread_other_user_reply(
    thread_reply_factory, old_other_user_thread, other_user
):
    reply = thread_reply_factory(old_other_user_thread, poster=other_user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def private_thread(thread_factory, private_threads_category):
    thread = thread_factory(private_threads_category)

    private_threads_category.synchronize()
    private_threads_category.save()

    return thread


@pytest.fixture
def private_thread_post(private_thread):
    return private_thread.first_post


@pytest.fixture
def private_thread_reply(thread_reply_factory, private_thread):
    reply = thread_reply_factory(private_thread, poster="Ghost")

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def private_thread_user_reply(thread_reply_factory, private_thread, user):
    reply = thread_reply_factory(private_thread, poster=user)

    reply.category.synchronize()
    reply.category.save()

    return reply


@pytest.fixture
def user_private_thread(
    thread_factory, private_threads_category, user, other_user, moderator
):
    thread = thread_factory(
        private_threads_category,
        title="User Private Thread",
        starter=user,
    )

    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=True)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=False)
    PrivateThreadMember.objects.create(thread=thread, user=moderator, is_owner=False)

    private_threads_category.synchronize()
    private_threads_category.save()

    return thread


@pytest.fixture
def other_user_private_thread(
    thread_factory, private_threads_category, user, other_user, moderator
):
    thread = thread_factory(
        private_threads_category,
        title="Other User Private Thread",
        starter=other_user,
    )

    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)
    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=False)
    PrivateThreadMember.objects.create(thread=thread, user=moderator, is_owner=False)

    private_threads_category.synchronize()
    private_threads_category.save()

    return thread


@pytest.fixture
def old_private_thread(thread_factory, private_threads_category):
    thread = thread_factory(private_threads_category, started_at=-3600)

    private_threads_category.synchronize()
    private_threads_category.save()

    return thread


@pytest.fixture
def old_private_thread_user_reply(thread_reply_factory, old_private_thread, user):
    reply = thread_reply_factory(old_private_thread, poster=user)

    reply.category.synchronize()
    reply.category.save()

    return reply


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
        thread_age = timezone.now() - thread.started_at
        if thread_age.total_seconds() < 10:
            raise ValueError(
                "'thread' passed to 'watched_thread_factory' must be "
                "at least 10 seconds old"
            )

        read_time = thread.started_at + timedelta(
            seconds=random.randint(1, int(thread_age.total_seconds()) - 1),
        )

        return WatchedThread.objects.create(
            user=user,
            category_id=thread.category_id,
            thread=thread,
            send_emails=send_emails,
            read_time=read_time,
        )

    return create_watched_thread


@pytest.fixture
def attachment_factory(db, teardown_attachments):
    def _attachment_factory(
        file_path: str,
        *,
        name=None,
        uploader=None,
        post=None,
        thumbnail_path=None,
        is_deleted=False,
    ):
        name = name or str(os.path.split(file_path)[-1])
        filetype = filetypes.match_filetype(name)
        content_type = filetype.content_types[0]
        assert filetype, f"'{name}' is not supported"

        with open(file_path, "rb") as fp:
            upload = SimpleUploadedFile(name, fp.read(), content_type)

        if thumbnail_path:
            thumbnail_filename = str(os.path.split(thumbnail_path)[-1])
            thumbnail_filetype = filetypes.match_filetype(name)
            thumbnail_content_type = thumbnail_filetype.content_types[0]
            assert thumbnail_filetype, f"'{thumbnail_filename}' is not supported"

            with open(thumbnail_path, "rb") as fp:
                thumbnail = SimpleUploadedFile(
                    thumbnail_filename, fp.read(), thumbnail_content_type
                )
                thumbnail_size = thumbnail.size
        else:
            thumbnail = None
            thumbnail_size = 0

        return Attachment.objects.create(
            category_id=post.category_id if post else None,
            thread_id=post.thread_id if post else None,
            post=post,
            uploader=uploader,
            uploader_name=uploader.username if uploader else "Anonymous",
            uploader_slug=uploader.slug if uploader else "anonymous",
            uploaded_at=timezone.now(),
            name=name,
            slug=slugify(name),
            filetype_id=filetype.id,
            upload=upload,
            size=upload.size,
            thumbnail=thumbnail,
            thumbnail_size=thumbnail_size,
            is_deleted=is_deleted,
        )

    return _attachment_factory


@pytest.fixture
def image_invalid():
    return IMAGE_INVALID


@pytest.fixture
def image_large():
    return IMAGE_LARGE


@pytest.fixture
def image_small():
    return IMAGE_SMALL


@pytest.fixture
def text_file():
    return TEXT_FILE


@pytest.fixture
def text_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="text.txt",
        slug="text-txt",
        upload="attachments/text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def image_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="image.png",
        slug="image-png",
        upload="attachments/image.png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def image_thumbnail_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="image-with-thumbnail.png",
        slug="image-with-thumbnail-png",
        upload="attachments/image-with-thumbnail.png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail="attachments/image-thumbnail.png",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def video_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="video.mp4",
        slug="video-mp4",
        upload="attachments/video.mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def broken_text_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="broken-text.txt",
        slug="broken-text-txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def broken_image_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="broken-image.png",
        slug="broken-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def broken_image_thumbnail_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="broken-image-with-thumbnail.png",
        slug="broken-image-with-thumbnail-png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def broken_video_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="broken-video.mp4",
        slug="broken-video-mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def user_text_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-text.txt",
        slug="user-text-txt",
        upload="attachments/user-text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def user_image_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-image.png",
        slug="user-image-png",
        upload="attachments/user-image.png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def user_image_thumbnail_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-image-with-thumbnail.png",
        slug="user-image-with-thumbnail-png",
        upload="attachments/user-image-with-thumbnail.png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail="attachments/user-image-thumbnail.png",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def user_video_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-video.mp4",
        slug="user-video-mp4",
        upload="attachments/user-video.mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def user_broken_text_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-broken-text.txt",
        slug="user-broken-text-txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def user_broken_image_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-broken-image.png",
        slug="user-broken-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def user_broken_image_thumbnail_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-broken-image-with-thumbnail.png",
        slug="user-broken-image-with-thumbnail-png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def user_broken_video_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-broken-video.mp4",
        slug="user-broken-video-mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def other_user_text_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-text.txt",
        slug="other-user-text-txt",
        upload="attachments/other_user-text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def other_user_image_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-image.png",
        slug="other-user-image-png",
        upload="attachments/other_user-image.png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def other_user_image_thumbnail_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-image.png",
        slug="other-user-image-png",
        upload="attachments/other_user-image.png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail="attachments/other-user-image-thumbnail.png",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def other_user_video_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-video.mp4",
        slug="other-user-video-mp4",
        upload="attachments/other_user-video.mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def other_user_broken_text_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-broken-text.txt",
        slug="other-user-broken-text-txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def other_user_broken_image_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-broken-image.png",
        slug="other-user-broken-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def other_user_broken_image_thumbnail_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-broken-image.png",
        slug="other-user-broken-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        thumbnail_size=128 * 1024,
        thumbnail_dimensions="50x50",
        filetype_id="png",
    )


@pytest.fixture
def other_user_broken_video_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other-user-broken-video.mp4",
        slug="other-user-broken-video-mp4",
        size=1024 * 1024,
        filetype_id="mp4",
    )


@pytest.fixture
def social_auth_github(db):
    return SocialAuthProvider.objects.create(
        provider="github",
        is_active=True,
        order=SocialAuthProvider.objects.filter(is_active=True).count(),
    )


@pytest.fixture
def social_auth_facebook(db):
    return SocialAuthProvider.objects.create(
        provider="facebook",
        is_active=True,
        order=SocialAuthProvider.objects.filter(is_active=True).count(),
    )
