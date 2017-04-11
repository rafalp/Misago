from copy import deepcopy

from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.acl import add_acl
from misago.threads.permissions import allow_vote_poll
from misago.threads.serializers import PollSerializer


def poll_vote_create(request, thread, poll):
    poll.make_choices_votes_aware(request.user)

    allow_vote_poll(request.user, poll)

    try:
        clean_votes = validate_votes(poll, request.data)
    except ValidationError as e:
        return Response({'detail': six.text_type(e)}, status=400)

    remove_user_votes(request.user, poll, clean_votes)
    set_new_votes(request, poll, clean_votes)

    add_acl(request.user, poll)
    serialized_poll = PollSerializer(poll).data

    poll.choices = list(map(presave_clean_choice, deepcopy(poll.choices)))
    poll.save()

    return Response(serialized_poll)


def presave_clean_choice(choice):
    del choice['selected']
    return choice


def validate_votes(poll, votes):
    try:
        votes_len = len(votes)
        if votes_len > poll.allowed_choices:
            message = ungettext(
                "This poll disallows voting for more than %(choices)s choice.",
                "This poll disallows voting for more than %(choices)s choices.",
                poll.allowed_choices,
            )
            raise ValidationError(message % {'choices': poll.allowed_choices})
    except TypeError:
        raise ValidationError(_("One or more of poll choices were invalid."))

    valid_choices = [c['hash'] for c in poll.choices]
    clean_votes = []

    for vote in votes:
        if vote in valid_choices:
            clean_votes.append(vote)

    if len(clean_votes) != len(votes):
        raise ValidationError(_("One or more of poll choices were invalid."))
    if not len(votes):
        raise ValidationError(_("You have to make a choice."))

    return clean_votes


def remove_user_votes(user, poll, final_votes):
    removed_votes = []
    for choice in poll.choices:
        if choice['selected'] and choice['hash'] not in final_votes:
            poll.votes -= 1
            choice['votes'] -= 1

            choice['selected'] = False
            removed_votes.append(choice['hash'])

    if removed_votes:
        poll.pollvote_set.filter(voter=user, choice_hash__in=removed_votes).delete()


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
