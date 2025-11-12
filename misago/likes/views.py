from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View

from ..permissions.likes import check_like_post_permission, check_unlike_post_permission
from ..privatethreads.views.generic import PrivateThreadView
from ..threads.redirect import redirect_to_post
from ..threads.views.generic import ThreadView
from .like import like_post, remove_post_like
from .models import Like


class PostLikeView(View):
    def post(
        self, request: HttpRequest, thread_id: int, slug: str, post_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        with transaction.atomic():
            post = self.get_thread_post(request, thread, post_id, for_update=True)
            check_like_post_permission(
                request.user_permissions, thread.category, thread, post
            )

            if not Like.objects.filter(post=post, user=request.user).exists():
                like_post(post, request.user, request=True)

        if not request.is_htmx:
            messages.success(request, pgettext("post like view", "Post liked"))
            return redirect_to_post(request, post)

        post_feed = self.get_posts_feed(request, thread, [])
        context_data = post_feed.get_like_context_data(post, True)
        return render(request, context_data["template_name"], context_data)


class ThreadPostLikeView(PostLikeView, ThreadView):
    pass


class PrivateThreadPostLikeView(PostLikeView, PrivateThreadView):
    pass


class PostUnlikeView(View):
    def post(
        self, request: HttpRequest, thread_id: int, slug: str, post_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        with transaction.atomic():
            post = self.get_thread_post(request, thread, post_id, for_update=True)
            check_unlike_post_permission(
                request.user_permissions, thread.category, thread, post
            )
            remove_post_like(post, request.user, request=True)

        if not request.is_htmx:
            messages.success(request, pgettext("post unlike view", "Post like removed"))
            return redirect_to_post(request, post)

        post_feed = self.get_posts_feed(request, thread, [])
        context_data = post_feed.get_like_context_data(post, False)
        return render(request, context_data["template_name"], context_data)


class ThreadPostUnlikeView(PostUnlikeView, ThreadView):
    pass


class PrivateThreadPostUnlikeView(PostUnlikeView, PrivateThreadView):
    pass


class PostLikesView(View):
    def get(
        self, request: HttpRequest, thread_id: int, slug: str, post_id: int
    ) -> HttpResponse:
        pass


class ThreadPostLikesView(PostLikesView, ThreadView):
    pass


class PrivateThreadPostLikesView(PostLikesView, PrivateThreadView):
    pass
