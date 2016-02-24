from django.contrib.auth import get_user_model

from misago.categories.models import Category
from misago.core import threadstore
from misago.core.cache import cache
from misago.threads.testutils import post_thread

from misago.users.testutils import AuthenticatedUserTestCase
from misago.users.activepostersranking import (get_active_posters_ranking,
                                               get_real_active_posts_ranking,
                                               clear_active_posters_ranking)


class TestActivePostersRanking(AuthenticatedUserTestCase):
    def setUp(self):
        super(TestActivePostersRanking, self).setUp()

        cache.clear()
        threadstore.clear()

        self.category = Category.objects.all_categories()[:1][0]

    def tearDown(self):
        super(TestActivePostersRanking, self).tearDown()

        cache.clear()
        threadstore.clear()

    def test_get_real_active_posts_ranking(self):
        """get_real_active_posts_ranking returns list of active posters"""
        # no posts, empty tanking
        empty_ranking = get_real_active_posts_ranking()

        self.assertEqual(empty_ranking['users'], [])
        self.assertEqual(empty_ranking['users_count'], 0)

        # other user
        User = get_user_model()
        other_user = User.objects.create_user(
            "OtherUser", "other@user.com", "pass123")

        other_user.posts = 1
        other_user.save()

        post_thread(self.category, poster=other_user)

        ranking = get_real_active_posts_ranking()

        self.assertEqual(ranking['users'], [other_user])
        self.assertEqual(ranking['users_count'], 1)

        # two users in ranking
        post_thread(self.category, poster=self.user)
        post_thread(self.category, poster=self.user)

        self.user.posts = 2
        self.user.save()

        ranking = get_real_active_posts_ranking()

        self.assertEqual(ranking['users'], [self.user, other_user])
        self.assertEqual(ranking['users_count'], 2)

        self.assertEqual(ranking['users'][0].score, 2)
        self.assertEqual(ranking['users'][1].score, 1)

    def test_get_active_posters_ranking(self):
        """get_active_posters_ranking returns cached list of active posters"""
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking['users'], [])
        self.assertEqual(ranking['users_count'], 0)

        # post something
        post_thread(self.category, poster=self.user)
        post_thread(self.category, poster=self.user)

        self.user.posts = 2
        self.user.save()

        # cache returns results
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking['users'], [])
        self.assertEqual(ranking['users_count'], 0)

        # cache clear works
        clear_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking['users'], [self.user])
        self.assertEqual(ranking['users_count'], 1)