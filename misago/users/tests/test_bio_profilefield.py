from django.contrib.auth import get_user_model
from django.urls import reverse

from ...admin.test import AdminTestCase

User = get_user_model()


class BioProfileFieldTests(AdminTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:admin:users:edit", kwargs={"pk": self.user.pk})

    def test_field_displays_in_admin(self):
        """field displays in admin"""
        response = self.client.get(self.test_link)
        self.assertContains(response, 'name="bio"')

    def test_admin_clears_field(self):
        """admin form allows admins to clear field"""
        self.user.profile_fields["bio"] = "Exists!"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["bio"], "Exists!")

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
        self.assertEqual(self.user.profile_fields["bio"], "")

    def test_admin_edits_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "bio": "Edited field!",
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
        self.assertEqual(self.user.profile_fields["bio"], "Edited field!")

    def test_admin_search_field(self):
        """admin users search searches this field"""
        test_link = reverse("misago:admin:users:index")

        response = self.client.get("%s?redirected=1&profilefields=Ipsum" % test_link)
        self.assertContains(response, "No users matching criteria exist.")

        self.user.profile_fields["bio"] = "Lorem Ipsum Dolor Met"
        self.user.save()

        response = self.client.get("%s?redirected=1&profilefields=Ipsum" % test_link)
        self.assertNotContains(response, "No users matching criteria exist.")

    def test_field_display(self):
        """field displays on user profile when filled in"""
        test_link = reverse(
            "misago:user-details", kwargs={"pk": self.user.pk, "slug": self.user.slug}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, "Bio")

        self.user.profile_fields["bio"] = "I am Bob!\n\nThis is <b>my</b> bio!"
        self.user.save()

        response = self.client.get(test_link)
        self.assertContains(response, "Bio")
        self.assertContains(response, "<p>I am Bob!</p>")
        self.assertContains(response, "<p>This is &lt;b&gt;my&lt;/b&gt; bio!</p>")

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

        self.user.profile_fields["bio"] = "I am Bob!\n\nThis is <b>my</b> bio!"
        self.user.save()

        response = self.client.get(test_link)
        self.assertEqual(
            response.json()["groups"],
            [
                {
                    "name": "Personal",
                    "fields": [
                        {
                            "fieldname": "bio",
                            "name": "Bio",
                            "html": (
                                "<p>I am Bob!</p>\n\n"
                                "<p>This is &lt;b&gt;my&lt;/b&gt; bio!</p>"
                            ),
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
                if field["fieldname"] == "bio":
                    found_field = field

        self.assertEqual(
            found_field,
            {
                "fieldname": "bio",
                "label": "Bio",
                "help_text": None,
                "input": {"type": "textarea"},
                "initial": "",
            },
        )

    def test_api_clears_field(self):
        """field can be cleared via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        self.user.profile_fields["bio"] = "Exists!"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["bio"], "Exists!")

        response = self.client.post(test_link, data={})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["bio"], "")

    def test_api_edits_field(self):
        """field can be edited via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.post(test_link, data={"bio": "Lorem Ipsum!"})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["bio"], "Lorem Ipsum!")
