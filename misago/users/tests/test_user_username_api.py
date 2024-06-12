import json

from ...acl.test import patch_user_acl
from ...conf.test import override_dynamic_settings
from ..test import AuthenticatedUserTestCase, create_test_user


class UserUsernameModerationTests(AuthenticatedUserTestCase):
    """tests for moderate username RPC (/api/users/1/moderate-username/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("Other_User", "otheruser@example.com")
        self.link = "/api/users/%s/moderate-username/" % self.other_user.pk

    @patch_user_acl({"can_rename_users": 0})
    def test_no_permission(self):
        """no permission to moderate username"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't rename users."})

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't rename users."})

    @patch_user_acl({"can_rename_users": 1})
    @override_dynamic_settings(username_length_min=3, username_length_max=12)
    def test_moderate_username(self):
        """moderate username"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertEqual(options["length_min"], 3)
        self.assertEqual(options["length_max"], 12)

        response = self.client.post(
            self.link, json.dumps({"username": ""}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter new username."})

        response = self.client.post(
            self.link, json.dumps({"username": "$$$"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "Username can only contain Latin alphabet letters, digits, "
                    "and an underscore sign."
                ),
            },
        )

        response = self.client.post(
            self.link, json.dumps({"username": "a"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "Username must be at least 3 characters long."}
        )

        response = self.client.post(
            self.link,
            json.dumps({"username": "NewName"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.other_user.refresh_from_db()
        self.assertEqual("NewName", self.other_user.username)
        self.assertEqual("newname", self.other_user.slug)

        options = response.json()
        self.assertEqual(options["username"], self.other_user.username)
        self.assertEqual(options["slug"], self.other_user.slug)

    @patch_user_acl({"can_rename_users": 1})
    def test_moderate_own_username(self):
        """moderate own username"""
        response = self.client.get("/api/users/%s/moderate-username/" % self.user.pk)
        self.assertEqual(response.status_code, 200)
