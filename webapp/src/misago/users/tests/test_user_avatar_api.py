import json
import os
from pathlib import Path

from ...acl.test import patch_user_acl
from ...conf import settings
from ...conf.test import override_dynamic_settings
from ..avatars import gallery, store
from ..models import AvatarGallery
from ..test import AuthenticatedUserTestCase, create_test_user

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_AVATAR_PATH = os.path.join(TESTFILES_DIR, "avatar.png")


class UserAvatarTests(AuthenticatedUserTestCase):
    """tests for user avatar RPC (/api/users/1/avatar/)"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/avatar/" % self.user.pk
        self.client.post(self.link, data={"avatar": "generated"})

    def get_current_user(self):
        self.user.refresh_from_db()
        return self.user

    def assertOldAvatarsAreDeleted(self, user):
        self.assertEqual(user.avatar_set.count(), len(settings.MISAGO_AVATARS_SIZES))

    @override_dynamic_settings(allow_custom_avatars=False)
    def test_avatars_off(self):
        """custom avatars are not allowed"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options["generated"])
        self.assertFalse(options["gravatar"])
        self.assertFalse(options["crop_src"])
        self.assertFalse(options["crop_tmp"])
        self.assertFalse(options["upload"])
        self.assertFalse(options["galleries"])

    @override_dynamic_settings(allow_custom_avatars=True)
    def test_avatars_on(self):
        """custom avatars are allowed"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options["generated"])
        self.assertTrue(options["gravatar"])
        self.assertFalse(options["crop_src"])
        self.assertFalse(options["crop_tmp"])
        self.assertTrue(options["upload"])
        self.assertFalse(options["galleries"])

    def test_gallery_exists(self):
        """api returns gallery"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options["galleries"])

    def test_avatar_locked(self):
        """requests to api error if user's avatar is locked"""
        self.user.is_avatar_locked = True
        self.user.avatar_lock_user_message = "Your avatar is pwnt."
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": "Your avatar is locked. You can't change it.",
                "reason": "<p>Your avatar is pwnt.</p>",
            },
        )

    def test_other_user_avatar(self):
        """requests to api error if user tries to access other user"""
        self.logout_user()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to perform this action."}
        )

        self.login_user(create_test_user("OtherUser", "otheruser@example.com"))

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't change other users avatars."}
        )

    def test_empty_requests(self):
        """empty request errors with code 400"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Unknown avatar type."})

    def test_failed_gravatar_request(self):
        """no gravatar RPC fails"""
        self.user.email_hash = "wolololo"
        self.user.save()

        response = self.client.post(self.link, data={"avatar": "gravatar"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "No Gravatar is associated with your e-mail address."},
        )

    def test_successful_gravatar_request(self):
        """gravatar RPC passes"""
        self.user.set_email("rafio.xudb@gmail.com")
        self.user.save()

        response = self.client.post(self.link, data={"avatar": "gravatar"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["detail"], "Gravatar was downloaded and set as new avatar."
        )

        self.assertOldAvatarsAreDeleted(self.user)

    def test_generation_request(self):
        """generated avatar is set"""
        response = self.client.post(self.link, data={"avatar": "generated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["detail"], "New avatar based on your account was set."
        )

        self.assertOldAvatarsAreDeleted(self.user)

    def test_avatar_upload_and_crop(self):
        """avatar can be uploaded and cropped"""
        response = self.client.post(self.link, data={"avatar": "upload"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "No file was sent."})

        with open(TEST_AVATAR_PATH, "rb") as avatar:
            response = self.client.post(
                self.link, data={"avatar": "upload", "image": avatar}
            )
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertTrue(response_json["crop_tmp"])
            self.assertEqual(
                self.get_current_user().avatar_tmp.url, response_json["crop_tmp"]["url"]
            )

        avatar = Path(self.get_current_user().avatar_tmp.path)
        self.assertTrue(avatar.exists())
        self.assertTrue(avatar.is_file())

        response = self.client.post(
            self.link,
            json.dumps(
                {"avatar": "crop_tmp", "crop": {"offset": {"x": 0, "y": 0}, "zoom": 1}}
            ),
            content_type="application/json",
        )

        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Uploaded avatar was set.")

        self.assertFalse(self.get_current_user().avatar_tmp)
        self.assertOldAvatarsAreDeleted(self.user)

        avatar = Path(self.get_current_user().avatar_src.path)
        self.assertTrue(avatar.exists())
        self.assertTrue(avatar.is_file())

        response = self.client.post(
            self.link,
            json.dumps(
                {"avatar": "crop_tmp", "crop": {"offset": {"x": 0, "y": 0}, "zoom": 1}}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "This avatar type is not allowed."}
        )

        response = self.client.post(
            self.link,
            json.dumps(
                {"avatar": "crop_src", "crop": {"offset": {"x": 0, "y": 0}, "zoom": 1}}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Avatar was re-cropped.")
        self.assertOldAvatarsAreDeleted(self.user)

        # delete user avatars, test if it deletes src and tmp
        store.delete_avatar(self.get_current_user())

        self.assertTrue(self.get_current_user().avatar_src.path)

        avatar = Path(self.get_current_user().avatar_src.path)
        self.assertFalse(avatar.exists())
        self.assertFalse(avatar.is_file())

    def test_gallery_set_empty_gallery(self):
        """gallery handles set avatar on empty gallery"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.link, data={"avatar": "galleries", "image": 123}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "This avatar type is not allowed."}
        )

    def test_gallery_image_validation(self):
        """gallery validates image to set"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        # no image id is handled
        response = self.client.post(self.link, data={"avatar": "galleries"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Incorrect image."})

        # invalid id is handled
        response = self.client.post(
            self.link, data={"avatar": "galleries", "image": "asdsadsadsa"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Incorrect image."})

        # nonexistant image is handled
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options["galleries"])

        test_avatar = options["galleries"][0]["images"][0]["id"]
        response = self.client.post(
            self.link, data={"avatar": "galleries", "image": test_avatar + 5000}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Incorrect image."})

        # default gallery image is handled
        AvatarGallery.objects.filter(pk=test_avatar).update(
            gallery=gallery.DEFAULT_GALLERY
        )

        response = self.client.post(
            self.link, data={"avatar": "galleries", "image": test_avatar}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Incorrect image."})

    def test_gallery_set_valid_avatar(self):
        """its possible to set avatar from gallery"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options["galleries"])

        test_avatar = options["galleries"][0]["images"][0]["id"]
        response = self.client.post(
            self.link, data={"avatar": "galleries", "image": test_avatar}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Avatar from gallery was set.")
        self.assertOldAvatarsAreDeleted(self.user)


class UserAvatarModerationTests(AuthenticatedUserTestCase):
    """tests for moderate user avatar RPC (/api/users/1/moderate-avatar/)"""

    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "other@user.com")
        self.link = "/api/users/%s/moderate-avatar/" % self.other_user.pk

    @patch_user_acl({"can_moderate_avatars": 0})
    def test_no_permission(self):
        """no permission to moderate avatar"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't moderate avatars."})

    @patch_user_acl({"can_moderate_avatars": 1})
    def test_moderate_avatar(self):
        """moderate avatar"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertEqual(options["is_avatar_locked"], self.other_user.is_avatar_locked)
        self.assertEqual(
            options["avatar_lock_user_message"],
            self.other_user.avatar_lock_user_message,
        )
        self.assertEqual(
            options["avatar_lock_staff_message"],
            self.other_user.avatar_lock_staff_message,
        )

        response = self.client.post(
            self.link,
            json.dumps(
                {
                    "is_avatar_locked": True,
                    "avatar_lock_user_message": "Test user message.",
                    "avatar_lock_staff_message": "Test staff message.",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.other_user.refresh_from_db()

        options = response.json()
        self.assertEqual(self.other_user.is_avatar_locked, True)
        self.assertEqual(self.other_user.avatar_lock_user_message, "Test user message.")
        self.assertEqual(
            self.other_user.avatar_lock_staff_message, "Test staff message."
        )

        self.assertEqual(options["avatars"], self.other_user.avatars)
        self.assertEqual(options["is_avatar_locked"], self.other_user.is_avatar_locked)
        self.assertEqual(
            options["avatar_lock_user_message"],
            self.other_user.avatar_lock_user_message,
        )
        self.assertEqual(
            options["avatar_lock_staff_message"],
            self.other_user.avatar_lock_staff_message,
        )

        response = self.client.post(
            self.link,
            json.dumps(
                {
                    "is_avatar_locked": False,
                    "avatar_lock_user_message": None,
                    "avatar_lock_staff_message": None,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.other_user.refresh_from_db()
        self.assertFalse(self.other_user.is_avatar_locked)
        self.assertIsNone(self.other_user.avatar_lock_user_message)
        self.assertIsNone(self.other_user.avatar_lock_staff_message)

        options = response.json()
        self.assertEqual(options["avatars"], self.other_user.avatars)
        self.assertEqual(options["is_avatar_locked"], self.other_user.is_avatar_locked)
        self.assertEqual(
            options["avatar_lock_user_message"],
            self.other_user.avatar_lock_user_message,
        )
        self.assertEqual(
            options["avatar_lock_staff_message"],
            self.other_user.avatar_lock_staff_message,
        )

        response = self.client.post(
            self.link,
            json.dumps(
                {
                    "is_avatar_locked": True,
                    "avatar_lock_user_message": "",
                    "avatar_lock_staff_message": "",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.is_avatar_locked)
        self.assertEqual(self.other_user.avatar_lock_user_message, "")
        self.assertEqual(self.other_user.avatar_lock_staff_message, "")

        options = response.json()
        self.assertEqual(options["avatars"], self.other_user.avatars)
        self.assertEqual(options["is_avatar_locked"], self.other_user.is_avatar_locked)
        self.assertEqual(
            options["avatar_lock_user_message"],
            self.other_user.avatar_lock_user_message,
        )
        self.assertEqual(
            options["avatar_lock_staff_message"],
            self.other_user.avatar_lock_staff_message,
        )

        response = self.client.post(
            self.link,
            json.dumps({"is_avatar_locked": False}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.other_user.refresh_from_db()
        self.assertFalse(self.other_user.is_avatar_locked)
        self.assertEqual(self.other_user.avatar_lock_user_message, "")
        self.assertEqual(self.other_user.avatar_lock_staff_message, "")

        options = response.json()
        self.assertEqual(options["avatars"], self.other_user.avatars)
        self.assertEqual(options["is_avatar_locked"], self.other_user.is_avatar_locked)
        self.assertEqual(
            options["avatar_lock_user_message"],
            self.other_user.avatar_lock_user_message,
        )
        self.assertEqual(
            options["avatar_lock_staff_message"],
            self.other_user.avatar_lock_staff_message,
        )

    @patch_user_acl({"can_moderate_avatars": 1})
    def test_moderate_own_avatar(self):
        """moderate own avatar"""
        response = self.client.get("/api/users/%s/moderate-avatar/" % self.user.pk)
        self.assertEqual(response.status_code, 200)
