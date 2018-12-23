import os

from django.urls import reverse

from .. import test
from ...acl.models import Role
from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...conf import settings
from ...users.test import AuthenticatedUserTestCase
from ..models import Attachment, AttachmentType

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_DOCUMENT_PATH = os.path.join(TESTFILES_DIR, "document.pdf")
TEST_SMALLJPG_PATH = os.path.join(TESTFILES_DIR, "small.jpg")


def patch_attachments_acl(acl_patch=None):
    acl_patch = acl_patch or {}
    acl_patch.setdefault("max_attachment_size", 1024)
    acl_patch.setdefault("can_download_other_users_attachments", True)
    return patch_user_acl(acl_patch)


class AttachmentViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        AttachmentType.objects.all().delete()

        self.category = Category.objects.get(slug="first-category")
        self.post = test.post_thread(category=self.category).first_post

        self.api_link = reverse("misago:api:attachment-list")

        self.attachment_type_jpg = AttachmentType.objects.create(
            name="JPG", extensions="jpeg,jpg"
        )
        self.attachment_type_pdf = AttachmentType.objects.create(
            name="PDF", extensions="pdf"
        )

    def upload_document(self, is_orphaned=False, by_other_user=False):
        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        attachment = Attachment.objects.order_by("id").last()

        if not is_orphaned:
            attachment.post = self.post
            attachment.save()
        if by_other_user:
            attachment.uploader = None
            attachment.save()

        return attachment

    def upload_image(self):
        with open(TEST_SMALLJPG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        return Attachment.objects.order_by("id").last()

    @patch_attachments_acl()
    def assertIs404(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["location"].endswith(settings.MISAGO_404_IMAGE))

    @patch_attachments_acl()
    def assertIs403(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["location"].endswith(settings.MISAGO_403_IMAGE))

    @patch_attachments_acl()
    def assertSuccess(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response["location"].endswith(settings.MISAGO_404_IMAGE))
        self.assertFalse(response["location"].endswith(settings.MISAGO_403_IMAGE))

    @patch_attachments_acl()
    def test_nonexistant_file(self):
        """user tries to retrieve nonexistant file"""
        response = self.client.get(
            reverse("misago:attachment", kwargs={"pk": 123, "secret": "qwertyuiop"})
        )

        self.assertIs404(response)

    @patch_attachments_acl()
    def test_invalid_secret(self):
        """user tries to retrieve existing file using invalid secret"""
        attachment = self.upload_document()

        response = self.client.get(
            reverse(
                "misago:attachment",
                kwargs={"pk": attachment.pk, "secret": "qwertyuiop"},
            )
        )

        self.assertIs404(response)

    @patch_attachments_acl({"can_download_other_users_attachments": False})
    def test_other_user_file_no_permission(self):
        """user tries to retrieve other user's file without perm"""
        attachment = self.upload_document(by_other_user=True)

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs403(response)

    @patch_attachments_acl({"can_download_other_users_attachments": False})
    def test_other_user_orphaned_file(self):
        """user tries to retrieve other user's orphaned file"""
        attachment = self.upload_document(is_orphaned=True, by_other_user=True)

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs404(response)

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertIs404(response)

    @patch_attachments_acl()
    def test_document_thumbnail(self):
        """user tries to retrieve thumbnail from non-image attachment"""
        attachment = self.upload_document()

        response = self.client.get(
            reverse(
                "misago:attachment-thumbnail",
                kwargs={"pk": attachment.pk, "secret": attachment.secret},
            )
        )
        self.assertIs404(response)

    @patch_attachments_acl()
    def test_no_role(self):
        """user tries to retrieve attachment without perm to its type"""
        attachment = self.upload_document()

        user_roles = (r.pk for r in self.user.get_roles())
        self.attachment_type_pdf.limit_downloads_to.set(
            Role.objects.exclude(id__in=user_roles)
        )

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs403(response)

    @patch_attachments_acl()
    def test_type_disabled(self):
        """user tries to retrieve attachment the type disabled downloads"""
        attachment = self.upload_document()

        self.attachment_type_pdf.status = AttachmentType.DISABLED
        self.attachment_type_pdf.save()

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs403(response)

    @patch_attachments_acl()
    def test_locked_type(self):
        """user retrieves own locked file"""
        attachment = self.upload_document()

        self.attachment_type_pdf.status = AttachmentType.LOCKED
        self.attachment_type_pdf.save()

        response = self.client.get(attachment.get_absolute_url())
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_own_file(self):
        """user retrieves own file"""
        attachment = self.upload_document()

        response = self.client.get(attachment.get_absolute_url())
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_other_user_file(self):
        """user retrieves other user's file with perm"""
        attachment = self.upload_document(by_other_user=True)

        response = self.client.get(attachment.get_absolute_url())
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_other_user_orphaned_file_is_staff(self):
        """user retrieves other user's orphaned file because he is staff"""
        attachment = self.upload_document(is_orphaned=True, by_other_user=True)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs404(response)

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_orphaned_file_is_uploader(self):
        """user retrieves orphaned file because he is its uploader"""
        attachment = self.upload_document(is_orphaned=True)

        response = self.client.get(attachment.get_absolute_url())
        self.assertIs404(response)

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_has_role(self):
        """user retrieves file he has roles to download"""
        attachment = self.upload_document()

        user_roles = self.user.get_roles()
        self.attachment_type_pdf.limit_downloads_to.set(user_roles)

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_image(self):
        """user retrieves """
        attachment = self.upload_image()

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertSuccess(response)

    @patch_attachments_acl()
    def test_image_thumb(self):
        """user retrieves image's thumbnail"""
        attachment = self.upload_image()

        response = self.client.get(attachment.get_absolute_url() + "?shva=1")
        self.assertSuccess(response)
