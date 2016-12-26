import json

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils import six
from django.utils.encoding import smart_str
from django.utils.six.moves import range

from misago.acl.models import Role
from misago.admin.testutils import AdminTestCase
from misago.categories.models import Category
from misago.threads.testutils import post_thread, reply_thread

from ..models import Ban, Rank


class UserAdminViewsTests(AdminTestCase):
    AJAX_HEADER = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_link_registered(self):
        """admin index view contains users link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, reverse('misago:admin:users:accounts:index'))

    def test_list_view(self):
        """users list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_list_search(self):
        """users list is searchable"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))
        self.assertEqual(response.status_code, 302)

        link_base = response['location']
        response = self.client.get(link_base)
        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        user_a = User.objects.create_user('Tyrael', 't123@test.com', 'pass123')
        user_b = User.objects.create_user('Tyrion', 't321@test.com', 'pass123')

        # Search both
        response = self.client.get(link_base + '&username=tyr')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_a.username)
        self.assertContains(response, user_b.username)

        # Search tyrion
        response = self.client.get(link_base + '&username=tyrion')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_a.username)
        self.assertContains(response, user_b.username)

        # Search tyrael
        response = self.client.get(link_base + '&email=t123@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_a.username)
        self.assertNotContains(response, user_b.username)

    def test_mass_activation(self):
        """users list activates multiple users"""
        User = get_user_model()

        user_pks = []
        for i in range(10):
            test_user = User.objects.create_user(
                'Bob%s' % i,
                'bob%s@test.com' % i,
                'pass123',
                requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse('misago:admin:users:accounts:index'),
            data={'action': 'activate', 'selected_items': user_pks})
        self.assertEqual(response.status_code, 302)

        inactive_qs = User.objects.filter(id__in=user_pks,
                                          requires_activation=1)
        self.assertEqual(inactive_qs.count(), 0)
        self.assertIn("has been activated", mail.outbox[0].subject)

    def test_mass_ban(self):
        """users list bans multiple users"""
        User = get_user_model()

        user_pks = []
        for i in range(10):
            test_user = User.objects.create_user(
                'Bob%s' % i,
                'bob%s@test.com' % i,
                'pass123',
                requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse('misago:admin:users:accounts:index'),
            data={'action': 'ban', 'selected_items': user_pks})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:accounts:index'),
            data={
                'action': 'ban',
                'selected_items': user_pks,
                'ban_type': [
                    'usernames', 'emails', 'domains',
                    'ip', 'ip_first', 'ip_two'
                ],
                'finalize': ''
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ban.objects.count(), 24)

    def test_mass_delete_accounts(self):
        """users list deletes users"""
        User = get_user_model()

        user_pks = []
        for i in range(10):
            test_user = User.objects.create_user(
                'Bob%s' % i,
                'bob%s@test.com' % i,
                'pass123',
                requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse('misago:admin:users:accounts:index'),
            data={'action': 'delete_accounts', 'selected_items': user_pks})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_mass_delete_all(self):
        """users list deletes users and their content"""
        User = get_user_model()

        user_pks = []
        for i in range(10):
            test_user = User.objects.create_user(
                'Bob%s' % i,
                'bob%s@test.com' % i,
                'pass123',
                requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse('misago:admin:users:accounts:index'),
            data={'action': 'delete_accounts', 'selected_items': user_pks})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_new_view(self):
        """new user view creates account"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:new'))
        self.assertEqual(response.status_code, 200)

        default_rank = Rank.objects.get_default()
        authenticated_role = Role.objects.get(special_role='authenticated')

        response = self.client.post(reverse('misago:admin:users:accounts:new'),
            data={
                'username': 'Bawww',
                'rank': six.text_type(default_rank.pk),
                'roles': six.text_type(authenticated_role.pk),
                'email': 'reg@stered.com',
                'new_password': 'pass123',
                'staff_level': '0'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        User.objects.get_by_username('Bawww')

    def test_edit_view(self):
        """edit user view changes account"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'pk': test_user.pk})

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(test_link, data={
            'username': 'Bawww',
            'rank': six.text_type(test_user.rank_id),
            'roles': six.text_type(test_user.roles.all()[0].pk),
            'email': 'reg@stered.com',
            'new_password': 'newpass123',
            'staff_level': '0',
            'signature': 'Hello world!',
            'is_signature_locked': '1',
            'is_hiding_presence': '0',
            'limits_private_thread_invites_to': '0',
            'signature_lock_staff_message': 'Staff message',
            'signature_lock_user_message': 'User message',
            'subscribe_to_started_threads': '2',
            'subscribe_to_replied_threads': '2',
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.check_password('newpass123'))
        self.assertEqual(updated_user.username, 'Bawww')
        self.assertEqual(updated_user.slug, 'bawww')

        User.objects.get_by_username('Bawww')
        User.objects.get_by_email('reg@stered.com')

    def test_edit_dont_change_username(self):
        """
        If username wasn't changed, don't touch user's username, slug or history

        This is regression test for issue #640
        """
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'pk': test_user.pk})

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(test_link, data={
            'username': 'Bob',
            'rank': six.text_type(test_user.rank_id),
            'roles': six.text_type(test_user.roles.all()[0].pk),
            'email': 'reg@stered.com',
            'new_password': 'pass123',
            'signature': 'Hello world!',
            'is_signature_locked': '1',
            'is_hiding_presence': '0',
            'limits_private_thread_invites_to': '0',
            'signature_lock_staff_message': 'Staff message',
            'signature_lock_user_message': 'User message',
            'subscribe_to_started_threads': '2',
            'subscribe_to_replied_threads': '2',
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(updated_user.username, 'Bob')
        self.assertEqual(updated_user.slug, 'bob')
        self.assertEqual(updated_user.namechanges.count(), 0)

    def test_edit_make_admin(self):
        """edit user view allows super admin to make other user admin"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'pk': test_user.pk})

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_staff_1"')
        self.assertContains(response, 'id="id_is_superuser_1"')

        response = self.client.post(test_link, data={
            'username': 'Bawww',
            'rank': six.text_type(test_user.rank_id),
            'roles': six.text_type(test_user.roles.all()[0].pk),
            'email': 'reg@stered.com',
            'new_password': 'pass123',
            'is_staff': '1',
            'is_superuser': '0',
            'signature': 'Hello world!',
            'is_signature_locked': '1',
            'is_hiding_presence': '0',
            'limits_private_thread_invites_to': '0',
            'signature_lock_staff_message': 'Staff message',
            'signature_lock_user_message': 'User message',
            'subscribe_to_started_threads': '2',
            'subscribe_to_replied_threads': '2',
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.is_staff)
        self.assertFalse(updated_user.is_superuser)

    def test_edit_make_superadmin_admin(self):
        """edit user view allows super admin to make other user super admin"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'pk': test_user.pk})

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_staff_1"')
        self.assertContains(response, 'id="id_is_superuser_1"')

        response = self.client.post(test_link, data={
            'username': 'Bawww',
            'rank': six.text_type(test_user.rank_id),
            'roles': six.text_type(test_user.roles.all()[0].pk),
            'email': 'reg@stered.com',
            'new_password': 'pass123',
            'is_staff': '0',
            'is_superuser': '1',
            'signature': 'Hello world!',
            'is_signature_locked': '1',
            'is_hiding_presence': '0',
            'limits_private_thread_invites_to': '0',
            'signature_lock_staff_message': 'Staff message',
            'signature_lock_user_message': 'User message',
            'subscribe_to_started_threads': '2',
            'subscribe_to_replied_threads': '2',
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_staff)
        self.assertTrue(updated_user.is_superuser)

    def test_edit_cant_make_admin(self):
        """edit user view forbids admins from making other admins"""
        self.user.is_superuser = False
        self.user.save()

        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'pk': test_user.pk})

        response = self.client.get(test_link)
        self.assertNotContains(response, 'id="id_is_staff_1"')
        self.assertNotContains(response, 'id="id_is_superuser_1"')

        response = self.client.post(test_link, data={
            'username': 'Bawww',
            'rank': six.text_type(test_user.rank_id),
            'roles': six.text_type(test_user.roles.all()[0].pk),
            'email': 'reg@stered.com',
            'new_password': 'pass123',
            'is_staff': '1',
            'is_superuser': '1',
            'signature': 'Hello world!',
            'is_signature_locked': '1',
            'is_hiding_presence': '0',
            'limits_private_thread_invites_to': '0',
            'signature_lock_staff_message': 'Staff message',
            'signature_lock_user_message': 'User message',
            'subscribe_to_started_threads': '2',
            'subscribe_to_replied_threads': '2',
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_staff)
        self.assertFalse(updated_user.is_superuser)

    def test_delete_threads_view(self):
        """delete user threads view deletes threads"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete-threads',
                            kwargs={'pk': test_user.pk})

        category = Category.objects.all_categories()[:1][0]
        [post_thread(category, poster=test_user) for i in range(10)]

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(smart_str(response.content))
        self.assertEqual(response_dict['deleted_count'], 10)
        self.assertFalse(response_dict['is_completed'])

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(smart_str(response.content))
        self.assertEqual(response_dict['deleted_count'], 0)
        self.assertTrue(response_dict['is_completed'])

    def test_delete_posts_view(self):
        """delete user posts view deletes posts"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete-posts',
                            kwargs={'pk': test_user.pk})

        category = Category.objects.all_categories()[:1][0]
        thread = post_thread(category)
        [reply_thread(thread, poster=test_user) for i in range(10)]

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(smart_str(response.content))
        self.assertEqual(response_dict['deleted_count'], 10)
        self.assertFalse(response_dict['is_completed'])

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(smart_str(response.content))
        self.assertEqual(response_dict['deleted_count'], 0)
        self.assertTrue(response_dict['is_completed'])

    def test_delete_account_view(self):
        """delete user account view deletes user account"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete-account',
                            kwargs={'pk': test_user.pk})

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(smart_str(response.content))
        self.assertTrue(response_dict['is_completed'])
