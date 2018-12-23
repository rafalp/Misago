import json

from ...acl.test import patch_user_acl
from ...conf.test import override_dynamic_settings
from ..test import AuthenticatedUserTestCase, create_test_user


class UserUsernameTests(AuthenticatedUserTestCase):
    """tests for user change name RPC (POST to /api/users/1/username/)"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/username/" % self.user.pk

    @override_dynamic_settings(username_length_min=2, username_length_max=4)
    def test_get_change_username_options(self):
        """get to API returns options"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertIsNotNone(response_json["changes_left"])
        self.assertEqual(response_json["length_min"], 2)
        self.assertEqual(response_json["length_max"], 4)
        self.assertIsNone(response_json["next_on"])

        for i in range(response_json["changes_left"]):
            self.user.set_username("NewName%s" % i, self.user)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["changes_left"], 0)
        self.assertIsNotNone(response_json["next_on"])

    def test_change_username_no_changes_left(self):
        """api returns error 400 if there are no username changes left"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        for i in range(response.json()["changes_left"]):
            self.user.set_username("NewName%s" % i, self.user)

        response = self.client.get(self.link)
        self.assertEqual(response.json()["changes_left"], 0)

        response = self.client.post(self.link, data={"username": "Pointless"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "You can't change your username now."
        )
        self.assertTrue(self.user.username != "Pointless")

    def test_change_username_no_input(self):
        """api returns error 400 if new username is empty"""
        response = self.client.post(self.link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter new username."})

    def test_change_username_invalid_name(self):
        """api returns error 400 if new username is wrong"""
        response = self.client.post(self.link, data={"username": "####"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Username can only contain latin alphabet letters and digits."},
        )

    def test_change_username(self):
        """api changes username and records change"""
        response = self.client.get(self.link)
        changes_left = response.json()["changes_left"]

        old_username = self.user.username
        new_username = "NewUsernamu"

        response = self.client.post(self.link, data={"username": new_username})

        self.assertEqual(response.status_code, 200)
        options = response.json()["options"]
        self.assertEqual(changes_left, options["changes_left"] + 1)

        self.reload_user()
        self.assertEqual(self.user.username, new_username)
        self.assertTrue(self.user.username != old_username)

        self.assertEqual(self.user.namechanges.last().new_username, new_username)


class UserUsernameModerationTests(AuthenticatedUserTestCase):
    """tests for moderate username RPC (/api/users/1/moderate-username/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")
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
            {"detail": "Username can only contain latin alphabet letters and digits."},
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
