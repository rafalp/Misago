from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from misago.core.shortcuts import get_int_or_404
from misago.users.online.utils import make_users_status_aware

from ..models import Post
from ..permissions.threads import allow_edit_post, allow_reply_thread
from ..serializers import PostSerializer
from ..viewmodels.post import ThreadPost
from ..viewmodels.posts import ThreadPosts
from ..viewmodels.thread import ForumThread
from .postingendpoint import PostingEndpoint


class ViewSet(viewsets.ViewSet):
    thread = None
    posts = None

    def get_thread(self, request, pk):
        return self.thread(request, get_int_or_404(pk), read_aware=True, subscription_aware=True)

    def get_posts(self, request, thread, page):
        return self.posts(request, thread, page)

    def create(self, request, thread_pk):
        thread = self.thread(request, get_int_or_404(thread_pk))
        allow_reply_thread(request.user, thread.thread)

        post = Post(thread=thread.thread, category=thread.category)

        # Put them through posting pipeline
        posting = PostingEndpoint(
            request,
            PostingEndpoint.REPLY,
            thread=thread.thread,
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

    def update(self, request, thread_pk, pk):
        thread = self.thread(request, get_int_or_404(thread_pk))
        post = ThreadPost(request, thread, get_int_or_404(pk)).post

        allow_edit_post(request.user, post)

        posting = PostingEndpoint(
            request,
            PostingEndpoint.EDIT,
            thread=thread.thread,
            post=post
        )

        if posting.is_valid():
            raise NotImplementedError("NOT YET!")
        else:
            return Response(posting.errors, status=400)

        return Response({})

    def list(self, request, thread_pk):
        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0 # api allows explicit first page

        thread = self.get_thread(request, thread_pk)
        posts = self.get_posts(request, thread, page)

        data = thread.get_frontend_context()
        data['post_set'] = posts.get_frontend_context()

        return Response(data)

    @detail_route(methods=['get'], url_path='editor')
    def post_editor(self, request, thread_pk, pk):
        thread = self.thread(request, get_int_or_404(thread_pk))
        post = ThreadPost(request, thread, get_int_or_404(pk)).post

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
            reply_to = ThreadPost(request, thread, get_int_or_404(request.query_params['reply'])).post

            if reply_to.is_hidden and not reply_to.acl['can_see_hidden']:
                raise PermissionDenied(_("You can't reply to hidden posts"))

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
