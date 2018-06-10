from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import six

from misago.admin.testutils import AdminTestCase
from misago.acl.testutils import override_acl


UserModel = get_user_model()


class JoinIpProfileFieldTests(AdminTestCase):
    def setUp(self):
        super(JoinIpProfileFieldTests, self).setUp()

        self.test_link = reverse(
            'misago:admin:users:accounts:edit',
            kwargs={
                'pk': self.user.pk,
            },
        )

    def test_field_hidden_in_admin(self):
        """readonly field doesn't display in the admin"""
        response = self.client.get(self.test_link)
        self.assertNotContains(response, 'name="join_ip"')
        self.assertNotContains(response, "IP address")
        self.assertNotContains(response, "Join IP")

    def test_admin_edits_field(self):
        """admin form allows admins to edit field"""
        response = self.client.post(
            self.test_link,
            data={
                'username': 'Edited',
                'rank': six.text_type(self.user.rank_id),
                'roles': six.text_type(self.user.roles.all()[0].pk),
                'email': 'reg@stered.com',
                'join_ip': '127.0.0.1',
                'new_password': '',
                'signature': '',
                'is_signature_locked': '0',
                'is_hiding_presence': '0',
                'limits_private_thread_invites_to': '0',
                'signature_lock_staff_message': '',
                'signature_lock_user_message': '',
                'subscribe_to_started_threads': '2',
                'subscribe_to_replied_threads': '2',
            }
        )
        self.assertEqual(response.status_code, 302)

        self.reload_user()
        self.assertNotIn('join_ip', self.user.profile_fields)

    def test_admin_search_field(self):
        """admin users search searches this field"""
        test_link = reverse('misago:admin:users:accounts:index')

        response = self.client.get('{}?redirected=1&profilefields=127.0.0.1'.format(test_link))
        self.assertContains(response, "No users matching search criteria have been found.")

    def test_field_display(self):
        """field displays on user profile"""
        test_link = reverse(
            'misago:user-details',
            kwargs={
                'pk': self.user.pk,
                'slug': self.user.slug,
            },
        )

        response = self.client.get(test_link)
        self.assertContains(response, "IP address")
        self.assertContains(response, "Join IP")
        self.assertContains(response, "127.0.0.1")

    def test_field_hidden_no_permission(self):
        """field is hidden on user profile if user has no permission"""
        test_link = reverse(
            'misago:user-details',
            kwargs={
                'pk': self.user.pk,
                'slug': self.user.slug,
            },
        )

        override_acl(self.user, {
            'can_see_users_ips': 0
        })

        response = self.client.get(test_link)
        self.assertNotContains(response, "IP address")
        self.assertNotContains(response, "Join IP")
        self.assertNotContains(response, "127.0.0.1")

    def test_field_hidden_ip_removed(self):
        """field is hidden on user profile if ip is removed"""
        test_link = reverse(
            'misago:user-details',
            kwargs={
                'pk': self.user.pk,
                'slug': self.user.slug,
            },
        )

        self.user.joined_from_ip = None
        self.user.save()

        response = self.client.get(test_link)
        self.assertNotContains(response, "IP address")
        self.assertNotContains(response, "Join IP")
        self.assertNotContains(response, "127.0.0.1")

    def test_field_display_json(self):
        """field is included in display json"""
        test_link = reverse('misago:api:user-details', kwargs={'pk': self.user.pk})

        response = self.client.get(test_link)
        self.assertEqual(
            response.json()['groups'],
            [
                {
                    'name': 'IP address',
                    'fields': [
                        {
                            'fieldname': 'join_ip',
                            'name': 'Join IP',
                            'text': '127.0.0.1',
                        },
                    ],
                },
            ]
        )

    def test_field_hidden_no_permission_json(self):
        """field is not included in display json if user has no permission"""
        test_link = reverse('misago:api:user-details', kwargs={'pk': self.user.pk})

        override_acl(self.user, {
            'can_see_users_ips': 0
        })

        response = self.client.get(test_link)
        self.assertEqual(response.json()['groups'], [])

    def test_field_hidden_ip_removed_json(self):
        """field is not included in display json if user ip is removed"""
        test_link = reverse('misago:api:user-details', kwargs={'pk': self.user.pk})

        self.user.joined_from_ip = None
        self.user.save()

        response = self.client.get(test_link)
        self.assertEqual(response.json()['groups'], [])

    def test_field_not_in_edit_json(self):
        """readonly field json is not returned from API"""
        test_link = reverse('misago:api:user-edit-details', kwargs={'pk': self.user.pk})

        response = self.client.get(test_link)

        found_field = None
        for group in response.json():
            for field in group['fields']:
                if field['fieldname'] == 'join_ip':
                    found_field = field

        self.assertIsNone(found_field)

    def test_field_is_not_editable_in_api(self):
        """readonly field can't be edited via api"""
        test_link = reverse('misago:api:user-edit-details', kwargs={'pk': self.user.pk})

        response = self.client.post(test_link, data={'join_ip': '88.12.13.14'})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertNotIn('join_ip', self.user.profile_fields)
