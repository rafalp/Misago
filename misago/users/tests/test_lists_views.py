from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl

from misago.users.models import Rank
from misago.users.testutils import AuthenticatedUserTestCase


class UsersListTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(UsersListTestCase, self).setUp()
        override_acl(self.user, {
            'can_browse_users_list': 1,
        })


class UsersListLanderTests(UsersListTestCase):
    def test_lander_no_permission(self):
        """lander returns 403 if user has no permission"""
        override_acl(self.user, {
            'can_browse_users_list': 0,
        })

        response = self.client.get(reverse('misago:users'))
        self.assertEqual(response.status_code, 403)

    def test_lander_redirect(self):
        """lander returns redirect to valid page if user has permission"""
        response = self.client.get(reverse('misago:users'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(
                        reverse('misago:users_active_posters')))


class ActivePostersTests(UsersListTestCase):
    def test_active_posters_list(self):
        """active posters page has no showstoppers"""
        view_link = reverse('misago:users_active_posters')

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)

        # Create 200 test users and see if errors appeared
        User = get_user_model()
        for i in xrange(200):
            User.objects.create_user('Bob%s' % i, 'm%s@te.com' % i, 'Pass.123',
                                     posts=12345)

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)


class UsersRankTests(UsersListTestCase):
    def test_ranks(self):
        """ranks lists are handled correctly"""
        for rank in Rank.objects.iterator():
            rank_link = reverse('misago:users_rank',
                                kwargs={'rank_slug': rank.slug})
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
