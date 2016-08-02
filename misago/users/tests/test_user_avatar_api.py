import json

from path import Path

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.conf import settings

from ..avatars import store
from ..testutils import AuthenticatedUserTestCase


class UserAvatarTests(AuthenticatedUserTestCase):
    """
    tests for user avatar RPC (/api/users/1/avatar/)
    """
    def setUp(self):
        super(UserAvatarTests, self).setUp()
        self.link = '/api/users/%s/avatar/' % self.user.pk

    def test_avatars_off(self):
        """custom avatars are not allowed"""
        with self.settings(allow_custom_avatars=False):
            response = self.client.get(self.link)
            self.assertEqual(response.status_code, 200)

            options = json.loads(smart_str(response.content))
            self.assertTrue(options['generated'])
            self.assertFalse(options['gravatar'])
            self.assertFalse(options['crop_org'])
            self.assertFalse(options['crop_tmp'])
            self.assertFalse(options['upload'])
            self.assertTrue(options['galleries'])

    def test_avatars_on(self):
        """custom avatars are not allowed"""
        with self.settings(allow_custom_avatars=True):
            response = self.client.get(self.link)
            self.assertEqual(response.status_code, 200)

            options = json.loads(smart_str(response.content))
            self.assertTrue(options['generated'])
            self.assertTrue(options['gravatar'])
            self.assertFalse(options['crop_org'])
            self.assertFalse(options['crop_tmp'])
            self.assertTrue(options['upload'])
            self.assertTrue(options['galleries'])

    def test_avatar_locked(self):
        """requests to api error if user's avatar is locked"""
        self.user.is_avatar_locked = True
        self.user.avatar_lock_user_message = 'Your avatar is pwnt.'
        self.user.save()

        response = self.client.get(self.link)
        self.assertContains(response, 'Your avatar is pwnt', status_code=403)

    def test_other_user_avatar(self):
        """requests to api error if user tries to access other user"""
        self.logout_user();

        response = self.client.get(self.link)
        self.assertContains(response, 'You have to sign in', status_code=403)

        User = get_user_model()
        self.login_user(User.objects.create_user(
            "BobUser", "bob@bob.com", self.USER_PASSWORD))

        response = self.client.get(self.link)
        self.assertContains(response, 'can\'t change other users avatars', status_code=403)

    def test_empty_requests(self):
        """empty request errors with code 400"""
        response = self.client.post(self.link)
        self.assertContains(response, 'Unknown avatar type.', status_code=400)

    def test_failed_gravatar_request(self):
        """no gravatar RPC fails"""
        self.user.email_hash = 'wolololo'
        self.user.save()

        response = self.client.post(self.link, data={'avatar': 'gravatar'})
        self.assertContains(response, 'No Gravatar is associated', status_code=400)

    def test_successful_gravatar_request(self):
        """gravatar RPC fails"""
        self.user.set_email('rafio.xudb@gmail.com')
        self.user.save()

        response = self.client.post(self.link, data={'avatar': 'gravatar'})
        self.assertContains(response, 'Gravatar was downloaded and set')

    def test_generation_request(self):
        """generated avatar is set"""
        response = self.client.post(self.link, data={'avatar': 'generated'})
        self.assertContains(response, 'New avatar based on your account')

    def test_avatar_upload_and_crop(self):
        """avatar can be uploaded and cropped"""
        response = self.client.post(self.link, data={'avatar': 'generated'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.link, data={'avatar': 'upload'})
        self.assertContains(response, 'No file was sent.', status_code=400)

        avatar_path = (settings.MEDIA_ROOT, 'avatars', 'blank.png')
        with open('/'.join(avatar_path), 'rb') as avatar:
            response = self.client.post(self.link,
                                        data={
                                            'avatar': 'upload',
                                            'image': avatar
                                        })
            self.assertEqual(response.status_code, 200)

            response_json = json.loads(smart_str(response.content))
            self.assertTrue(response_json['options']['crop_tmp'])

            avatar_dir = store.get_existing_avatars_dir(self.user)
            avatar = Path('%s/%s_tmp.png' % (avatar_dir, self.user.pk))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

            tmp_avatar_kwargs = {
                'pk': self.user.pk,
                'secret': response_json['options']['crop_tmp']['secret'],
                'hash': response_json['avatar_hash'],
            }
            tmp_avatar_path = reverse('misago:user-avatar-source',
                                      kwargs=tmp_avatar_kwargs)
            response = self.client.get(tmp_avatar_path)
            self.assertEqual(response.status_code, 200)

            response = self.client.post(self.link, json.dumps({
                    'avatar': 'crop_tmp',
                    'crop': {
                        'offset': {
                            'x': 0, 'y': 0
                        },
                        'zoom': 1
                    }
                }),
                content_type="application/json")
            response_json = json.loads(smart_str(response.content))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Uploaded avatar was set.')

            avatar_dir = store.get_existing_avatars_dir(self.user)
            avatar = Path('%s/%s_tmp.png' % (avatar_dir, self.user.pk))
            self.assertFalse(avatar.exists())

            avatar = Path('%s/%s_org.png' % (avatar_dir, self.user.pk))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

            org_avatar_kwargs = {
                'pk': self.user.pk,
                'secret': response_json['options']['crop_org']['secret'],
                'hash': response_json['avatar_hash'],
            }
            org_avatar_path = reverse('misago:user-avatar-source',
                                      kwargs=tmp_avatar_kwargs)
            response = self.client.get(org_avatar_path)
            self.assertEqual(response.status_code, 200)

            response = self.client.post(self.link, json.dumps({
                    'avatar': 'crop_tmp',
                    'crop': {
                        'offset': {
                            'x': 0, 'y': 0
                        },
                        'zoom': 1
                    }
                }),
                content_type="application/json")
            self.assertContains(response, 'This avatar type is not allowed.', status_code=400)

            response = self.client.post(self.link, json.dumps({
                    'avatar': 'crop_org',
                    'crop': {
                        'offset': {
                            'x': 0, 'y': 0
                        },
                        'zoom': 1
                    }
                }),
                content_type="application/json")
            self.assertContains(response, 'Avatar was re-cropped.')

    def test_gallery(self):
        """its possible to set avatar from gallery"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = json.loads(smart_str(response.content))
        self.assertTrue(options['galleries'])

        for gallery in options['galleries']:
            for image in gallery['images']:
                response = self.client.post(self.link, data={
                    'avatar': 'galleries',
                    'image': image
                })

                self.assertContains(response, 'Avatar from gallery was set.')


class UserAvatarModerationTests(AuthenticatedUserTestCase):
    """
    tests for moderate user avatar RPC (/api/users/1/moderate-avatar/)
    """
    def setUp(self):
        super(UserAvatarModerationTests, self).setUp()

        User = get_user_model()
        self.other_user = User.objects.create_user(
            "OtherUser", "other@user.com", "pass123")

        self.link = '/api/users/%s/moderate-avatar/' % self.other_user.pk

    def test_no_permission(self):
        """no permission to moderate avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 0,
        })

        response = self.client.get(self.link)
        self.assertContains(response, "can't moderate avatars", status_code=403)

        override_acl(self.user, {
            'can_moderate_avatars': 0,
        })

        response = self.client.post(self.link)
        self.assertContains(response, "can't moderate avatars", status_code=403)

    def test_moderate_avatar(self):
        """moderate avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

        options = json.loads(smart_str(response.content))
        self.assertEqual(options['is_avatar_locked'],
                         self.other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'],
                         self.other_user.avatar_lock_user_message)
        self.assertEqual(options['avatar_lock_staff_message'],
                         self.other_user.avatar_lock_staff_message)

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'is_avatar_locked': True,
                'avatar_lock_user_message': "Test user message.",
                'avatar_lock_staff_message': "Test staff message.",
            }),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        other_user = User.objects.get(pk=self.other_user.pk)

        options = json.loads(smart_str(response.content))
        self.assertEqual(other_user.is_avatar_locked, True)
        self.assertEqual(
            other_user.avatar_lock_user_message, "Test user message.")
        self.assertEqual(
            other_user.avatar_lock_staff_message, "Test staff message.")

        self.assertEqual(options['avatar_hash'],
                         other_user.avatar_hash)
        self.assertEqual(options['is_avatar_locked'],
                         other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'],
                         other_user.avatar_lock_user_message)
        self.assertEqual(options['avatar_lock_staff_message'],
                         other_user.avatar_lock_staff_message)

        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.post(self.link, json.dumps({
                'is_avatar_locked': False,
                'avatar_lock_user_message': None,
                'avatar_lock_staff_message': None,
            }),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

        other_user = User.objects.get(pk=self.other_user.pk)

        options = json.loads(smart_str(response.content))
        self.assertEqual(options['avatar_hash'],
                         other_user.avatar_hash)
        self.assertEqual(options['is_avatar_locked'],
                         other_user.is_avatar_locked)
        self.assertEqual(options['avatar_lock_user_message'],
                         other_user.avatar_lock_user_message)
        self.assertEqual(options['avatar_lock_staff_message'],
                         other_user.avatar_lock_staff_message)

    def test_moderate_own_avatar(self):
        """moderate own avatar"""
        override_acl(self.user, {
            'can_moderate_avatars': 1,
        })

        response = self.client.get(
            '/api/users/%s/moderate-avatar/' % self.user.pk)
        self.assertEqual(response.status_code, 200)
