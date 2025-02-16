import os

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
from .themes import THEME_CACHE
from .threads.models import Thread, ThreadParticipant
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
    return reply_thread(
        thread,
        poster="Ghost",
        posted_on=timezone.now(),
        message="I am reply",
    )


@pytest.fixture
def hidden_reply(thread):
    return reply_thread(
        thread,
        poster="Ghost",
        posted_on=timezone.now(),
        message="I am hidden reply",
        is_hidden=True,
    )


@pytest.fixture
def unapproved_reply(thread):
    return reply_thread(
        thread,
        poster="Ghost",
        posted_on=timezone.now(),
        message="I am unapproved reply",
        is_unapproved=True,
    )


@pytest.fixture
def user_reply(thread, user):
    return reply_thread(
        thread,
        poster=user,
        posted_on=timezone.now(),
        message="I am user reply",
    )


@pytest.fixture
def user_hidden_reply(thread, user):
    return reply_thread(
        thread,
        poster=user,
        posted_on=timezone.now(),
        message="I am user hidden reply",
        is_hidden=True,
    )


@pytest.fixture
def user_unapproved_reply(thread, user):
    return reply_thread(
        thread,
        poster=user,
        posted_on=timezone.now(),
        message="I am user unapproved reply",
        is_unapproved=True,
    )


@pytest.fixture
def other_user_reply(thread, other_user):
    return reply_thread(
        thread,
        poster=other_user,
        posted_on=timezone.now(),
        message="I am other user reply",
    )


@pytest.fixture
def other_user_hidden_reply(thread, other_user):
    return reply_thread(
        thread,
        poster=other_user,
        posted_on=timezone.now(),
        message="I am user hidden reply",
        is_hidden=True,
    )


@pytest.fixture
def other_user_unapproved_reply(thread, other_user):
    return reply_thread(
        thread,
        poster=other_user,
        posted_on=timezone.now(),
        message="I am other user unapproved reply",
        is_unapproved=True,
    )


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
def user_private_thread(private_threads_category, user, other_user, moderator):
    thread = post_thread(
        private_threads_category,
        "User Private Thread",
        poster=user,
    )

    ThreadParticipant.objects.create(thread=thread, user=user, is_owner=True)
    ThreadParticipant.objects.create(thread=thread, user=other_user, is_owner=False)
    ThreadParticipant.objects.create(thread=thread, user=moderator, is_owner=False)

    return thread


@pytest.fixture
def other_user_private_thread(private_threads_category, user, other_user, moderator):
    thread = post_thread(
        private_threads_category,
        "Other User Private Thread",
        poster=other_user,
    )

    ThreadParticipant.objects.create(thread=thread, user=other_user, is_owner=True)
    ThreadParticipant.objects.create(thread=thread, user=user, is_owner=False)
    ThreadParticipant.objects.create(thread=thread, user=moderator, is_owner=False)

    return thread


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
        name="text.txt",
        slug="text-txt",
        size=1024 * 1024,
        filetype_id="txt",
    )


@pytest.fixture
def broken_image_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="image.png",
        slug="image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def broken_video_attachment(db):
    return Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="video.mp4",
        slug="video-mp4",
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
        name="user-text.txt",
        slug="user-text-txt",
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
        name="user-image.png",
        slug="user-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def user_broken_video_attachment(user):
    return Attachment.objects.create(
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        uploaded_at=timezone.now(),
        name="user-video.mp4",
        slug="user-video-mp4",
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
        name="other_user-text.txt",
        slug="other_user-text-txt",
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
        name="other_user-image.png",
        slug="other_user-image-png",
        upload="attachments/other_user-image.png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def other_user_video_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other_user-video.mp4",
        slug="other_user-video-mp4",
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
        name="other_user-text.txt",
        slug="other_user-text-txt",
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
        name="other_user-image.png",
        slug="other_user-image-png",
        size=1024 * 1024,
        dimensions="200x200",
        filetype_id="png",
    )


@pytest.fixture
def other_user_broken_video_attachment(other_user):
    return Attachment.objects.create(
        uploader=other_user,
        uploader_name=other_user.username,
        uploader_slug=other_user.slug,
        uploaded_at=timezone.now(),
        name="other_user-video.mp4",
        slug="other_user-video-mp4",
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
