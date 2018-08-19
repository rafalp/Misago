from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.shortcuts import get_int_or_404
from misago.threads.models import Poll
from misago.threads.permissions import (
    allow_delete_poll, allow_edit_poll, allow_see_poll_votes, allow_start_poll, can_start_poll)
from misago.threads.serializers import (
    EditPollSerializer, NewPollSerializer, PollSerializer, PollVoteSerializer)
from misago.threads.viewmodels import ForumThread
from misago.users.audittrail import create_audit_trail

from .pollvotecreateendpoint import poll_vote_create


class ViewSet(viewsets.ViewSet):
    thread = None

    def get_thread(self, request, thread_pk):
        return self.thread(
            request,
            get_int_or_404(thread_pk),
        ).unwrap()

    def get_poll(self, thread, pk):
        try:
            poll_id = get_int_or_404(pk)
            if thread.poll.pk != poll_id:
                raise Http404()

            poll = Poll.objects.get(pk=thread.poll.pk)

            poll.thread = thread
            poll.category = thread.category

            return poll
        except Poll.DoesNotExist:
            raise Http404()

    @transaction.atomic
    def create(self, request, thread_pk):
        thread = self.get_thread(request, thread_pk)
        allow_start_poll(request.user, thread)

        try:
            if thread.poll and thread.poll.pk:
                raise PermissionDenied(_("There's already a poll in this thread."))
        except Poll.DoesNotExist:
            pass

        instance = Poll(
            thread=thread,
            category=thread.category,
            poster=request.user,
            poster_name=request.user.username,
            poster_slug=request.user.slug,
        )

        serializer = NewPollSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        add_acl(request.user, instance)
        for choice in instance.choices:
            choice['selected'] = False

        thread.has_poll = True
        thread.save()

        create_audit_trail(request, instance)

        return Response(PollSerializer(instance).data)

    @transaction.atomic
    def update(self, request, thread_pk, pk=None):
        thread = self.get_thread(request, thread_pk)
        instance = self.get_poll(thread, pk)

        allow_edit_poll(request.user, instance)

        serializer = EditPollSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        add_acl(request.user, instance)
        instance.make_choices_votes_aware(request.user)

        create_audit_trail(request, instance)

        return Response(PollSerializer(instance).data)

    @transaction.atomic
    def delete(self, request, thread_pk, pk=None):
        thread = self.get_thread(request, thread_pk)
        instance = self.get_poll(thread, pk)

        allow_delete_poll(request.user, instance)

        thread.poll.delete()

        thread.has_poll = False
        thread.save()

        return Response({
            'can_start_poll': can_start_poll(request.user, thread),
        })

    @detail_route(methods=['get', 'post'])
    def votes(self, request, thread_pk, pk=None):
        if request.method == 'POST':
            return self.post_votes(request, thread_pk, pk)
        else:
            return self.get_votes(request, thread_pk, pk)

    @transaction.atomic
    def post_votes(self, request, thread_pk, pk=None):
        thread = self.get_thread(request, thread_pk)
        instance = self.get_poll(thread, pk)

        return poll_vote_create(request, thread, instance)

    def get_votes(self, request, thread_pk, pk=None):
        poll_pk = get_int_or_404(pk)

        try:
            thread = self.get_thread(request, thread_pk)
            if thread.poll.pk != poll_pk:
                raise Http404()
        except Poll.DoesNotExist:
            raise Http404()

        allow_see_poll_votes(request.user, thread.poll)

        choices = []
        voters = {}

        for choice in thread.poll.choices:
            choice['voters'] = []
            voters[choice['hash']] = choice['voters']

            choices.append(choice)

        queryset = thread.poll.pollvote_set.values(
            'voter_id', 'voter_name', 'voter_slug', 'voted_on', 'choice_hash'
        )

        for voter in queryset.order_by('voter_name').iterator():
            voters[voter['choice_hash']].append(PollVoteSerializer(voter).data)

        return Response(choices)


class ThreadPollViewSet(ViewSet):
    thread = ForumThread
