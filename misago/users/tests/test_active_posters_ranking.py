from ...conf.test import override_dynamic_settings
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
def test_recent_post_by_user_counts_to_ranking(thread_factory, user, default_category):
    thread_factory(default_category, starter=user)
    assert build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_length=5)
def test_recent_post_by_removed_user_doesnt_count_to_ranking(
    thread_factory, default_category
):
    thread_factory(default_category)
    assert not build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_length=5)
def test_old_post_by_user_doesnt_count_to_ranking(
    thread_factory, user, default_category, day_seconds
):
    thread_factory(default_category, starter=user, started_at=day_seconds * -6)
    assert not build_active_posters_ranking()


@override_dynamic_settings(top_posters_ranking_size=2)
def test_ranking_size_is_limited(thread_factory, default_category):
    for i in range(3):
        user = create_test_user("User%s" % i, "user%s@example.com" % i)
        thread_factory(default_category, starter=user)
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
