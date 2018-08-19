import json
import os

from path import Path

from django.contrib.auth import get_user_model

from misago.acl.testutils import override_acl
from misago.users.avatars import gallery, store
from misago.users.models import AvatarGallery
from misago.users.testutils import AuthenticatedUserTestCase


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_AVATAR_PATH = os.path.join(TESTFILES_DIR, 'avatar.png')

UserModel = get_user_model()


class UserAvatarTests(AuthenticatedUserTestCase):
    """tests for user avatar RPC (/api/users/1/avatar/)"""

    def setUp(self):
        super(UserAvatarTests, self).setUp()
        self.link = '/api/users/%s/avatar/' % self.user.pk

    def get_current_user(self):
        return UserModel.objects.get(pk=self.user.pk)

    def test_avatars_off(self):
        """custom avatars are not allowed"""
        with self.settings(allow_custom_avatars=False):
            response = self.client.get(self.link)
            self.assertEqual(response.status_code, 200)

            options = response.json()
            self.assertTrue(options['generated'])
            self.assertFalse(options['gravatar'])
            self.assertFalse(options['crop_src'])
            self.assertFalse(options['crop_tmp'])
            self.assertFalse(options['upload'])
            self.assertFalse(options['galleries'])

    def test_avatars_on(self):
        """custom avatars are not allowed"""
        with self.settings(allow_custom_avatars=True):
            response = self.client.get(self.link)
            self.assertEqual(response.status_code, 200)

            options = response.json()
            self.assertTrue(options['generated'])
            self.assertTrue(options['gravatar'])
            self.assertFalse(options['crop_src'])
            self.assertFalse(options['crop_tmp'])
            self.assertTrue(options['upload'])
            self.assertFalse(options['galleries'])

    def test_gallery_exists(self):
        """api returns gallery"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options['galleries'])

    def test_avatar_locked(self):
        """requests to api error if user's avatar is locked"""
        self.user.is_avatar_locked = True
        self.user.avatar_lock_user_message = "Your avatar is pwnt."
        self.user.save()

        response = self.client.get(self.link)
        self.assertContains(response, "Your avatar is pwnt", status_code=403)

    def test_other_user_avatar(self):
        """requests to api error if user tries to access other user"""
        self.logout_user()

        response = self.client.get(self.link)
        self.assertContains(response, "You have to sign in", status_code=403)

        self.login_user(
            UserModel.objects.create_user("BobUser", "bob@bob.com", self.USER_PASSWORD)
        )

        response = self.client.get(self.link)
        self.assertContains(response, "can't change other users avatars", status_code=403)

    def test_empty_requests(self):
        """empty request errors with code 400"""
        response = self.client.post(self.link)
        self.assertContains(response, "Unknown avatar type.", status_code=400)

    def test_failed_gravatar_request(self):
        """no gravatar RPC fails"""
        self.user.email_hash = 'wolololo'
        self.user.save()

        response = self.client.post(self.link, data={'avatar': 'gravatar'})
        self.assertContains(response, "No Gravatar is associated", status_code=400)

    def test_successful_gravatar_request(self):
        """gravatar RPC passes"""
        self.user.set_email('rafio.xudb@gmail.com')
        self.user.save()

        response = self.client.post(self.link, data={'avatar': 'gravatar'})
        self.assertContains(response, "Gravatar was downloaded and set")

    def test_generation_request(self):
        """generated avatar is set"""
        response = self.client.post(self.link, data={'avatar': 'generated'})
        self.assertContains(response, "New avatar based on your account")

    def test_avatar_upload_and_crop(self):
        """avatar can be uploaded and cropped"""
        response = self.client.post(self.link, data={'avatar': 'generated'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.link, data={'avatar': 'upload'})
        self.assertContains(response, "No file was sent.", status_code=400)

        with open(TEST_AVATAR_PATH, 'rb') as avatar:
            response = self.client.post(self.link, data={'avatar': 'upload', 'image': avatar})
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertTrue(response_json['crop_tmp'])
            self.assertEqual(
                self.get_current_user().avatar_tmp.url, response_json['crop_tmp']['url']
            )

        avatar = Path(self.get_current_user().avatar_tmp.path)
        self.assertTrue(avatar.exists())
        self.assertTrue(avatar.isfile())

        response = self.client.post(
            self.link,
            json.dumps({
                'avatar': 'crop_tmp',
                'crop': {
                    'offset': {
                        'x': 0,
                        'y': 0
                    },
                    'zoom': 1,
                },
            }),
            content_type="application/json",
        )

        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uploaded avatar was set.")

        self.assertFalse(self.get_current_user().avatar_tmp)

        avatar = Path(self.get_current_user().avatar_src.path)
        self.assertTrue(avatar.exists())
        self.assertTrue(avatar.isfile())

        response = self.client.post(
            self.link,
            json.dumps({
                'avatar': 'crop_tmp',
                'crop': {
                    'offset': {
                        'x': 0,
                        'y': 0
                    },
                    'zoom': 1,
                },
            }),
            content_type="application/json",
        )
        self.assertContains(response, "This avatar type is not allowed.", status_code=400)

        response = self.client.post(
            self.link,
            json.dumps({
                'avatar': 'crop_src',
                'crop': {
                    'offset': {
                        'x': 0,
                        'y': 0
                    },
                    'zoom': 1,
                },
            }),
            content_type="application/json",
        )
        self.assertContains(response, "Avatar was re-cropped.")

        # delete user avatars, test if it deletes src and tmp
        store.delete_avatar(self.get_current_user())

        self.assertTrue(self.get_current_user().avatar_src.path)

        avatar = Path(self.get_current_user().avatar_src.path)
        self.assertFalse(avatar.exists())
        self.assertFalse(avatar.isfile())

    def test_gallery_set_empty_gallery(self):
        """gallery handles set avatar on empty gallery"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.link, data={'avatar': 'galleries', 'image': 123})

        self.assertContains(response, "This avatar type is not allowed.", status_code=400)

    def test_gallery_image_validation(self):
        """gallery validates image to set"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        # no image id is handled
        response = self.client.post(
            self.link,
            data={
                'avatar': 'galleries',
            },
        )
        self.assertContains(response, "Incorrect image.", status_code=400)

        # invalid id is handled
        response = self.client.post(
            self.link,
            data={
                'avatar': 'galleries',
                'image': 'asdsadsadsa',
            },
        )
        self.assertContains(response, "Incorrect image.", status_code=400)

        # nonexistant image is handled
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options['galleries'])

        test_avatar = options['galleries'][0]['images'][0]['id']
        response = self.client.post(
            self.link,
            data={
                'avatar': 'galleries',
                'image': test_avatar + 5000,
            },
        )
        self.assertContains(response, "Incorrect image.", status_code=400)

        # default gallery image is handled
        AvatarGallery.objects.filter(pk=test_avatar).update(gallery=gallery.DEFAULT_GALLERY)

        response = self.client.post(self.link, data={'avatar': 'galleries', 'image': test_avatar})
        self.assertContains(response, "Incorrect image.", status_code=400)

    def test_gallery_set_valid_avatar(self):
        """its possible to set avatar from gallery"""
        gallery.load_avatar_galleries()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertTrue(options['galleries'])

        test_avatar = options['galleries'][0]['images'][0]['id']
        response = self.client.post(
            self.link,
            data={
                'avatar': 'galleries',
                'image': test_avatar,
            },
        )

        self.assertContains(response, "Avatar from gallery was set.")


class UserAvatarModerationTests(AuthenticatedUserTestCase):
    """tests for moderate user avatar RPC (/api/users/1/moderate-avatar/)"""

    def setUp(self):
        super(UserAvatarModerationTests, self).setUp()

        self.other_user = UserModel.objects.create_user("OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/moderate-avatar/' % self.other_user.pk

    def test_no_permission(self):
        """no permission to moderate avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 0,
        })

        response = self.client.get(self.link)
        self.assertContains(response, "can't moderate avatars", status_code=403)

    def test_moderate_avatar(self):
        """moderate avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = response.json()
        self.assertEqual(options['is_avatar_locked'], self.other_user.is_avatar_locked)
        self.assertEqual(
            options['avatar_lock_user_message'], self.other_user.avatar_lock_user_message
        )
        self.assertEqual(
            options['avatar_lock_staff_message'], self.other_user.avatar_lock_staff_message
        )

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'is_avatar_locked': True,
                'avatar_lock_user_message': "Test user message.",
                'avatar_lock_staff_message': "Test staff message.",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.get(pk=self.other_user.pk)

        options = response.json()
        self.assertEqual(other_user.is_avatar_locked, True)
        self.assertEqual(other_user.avatar_lock_user_message, "Test user message.")
        self.assertEqual(other_user.avatar_lock_staff_message, "Test staff message.")

        self.assertEqual(options['avatars'], other_user.avatars)
        self.assertEqual(options['is_avatar_locked'], other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'], other_user.avatar_lock_user_message)
        self.assertEqual(
            options['avatar_lock_staff_message'], other_user.avatar_lock_staff_message
        )

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'is_avatar_locked': False,
                'avatar_lock_user_message': None,
                'avatar_lock_staff_message': None,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.get(pk=self.other_user.pk)
        self.assertFalse(other_user.is_avatar_locked)
        self.assertIsNone(other_user.avatar_lock_user_message)
        self.assertIsNone(other_user.avatar_lock_staff_message)

        options = response.json()
        self.assertEqual(options['avatars'], other_user.avatars)
        self.assertEqual(options['is_avatar_locked'], other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'], other_user.avatar_lock_user_message)
        self.assertEqual(
            options['avatar_lock_staff_message'], other_user.avatar_lock_staff_message
        )

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'is_avatar_locked': True,
                'avatar_lock_user_message': '',
                'avatar_lock_staff_message': '',
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.get(pk=self.other_user.pk)
        self.assertTrue(other_user.is_avatar_locked)
        self.assertEqual(other_user.avatar_lock_user_message, '')
        self.assertEqual(other_user.avatar_lock_staff_message, '')

        options = response.json()
        self.assertEqual(options['avatars'], other_user.avatars)
        self.assertEqual(options['is_avatar_locked'], other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'], other_user.avatar_lock_user_message)
        self.assertEqual(
            options['avatar_lock_staff_message'], other_user.avatar_lock_staff_message
        )

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(
            self.link,
            json.dumps({
                'is_avatar_locked': False,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.get(pk=self.other_user.pk)
        self.assertFalse(other_user.is_avatar_locked)
        self.assertEqual(other_user.avatar_lock_user_message, '')
        self.assertEqual(other_user.avatar_lock_staff_message, '')

        options = response.json()
        self.assertEqual(options['avatars'], other_user.avatars)
        self.assertEqual(options['is_avatar_locked'], other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'], other_user.avatar_lock_user_message)
        self.assertEqual(
            options['avatar_lock_staff_message'], other_user.avatar_lock_staff_message
        )

    def test_moderate_own_avatar(self):
        """moderate own avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.get('/api/users/%s/moderate-avatar/' % self.user.pk)
        self.assertEqual(response.status_code, 200)
