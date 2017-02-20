from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.utils import timezone

from misago.categories.models import Category
from misago.threads.models import Post, PostEdit, PostLike, Thread, ThreadParticipant

from . import fetch_assoc, localise_datetime, markup, movedids


UserModel = get_user_model()


def move_threads(stdout, style):
    special_categories = get_special_categories_dict()

    for thread in fetch_assoc('SELECT * FROM misago_thread ORDER BY id'):
        if special_categories.get(thread['forum_id']) == 'reports':
            stdout.write(style.WARNING("Skipping report: %s" % thread['name']))
            continue

        if not thread['start_post_id']:
            stdout.write(style.ERROR("Corrupted thread: %s" % thread['name']))
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
            deleter = UserModel.objects.filter(is_staff=True).order_by('id').last()

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
            original=post['post'],
            parsed=post['post_preparsed'],
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

        movedids.set('post', post['id'], new_post.pk)


def move_mentions():
    for metion in fetch_assoc('SELECT * FROM misago_post_mentions'):
        try:
            post_pk = movedids.get('post', metion['post_id'])
            user_pk = movedids.get('user', metion['user_id'])

            post = Post.objects.get(pk=post_pk)
            user = UserModel.objects.get(pk=user_pk)

            post.mentions.add(user)
        except:
            continue


def move_edits():
    query = 'SELECT DISTINCT post_id FROM misago_change ORDER BY post_id'
    for edit in fetch_assoc(query):
        post_pk = movedids.get('post', edit['post_id'])
        post = Post.objects.select_related().get(pk=post_pk)

        move_post_edits(post, edit['post_id'])


def move_post_edits(post, old_id):
    query = '''
        SELECT *
        FROM
            misago_change
        WHERE
            post_id = %s AND `change` <> 0
        ORDER BY
            id
    '''

    changelog = []
    for edit in fetch_assoc(query, [old_id]):
        if edit['user_id']:
            editor_pk = movedids.get('user', edit['user_id'])
            editor = UserModel.objects.get(pk=editor_pk)
        else:
            editor = None

        if changelog:
            changelog[-1].edited_to = markup.clean_original(edit['post_content'])

        changelog.append(
            PostEdit(
                category=post.category,
                thread=post.thread,
                post=post,
                edited_on=localise_datetime(edit['date']),
                editor=editor,
                editor_name=edit['user_name'],
                editor_slug=edit['user_slug'],
                editor_ip=edit['ip'],
                edited_from=markup.clean_original(edit['post_content']),
                edited_to=markup.clean_original(post.original),
            )
        )

    if changelog:
        PostEdit.objects.bulk_create(changelog)


def move_likes():
    query = '''
        SELECT *
        FROM
            misago_karma
        WHERE
            score > 0
        ORDER BY
            id
    '''

    posts = []
    for karma in fetch_assoc(query):
        post_pk = movedids.get('post', karma['post_id'])
        post = Post.objects.select_related().get(pk=post_pk)

        if karma['user_id']:
            liker_pk = movedids.get('user', karma['user_id'])
            liker = UserModel.objects.get(pk=liker_pk)
        else:
            liker = None

        PostLike.objects.create(
            category=post.category,
            thread=post.thread,
            post=post,
            liker=liker,
            liker_name=karma['user_name'],
            liker_slug=karma['user_slug'],
            liker_ip=karma['ip'],
            liked_on=localise_datetime(karma['date']),
        )

        posts.append(post_pk)

    for post in Post.objects.filter(id__in=posts).iterator():
        post.last_likes = []
        for like in post.postlike_set.all()[:4]:
            post.last_likes.append({'id': like.liker_id, 'username': like.liker_name})
        post.save(update_fields=['last_likes'])


def move_participants():
    for participant in fetch_assoc('SELECT * FROM misago_thread_participants'):
        thread_pk = movedids.get('thread', participant['thread_id'])
        thread = Thread.objects.get(pk=thread_pk)

        user_pk = movedids.get('user', participant['user_id'])
        user = UserModel.objects.get(pk=user_pk)

        starter = thread.post_set.order_by('id').first().poster

        ThreadParticipant.objects.create(thread=thread, user=user, is_owner=(user == starter))


def clean_private_threads(stdout, style):
    category = Category.objects.private_threads()

    # prune threads without participants
    participated_threads = ThreadParticipant.objects.values_list('thread_id', flat=True).distinct()
    for thread in category.thread_set.exclude(pk__in=participated_threads):
        thread.delete()

    # close threads with single participant, delete empty ones
    for thread in category.thread_set.iterator():
        participants_count = thread.participants.count()
        if participants_count == 1:
            thread.is_closed = True
            thread.save()
        elif participants_count == 0:
            thread.delete()
            stdout.write(style.ERROR("Delete empty private thread: %s" % thread.title))


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
