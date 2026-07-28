import pytest

from ...privatethreads.members import (
    get_private_thread_members,
    prefetch_private_thread_member_ids,
)
from ...privatethreads.models import PrivateThreadMember


def test_thread_model_set_first_post(post_factory, thread, user):
    post = post_factory(thread, poster=user)

    thread.set_first_post(post)
    thread.save()

    assert thread.started_at == post.posted_at
    assert thread.first_post == post
    assert thread.starter == user
    assert thread.starter_name == user.username
    assert thread.starter_slug == user.slug

    thread.refresh_from_db()

    assert thread.started_at == post.posted_at
    assert thread.first_post == post
    assert thread.starter == user
    assert thread.starter_name == user.username
    assert thread.starter_slug == user.slug


def test_thread_model_set_last_post(post_factory, thread, user):
    post = post_factory(thread, poster=user)

    thread.set_last_post(post)
    thread.save()

    assert thread.last_posted_at == post.posted_at
    assert thread.last_post == post
    assert thread.last_poster == user
    assert thread.last_poster_name == user.username
    assert thread.last_poster_slug == user.slug

    thread.refresh_from_db()

    assert thread.last_posted_at == post.posted_at
    assert thread.last_post == post
    assert thread.last_poster == user
    assert thread.last_poster_name == user.username
    assert thread.last_poster_slug == user.slug


def test_thread_private_thread_owner_property_returns_populated_thread_owner(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    owner, _ = get_private_thread_members(thread)
    assert owner == other_user
    assert thread.private_thread_owner == other_user


def test_thread_private_thread_owner_property_raises_attribute_error_if_accessed_without_populating(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with pytest.raises(AttributeError):
        thread.private_thread_owner


def test_thread_private_thread_members_property_returns_populated_members_list(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    _, members = get_private_thread_members(thread)
    assert members == [user, other_user]
    assert thread.private_thread_members == [user, other_user]


def test_thread_private_thread_members_property_raises_attribute_error_if_accessed_without_populating(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with pytest.raises(AttributeError):
        thread.private_thread_members


def test_thread_private_thread_owner_id_property_returns_populated_id_of_private_thread_owner(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    get_private_thread_members(thread)

    with django_assert_num_queries(0):
        assert thread.private_thread_owner_id == other_user.id


def test_thread_private_thread_owner_id_property_returns_prefetched_id_of_private_thread_owner(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    prefetch_private_thread_member_ids([thread])

    with django_assert_num_queries(0):
        assert thread.private_thread_owner_id == other_user.id


def test_thread_private_thread_owner_id_property_fetches_ids(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with django_assert_num_queries(1):
        thread.private_thread_owner_id
        thread.private_thread_member_ids


def test_thread_private_thread_member_ids_property_returns_populated_list_of_private_thread_member_ids(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    get_private_thread_members(thread)

    with django_assert_num_queries(0):
        private_thread_member_ids = list(thread.private_thread_member_ids)
        assert private_thread_member_ids == [user.id, other_user.id]


def test_thread_private_thread_member_ids_property_returns_prefetched_list_of_private_thread_member_ids(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    prefetch_private_thread_member_ids([thread])

    with django_assert_num_queries(0):
        private_thread_member_ids = list(thread.private_thread_member_ids)
        assert private_thread_member_ids == [user.id, other_user.id]


def test_thread_private_thread_member_ids_property_fetches_ids(
    django_assert_num_queries, thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with django_assert_num_queries(1):
        thread.private_thread_member_ids
        thread.private_thread_owner_id
