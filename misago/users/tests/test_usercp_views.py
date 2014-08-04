from path import path

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase
from misago.conf import settings
from misago.core import threadstore

from misago.users.avatars import store


class ChangeForumOptionsTests(AdminTestCase):
    def setUp(self):
        super(ChangeForumOptionsTests, self).setUp()
        self.view_link = reverse('misago:usercp_change_forum_options')

    def test_change_forum_options_get(self):
        """GET to usercp change options view returns 200"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Change forum options', response.content)

    def test_change_forum_options_post(self):
        """POST to usercp change options view returns 302"""
        response = self.client.post(self.view_link, data={
                'timezone': 'Asia/Qatar',
                'is_hiding_presence': '1',
                'subscribe_to_started_threads': '0',
                'subscribe_to_replied_threads': '1',
            })

        self.assertEqual(response.status_code, 302)

        test_user = get_user_model().objects.get(pk=self.test_admin.pk)
        self.assertEqual(test_user.timezone, 'Asia/Qatar')
        self.assertEqual(test_user.is_hiding_presence, 1)
        self.assertEqual(test_user.subscribe_to_started_threads, 0)
        self.assertEqual(test_user.subscribe_to_replied_threads, 1)


class ChangeAvatarTests(AdminTestCase):
    def setUp(self):
        super(ChangeAvatarTests, self).setUp()
        self.view_link = reverse('misago:usercp_change_avatar')

    def test_avatar_get(self):
        """GET to change avatar returns 200"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

    def test_avatar_locked(self):
        """usercp locked change avatar view returns 200"""
        self.test_admin.is_avatar_locked = True
        self.test_admin.avatar_lock_user_message = 'Your avatar is banned.'
        self.test_admin.save()

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your avatar is banned', response.content)

    def test_set_gravatar(self):
        """view sets user gravatar"""
        self.test_admin.set_email('kontakt@rpiton.com')
        self.test_admin.save()

        response = self.client.post(self.view_link, data={'dl-gravatar': '1'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Gravatar was downloaded', response.content)

        self.test_admin.set_email('test@test.com')
        self.test_admin.save()

        self.client.post(self.view_link, data={'dl-gravatar': '1'})
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('No Gravatar is associated', response.content)

    def test_set_dynamic(self):
        """view sets user dynamic avatar"""
        response = self.client.post(self.view_link, data={'set-dynamic': '1'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('New avatar based', response.content)


class AvatarUploadTests(AdminTestCase):
    def setUp(self):
        super(AvatarUploadTests, self).setUp()
        store.delete_avatar(self.test_admin)

    def tearDown(self):
        store.delete_avatar(self.test_admin)

    def test_upload_form_view(self):
        """upload view renders on get"""
        response = self.client.get(reverse('misago:usercp_upload_avatar'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Upload avatar', response.content)

    def test_upload_view(self):
        """upload view renders on get"""
        handler_link = reverse('misago:usercp_upload_avatar_handler')

        response = self.client.get(handler_link)
        self.assertEqual(response.status_code, 405)

        ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = self.client.post(handler_link,
                                    data={'baww': 'nope'},
                                    **ajax_header)

        self.assertEqual(response.status_code, 406)
        self.assertIn('No file was sent.', response.content)

        with open('%s/%s' % (settings.MEDIA_ROOT, 'misago.png')) as avatar:
            response = self.client.post(handler_link,
                                        data={'new-avatar': avatar},
                                        **ajax_header)
            self.assertEqual(response.status_code, 200)

            avatar_dir = store.get_existing_avatars_dir(self.test_admin)
            avatar = path('%s/%s_tmp.png' % (avatar_dir, self.test_admin.pk))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

    def test_crop_view(self):
        """avatar gets cropped"""
        with open('%s/%s' % (settings.MEDIA_ROOT, 'misago.png')) as avatar:
            handler_link = reverse('misago:usercp_upload_avatar_handler')
            ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
            response = self.client.post(handler_link,
                                        data={'new-avatar': avatar},
                                        **ajax_header)
            self.assertEqual(response.status_code, 200)

            crop_link = reverse('misago:usercp_crop_new_avatar')
            response = self.client.post(crop_link, data={'crop': '1245'})
            self.assertEqual(response.status_code, 200)

            test_crop = '619,201,150,150,0,0,150,150'
            response = self.client.post(crop_link, data={'crop': test_crop})
            self.assertEqual(response.status_code, 302)

            avatar_dir = store.get_existing_avatars_dir(self.test_admin)
            avatar = path('%s/%s_tmp.png' % (avatar_dir, self.test_admin.pk))
            self.assertFalse(avatar.exists())

            avatar = path('%s/%s_org.png' % (avatar_dir, self.test_admin.pk))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())


class AvatarGalleryTests(AdminTestCase):
    def setUp(self):
        super(AvatarGalleryTests, self).setUp()
        self.view_link = reverse('misago:usercp_avatar_galleries')

    def test_gallery_list(self):
        """view renders gallery on GET"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Select avatar from gallery', response.content)

    def test_gallery_set_avatar(self):
        """view changes user avatar on post"""
        response = self.client.post(self.view_link, data={
            'new-image': 'avatars/Nature/serval.jpg'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:usercp_change_avatar'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Avatar from gallery was set', response.content)

        response = self.client.post(self.view_link, data={
            'new-image': 'baww.jpg'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incorrect image', response.content)


class EditSignatureTests(AdminTestCase):
    def setUp(self):
        super(EditSignatureTests, self).setUp()
        self.view_link = reverse('misago:usercp_edit_signature')

    def test_signature_no_permission(self):
        """edit signature view with no ACL returns 404"""
        override_acl(self.test_admin, {
            'misago.users.permissions.account': {
                'can_have_signature': 0,
            }
        })

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 404)

    def test_signature_locked(self):
        """locked edit signature view returns 200"""
        override_acl(self.test_admin, {
            'misago.users.permissions.account': {
                'can_have_signature': 1,
            }
        })

        self.test_admin.is_signature_locked = True
        self.test_admin.signature_lock_user_message = 'Your siggy is banned.'
        self.test_admin.save()

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your siggy is banned', response.content)

    def test_signature_change(self):
        """GET to usercp change options view returns 200"""
        override_acl(self.test_admin, {
            'misago.users.permissions.account': {
                'can_have_signature': 1,
            }
        })

        self.test_admin.is_signature_locked = False
        self.test_admin.save()

        response = self.client.post(self.view_link,
            data={'signature': 'Hello siggy!'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertIn('<p>Hello siggy!</p>', response.content)


class ChangeUsernameTests(AdminTestCase):
    def setUp(self):
        super(ChangeUsernameTests, self).setUp()
        self.view_link = reverse('misago:usercp_change_username')

    def test_change_username_get(self):
        """GET to usercp change username view returns 200"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Change username', response.content)

    def test_change_username_post(self):
        """POST to usercp change username view returns 302"""
        response = self.client.post(self.view_link,
                                    data={'new_username': 'Boberson'})
        self.assertEqual(response.status_code, 302)

        test_user = get_user_model().objects.get(pk=self.test_admin.pk)
        self.assertEqual(test_user.username, 'Boberson')

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_user.username, response.content)


class ChangeEmailPasswordTests(AdminTestCase):
    def setUp(self):
        super(ChangeEmailPasswordTests, self).setUp()
        self.view_link = reverse('misago:usercp_change_email_password')

        threadstore.clear()

    def _link_from_mail(self, mail_body):
        for line in mail.outbox[0].body.splitlines():
            if line.strip().startswith('http://testserver/'):
                return line.strip()[len('http://testserver'):]
        raise ValueError("mail body didn't contain link with token")

    def test_change_email_password_get(self):
        """GET to usercp change email/pass view returns 200"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Change email or password', response.content)

    def test_change_email(self):
        """POST to usercp change email view returns 302"""
        response = self.client.post(self.view_link,
                                    data={'new_email': 'newmail@test.com',
                                          'current_password': 'Pass.123'})
        self.assertEqual(response.status_code, 302)

        self.assertIn('Confirm changes to', mail.outbox[0].subject)
        confirmation_link = self._link_from_mail(mail.outbox[0].body)

        response = self.client.get(confirmation_link)
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        test_user = User.objects.get(email='newmail@test.com')

    def test_change_password(self):
        """POST to usercp change password view returns 302"""
        response = self.client.post(self.view_link,
                                    data={'new_password': 'newpass123',
                                          'current_password': 'Pass.123'})
        self.assertEqual(response.status_code, 302)

        self.assertIn('Confirm changes to', mail.outbox[0].subject)
        confirmation_link = self._link_from_mail(mail.outbox[0].body)

        response = self.client.get(confirmation_link)
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        test_user = User.objects.get(pk=self.test_admin.pk)
        self.assertFalse(test_user.check_password('Pass.123'))
        self.assertTrue(test_user.check_password('newpass123'))
