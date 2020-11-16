import os

from django.urls import reverse
from PIL import Image

from ...acl.models import Role
from ...acl.test import patch_user_acl
from ...conf import settings
from ...users.test import AuthenticatedUserTestCase
from ..models import Attachment, AttachmentType

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_DOCUMENT_PATH = os.path.join(TESTFILES_DIR, "document.pdf")
TEST_LARGEPNG_PATH = os.path.join(TESTFILES_DIR, "large.png")
TEST_SMALLJPG_PATH = os.path.join(TESTFILES_DIR, "small.jpg")
TEST_ANIMATEDGIF_PATH = os.path.join(TESTFILES_DIR, "animated.gif")
TEST_CORRUPTEDIMG_PATH = os.path.join(TESTFILES_DIR, "corrupted.gif")


class AttachmentsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        AttachmentType.objects.all().delete()

        self.api_link = reverse("misago:api:attachment-list")

    def test_anonymous(self):
        """user has to be authenticated to be able to upload files"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    @patch_user_acl({"max_attachment_size": 0})
    def test_no_permission(self):
        """user needs permission to upload files"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You don't have permission to upload new files."},
        )

    def test_no_file_uploaded(self):
        """no file uploaded scenario is handled"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "No file has been uploaded."})

    def test_invalid_extension(self):
        """uploaded file's extension is rejected as invalid"""
        AttachmentType.objects.create(
            name="Test extension", extensions="jpg,jpeg", mimetypes=None
        )

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "You can't upload files of this type."}
            )

    def test_invalid_mime(self):
        """uploaded file's mimetype is rejected as invalid"""
        AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="loremipsum"
        )

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "You can't upload files of this type."}
            )

    def test_no_perm_to_type(self):
        """user needs permission to upload files of this type"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="application/pdf"
        )

        user_roles = (r.pk for r in self.user.get_roles())
        attachment_type.limit_uploads_to.set(Role.objects.exclude(id__in=user_roles))

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "You can't upload files of this type."}
            )

    def test_type_is_locked(self):
        """new uploads for this filetype are locked"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions="png",
            mimetypes="application/pdf",
            status=AttachmentType.LOCKED,
        )

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "You can't upload files of this type."}
            )

    def test_type_is_disabled(self):
        """new uploads for this filetype are disabled"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions="png",
            mimetypes="application/pdf",
            status=AttachmentType.DISABLED,
        )

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "You can't upload files of this type."}
            )

    def test_upload_too_big_for_type(self):
        """too big uploads are rejected"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions="png",
            mimetypes="image/png",
            size_limit=100,
        )

        with open(TEST_LARGEPNG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(),
                {
                    "detail": (
                        "You can't upload files of this type larger "
                        "than 100.0\xa0KB (your file has 253.9\xa0KB)."
                    )
                },
            )

    @patch_user_acl({"max_attachment_size": 100})
    def test_upload_too_big_for_user(self):
        """too big uploads are rejected"""
        AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="image/png"
        )

        with open(TEST_LARGEPNG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(),
                {
                    "detail": (
                        "You can't upload files larger than 100.0\xa0KB "
                        "(your file has 253.9\xa0KB)."
                    )
                },
            )

    def test_corrupted_image_upload(self):
        """corrupted image upload is handled"""
        AttachmentType.objects.create(name="Test extension", extensions="gif")

        with open(TEST_CORRUPTEDIMG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(), {"detail": "Uploaded image was corrupted or invalid."}
            )

    def test_document_upload(self):
        """successful upload creates orphan attachment"""
        AttachmentType.objects.create(
            name="Test extension", extensions="pdf", mimetypes="application/pdf"
        )

        with open(TEST_DOCUMENT_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        attachment = Attachment.objects.get(id=response_json["id"])

        self.assertEqual(attachment.filename, "document.pdf")
        self.assertTrue(attachment.is_file)
        self.assertFalse(attachment.is_image)

        self.assertIsNotNone(attachment.file)
        self.assertTrue(not attachment.image)
        self.assertTrue(not attachment.thumbnail)

        self.assertTrue(str(attachment.file).endswith("document.pdf"))

        self.assertIsNone(response_json["post"])
        self.assertEqual(response_json["uploader_name"], self.user.username)
        self.assertEqual(response_json["url"]["index"], attachment.get_absolute_url())
        self.assertIsNone(response_json["url"]["thumb"])
        self.assertEqual(response_json["url"]["uploader"], self.user.get_absolute_url())

        self.assertEqual(self.user.audittrail_set.count(), 1)

        # files associated with attachment are deleted on its deletion
        file_path = attachment.file.path
        self.assertTrue(os.path.exists(file_path))
        attachment.delete()
        self.assertFalse(os.path.exists(file_path))

    def test_small_image_upload(self):
        """successful small image upload creates orphan attachment without thumbnail"""
        AttachmentType.objects.create(
            name="Test extension", extensions="jpeg,jpg", mimetypes="image/jpeg"
        )

        with open(TEST_SMALLJPG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        attachment = Attachment.objects.get(id=response_json["id"])

        self.assertEqual(attachment.filename, "small.jpg")
        self.assertFalse(attachment.is_file)
        self.assertTrue(attachment.is_image)

        self.assertTrue(not attachment.file)
        self.assertIsNotNone(attachment.image)
        self.assertTrue(not attachment.thumbnail)

        self.assertTrue(str(attachment.image).endswith("small.jpg"))

        self.assertIsNone(response_json["post"])
        self.assertEqual(response_json["uploader_name"], self.user.username)
        self.assertEqual(response_json["url"]["index"], attachment.get_absolute_url())
        self.assertIsNone(response_json["url"]["thumb"])
        self.assertEqual(response_json["url"]["uploader"], self.user.get_absolute_url())

        self.assertEqual(self.user.audittrail_set.count(), 1)

    @patch_user_acl({"max_attachment_size": 10 * 1024})
    def test_large_image_upload(self):
        """successful large image upload creates orphan attachment with thumbnail"""
        AttachmentType.objects.create(
            name="Test extension", extensions="png", mimetypes="image/png"
        )

        with open(TEST_LARGEPNG_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        attachment = Attachment.objects.get(id=response_json["id"])

        self.assertEqual(attachment.filename, "large.png")
        self.assertFalse(attachment.is_file)
        self.assertTrue(attachment.is_image)

        self.assertTrue(not attachment.file)
        self.assertIsNotNone(attachment.image)
        self.assertIsNotNone(attachment.thumbnail)

        self.assertTrue(str(attachment.image).endswith("large.png"))
        self.assertTrue(str(attachment.thumbnail).endswith("large.png"))

        self.assertIsNone(response_json["post"])
        self.assertEqual(response_json["uploader_name"], self.user.username)
        self.assertEqual(response_json["url"]["index"], attachment.get_absolute_url())
        self.assertEqual(response_json["url"]["thumb"], attachment.get_thumbnail_url())
        self.assertEqual(response_json["url"]["uploader"], self.user.get_absolute_url())

        self.assertEqual(self.user.audittrail_set.count(), 1)

        # thumbnail was scaled down
        thumbnail = Image.open(attachment.thumbnail.path)
        self.assertEqual(
            thumbnail.size[0], settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[0]
        )
        self.assertLess(
            thumbnail.size[1], settings.MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT[1]
        )

        # files associated with attachment are deleted on its deletion
        image_path = attachment.image.path
        thumbnail_path = attachment.thumbnail.path

        self.assertTrue(os.path.exists(image_path))
        self.assertTrue(os.path.exists(thumbnail_path))

        attachment.delete()

        self.assertFalse(os.path.exists(image_path))
        self.assertFalse(os.path.exists(thumbnail_path))

    def test_animated_image_upload(self):
        """successful gif upload creates orphan attachment with thumbnail"""
        AttachmentType.objects.create(
            name="Test extension", extensions="gif", mimetypes="image/gif"
        )

        with open(TEST_ANIMATEDGIF_PATH, "rb") as upload:
            response = self.client.post(self.api_link, data={"upload": upload})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        attachment = Attachment.objects.get(id=response_json["id"])

        self.assertEqual(attachment.filename, "animated.gif")
        self.assertFalse(attachment.is_file)
        self.assertTrue(attachment.is_image)

        self.assertTrue(not attachment.file)
        self.assertIsNotNone(attachment.image)
        self.assertIsNotNone(attachment.thumbnail)

        self.assertTrue(str(attachment.image).endswith("animated.gif"))
        self.assertTrue(str(attachment.thumbnail).endswith("animated.gif"))

        self.assertIsNone(response_json["post"])
        self.assertEqual(response_json["uploader_name"], self.user.username)
        self.assertEqual(response_json["url"]["index"], attachment.get_absolute_url())
        self.assertEqual(response_json["url"]["thumb"], attachment.get_thumbnail_url())
        self.assertEqual(response_json["url"]["uploader"], self.user.get_absolute_url())

        self.assertEqual(self.user.audittrail_set.count(), 1)
