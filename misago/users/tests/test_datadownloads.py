import os
from datetime import timedelta

import pytest
from django.core.files import File
from django.utils import timezone

from ...notifications.models import Notification
from ..audittrail import create_user_audit_trail
from ..datadownloads import (
    expire_user_data_download,
    prepare_user_data_download,
    request_user_data_download,
    user_has_data_download_request,
)
from ..models import DataDownload
from ..test import AuthenticatedUserTestCase

EXPIRATION = 4
TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_FILE_PATH = os.path.join(TESTFILES_DIR, "avatar.png")


class ExpireUserDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_marks_download_as_expired(self):
        """expire_user_data_download changed data download status to expired"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        with open(TEST_FILE_PATH, "rb") as download_file:
            data_download.file = File(download_file)
            data_download.save()

        expire_user_data_download(data_download)

        self.assertEqual(data_download.status, DataDownload.STATUS_EXPIRED)

    def test_util_deletes_file(self):
        """expire_user_data_download deleted file associated with download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        with open(TEST_FILE_PATH, "rb") as download_file:
            data_download.file = File(download_file)
            data_download.save()

        download_file_path = data_download.file.path

        expire_user_data_download(data_download)

        self.assertFalse(data_download.file)
        self.assertFalse(os.path.isdir(download_file_path))

    def test_util_expires_download_without_file(self):
        """expire_user_data_download handles missing download file"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        expire_user_data_download(data_download)

        self.assertEqual(data_download.status, DataDownload.STATUS_EXPIRED)


def test_prepare_user_data_download_prepares_basic_download_file(user):
    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_sets_future_expiration_date(user):
    expires_on = timezone.now() + timedelta(hours=EXPIRATION)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.expires_on > expires_on


def test_prepare_user_data_download_includes_user_profile_fields(user):
    user.profile_fields = {"real_name": "Bob Boberthon!"}
    user.save()

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_tmp_avatar(user):
    with open(TEST_FILE_PATH, "rb") as test_file:
        user.avatar_tmp = File(test_file)
        user.save()

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_src_avatar(user):
    with open(TEST_FILE_PATH, "rb") as test_file:
        user.avatar_src = File(test_file)
        user.save()

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_avatar_set(user):
    with open(TEST_FILE_PATH, "rb") as test_file:
        user.avatar_set.create(size=100, image=File(test_file))

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_file_attachment(
    attachment_factory, text_file, user
):
    attachment_factory(text_file, uploader=user)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_image_attachment(
    attachment_factory, image_small, user
):
    attachment_factory(image_small, uploader=user)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_image_thumbnail_attachment(
    attachment_factory, image_large, user
):
    attachment_factory(image_large, uploader=user)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_self_username_change(user):
    user.record_name_change(user, "aerith", "alice")

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_username_changed_by_staff(admin, user):
    user.record_name_change(admin, "aerith", "alice")

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_username_changed_by_deleted_user(user):
    user.record_name_change(user, "aerith", "alice")
    user.namechanges.update(changed_by=None)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_audit_trail(user):
    create_user_audit_trail(user, "127.0.0.1", user)

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_notification(user):
    Notification.objects.create(user=user, verb="TEST")

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


def test_prepare_user_data_download_includes_post(user, user_thread):
    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


@pytest.mark.xfail(reason="post edits broken by `misago.posts` introduction")
def test_prepare_user_data_download_includes_own_post_edit(
    default_category, user, user_thread
):
    post = user_thread.first_post

    post.edits_record.create(
        category=default_category,
        thread=user_thread,
        editor=user,
        editor_name=user.username,
        editor_slug=user.slug,
        edited_from="edited from",
        edited_to="edited to",
    )

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


@pytest.mark.xfail(reason="post edits broken by `misago.posts` introduction")
def test_prepare_user_data_download_includes_other_users_post_edit(
    default_category, user, thread
):
    post = thread.first_post

    post.edits_record.create(
        category=default_category,
        thread=thread,
        editor=user,
        editor_name=user.username,
        editor_slug=user.slug,
        edited_from="edited from",
        edited_to="edited to",
    )

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


@pytest.mark.xfail(reason="post edits broken by `misago.posts` introduction")
def test_prepare_user_data_download_includes_own_post_edit_by_other_user(
    default_category, user, moderator, user_thread
):
    post = user_thread.first_post

    post.edits_record.create(
        category=default_category,
        thread=user_thread,
        editor=moderator,
        editor_name=moderator.username,
        editor_slug=moderator.slug,
        edited_from="edited from",
        edited_to="edited to",
    )

    download = request_user_data_download(user)
    assert prepare_user_data_download(download, EXPIRATION)

    download.refresh_from_db()
    assert download.file


class RequestUserDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_creates_data_download_for_user_with_them_as_requester(self):
        """request_user_data_download created valid data download for user"""
        data_download = request_user_data_download(self.user)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, self.user)
        self.assertEqual(data_download.requester_name, self.user.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)

    def test_util_creates_data_download_for_user_explicit_requester(self):
        """
        request_user_data_download created valid data download
        for user with other requester
        """
        requester = self.get_superuser()
        data_download = request_user_data_download(self.user, requester)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, requester)
        self.assertEqual(data_download.requester_name, requester.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)


class UserHasRequestedDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_returns_false_for_no_download(self):
        """
        user_has_data_download_request returns false if user has no requests in progress
        """
        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_false_for_ready_download(self):
        """user_has_data_download_request returns false if user has ready download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        data_download.save()

        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_false_for_expired_download(self):
        """user_has_data_download_request returns false if user has expired download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_EXPIRED
        data_download.save()

        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_true_for_pending_download(self):
        """user_has_data_download_request returns true if user has pending download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PENDING
        data_download.save()

        self.assertTrue(user_has_data_download_request(self.user))

    def test_util_returns_true_for_processing_download(self):
        """
        user_has_data_download_request returns true if user has processing download
        """
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PROCESSING
        data_download.save()

        self.assertTrue(user_has_data_download_request(self.user))
