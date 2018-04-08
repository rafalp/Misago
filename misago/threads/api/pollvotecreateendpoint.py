from copy import deepcopy

from rest_framework.response import Response

from misago.acl import add_acl
from misago.threads.permissions import allow_vote_poll
from misago.threads.serializers import PollSerializer, NewVoteSerializer


def poll_vote_create(request, thread, poll):
    poll.make_choices_votes_aware(request.user)

    allow_vote_poll(request.user, poll)

    serializer = NewVoteSerializer(
        # FIXME: lets use {'choices': []} JSON instead!
        data={'choices': request.data},
        context={
            'allowed_choices': poll.allowed_choices,
            'choices': poll.choices,
        },
    )

    serializer.is_valid(raise_exception=True)

    validated_choices = serializer.validated_data['choices']

    remove_user_votes(request.user, poll, validated_choices)
    set_new_votes(request, poll, validated_choices)

    add_acl(request.user, poll)
    serialized_poll = PollSerializer(poll).data

    poll.choices = list(map(presave_clean_choice, deepcopy(poll.choices)))
    poll.save()

    return Response(serialized_poll)


def presave_clean_choice(choice):
    del choice['selected']
    return choice


def remove_user_votes(user, poll, final_votes):
    removed_votes = []
    for choice in poll.choices:
        if choice['selected'] and choice['hash'] not in final_votes:
            poll.votes -= 1
            choice['votes'] -= 1

            choice['selected'] = False
            removed_votes.append(choice['hash'])

    if removed_votes:
        poll.pollvote_set.filter(
            voter=user,
            choice_hash__in=removed_votes,
        ).delete()


def set_new_votes(request, poll, final_votes):
    for choice in poll.choices:
        if not choice['selected'] and choice['hash'] in final_votes:
            poll.votes += 1
            choice['votes'] += 1

            choice['selected'] = True
            poll.pollvote_set.create(
                category=poll.category,
                thread=poll.thread,
                voter=request.user,
                voter_name=request.user.username,
                voter_slug=request.user.slug,
                choice_hash=choice['hash'],
                voter_ip=request.user_ip,
            )
