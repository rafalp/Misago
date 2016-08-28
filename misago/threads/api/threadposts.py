from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import ugettext as _

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from misago.core.shortcuts import get_int_or_404
from misago.users.online.utils import make_users_status_aware

from ..models import Post
from ..moderation import posts as moderation
from ..permissions.threads import (
    allow_delete_event, allow_delete_post, allow_edit_post, allow_reply_thread)
from ..serializers import PostSerializer
from ..viewmodels.post import ThreadPost
from ..viewmodels.posts import ThreadPosts
from ..viewmodels.thread import ForumThread
from .postingendpoint import PostingEndpoint
from .postendpoints.patch_event import event_patch_endpoint
from .postendpoints.patch_post import post_patch_endpoint


class ViewSet(viewsets.ViewSet):
    thread = None
    posts = None
    post = None

    def get_thread(self, request, pk, read_aware=True, subscription_aware=True, select_for_update=False):
        return self.thread(
            request,
            get_int_or_404(pk),
            None,
            read_aware,
            subscription_aware,
            select_for_update
        )

    def get_thread_for_update(self, request, pk):
        return self.get_thread(
            request, pk,
            read_aware=False,
            subscription_aware=False,
            select_for_update=True
        )

    def get_posts(self, request, thread, page):
        return self.posts(request, thread, page)

    def get_post(self, request, thread, pk, select_for_update=False):
        return self.post(request, thread, get_int_or_404(pk), select_for_update)

    def get_post_for_update(self, request, thread, pk):
        return self.get_post(request, thread, pk, select_for_update=True)

    def list(self, request, thread_pk):
        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0 # api allows explicit first page

        thread = self.get_thread(request, thread_pk)
        posts = self.get_posts(request, thread, page)

        data = thread.get_frontend_context()
        data['post_set'] = posts.get_frontend_context()

        return Response(data)

    @transaction.atomic
    def create(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).thread
        allow_reply_thread(request.user, thread)

        post = Post(thread=thread, category=thread.category)

        # Put them through posting pipeline
        posting = PostingEndpoint(
            request,
            PostingEndpoint.REPLY,
            thread=thread,
            post=post
        )

        if posting.is_valid():
            user_posts = request.user.posts

            posting.save()

            # setup extra data for serialization
            post.is_read = False
            post.is_new = True
            post.poster.posts = user_posts + 1

            make_users_status_aware(request.user, [post.poster])

            return Response(PostSerializer(post).data)
        else:
            return Response(posting.errors, status=400)

    @transaction.atomic
    def update(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk)
        post = self.get_post_for_update(request, thread, pk).post

        allow_edit_post(request.user, post)

        posting = PostingEndpoint(
            request,
            PostingEndpoint.EDIT,
            thread=thread.thread,
            post=post
        )

        if posting.is_valid():
            post_edits = post.edits

            posting.save()

            post.is_read = True
            post.is_new = False
            post.edits = post_edits + 1

            if post.poster:
                make_users_status_aware(request.user, [post.poster])

            return Response(PostSerializer(post).data)
        else:
            return Response(posting.errors, status=400)

        return Response({})

    @transaction.atomic
    def partial_update(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk)
        post = self.get_post_for_update(request, thread, pk).post

        if post.is_event:
            return event_patch_endpoint(request, post)
        else:
            return post_patch_endpoint(request, post)

    @transaction.atomic
    def delete(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk)
        post = self.get_post_for_update(request, thread, pk).post

        if post.is_event:
            allow_delete_event(request.user, post)
        else:
            allow_delete_post(request.user, post)

        moderation.delete_post(request.user, post)

        thread.thread.synchronize()
        thread.thread.save()

        thread.category.synchronize()
        thread.category.save()

        return Response({})

    @detail_route(methods=['get'], url_path='editor')
    def post_editor(self, request, thread_pk, pk):
        thread = self.thread(request, get_int_or_404(thread_pk))
        post = self.post(request, thread, get_int_or_404(pk)).post

        allow_edit_post(request.user, post)

        return Response({
            'id': post.pk,
            'api': post.get_api_url(),
            'post': post.original,
            'can_protect': bool(thread.category.acl['can_protect_posts']),
            'is_protected': post.is_protected,
            'poster': post.poster_name
        })

    @list_route(methods=['get'], url_path='editor')
    def reply_editor(self, request, thread_pk):
        thread = self.thread(request, get_int_or_404(thread_pk))
        allow_reply_thread(request.user, thread.thread)

        if 'reply' in request.query_params:
            reply_to = self.post(request, thread, get_int_or_404(request.query_params['reply'])).post

            if reply_to.is_event:
                raise PermissionDenied(_("You can't reply to events."))
            if reply_to.is_hidden and not reply_to.acl['can_see_hidden']:
                raise PermissionDenied(_("You can't reply to hidden posts."))

            return Response({
                'id': reply_to.pk,
                'post': reply_to.original,
                'poster': reply_to.poster_name
            })
        else:
            return Response({})


class ThreadPostsViewSet(ViewSet):
    thread = ForumThread
    posts = ThreadPosts
    post = ThreadPost
