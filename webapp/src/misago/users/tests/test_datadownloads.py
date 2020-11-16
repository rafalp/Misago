import os
from datetime import timedelta

from django.core.files import File
from django.utils import timezone

from ...categories.models import Category
from ...threads.models import AttachmentType
from ...threads.test import post_poll, post_thread
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


class PrepareUserDataDownload(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.download = request_user_data_download(self.user)

    def assert_download_is_valid(self):
        result = prepare_user_data_download(self.download, EXPIRATION)
        self.assertTrue(result)

        self.download.refresh_from_db()
        self.assertTrue(self.download.file)

    def test_prepare_basic_download(self):
        """function creates data download for basic user account"""
        self.assert_download_is_valid()

    def test_data_download_is_prepared_with_expiration_date(self):
        """function creates data download with specified expiration date"""
        expires_on = timezone.now() + timedelta(hours=EXPIRATION)
        prepare_user_data_download(self.download, EXPIRATION)
        self.download.refresh_from_db
        self.assertGreater(self.download.expires_on, expires_on)

    def test_prepare_download_with_profle_fields(self):
        """function creates data download for user with profile fields"""
        self.user.profile_fields = {"real_name": "Bob Boberthon!"}
        self.user.save()

        self.assert_download_is_valid()

    def test_prepare_download_with_tmp_avatar(self):
        """function creates data download for user with tmp avatar"""
        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.avatar_tmp = File(test_file)
            self.user.save()

        self.assert_download_is_valid()

    def test_prepare_download_with_src_avatar(self):
        """function creates data download for user with src avatar"""
        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.avatar_src = File(test_file)
            self.user.save()

        self.assert_download_is_valid()

    def test_prepare_download_with_avatar_set(self):
        """function creates data download for user with avatar set"""
        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.avatar_set.create(size=100, image=File(test_file))

        self.assert_download_is_valid()

    def test_prepare_download_with_file_attachment(self):
        """function creates data download for user with file attachment"""
        filetype = AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="image/png"
        )

        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.attachment_set.create(
                secret="test",
                filetype=filetype,
                uploader_name=self.user.username,
                uploader_slug=self.user.slug,
                filename="test.png",
                size=1000,
                file=File(test_file),
            )

        self.assert_download_is_valid()

    def test_prepare_download_with_image_attachment(self):
        """function creates data download for user with image attachment"""
        filetype = AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="image/png"
        )

        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.attachment_set.create(
                secret="test",
                filetype=filetype,
                uploader_name=self.user.username,
                uploader_slug=self.user.slug,
                filename="test.png",
                size=1000,
                image=File(test_file),
            )

        self.assert_download_is_valid()

    def test_prepare_download_with_thumbnail_attachment(self):
        """function creates data download for user with thumbnail attachment"""
        filetype = AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="image/png"
        )

        with open(TEST_FILE_PATH, "rb") as test_file:
            self.user.attachment_set.create(
                secret="test",
                filetype=filetype,
                uploader_name=self.user.username,
                uploader_slug=self.user.slug,
                filename="test.png",
                size=1000,
                thumbnail=File(test_file),
            )

        self.assert_download_is_valid()

    def test_prepare_download_with_self_username_change(self):
        """function creates data download for user that changed their username"""
        self.user.record_name_change(self.user, "aerith", "alice")

        self.assert_download_is_valid()

    def test_prepare_download_with_username_changed_by_staff(self):
        """function creates data download for user with username changed by staff"""
        staff_user = self.get_superuser()
        self.user.record_name_change(staff_user, "aerith", "alice")

        self.assert_download_is_valid()

    def test_prepare_download_with_username_changed_by_deleted_user(self):
        """
        function creates data download for user with username changed by deleted user
        """
        self.user.record_name_change(self.user, "aerith", "alice")
        self.user.namechanges.update(changed_by=None)

        self.assert_download_is_valid()

    def test_prepare_download_with_audit_trail(self):
        """function creates data download for user with audit trail"""
        create_user_audit_trail(self.user, "127.0.0.1", self.user)

        self.assert_download_is_valid()

    def test_prepare_download_with_post(self):
        """function creates data download for user with post"""
        category = Category.objects.get(slug="first-category")
        post_thread(category, poster=self.user)

        self.assert_download_is_valid()

    def test_prepare_download_with_owm_post_edit(self):
        """function creates data download for user with own post edit"""
        category = Category.objects.get(slug="first-category")
        thread = post_thread(category, poster=self.user)
        post = thread.first_post

        post.edits_record.create(
            category=category,
            thread=thread,
            editor=self.user,
            editor_name=self.user.username,
            editor_slug=self.user.slug,
            edited_from="edited from",
            edited_to="edited to",
        )

        self.assert_download_is_valid()

    def test_prepare_download_with_other_users_post_edit(self):
        """function creates data download for user with other user's post edit"""
        category = Category.objects.get(slug="first-category")
        thread = post_thread(category)
        post = thread.first_post

        post.edits_record.create(
            category=category,
            thread=thread,
            editor=self.user,
            editor_name=self.user.username,
            editor_slug=self.user.slug,
            edited_from="edited from",
            edited_to="edited to",
        )

        self.assert_download_is_valid()

    def test_prepare_download_with_own_post_edit_by_staff(self):
        """function creates data download for user with post edited by staff"""
        category = Category.objects.get(slug="first-category")
        thread = post_thread(category, poster=self.user)
        post = thread.first_post

        staff_user = self.get_superuser()

        post.edits_record.create(
            category=category,
            thread=thread,
            editor=staff_user,
            editor_name=staff_user.username,
            editor_slug=staff_user.slug,
            edited_from="edited from",
            edited_to="edited to",
        )

        self.assert_download_is_valid()

    def test_prepare_download_with_poll(self):
        """function creates data download for user with poll"""
        category = Category.objects.get(slug="first-category")
        thread = post_thread(category, poster=self.user)
        post_poll(thread, self.user)

        self.assert_download_is_valid()


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
