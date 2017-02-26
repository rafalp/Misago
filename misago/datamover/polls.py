from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from misago.threads.models import Poll, PollVote, Thread

from . import fetch_assoc, localise_datetime, movedids


UserModel = get_user_model()


def move_polls():
    for poll in fetch_assoc('SELECT * FROM misago_poll ORDER BY thread_id'):
        thread_pk = movedids.get('thread', poll['thread_id'])
        thread = Thread.objects.select_related().get(pk=thread_pk)

        poster = None
        if poll['user_id']:
            poster_pk = movedids.get('user', poll['user_id'])
            poster = UserModel.objects.get(pk=poster_pk)

        choices = []
        choices_map = {}

        query = 'SELECT * FROM misago_polloption WHERE poll_id = %s ORDER BY id'
        for choice in fetch_assoc(query, [poll['thread_id']]):
            choices.append({
                'hash': get_random_string(12),
                'label': choice['name'],
                'votes': choice['votes'],
            })

            choices_map[choice['id']] = choices[-1]['hash']

        new_poll = Poll.objects.create(
            category=thread.category,
            thread=thread,
            poster=poster,
            poster_name=poll['user_name'],
            poster_slug=poll['user_slug'],
            poster_ip=thread.post_set.order_by('id').first().poster_ip,
            posted_on=localise_datetime(poll['start_date']),
            length=poll['length'],
            question=poll['question'],
            choices=choices,
            allowed_choices=poll['max_choices'],
            allow_revotes=poll['vote_changing'],
            votes=poll['votes'],
            is_public=poll['public'],
        )

        query = 'SELECT * FROM misago_pollvote WHERE poll_id = %s ORDER BY id'
        for vote in fetch_assoc(query, [poll['thread_id']]):
            if not vote['option_id']:
                continue

            voter = None
            if vote['user_id']:
                voter_pk = movedids.get('user', vote['user_id'])
                voter = UserModel.objects.get(pk=voter_pk)

            PollVote.objects.create(
                category=thread.category,
                thread=thread,
                poll=new_poll,
                voter=voter,
                voter_name=vote['user_name'],
                voter_slug=vote['user_slug'],
                voter_ip=vote['ip'],
                voted_on=localise_datetime(vote['date']),
                choice_hash=choices_map[vote['option_id']],
            )
