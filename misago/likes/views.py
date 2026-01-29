from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import npgettext, pgettext
from django.views import View

from ..permissions.likes import (
    check_like_post_permission,
    check_see_post_likes_permission,
    check_unlike_post_permission,
)
from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Post, Thread
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
        context_data["post_number"] = self.get_thread_post_number(
            self.request, thread, post
        )

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
        context_data["post_number"] = self.get_thread_post_number(
            self.request, thread, post
        )

        return render(request, context_data["template_name"], context_data)


class ThreadPostUnlikeView(PostUnlikeView, ThreadView):
    pass


class PrivateThreadPostUnlikeView(PostUnlikeView, PrivateThreadView):
    pass


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class PostLikesView(View):
    template_name: str
    partial_template_name = "misago/post_likes/partial.html"
    modal_template_name = "misago/post_likes/modal/index.html"

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        page: int | None = None,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        check_see_post_likes_permission(
            request.user_permissions, thread.category, thread, post
        )

        if not request.is_htmx and (thread.slug != slug or page == 1):
            return redirect(
                self.get_post_likes_url(thread, post), permanent=thread.slug != slug
            )

        try:
            likes_data = self.get_likes_data(request, post, page)
        except PageOutOfRangeError as exc:
            return redirect(exc.redirect_to)

        if request.is_htmx:
            if request.GET.get("modal"):
                template_name = self.modal_template_name
            else:
                template_name = self.partial_template_name

            likes_data.update(
                {
                    "category": thread.category,
                    "thread": thread,
                    "post": post,
                }
            )

            return render(request, template_name, likes_data)

        return render(
            request,
            self.template_name,
            {
                "category": thread.category,
                "thread": thread,
                "post": post,
                "post_number": self.get_thread_post_number(request, thread, post),
                "likes": likes_data,
                "thread_url": self.get_thread_url(thread),
                "post_url": self.get_thread_post_url(thread, post),
            },
        )

    def get_likes_data(
        self, request: HttpRequest, post: Post, page: int | None
    ) -> dict:
        is_modal = request.is_htmx and request.GET.get("modal")
        per_page = 10 if request.is_htmx and is_modal else 32

        queryset = (
            Like.objects.filter(post=post)
            .select_related("user")
            .prefetch_related("user__group")
            .order_by("-id")
        )

        paginator = Paginator(queryset, per_page, 4)
        if page and page > paginator.num_pages:
            if not request.is_htmx:
                raise PageOutOfRangeError(
                    self.get_post_likes_url(post.thread, post, paginator.num_pages)
                )

            page = paginator.num_pages

        page_obj = paginator.get_page(page)

        if request.user.is_authenticated:
            is_liked = Like.objects.filter(post=post, user=request.user).exists()
        else:
            is_liked = False

        if post.likes:
            description = self.get_likes_description(post.likes, is_liked)
        else:
            description = None

        return {
            "template_name": self.partial_template_name,
            "paginator": paginator,
            "page": page_obj,
            "is_liked": is_liked,
            "description": description,
            "items": page_obj.object_list,
            "likes_url": self.get_post_likes_url(post.thread, post),
        }

    def get_likes_description(self, likes: int, is_liked: bool) -> str | None:
        if is_liked:
            remaining_likes = likes - 1
            if remaining_likes:
                return npgettext(
                    "post likes page description",
                    "You and %(users)s other likes this post.",
                    "You and %(users)s others like this post.",
                    likes,
                ) % {"users": remaining_likes}

            return pgettext("post likes page description", "You like this post.")

        return npgettext(
            "post likes page description",
            "%(users)s user likes this post.",
            "%(users)s users like this post.",
            likes,
        ) % {"users": likes}

    def get_post_likes_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        raise NotImplementedError()


class ThreadPostLikesView(PostLikesView, ThreadView):
    template_name = "misago/thread_post_likes/index.html"

    def get_post_likes_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        if page and page > 1:
            return reverse(
                "misago:thread-post-likes",
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "post_id": post.id,
                    "page": page,
                },
            )

        return reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )


class PrivateThreadPostLikesView(PostLikesView, PrivateThreadView):
    template_name = "misago/private_thread_post_likes/index.html"

    def get_post_likes_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        if page and page > 1:
            return reverse(
                "misago:private-thread-post-likes",
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "post_id": post.id,
                    "page": page,
                },
            )

        return reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
