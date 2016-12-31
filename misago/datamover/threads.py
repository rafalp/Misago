from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.utils import timezone

from misago.categories.models import Category
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Thread, Post

from . import fetch_assoc, markup, movedids, localise_datetime


UserModel = get_user_model()


def move_threads(stdout, style):
    special_categories = get_special_categories_dict()

    for thread in fetch_assoc('SELECT * FROM misago_thread ORDER BY id'):
        if special_categories.get(thread['forum_id']) == 'reports':
            stdout.write(style.WARNING(
                "Skipping report: %s" % thread['name']))
            continue

        if not thread['start_post_id']:
            stdout.write(style.ERROR(
                "Corrupted thread: %s" % thread['name']))
            continue

        if special_categories.get(thread['forum_id']) == 'private_threads':
            category = Category.objects.private_threads()
        else:
            if thread['prefix_id']:
                label_id = '%s-%s' % (thread['prefix_id'], thread['forum_id'])
                category_pk = movedids.get('label', label_id)
            else:
                category_pk = movedids.get('category', thread['forum_id'])
            category = Category.objects.get(pk=category_pk)

        new_thread = Thread.objects.create(
            category=category,
            title=thread['name'],
            slug=thread['slug'],
            started_on=timezone.now(),
            last_post_on=timezone.now(),
            starter_name='none',
            starter_slug='none',
            weight=thread['weight'],
            is_hidden=thread['deleted'],
            is_closed=thread['closed'],
        )

        movedids.set('thread', thread['id'], new_thread.pk)


def move_posts():
    special_categories = get_special_categories_dict()
    for post in fetch_assoc('SELECT * FROM misago_post ORDER BY id'):
        if special_categories.get(post['forum_id']) == 'reports':
            continue

        thread_pk = movedids.get('thread', post['thread_id'])
        thread = Thread.objects.select_related('category').get(pk=thread_pk)

        poster = None
        last_editor = None

        if post['user_id']:
            poster_id = movedids.get('user', post['user_id'])
            poster = UserModel.objects.get(pk=poster_id)


        if post['edit_user_id']:
            last_editor_id = movedids.get('user', post['edit_user_id'])
            last_editor = UserModel.objects.get(pk=last_editor_id)

        deleter = None
        deleter_name = None
        deleter_slug = None
        if post['deleted']:
            deleter = UserModel.objects.filter(
                is_staff=True
            ).order_by('id').last()

            if deleter:
                deleter_name = deleter.username
                deleter_slug = deleter.slug
            else:
                deleter = poster
                deleter_name = poster.username
                deleter_slug = poster.slug

        new_post = Post.objects.create(
            category=thread.category,
            thread=thread,
            poster=poster,
            poster_name=post['user_name'],
            poster_ip=post['ip'],
            original=markup.convert_original(post['post']),
            parsed=markup.convert_parsed(post['post_preparsed']),
            posted_on=localise_datetime(post['date']),
            updated_on=localise_datetime(post['current_date'] or post['date']),
            hidden_on=localise_datetime(post['delete_date'] or post['date']),
            edits=post['edits'],
            last_editor=last_editor,
            last_editor_name=post['edit_user_name'],
            last_editor_slug=post['edit_user_slug'],
            hidden_by=deleter,
            hidden_by_name=deleter_name,
            hidden_by_slug=deleter_slug,
            is_hidden=post['deleted'],
            is_protected=post['protected'],
            likes=post['upvotes']
        )

        update_post_checksum(new_post)
        new_post.save()

        movedids.set('post', post['id'], new_post.pk)


def get_special_categories_dict():
    special_categories = {}

    query = '''
        SELECT
            id, special
        FROM
            misago_forum
        WHERE
            special IS NOT NULL
    '''

    for special in fetch_assoc(query):
        special_categories[special['id']] = special['special']
    return special_categories
