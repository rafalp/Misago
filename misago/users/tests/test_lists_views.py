from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads.testutils import post_thread
from misago.users.activepostersranking import build_active_posters_ranking
from misago.users.models import Rank
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


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
        self.assertTrue(response['location'].endswith(reverse('misago:users-active-posters')))


class ActivePostersTests(UsersListTestCase):
    def test_empty_active_posters_list(self):
        """empty active posters page has no showstoppers"""
        view_link = reverse('misago:users-active-posters')

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)

    def test_active_posters_list(self):
        """active posters page has no showstoppers"""
        category = Category.objects.get(slug='first-category')
        view_link = reverse('misago:users-active-posters')

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)

        # Create 50 test users and see if errors appeared
        for i in range(50):
            user = UserModel.objects.create_user(
                'Bob%s' % i,
                'm%s@te.com' % i,
                'Pass.123',
                posts=12345,
            )
            post_thread(category, poster=user)

        build_active_posters_ranking()

        response = self.client.get(view_link)
        self.assertEqual(response.status_code, 200)


class UsersRankTests(UsersListTestCase):
    def test_ranks(self):
        """ranks lists are handled correctly"""
        rank_user = UserModel.objects.create_user('Visible', 'visible@te.com', 'Pass.123')

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse(
                'misago:users-rank',
                kwargs={
                    'slug': rank.slug,
                },
            )
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)

    def test_disabled_users(self):
        """ranks lists excludes disabled accounts"""
        rank_user = UserModel.objects.create_user(
            'Visible',
            'visible@te.com',
            'Pass.123',
            is_active=False,
        )

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse(
                'misago:users-rank',
                kwargs={
                    'slug': rank.slug,
                },
            )
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)

    def test_staff_see_disabled_users(self):
        """ranks lists shows disabled accounts for staff members"""
        self.user.is_staff = True
        self.user.save()

        rank_user = UserModel.objects.create_user(
            'Visible',
            'visible@te.com',
            'Pass.123',
            is_active=False,
        )

        for rank in Rank.objects.iterator():
            rank_user.rank = rank
            rank_user.save()

            rank_link = reverse(
                'misago:users-rank',
                kwargs={
                    'slug': rank.slug,
                },
            )
            response = self.client.get(rank_link)

            if rank.is_tab:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, rank_user.get_absolute_url())
            else:
                self.assertEqual(response.status_code, 404)
