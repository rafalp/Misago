from django.contrib.auth import get_user_model
from django.urls import reverse

from ...admin.test import AdminTestCase

User = get_user_model()


class TwitterProfileFieldTests(AdminTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:admin:users:edit", kwargs={"pk": self.user.pk})

    def test_field_displays_in_admin(self):
        """field displays in admin"""
        response = self.client.get(self.test_link)
        self.assertContains(response, 'name="twitter"')

    def test_admin_clears_field(self):
        """admin form allows admins to clear field"""
        self.user.profile_fields["twitter"] = "lorem_ipsum"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "lorem_ipsum")

        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "new_password": "",
                "signature": "",
                "is_signature_locked": "0",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "",
                "signature_lock_user_message": "",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "")

    def test_admin_validates_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "twitter": "lorem!ipsum",
                "new_password": "",
                "signature": "",
                "is_signature_locked": "0",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "",
                "signature_lock_user_message": "",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )

        self.assertContains(response, "This is not a valid twitter handle.")

    def test_admin_edits_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "twitter": "lorem_ipsum",
                "new_password": "",
                "signature": "",
                "is_signature_locked": "0",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "",
                "signature_lock_user_message": "",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "lorem_ipsum")

    def test_admin_search_field(self):
        """admin users search searches this field"""
        test_link = reverse("misago:admin:users:index")

        response = self.client.get("%s?redirected=1&profilefields=ipsum" % test_link)
        self.assertContains(response, "No users matching criteria exist.")

        self.user.profile_fields["twitter"] = "lorem_ipsum"
        self.user.save()

        response = self.client.get("%s?redirected=1&profilefields=ipsum" % test_link)
        self.assertNotContains(response, "No users matching criteria exist.")

    def test_field_display(self):
        """field displays on user profile when filled in"""
        test_link = reverse(
            "misago:user-details", kwargs={"pk": self.user.pk, "slug": self.user.slug}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, "Twitter")

        self.user.profile_fields["twitter"] = "lorem_ipsum"
        self.user.save()

        response = self.client.get(test_link)
        self.assertContains(response, "Twitter")
        self.assertContains(response, 'href="https://twitter.com/lorem_ipsum"')
        self.assertContains(response, "@lorem_ipsum")

    def test_field_display_json(self):
        """field is included in display json"""
        test_link = reverse("misago:api:user-details", kwargs={"pk": self.user.pk})

        response = self.client.get(test_link)
        self.assertEqual(
            response.json()["groups"],
            [
                {
                    "name": "IP address",
                    "fields": [
                        {"fieldname": "join_ip", "name": "Join IP", "text": "127.0.0.1"}
                    ],
                }
            ],
        )

        self.user.profile_fields["twitter"] = "lorem_ipsum"
        self.user.save()

        response = self.client.get(test_link)
        self.assertEqual(
            response.json()["groups"],
            [
                {
                    "name": "Contact",
                    "fields": [
                        {
                            "fieldname": "twitter",
                            "name": "Twitter handle",
                            "text": "@lorem_ipsum",
                            "url": "https://twitter.com/lorem_ipsum",
                        }
                    ],
                },
                {
                    "name": "IP address",
                    "fields": [
                        {"fieldname": "join_ip", "name": "Join IP", "text": "127.0.0.1"}
                    ],
                },
            ],
        )

    def test_api_returns_field_json(self):
        """field json is returned from API"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.get(test_link)

        found_field = None
        for group in response.json():
            for field in group["fields"]:
                if field["fieldname"] == "twitter":
                    found_field = field

        self.assertEqual(
            found_field,
            {
                "fieldname": "twitter",
                "label": "Twitter handle",
                "help_text": (
                    "If you own Twitter account, here you may enter your Twitter "
                    'handle for other users to find you. Starting your handle with "@" '
                    'sign is optional. Either "@testsuperuser" or "testsuperuser" are '
                    "valid values."
                ),
                "input": {"type": "text"},
                "initial": "",
            },
        )

    def test_api_clears_field(self):
        """field can be cleared via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        self.user.profile_fields["twitter"] = "lorem_ipsum"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "lorem_ipsum")

        response = self.client.post(test_link, data={})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "")

    def test_api_validates_field(self):
        """field can be edited via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.post(test_link, data={"twitter": "@lorem!ipsum"})
        self.assertContains(
            response, "This is not a valid twitter handle.", status_code=400
        )

    def test_api_edits_field(self):
        """field can be edited via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.post(test_link, data={"twitter": "@lorem_ipsum"})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["twitter"], "lorem_ipsum")
