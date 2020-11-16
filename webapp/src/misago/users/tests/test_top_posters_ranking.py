from datetime import timedelta

from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...threads.test import reply_thread
from ..activepostersranking import (
    build_active_posters_ranking,
    get_active_posters_ranking,
)
from ..models import ActivityRanking
from ..test import create_test_user


def test_ranking_is_emptied_if_no_users_exist(post):
    assert not build_active_posters_ranking()


def test_ranking_is_emptied_if_no_posts_exist(user):
    assert not build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_length=5)
def test_recent_post_by_user_counts_to_ranking(thread, user):
    reply_thread(thread, poster=user)
    assert build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_length=5)
def test_recent_post_by_removed_user_doesnt_count_to_ranking(thread):
    reply_thread(thread)
    assert not build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_length=5)
def test_old_post_by_user_doesnt_count_to_ranking(thread, user):
    reply_thread(thread, poster=user, posted_on=timezone.now() - timedelta(days=6))
    assert not build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_size=2)
def test_ranking_size_is_limited(thread):
    for i in range(3):
        user = create_test_user("User%s" % i, "user%s@example.com" % i)
        reply_thread(thread, poster=user)
    assert len(build_active_posters_ranking()) == 2


@override_dynamic_settings(top_posters_ranking_size=2)
def test_old_ranking_is_removed_during_build(user):
    ActivityRanking.objects.create(user=user, score=1)
    build_active_posters_ranking()
    assert not ActivityRanking.objects.exists()


def test_empty_ranking_is_returned_from_db(db):
    assert get_active_posters_ranking() == {"users": [], "users_count": 0}


def test_ranking_is_returned_from_db(user):
    ActivityRanking.objects.create(user=user, score=1)
    assert get_active_posters_ranking() == {"users": [user], "users_count": 1}


def test_ranked_user_is_annotated_with_score(user):
    ActivityRanking.objects.create(user=user, score=1)
    ranked_user = get_active_posters_ranking()["users"][0]
    assert ranked_user.score == 1


def test_ranked_users_are_ordered_by_score(user, other_user):
    ActivityRanking.objects.create(user=user, score=1)
    ActivityRanking.objects.create(user=other_user, score=2)
    assert get_active_posters_ranking() == {
        "users": [other_user, user],
        "users_count": 2,
    }
