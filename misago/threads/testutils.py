from datetime import timedelta

from django.utils import timezone

from misago.core.utils import slugify

from misago.threads.models import Thread, Post


def post_thread(category, title='Test thread', poster='Tester',
                is_global=False, is_pinned=False, is_moderated=False,
                is_hidden=False, is_closed=False, started_on=None):
    started_on = started_on or timezone.now()

    kwargs = {
        'category': category,
        'title': title,
        'slug': slugify(title),
        'started_on': started_on,
        'last_post_on': started_on,
        'is_moderated': is_moderated,
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
    reply_thread(thread,
        poster=poster,
        posted_on=thread.last_post_on,
        is_hidden=is_hidden,
        is_moderated=is_moderated,
    )

    return thread


def reply_thread(thread, poster="Tester", message='I am test message',
                 is_moderated=False, is_hidden=False, has_reports=False,
                 has_open_reports=False, posted_on=None, poster_ip='127.0.0.1'):
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
        'is_moderated': is_moderated,
        'is_hidden': is_hidden,
        'has_reports': has_reports,
        'has_open_reports': has_open_reports,
    }

    try:
        kwargs.update({'poster': poster, 'poster_name': poster.username})
    except AttributeError:
        kwargs.update({'poster_name': poster})

    post = Post.objects.create(**kwargs)
    thread.synchronize()
    thread.save()
    thread.category.synchronize()
    thread.category.save()

    return post
