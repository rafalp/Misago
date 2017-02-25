from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.shortcuts import get_int_or_404
from misago.threads.models import Post
from misago.threads.moderation import posts as moderation
from misago.threads.permissions import (
    allow_delete_event, allow_delete_post, allow_edit_post, allow_reply_thread)
from misago.threads.serializers import AttachmentSerializer, PostSerializer
from misago.threads.viewmodels import ForumThread, PrivateThread, ThreadPost, ThreadPosts
from misago.users.online.utils import make_users_status_aware

from .postendpoints.edits import get_edit_endpoint, revert_post_endpoint
from .postendpoints.likes import likes_list_endpoint
from .postendpoints.merge import posts_merge_endpoint
from .postendpoints.move import posts_move_endpoint
from .postendpoints.patch_event import event_patch_endpoint
from .postendpoints.patch_post import post_patch_endpoint
from .postendpoints.read import post_read_endpoint
from .postendpoints.split import posts_split_endpoint
from .postingendpoint import PostingEndpoint


class ViewSet(viewsets.ViewSet):
    thread = None
    posts = ThreadPosts
    post_ = ThreadPost

    def get_thread(
            self,
            request,
            pk,
            read_aware=True,
            subscription_aware=True,
            select_for_update=False,
    ):
        return self.thread(
            request,
            get_int_or_404(pk),
            None,
            read_aware,
            subscription_aware,
            select_for_update,
        )

    def get_thread_for_update(self, request, pk):
        return self.get_thread(
            request,
            pk,
            read_aware=False,
            subscription_aware=False,
            select_for_update=True,
        )

    def get_posts(self, request, thread, page):
        return self.posts(request, thread, page)

    def get_post(self, request, thread, pk, select_for_update=False):
        return self.post_(request, thread, get_int_or_404(pk), select_for_update)

    def get_post_for_update(self, request, thread, pk):
        return self.get_post(request, thread, pk, select_for_update=True)

    def list(self, request, thread_pk):
        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        thread = self.get_thread(request, thread_pk)
        posts = self.get_posts(request, thread, page)

        data = thread.get_frontend_context()
        data['post_set'] = posts.get_frontend_context()

        return Response(data)

    @list_route(methods=['post'])
    @transaction.atomic
    def merge(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).unwrap()
        return posts_merge_endpoint(request, thread)

    @list_route(methods=['post'])
    @transaction.atomic
    def move(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).unwrap()
        return posts_move_endpoint(request, thread, self.thread)

    @list_route(methods=['post'])
    @transaction.atomic
    def split(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).unwrap()
        return posts_split_endpoint(request, thread)

    @transaction.atomic
    def create(self, request, thread_pk):
        thread = self.get_thread_for_update(request, thread_pk).unwrap()
        allow_reply_thread(request.user, thread)

        post = Post(
            thread=thread,
            category=thread.category,
        )

        # Put them through posting pipeline
        posting = PostingEndpoint(
            request,
            PostingEndpoint.REPLY,
            thread=thread,
            post=post,
        )

        if posting.is_valid():
            user_posts = request.user.posts

            posting.save()

            # setup extra data for serialization
            post.is_read = False
            post.is_new = True
            post.poster.posts = user_posts + 1

            make_users_status_aware(request.user, [post.poster])

            return Response(PostSerializer(post, context={'user': request.user}).data)
        else:
            return Response(posting.errors, status=400)

    @transaction.atomic
    def update(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk).unwrap()
        post = self.get_post_for_update(request, thread, pk).unwrap()

        allow_edit_post(request.user, post)

        posting = PostingEndpoint(
            request,
            PostingEndpoint.EDIT,
            thread=thread,
            post=post,
        )

        if posting.is_valid():
            post_edits = post.edits

            posting.save()

            post.is_read = True
            post.is_new = False
            post.edits = post_edits + 1

            if post.poster:
                make_users_status_aware(request.user, [post.poster])

            return Response(PostSerializer(post, context={'user': request.user}).data)
        else:
            return Response(posting.errors, status=400)

    @transaction.atomic
    def partial_update(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk)
        post = self.get_post_for_update(request, thread, pk).unwrap()

        if post.is_event:
            return event_patch_endpoint(request, post)
        else:
            return post_patch_endpoint(request, post)

    @transaction.atomic
    def delete(self, request, thread_pk, pk):
        thread = self.get_thread_for_update(request, thread_pk)
        post = self.get_post_for_update(request, thread, pk).unwrap()

        if post.is_event:
            allow_delete_event(request.user, post)
        else:
            allow_delete_post(request.user, post)

        moderation.delete_post(request.user, post)

        thread.synchronize()
        thread.save()

        thread.category.synchronize()
        thread.category.save()

        return Response({})

    @detail_route(methods=['post'])
    @transaction.atomic
    def read(self, request, thread_pk, pk):
        request.user.lock()

        thread = self.get_thread(request, thread_pk).unwrap()
        post = self.get_post(request, thread, pk).unwrap()

        return post_read_endpoint(request, thread, post)

    @detail_route(methods=['get'], url_path='editor')
    def post_editor(self, request, thread_pk, pk):
        thread = self.get_thread(
            request,
            thread_pk,
            read_aware=False,
            subscription_aware=False,
        )
        post = self.get_post(request, thread, pk).unwrap()

        allow_edit_post(request.user, post)

        attachments = []
        for attachment in post.attachment_set.order_by('-id'):
            add_acl(request.user, attachment)
            attachments.append(attachment)
        attachments_json = AttachmentSerializer(
            attachments, many=True, context={'user': request.user}
        ).data

        return Response({
            'id': post.pk,
            'api': post.get_api_url(),
            'post': post.original,
            'attachments': attachments_json,
            'can_protect': bool(thread.category.acl['can_protect_posts']),
            'is_protected': post.is_protected,
            'poster': post.poster_name,
        })

    @list_route(methods=['get'], url_path='editor')
    def reply_editor(self, request, thread_pk):
        thread = self.get_thread(
            request, thread_pk, read_aware=False, subscription_aware=False
        ).unwrap()
        allow_reply_thread(request.user, thread)

        if 'reply' in request.query_params:
            reply_to = self.get_post(request, thread, request.query_params['reply']).unwrap()

            if reply_to.is_event:
                raise PermissionDenied(_("You can't reply to events."))
            if reply_to.is_hidden and not reply_to.acl['can_see_hidden']:
                raise PermissionDenied(_("You can't reply to hidden posts."))

            return Response({
                'id': reply_to.pk,
                'post': reply_to.original,
                'poster': reply_to.poster_name,
            })
        else:
            return Response({})

    @detail_route(methods=['get', 'post'])
    def edits(self, request, thread_pk, pk):
        if request.method == 'GET':
            thread = self.get_thread(request, thread_pk)
            post = self.get_post(request, thread, pk).unwrap()

            return get_edit_endpoint(request, post)

        if request.method == 'POST':
            with transaction.atomic():
                thread = self.get_thread(request, thread_pk)
                post = self.get_post_for_update(request, thread, pk).unwrap()

                allow_edit_post(request.user, post)

                return revert_post_endpoint(request, post)

    @detail_route(methods=['get'])
    def likes(self, request, thread_pk, pk):
        thread = self.get_thread(request, thread_pk)
        post = self.get_post(request, thread, pk).unwrap()

        if post.acl['can_see_likes'] < 2:
            raise PermissionDenied(_("You can't see who liked this post."))

        return likes_list_endpoint(request, post)


class ThreadPostsViewSet(ViewSet):
    thread = ForumThread


class PrivateThreadPostsViewSet(ViewSet):
    thread = PrivateThread
