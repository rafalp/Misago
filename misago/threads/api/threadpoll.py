from django.db import transaction
from django.http import Http404

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from misago.acl import add_acl
from misago.core.shortcuts import get_int_or_404

from ..models import Poll, PollVote
from ..permissions.polls import allow_start_poll
from ..serializers import PollSerializer, NewPollSerializer, EditPollSerializer
from ..viewmodels.thread import ForumThread


class ViewSet(viewsets.ViewSet):
    thread = None

    def get_thread(self, request, thread_pk, select_for_update=False):
        return self.thread(
            request,
            get_int_or_404(thread_pk),
            select_for_update=select_for_update,
        )

    def get_thread_for_update(self, request, thread_pk):
        return self.get_thread(request, thread_pk, select_for_update=True)

    def get_poll(self, thread):
        try:
            return thread.poll
        except Poll.DoesNotExist:
            raise Http404()

    @transaction.atomic
    def create(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).model
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

    # create poll
    # edit poll
    # delete poll
    # vote in poll
    # see voters


class ThreadPollViewSet(ViewSet):
    thread = ForumThread
