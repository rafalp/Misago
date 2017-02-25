from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from misago.core.utils import slugify

from .checksums import update_post_checksum
from .models import Poll, Post, Thread


UserModel = get_user_model()


def post_thread(
        category,
        title='Test thread',
        poster='Tester',
        is_global=False,
        is_pinned=False,
        is_unapproved=False,
        is_hidden=False,
        is_closed=False,
        started_on=None
):
    started_on = started_on or timezone.now()

    kwargs = {
        'category': category,
        'title': title,
        'slug': slugify(title),
        'started_on': started_on,
        'last_post_on': started_on,
        'is_unapproved': is_unapproved,
        'is_hidden': is_hidden,
        'is_closed': is_closed,
    }

    if is_global:
        kwargs['weight'] = 2
    elif is_pinned:
        kwargs['weight'] = 1

    try:
        kwargs.update({
            'starter': poster,
            'starter_name': poster.username,
            'starter_slug': poster.slug,
            'last_poster': poster,
            'last_poster_name': poster.username,
            'last_poster_slug': poster.slug,
        })
    except AttributeError:
        kwargs.update({
            'starter_name': poster,
            'starter_slug': slugify(poster),
            'last_poster_name': poster,
            'last_poster_slug': slugify(poster),
        })

    thread = Thread.objects.create(**kwargs)
    reply_thread(
        thread,
        poster=poster,
        posted_on=started_on,
        is_hidden=is_hidden,
        is_unapproved=is_unapproved,
    )

    return thread


def reply_thread(
        thread,
        poster="Tester",
        message="I am test message",
        is_unapproved=False,
        is_hidden=False,
        is_event=False,
        has_reports=False,
        has_open_reports=False,
        posted_on=None,
        poster_ip='127.0.0.1'
):
    posted_on = posted_on or thread.last_post_on + timedelta(minutes=5)

    kwargs = {
        'category': thread.category,
        'thread': thread,
        'original': message,
        'parsed': message,
        'checksum': 'nope',
        'poster_ip': poster_ip,
        'posted_on': posted_on,
        'updated_on': posted_on,
        'is_event': is_event,
        'is_unapproved': is_unapproved,
        'is_hidden': is_hidden,
        'has_reports': has_reports,
        'has_open_reports': has_open_reports,
    }

    try:
        kwargs.update({
            'poster': poster,
            'poster_name': poster.username,
        })
    except AttributeError:
        kwargs.update({'poster_name': poster})

    post = Post.objects.create(**kwargs)

    update_post_checksum(post)
    post.save()

    thread.synchronize()
    thread.save()
    thread.category.synchronize()
    thread.category.save()

    return post


def post_poll(thread, poster):
    poll = Poll.objects.create(
        category=thread.category,
        thread=thread,
        poster=poster,
        poster_name=poster.username,
        poster_slug=poster.slug,
        poster_ip='127.0.0.1',
        question="Lorem ipsum dolor met?",
        choices=[
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 1
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 0
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 2
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 1
            },
        ],
        allowed_choices=2,
        votes=4
    )

    # one user voted for Alpha choice
    try:
        user = UserModel.objects.get(slug='bob')
    except UserModel.DoesNotExist:
        user = UserModel.objects.create_user('bob', 'bob@test.com', 'Pass.123')

    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=user,
        voter_name=user.username,
        voter_slug=user.slug,
        voter_ip='127.0.0.1',
        choice_hash='aaaaaaaaaaaa',
    )

    # test user voted on third and last choices
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=poster,
        voter_name=poster.username,
        voter_slug=poster.slug,
        voter_ip='127.0.0.1',
        choice_hash='gggggggggggg',
    )
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=poster,
        voter_name=poster.username,
        voter_slug=poster.slug,
        voter_ip='127.0.0.1',
        choice_hash='dddddddddddd',
    )

    # somebody else voted on third option before being deleted
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter_name='deleted',
        voter_slug='deleted',
        voter_ip='127.0.0.1',
        choice_hash='gggggggggggg',
    )

    return poll


def like_post(post, liker=None, username=None):
    if not post.last_likes:
        post.last_likes = []

    if liker:
        like = post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker=liker,
            liker_name=liker.username,
            liker_slug=liker.slug,
            liker_ip='127.0.0.1',
        )

        post.last_likes = [{
            'id': liker.id,
            'username': liker.username,
        }] + post.last_likes
    else:
        like = post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker_name=username,
            liker_slug=slugify(username),
            liker_ip='127.0.0.1',
        )

        post.last_likes = [{
            'id': None,
            'username': username,
        }] + post.last_likes

    post.likes += 1
    post.save()

    return like
