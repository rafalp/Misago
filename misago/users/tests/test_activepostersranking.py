from datetime import timedelta

from django.utils import timezone

from misago.categories.models import Category
from misago.threads.testutils import post_thread
from misago.users.activepostersranking import (
    build_active_posters_ranking,
    get_active_posters_ranking,
)
from misago.users.testutils import AuthenticatedUserTestCase, create_test_user


class TestActivePostersRanking(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")

    def test_get_active_posters_ranking(self):
        """get_active_posters_ranking returns list of active posters"""
        # no posts, empty tanking
        empty_ranking = get_active_posters_ranking()

        self.assertEqual(empty_ranking["users"], [])
        self.assertEqual(empty_ranking["users_count"], 0)

        # other user that will be posting
        other_user = create_test_user("OtherUser", "otheruser@example.com")

        # lurker user that won't post anything
        create_test_user("Lurker", "lurker@example.com")

        # unranked user that posted something 400 days ago
        unranked_user = create_test_user("UnrankedUser", "unranked@example.com")

        started_on = timezone.now() - timedelta(days=400)
        post_thread(self.category, poster=unranked_user, started_on=started_on)

        # Start testing scenarios
        post_thread(self.category, poster=other_user)

        build_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking["users"], [other_user])
        self.assertEqual(ranking["users_count"], 1)

        # two users in ranking
        post_thread(self.category, poster=self.user)
        post_thread(self.category, poster=self.user)

        build_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking["users"], [self.user, other_user])
        self.assertEqual(ranking["users_count"], 2)

        self.assertEqual(ranking["users"][0].score, 2)
        self.assertEqual(ranking["users"][1].score, 1)

        # disabled users are not ranked
        disabled = create_test_user("DisabledUser", "disableduser@example.com")

        disabled.is_active = False
        disabled.save()

        post_thread(self.category, poster=disabled)
        post_thread(self.category, poster=disabled)
        post_thread(self.category, poster=disabled)

        disabled.posts = 3
        disabled.save()

        build_active_posters_ranking()
        ranking = get_active_posters_ranking()

        self.assertEqual(ranking["users"], [self.user, other_user])
        self.assertEqual(ranking["users_count"], 2)

        self.assertEqual(ranking["users"][0].score, 2)
        self.assertEqual(ranking["users"][1].score, 1)
