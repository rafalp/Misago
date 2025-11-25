from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View

from ..permissions.likes import (
    check_like_post_permission,
    check_see_post_likes_permission,
    check_unlike_post_permission,
)
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

        post_feed = self.get_post_feed(request, thread, [])
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

        post_feed = self.get_post_feed(request, thread, [])
        context_data = post_feed.get_like_context_data(post, False)
        return render(request, context_data["template_name"], context_data)


class ThreadPostUnlikeView(PostUnlikeView, ThreadView):
    pass


class PrivateThreadPostUnlikeView(PostUnlikeView, PrivateThreadView):
    pass


class PostLikesView(View):
    template_name: str
    template_name_htmx = "misago/post_likes/htmx.html"
    template_name_modal = "misago/post_likes/modal.html"

    def get(
        self, request: HttpRequest, thread_id: int, slug: str, post_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        check_see_post_likes_permission(
            request.user_permissions, thread.category, thread, post
        )

        try:
            page = request.GET.get("page")
            if page is not None:
                page = int(page)
        except (TypeError, ValueError):
            raise Http404()

        if not request.is_htmx and (thread.slug != slug or page == 1):
            return redirect(self.get_thread_url(thread), permanent=thread.slug != slug)

        per_page = 10 if request.is_htmx else 32

        queryset = (
            Like.objects.filter(post=post)
            .select_related("user")
            .prefetch_related("user__group")
            .order_by("-id")
        )

        paginator = Paginator(queryset, per_page, 4)
        page_obj = paginator.get_page(page)

        if request.is_htmx:
            if request.GET.get("modal"):
                template_name = self.template_name_modal
            else:
                template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            {
                "category": thread.category,
                "thread": thread,
                "post": post,
                "paginator": paginator,
                "page": page_obj,
            },
        )


class ThreadPostLikesView(PostLikesView, ThreadView):
    template_name = "misago/thread_post_likes/index.html"


class PrivateThreadPostLikesView(PostLikesView, PrivateThreadView):
    template_name = "misago/private_thread_post_likes/index.html"
