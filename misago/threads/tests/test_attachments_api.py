import json
import os

from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

from misago.acl.models import Role
from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase

from ..models import Attachment, AttachmentType


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_DOCUMENT_PATH = os.path.join(TESTFILES_DIR, 'document.pdf')
TEST_LARGEPNG_PATH = os.path.join(TESTFILES_DIR, 'large.png')
TEST_SMALLJPG_PATH = os.path.join(TESTFILES_DIR, 'small.jpg')
TEST_CORRUPTEDIMG_PATH = os.path.join(TESTFILES_DIR, 'corrupted.gif')


class AttachmentsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(AttachmentsApiTestCase, self).setUp()

        AttachmentType.objects.all().delete()

        self.api_link = reverse('misago:api:attachment-list')

    def override_acl(self, new_acl=None):
        if new_acl:
            acl = self.user.acl.copy()
            acl.update(new_acl)
            override_acl(self.user, acl)

    def test_anonymous(self):
        """user has to be authenticated to be able to upload files"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_no_permission(self):
        """user needs permission to upload files"""
        self.override_acl({
            'max_attachment_size': 0
        })

        response = self.client.post(self.api_link)
        self.assertContains(response, "don't have permission to upload new files", status_code=403)

    def test_no_file_uploaded(self):
        """no file uploaded scenario is handled"""
        response = self.client.post(self.api_link)
        self.assertContains(response, "No file has been uploaded.", status_code=400)

    def test_invalid_extension(self):
        """uploaded file's extension is rejected as invalid"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions='jpg,jpeg',
            mimetypes=None
        )

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "You can't upload files of this type.", status_code=400)

    def test_invalid_mime(self):
        """uploaded file's mimetype is rejected as invalid"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='loremipsum'
        )

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "You can't upload files of this type.", status_code=400)

    def test_no_perm_to_type(self):
        """user needs permission to upload files of this type"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='application/pdf'
        )

        user_roles = (r.pk for r in self.user.get_roles())
        attachment_type.limit_uploads_to.set(Role.objects.exclude(id__in=user_roles))

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "You can't upload files of this type.", status_code=400)

    def test_type_is_locked(self):
        """new uploads for this filetype are locked"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='application/pdf',
            status=AttachmentType.LOCKED
        )

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "You can't upload files of this type.", status_code=400)

    def test_type_is_disabled(self):
        """new uploads for this filetype are disabled"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='application/pdf',
            status=AttachmentType.DISABLED
        )

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "You can't upload files of this type.", status_code=400)

    def test_upload_too_big_for_type(self):
        """too big uploads are rejected"""
        AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='image/png',
            size_limit=100
        )

        with open(TEST_LARGEPNG_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })

        self.assertContains(response, "can't upload files of this type larger than", status_code=400)

    def test_upload_too_big_for_user(self):
        """too big uploads are rejected"""
        self.override_acl({
            'max_attachment_size': 100
        })

        AttachmentType.objects.create(
            name="Test extension",
            extensions='png',
            mimetypes='image/png'
        )

        with open(TEST_LARGEPNG_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "can't upload files larger than", status_code=400)

    def test_corrupted_image_upload(self):
        """corrupted image upload is handled"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='gif'
        )

        with open(TEST_CORRUPTEDIMG_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertContains(response, "Uploaded image was corrupted or invalid.", status_code=400)

    def test_document_upload(self):
        """successful upload creates orphan attachment"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='pdf',
            mimetypes='application/pdf'
        )

        with open(TEST_DOCUMENT_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        attachment = Attachment.objects.get(id=response_json['id'])

        self.assertEqual(attachment.filename, 'document.pdf')
        self.assertIsNotNone(attachment.file)
        self.assertTrue(not attachment.image)
        self.assertTrue(not attachment.thumbnail)

        self.assertIsNone(response_json['post'])
        self.assertEqual(response_json['uploader_name'], self.user.username)
        self.assertEqual(response_json['url']['uploader'], self.user.get_absolute_url())

    def test_image_upload(self):
        """successful upload creates orphan attachment with thumbnail"""
        attachment_type = AttachmentType.objects.create(
            name="Test extension",
            extensions='jpeg,jpg',
            mimetypes='image/jpeg'
        )

        with open(TEST_SMALLJPG_PATH, 'rb') as upload:
            response = self.client.post(self.api_link, data={
                'upload': upload
            })
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        attachment = Attachment.objects.get(id=response_json['id'])

        self.assertEqual(attachment.filename, 'small.jpg')
        self.assertTrue(not attachment.file)
        self.assertIsNotNone(attachment.image)
        self.assertIsNotNone(attachment.thumbnail)

        self.assertIsNone(response_json['post'])
        self.assertEqual(response_json['uploader_name'], self.user.username)
        self.assertEqual(response_json['url']['uploader'], self.user.get_absolute_url())
