from django.urls import reverse

from ... import test
from ....admin.test import AdminTestCase
from ....categories.models import Category
from ...models import Attachment, AttachmentType


class AttachmentAdminViewsTests(AdminTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.post = test.post_thread(category=self.category).first_post

        self.filetype = AttachmentType.objects.order_by("id").first()

        self.admin_link = reverse("misago:admin:attachments:index")

    def mock_attachment(self, post=None, file=None, image=None, thumbnail=None):
        return Attachment.objects.create(
            secret=Attachment.generate_new_secret(),
            filetype=self.filetype,
            post=post,
            size=1000,
            uploader=self.user,
            uploader_name=self.user.username,
            uploader_slug=self.user.slug,
            filename="testfile_%s.zip" % (Attachment.objects.count() + 1),
            file=None,
            image=None,
            thumbnail=None,
        )

    def test_link_registered(self):
        """admin nav contains attachments link"""
        response = self.client.get(reverse("misago:admin:settings:index"))
        self.assertContains(response, self.admin_link)

    def test_list_view(self):
        """attachments list returns 200 and renders all attachments"""
        final_link = self.client.get(self.admin_link)["location"]

        response = self.client.get(final_link)
        self.assertEqual(response.status_code, 200)

        attachments = [
            self.mock_attachment(self.post, file="somefile.pdf"),
            self.mock_attachment(image="someimage.jpg"),
            self.mock_attachment(
                self.post, image="somelargeimage.png", thumbnail="somethumb.png"
            ),
        ]

        response = self.client.get(final_link)
        self.assertEqual(response.status_code, 200)

        for attachment in attachments:
            delete_link = reverse(
                "misago:admin:attachments:delete", kwargs={"pk": attachment.pk}
            )
            self.assertContains(response, attachment.filename)
            self.assertContains(response, delete_link)
            self.assertContains(response, attachment.get_absolute_url())
            self.assertContains(response, attachment.uploader.username)
            self.assertContains(response, attachment.uploader.get_absolute_url())

            if attachment.thumbnail:
                self.assertContains(response, attachment.get_thumbnail_url())

    def test_delete_multiple(self):
        """mass delete tool on list works"""
        attachments = [
            self.mock_attachment(self.post, file="somefile.pdf"),
            self.mock_attachment(image="someimage.jpg"),
            self.mock_attachment(
                self.post, image="somelargeimage.png", thumbnail="somethumb.png"
            ),
        ]

        self.post.attachments_cache = [{"id": attachments[-1].pk}]
        self.post.save()

        response = self.client.post(
            self.admin_link,
            data={"action": "delete", "selected_items": [a.pk for a in attachments]},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Attachment.objects.count(), 0)

        # assert attachments were removed from post's cache
        attachments_cache = self.category.post_set.get(
            pk=self.post.pk
        ).attachments_cache
        self.assertIsNone(attachments_cache)

    def test_delete_view(self):
        """delete attachment view has no showstoppers"""
        attachment = self.mock_attachment(self.post)
        self.post.attachments_cache = [
            {"id": attachment.pk + 1},
            {"id": attachment.pk},
            {"id": attachment.pk + 2},
        ]
        self.post.save()

        action_link = reverse(
            "misago:admin:attachments:delete", kwargs={"pk": attachment.pk}
        )

        response = self.client.post(action_link)
        self.assertEqual(response.status_code, 302)

        # clean alert about item, grab final list url
        final_link = self.client.get(self.admin_link)["location"]

        response = self.client.get(final_link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, action_link)

        # assert it was removed from post's attachments cache
        attachments_cache = self.category.post_set.get(
            pk=self.post.pk
        ).attachments_cache
        self.assertEqual(
            attachments_cache, [{"id": attachment.pk + 1}, {"id": attachment.pk + 2}]
        )
