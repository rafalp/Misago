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


def test_thread_private_thread_member_ids_property_returns_list_of_private_thread_member_ids(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    private_thread_member_ids = list(thread.private_thread_member_ids)
    assert private_thread_member_ids == [other_user.id, user.id]


def test_thread_private_thread_owner_id_property_returns_id_of_private_thread_owner(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    assert thread.private_thread_owner_id == other_user.id


def test_thread_private_thread_owner_id_property_returns_none_if_thread_has_no_members(
    thread,
):
    assert thread.private_thread_owner_id is None


def test_thread_private_thread_owner_id_property_returns_none_if_thread_has_no_owner(
    thread, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=other_user)
    assert thread.private_thread_owner_id is None
