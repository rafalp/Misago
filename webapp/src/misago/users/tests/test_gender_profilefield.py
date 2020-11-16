from django.contrib.auth import get_user_model
from django.urls import reverse

from ...admin.test import AdminTestCase

User = get_user_model()


class GenderProfileFieldTests(AdminTestCase):
    def setUp(self):
        super().setUp()

        self.test_link = reverse("misago:admin:users:edit", kwargs={"pk": self.user.pk})

    def test_field_displays_in_admin(self):
        """field displays in admin"""
        response = self.client.get(self.test_link)
        self.assertContains(response, 'name="gender"')

    def test_admin_clears_field(self):
        """admin form allows admins to clear field"""
        self.user.profile_fields["gender"] = "female"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["gender"], "female")

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
        self.assertEqual(self.user.profile_fields["gender"], "")

    def test_admin_validates_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "gender": "attackcopter",
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

        self.assertContains(
            response, "attackcopter is not one of the available choices."
        )

    def test_admin_edits_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                "username": "Edited",
                "rank": str(self.user.rank_id),
                "roles": str(self.user.roles.all()[0].pk),
                "email": "reg@stered.com",
                "gender": "female",
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
        self.assertEqual(self.user.profile_fields["gender"], "female")

    def test_admin_search_field(self):
        """admin users search searches this field"""
        test_link = reverse("misago:admin:users:index")

        response = self.client.get("%s?redirected=1&profilefields=female" % test_link)
        self.assertContains(response, "No users matching criteria exist.")

        # search by value
        self.user.profile_fields["gender"] = "female"
        self.user.save()

        response = self.client.get("%s?redirected=1&profilefields=female" % test_link)
        self.assertNotContains(response, "No users matching criteria exist.")

        # search by choice name
        self.user.profile_fields["gender"] = "secret"
        self.user.save()

        response = self.client.get("%s?redirected=1&profilefields=telling" % test_link)
        self.assertNotContains(response, "No users matching criteria exist.")

    def test_field_display(self):
        """field displays on user profile when filled in"""
        test_link = reverse(
            "misago:user-details", kwargs={"pk": self.user.pk, "slug": self.user.slug}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, "Gender")

        self.user.profile_fields["gender"] = "secret"
        self.user.save()

        response = self.client.get(test_link)
        self.assertContains(response, "Gender")
        self.assertContains(response, "Not telling")

    def test_field_outdated_hidden(self):
        """field with outdated value is hidden"""
        test_link = reverse(
            "misago:user-details", kwargs={"pk": self.user.pk, "slug": self.user.slug}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, "Gender")

        self.user.profile_fields["gender"] = "not valid"
        self.user.save()

        response = self.client.get(test_link)
        self.assertNotContains(response, "Gender")

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

        self.user.profile_fields["gender"] = "male"
        self.user.save()

        response = self.client.get(test_link)
        self.assertEqual(
            response.json()["groups"],
            [
                {
                    "name": "Personal",
                    "fields": [
                        {"fieldname": "gender", "name": "Gender", "text": "Male"}
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

    def test_field_outdated_hidden_json(self):
        """field with outdated value is removed in display json"""
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

        self.user.profile_fields["gender"] = "invalid"
        self.user.save()

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

    def test_api_returns_field_json(self):
        """field json is returned from API"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.get(test_link)

        found_field = None
        for group in response.json():
            for field in group["fields"]:
                if field["fieldname"] == "gender":
                    found_field = field

        self.assertEqual(
            found_field,
            {
                "fieldname": "gender",
                "label": "Gender",
                "help_text": None,
                "input": {
                    "type": "select",
                    "choices": [
                        {"label": "Not specified", "value": ""},
                        {"label": "Not telling", "value": "secret"},
                        {"label": "Female", "value": "female"},
                        {"label": "Male", "value": "male"},
                    ],
                },
                "initial": "",
            },
        )

    def test_api_clears_field(self):
        """field can be cleared via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        self.user.profile_fields["gender"] = "secret"
        self.user.save()

        self.reload_user()
        self.assertEqual(self.user.profile_fields["gender"], "secret")

        response = self.client.post(test_link, data={})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["gender"], "")

    def test_api_validates_field(self):
        """field can be edited via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.post(test_link, data={"gender": "attackhelicopter"})
        self.assertContains(
            response,
            "attackhelicopter is not one of the available choices.",
            status_code=400,
        )

    def test_api_edits_field(self):
        """field can be edited via api"""
        test_link = reverse("misago:api:user-edit-details", kwargs={"pk": self.user.pk})

        response = self.client.post(test_link, data={"gender": "female"})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.profile_fields["gender"], "female")
