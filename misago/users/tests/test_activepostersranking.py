from django.contrib.auth import get_user_model

from misago.categories.models import Category
from misago.core import threadstore
from misago.core.cache import cache
from misago.threads.testutils import post_thread

from ..activepostersranking import build_active_posters_ranking, get_active_posters_ranking
from ..testutils import AuthenticatedUserTestCase


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

    def test_get_active_posters_ranking(self):
        """get_active_posters_ranking returns list of active posters"""
        # no posts, empty tanking
        empty_ranking = get_active_posters_ranking()

        self.assertEqual(empty_ranking['users'], [])
        self.assertEqual(empty_ranking['users_count'], 0)

        # other user
        User = get_user_model()
        other_user = User.objects.create_user(
            "OtherUser", "other@user.com", "pass123")

        other_user.posts = 1
        other_user.save()

        post_thread(self.category, poster=other_user)

        build_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking['users'], [other_user])
        self.assertEqual(ranking['users_count'], 1)

        # two users in ranking
        post_thread(self.category, poster=self.user)
        post_thread(self.category, poster=self.user)

        self.user.posts = 2
        self.user.save()

        build_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking['users'], [self.user, other_user])
        self.assertEqual(ranking['users_count'], 2)

        self.assertEqual(ranking['users'][0].score, 2)
        self.assertEqual(ranking['users'][1].score, 1)
