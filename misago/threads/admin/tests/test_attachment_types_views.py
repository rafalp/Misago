from django.urls import reverse

from ....acl.models import Role
from ....admin.test import AdminTestCase
from ...models import AttachmentType


class AttachmentTypeAdminViewsTests(AdminTestCase):
    def setUp(self):
        super().setUp()
        self.admin_link = reverse("misago:admin:settings:attachment-types:index")

    def test_link_registered(self):
        """admin nav contains attachment types link"""
        response = self.client.get(reverse("misago:admin:settings:index"))
        self.assertContains(response, self.admin_link)

    def test_list_view(self):
        """attachment types list returns 200 and renders all attachment types"""
        response = self.client.get(self.admin_link)
        self.assertEqual(response.status_code, 200)

        for attachment_type in AttachmentType.objects.all():
            self.assertContains(response, attachment_type.name)
            for file_extension in attachment_type.extensions_list:
                self.assertContains(response, file_extension)
            for mimename in attachment_type.mimetypes_list:
                self.assertContains(response, mimename)

    def test_new_view(self):
        """new attachment type view has no showstoppers"""
        form_link = reverse("misago:admin:settings:attachment-types:new")

        response = self.client.get(form_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(form_link, data={})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            form_link,
            data={
                "name": "Test type",
                "extensions": ".test",
                "size_limit": 0,
                "status": AttachmentType.ENABLED,
            },
        )
        self.assertEqual(response.status_code, 302)

        # clean alert about new item created
        self.client.get(self.admin_link)

        response = self.client.get(self.admin_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test type")
        self.assertContains(response, "test")

    def test_edit_view(self):
        """edit attachment type view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:settings:attachment-types:new"),
            data={
                "name": "Test type",
                "extensions": ".test",
                "size_limit": 0,
                "status": AttachmentType.ENABLED,
            },
        )

        test_type = AttachmentType.objects.order_by("id").last()
        self.assertEqual(test_type.name, "Test type")

        form_link = reverse(
            "misago:admin:settings:attachment-types:edit", kwargs={"pk": test_type.pk}
        )

        response = self.client.get(form_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(form_link, data={})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            form_link,
            data={
                "name": "Test type edited",
                "extensions": ".test.extension",
                "mimetypes": "test/edited-mime",
                "size_limit": 512,
                "status": AttachmentType.DISABLED,
                "limit_uploads_to": [r.pk for r in Role.objects.all()],
                "limit_downloads_to": [r.pk for r in Role.objects.all()],
            },
        )
        self.assertEqual(response.status_code, 302)

        test_type = AttachmentType.objects.order_by("id").last()
        self.assertEqual(test_type.name, "Test type edited")

        # clean alert about new item created
        self.client.get(self.admin_link)

        response = self.client.get(self.admin_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_type.name)
        self.assertContains(response, test_type.extensions)
        self.assertContains(response, test_type.mimetypes)

        self.assertEqual(test_type.limit_uploads_to.count(), Role.objects.count())
        self.assertEqual(test_type.limit_downloads_to.count(), Role.objects.count())

        # remove limits from type
        response = self.client.post(
            form_link,
            data={
                "name": "Test type edited",
                "extensions": ".test.extension",
                "mimetypes": "test/edited-mime",
                "size_limit": 512,
                "status": AttachmentType.DISABLED,
                "limit_uploads_to": [],
                "limit_downloads_to": [],
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(test_type.limit_uploads_to.count(), 0)
        self.assertEqual(test_type.limit_downloads_to.count(), 0)

    def test_clean_params_view(self):
        """admin form nicely cleans lists of extensions/mimetypes"""
        TEST_CASES = [
            ("test", ["test"]),
            (".test", ["test"]),
            (".tar.gz", ["tar.gz"]),
            (". test", ["test"]),
            ("test, test", ["test"]),
            ("test, tEst", ["test"]),
            ("test, other, tEst", ["test", "other"]),
            ("test, other, tEst,OTher", ["test", "other"]),
        ]

        for raw, final in TEST_CASES:
            response = self.client.post(
                reverse("misago:admin:settings:attachment-types:new"),
                data={
                    "name": "Test type",
                    "extensions": raw,
                    "size_limit": 0,
                    "status": AttachmentType.ENABLED,
                },
            )
            self.assertEqual(response.status_code, 302)

            test_type = AttachmentType.objects.order_by("id").last()
            self.assertEqual(set(test_type.extensions_list), set(final))

    def test_delete_view(self):
        """delete attachment type view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:settings:attachment-types:new"),
            data={
                "name": "Test type",
                "extensions": ".test",
                "size_limit": 0,
                "status": AttachmentType.ENABLED,
            },
        )

        test_type = AttachmentType.objects.order_by("id").last()
        self.assertEqual(test_type.name, "Test type")

        action_link = reverse(
            "misago:admin:settings:attachment-types:delete", kwargs={"pk": test_type.pk}
        )

        response = self.client.post(action_link)
        self.assertEqual(response.status_code, 302)

        # clean alert about item deleted
        self.client.get(self.admin_link)

        response = self.client.get(self.admin_link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, test_type.name)

    def test_cant_delete_type_with_attachments_view(self):
        """delete attachment type is not allowed if it has attachments associated"""
        self.client.post(
            reverse("misago:admin:settings:attachment-types:new"),
            data={
                "name": "Test type",
                "extensions": ".test",
                "size_limit": 0,
                "status": AttachmentType.ENABLED,
            },
        )

        test_type = AttachmentType.objects.order_by("id").last()
        self.assertEqual(test_type.name, "Test type")

        test_type.attachment_set.create(
            secret="loremipsum",
            filetype=test_type,
            uploader_name="User",
            uploader_slug="user",
            filename="test.zip",
            file="sad76asd678as687sa.zip",
        )

        action_link = reverse(
            "misago:admin:settings:attachment-types:delete", kwargs={"pk": test_type.pk}
        )

        response = self.client.post(action_link)
        self.assertEqual(response.status_code, 302)

        # get alert form database
        AttachmentType.objects.get(pk=test_type.pk)
