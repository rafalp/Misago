import json

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse

from misago.acl.models import Role
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum
from misago.threads.testutils import post_thread, reply_thread

from misago.users.models import Ban, Rank


class UserAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin index view contains users link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertIn(reverse('misago:admin:users:accounts:index'),
                      response.content)

    def test_list_view(self):
        """users list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

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
        self.assertIn(user_a.username, response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrion
        response = self.client.get(link_base + '&username=tyrion')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_a.username in response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrael
        response = self.client.get(link_base + '&email=t123@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_a.username, response.content)
        self.assertFalse(user_b.username in response.content)

    def test_mass_activation(self):
        """users list activates multiple users"""
        User = get_user_model()

        user_pks = []
        for i in xrange(10):
            test_user = User.objects.create_user('Bob%s' % i,
                                                 'bob%s@test.com' % i,
                                                 'pass123',
                                                 requires_activation=1)
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
        for i in xrange(10):
            test_user = User.objects.create_user('Bob%s' % i,
                                                 'bob%s@test.com' % i,
                                                 'pass123',
                                                 requires_activation=1)
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
        for i in xrange(10):
            test_user = User.objects.create_user('Bob%s' % i,
                                                 'bob%s@test.com' % i,
                                                 'pass123',
                                                 requires_activation=1)
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
        for i in xrange(10):
            test_user = User.objects.create_user('Bob%s' % i,
                                                 'bob%s@test.com' % i,
                                                 'pass123',
                                                 requires_activation=1)
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
                'rank': unicode(default_rank.pk),
                'roles': unicode(authenticated_role.pk),
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
                            kwargs={'user_id': test_user.pk})

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(test_link,
            data={
                'username': 'Bawww',
                'rank': unicode(test_user.rank_id),
                'roles': unicode(test_user.roles.all()[0].pk),
                'email': 'reg@stered.com',
                'new_password': 'pass123',
                'staff_level': '0',
                'signature': 'Hello world!',
                'is_signature_locked': '1',
                'signature_lock_staff_message': 'Staff message',
                'signature_lock_user_message': 'User message',
            })
        self.assertEqual(response.status_code, 302)

        User.objects.get_by_username('Bawww')
        User.objects.get_by_email('reg@stered.com')

    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_delete_threads_view(self):
        """delete user threads view deletes threads"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete_threads',
                            kwargs={'user_id': test_user.pk})

        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        [post_thread(forum, poster=test_user) for i in xrange(10)]

        response = self.client.post(test_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['deleted_count'], 10)
        self.assertFalse(response_dict['is_completed'])

        response = self.client.post(test_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['deleted_count'], 0)
        self.assertTrue(response_dict['is_completed'])

    def test_delete_posts_view(self):
        """delete user posts view deletes posts"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete_posts',
                            kwargs={'user_id': test_user.pk})

        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        thread = post_thread(forum)
        [reply_thread(thread, poster=test_user) for i in xrange(10)]

        response = self.client.post(test_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['deleted_count'], 10)
        self.assertFalse(response_dict['is_completed'])

        response = self.client.post(test_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['deleted_count'], 0)
        self.assertTrue(response_dict['is_completed'])

    def test_delete_account_view(self):
        """delete user account view deletes user account"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:delete_account',
                            kwargs={'user_id': test_user.pk})

        response = self.client.post(test_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertTrue(response_dict['is_completed'])
