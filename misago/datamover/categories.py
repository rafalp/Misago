from __future__ import unicode_literals

from misago.categories.models import Category

from . import fetch_assoc, movedids


def move_categories(stdout, style):
    query = '''
        SELECT *
        FROM
            misago_forum
        WHERE
            tree_id = %s AND level > 0
        ORDER BY
            lft
    '''

    root = Category.objects.root_category()
    for forum in fetch_assoc(query, [get_root_tree()]):
        if forum['type'] == 'redirect':
            stdout.write(style.ERROR('Skipping redirect: %s' % forum['name']))
            continue

        if forum['level'] == 1:
            parent = root
        else:
            new_parent_id = movedids.get('category', forum['parent_id'])
            parent = Category.objects.get(pk=new_parent_id)

        category = Category.objects.insert_node(
            Category(
                name=forum['name'],
                slug=forum['slug'],
                description=forum['description'],
                is_closed=forum['closed'],
                prune_started_after=forum['prune_start'],
                prune_replied_after=forum['prune_last'],
            ),
            parent,
            save=True
        )

        movedids.set('category', forum['id'], category.pk)

    # second pass: move prune_archive_id
    for forum in fetch_assoc(query, [get_root_tree()]):
        if not forum['pruned_archive_id']:
            continue

        new_category_pk = movedids.get('category', forum['id'])
        new_archive_pk = movedids.get('category', forum['pruned_archive_id'])

        Category.objects.filter(pk=new_category_pk).update(
            archive_pruned_in=Category.objects.get(pk=new_archive_pk)
        )


def get_root_tree():
    query = 'SELECT tree_id FROM misago_forum WHERE special = %s'
    for root in fetch_assoc(query, ['root']):
        return root['tree_id']


def move_labels():
    labels = []
    for label in fetch_assoc('SELECT * FROM misago_threadprefix ORDER BY slug'):
        labels.append(label)

    for label in labels:
        query = 'SELECT * FROM misago_threadprefix_forums WHERE threadprefix_id= %s'
        for parent_row in fetch_assoc(query, [label['id']]):
            parent_id = movedids.get('category', parent_row['forum_id'])
            parent = Category.objects.get(pk=parent_id)

            category = Category.objects.insert_node(
                Category(
                    name=label['name'],
                    slug=label['slug'],
                ), parent, save=True
            )

            label_id = '%s-%s' % (label['id'], parent_row['forum_id'])
            movedids.set('label', label_id, category.pk)
