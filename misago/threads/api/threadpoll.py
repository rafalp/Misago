from django.db import transaction
from django.http import Http404

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from misago.acl import add_acl
from misago.core.shortcuts import get_int_or_404

from ..models import Poll, PollVote
from ..permissions.polls import allow_start_poll, allow_edit_poll
from ..serializers import PollSerializer, NewPollSerializer, EditPollSerializer
from ..viewmodels.thread import ForumThread


class ViewSet(viewsets.ViewSet):
    thread = None

    def get_thread(self, request, thread_pk, select_for_update=False):
        return self.thread(
            request,
            get_int_or_404(thread_pk),
            select_for_update=select_for_update,
        ).model

    def get_thread_for_update(self, request, thread_pk):
        return self.get_thread(request, thread_pk, select_for_update=True)

    def get_poll(self, thread, pk):
        try:
            poll_id = get_int_or_404(pk)
            if thread.poll.pk != poll_id:
                raise Http404()

            poll = Poll.objects.select_for_update().get(pk=thread.poll.pk)

            poll.thread = thread
            poll.category = thread.category

            return poll
        except Poll.DoesNotExist:
            raise Http404()

    @transaction.atomic
    def create(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk)
        allow_start_poll(request.user, thread)

        instance = Poll(
            thread=thread,
            category=thread.category,
            poster=request.user,
            poster_name=request.user.username,
            poster_slug=request.user.slug,
            poster_ip=request.user_ip,
        )

        serializer = NewPollSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            add_acl(request.user, instance)
            return Response(PollSerializer(instance).data)
        else:
            return Response(serializer.errors, status=400)

    @transaction.atomic
    def update(self, request, thread_pk, pk):
        thread = self.get_thread(request, thread_pk)
        instance = self.get_poll(thread, pk)

        allow_edit_poll(request.user, instance)

        serializer = EditPollSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            add_acl(request.user, instance)
            serialized_poll = PollSerializer(instance).data
            instance.make_choices_votes_aware(request.user, serialized_poll['choices'])
            return Response(serialized_poll)
        else:
            return Response(serializer.errors, status=400)


    # edit poll
    # delete poll
    # vote in poll
    # see voters


class ThreadPollViewSet(ViewSet):
    thread = ForumThread
