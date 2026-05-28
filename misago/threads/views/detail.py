from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import QuerySet
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ...categories.models import Category
from ...metadata import TextMetaData
from ...moderation.actions import (
    ModerationActionResult,
    ModerationActionTemplateResult,
    PostModerationAction,
    PostsModerationAction,
    ThreadModerationAction,
)
from ...moderation.post import get_thread_post_moderation_actions
from ...moderation.posts import get_thread_posts_moderation_actions
from ...moderation.thread import get_thread_moderation_actions
from ...moderation.views import (
    get_moderation_action,
    get_moderation_action_choices,
    set_moderation_response_headers,
)
from ...notifications.threads import get_watched_thread, update_watched_thread_read_time
from ...permissions.checkutils import check_permissions
from ...permissions.polls import check_start_thread_poll_permission
from ...permissions.threads import (
    check_edit_thread_permission,
    check_reply_thread_permission,
)
from ...polls.enums import PollTemplate
from ...polls.models import Poll
from ...polls.views import dispatch_thread_poll_view, get_poll_context_data
from ...polls.votes import get_user_poll_votes
from ...posting.formsets import (
    ThreadReplyFormset,
    get_thread_reply_formset,
)
from ...readtracker.tracker import (
    get_unread_posts,
    mark_category_read,
    mark_thread_read,
)
from ...readtracker.threads import is_category_read
from ...threadupdates.models import ThreadUpdate
from ..breadcrumbs import get_thread_breadcrumbs
from ..hooks import (
    get_thread_detail_view_context_data_hook,
    get_thread_detail_view_moderation_result_data_hook,
    get_thread_detail_view_posts_queryset_hook,
)
from ..models import Post, Thread
from ..paginator import ThreadPostsPaginator
from .backend import thread_backend
from .generic import GenericThreadView

if TYPE_CHECKING:
    from ...users.models import User


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class DetailView(GenericThreadView):
    template_name: str
    template_partial_name: str
    header_template_name: str
    meta_bar_template_name: str = "misago/thread/meta_bar.html"
    footer_template_name: str
    moderation_modal_template_name: str = "misago/thread/moderation_modal.html"
    moderation_page_template_name: str = "misago/thread/moderation_page.html"
    moderation_result_template_name: str = "misago/thread/moderation_result.html"
    reply_error_template_name: str = "misago/thread/reply_error.html"
    reply_template_name: str = "misago/quick_reply/form.html"
    watch_thread_template_name: str = "misago/thread/watch_thread.html"

    status_bars_template_name: str = "misago/thread/status_bars.html"
    locked_thread_status_bar_template_name: str = "misago/thread/locked_thread.html"
    unapproved_thread_status_bar_template_name: str = (
        "misago/thread/unapproved_thread.html"
    )
    unapproved_posts_status_bar_template_name: str = (
        "misago/thread/unapproved_posts.html"
    )

    # Dispatch

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except PageOutOfRangeError as exc:
            return redirect(exc.redirect_to)

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        page: int | None = None,
        **kwargs,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if not request.is_htmx and (thread.slug != slug or page == 1):
            return redirect(self.get_thread_url(thread), permanent=thread.slug != slug)

        context = self.get_context_data(request, thread, page, kwargs)

        if request.is_htmx:
            template_name = self.template_partial_name
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        if "thread_moderation" in request.POST:
            return self.handle_thread_moderation(request, thread_id, slug, page)

        if "post_moderation" in request.POST:
            return self.handle_post_moderation(request, thread_id, slug, page)

        if "posts_moderation" in request.POST:
            return self.handle_posts_moderation(request, thread_id, slug, page)

        return self.get(request, thread_id, slug, page)

    # View overrides

    def get_thread(self, *args, **kwargs) -> Thread:
        return super().get_thread(*args, annotate_read_time=True, **kwargs)

    # Moderation

    def handle_thread_moderation(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        try:
            result = self.execute_thread_moderation_action(request, thread)
        except ValidationError as e:
            if request.is_htmx:
                raise

            messages.error(request, e.message)
            return self.get(request, thread_id, slug, page)

        if isinstance(result, ModerationActionTemplateResult):
            if request.is_htmx:
                template_name = self.moderation_modal_template_name
            else:
                template_name = self.moderation_page_template_name

            return result.render(request, template_name)

        if thread.id in result.deleted_items:
            parent_url = self.get_thread_parent_url(request, thread)
            if not request.is_htmx:
                return redirect(parent_url)

            response = HttpResponse(status=201)
            response.headers["hx-redirect"] = parent_url
            set_moderation_response_headers(request, response)
            return response

        context_data = self.get_moderation_result_data(request, thread)

        if thread_updates := result.thread_updates:
            post_feed = self.get_post_feed(request, thread, [], thread_updates)
            post_feed.set_animated_thread_updates(
                [update.id for update in thread_updates]
            )
            context_data["thread_updates"] = post_feed.get_context_data()["items"]

        response = render(request, self.moderation_result_template_name, context_data)
        set_moderation_response_headers(request, response)

        return response

    def execute_thread_moderation_action(
        self, request: HttpRequest, thread: Thread
    ) -> HttpResponse:
        actions = self.get_thread_moderation_actions(request, thread)
        action: ThreadModerationAction = get_moderation_action(
            actions, request.POST["thread_moderation"]
        )

        action_obj = action(request, thread)
        action_obj.validate()

        result = action_obj.execute()

        if isinstance(result, ModerationActionTemplateResult):
            result.update_context(
                {
                    "moderation_action": action_obj,
                    "moderation_type": "thread_moderation",
                    "breadcrumbs": self.get_thread_breadcrumbs(request, thread),
                    "thread": thread,
                    "cancel_url": request.get_full_path(),
                }
            )

        return result

    def handle_posts_moderation(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        try:
            result = self.execute_posts_moderation_action(request, thread, page)
        except ValidationError as e:
            if request.is_htmx:
                raise

            messages.error(request, e.message)
            return self.get(request, thread_id, slug, page)

        if isinstance(result, ModerationActionTemplateResult):
            if request.is_htmx:
                template_name = self.moderation_modal_template_name
            else:
                template_name = self.moderation_page_template_name

            return result.render(request, template_name)

        if request.is_htmx:
            response = self.get(
                request,
                thread_id,
                slug,
                page,
                updated_posts=result.updated_items,
            )
            set_moderation_response_headers(request, response)
            return response

        return redirect(request.get_full_path())

    def execute_posts_moderation_action(
        self, request: HttpRequest, thread: Thread, page: int | None
    ) -> ModerationActionResult:
        actions = self.get_posts_moderation_actions(request, thread)
        action: PostsModerationAction = get_moderation_action(
            actions, request.POST["posts_moderation"]
        )

        page_obj = self.get_posts_page(request, thread, page)
        page_posts = list(page_obj.object_list)
        selected_posts = self.get_selected_posts(request, page_posts)

        action_obj = action(request, thread, selected_posts)
        action_obj.validate()

        result = action_obj.execute()

        if isinstance(result, ModerationActionTemplateResult):
            result.update_context(
                {
                    "moderation_action": action_obj,
                    "moderation_type": "posts_moderation",
                    "breadcrumbs": self.get_thread_breadcrumbs(request, thread),
                    "thread": thread,
                    "posts": page_posts,
                    "selection": selected_posts,
                    "cancel_url": request.get_full_path(),
                },
            )

        return result

    def handle_post_moderation(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        try:
            post = self.get_selected_post(request, thread)
            result = self.execute_post_moderation_action(request, thread, post)
        except ValidationError as e:
            if request.is_htmx:
                raise

            messages.error(request, e.message)
            return self.get(request, thread_id, slug, page)

        if isinstance(result, ModerationActionTemplateResult):
            if request.is_htmx:
                template_name = self.moderation_modal_template_name
            else:
                template_name = self.moderation_page_template_name

            return result.render(request, template_name)

        if result.deleted_items:
            if not request.is_htmx:
                return redirect(request.get_full_path())

            response = self.get(request, thread_id, slug, page)
            set_moderation_response_headers(request, response)

            return response

        if not request.is_htmx:
            return self.get_post_redirect(request, post)

        post_feed = self.get_post_feed(request, thread, [post])
        post_feed.set_animated_posts(result.updated_items)

        if post.id != thread.first_post_id:
            post_feed.set_counter_start(self.get_post_number(request, post) - 1)

        context_data = self.get_moderation_result_data(request, thread)
        context_data["update_posts"] = post_feed.get_feed_data()

        response = render(request, self.moderation_result_template_name, context_data)
        set_moderation_response_headers(request, response)

        return response

    def execute_post_moderation_action(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> ModerationActionResult:
        actions = self.get_post_moderation_actions(request, post)
        action: PostModerationAction = get_moderation_action(
            actions, request.POST["post_moderation"]
        )

        action_obj = action(request, thread, post)
        action_obj.validate()

        result = action_obj.execute()

        if isinstance(result, ModerationActionTemplateResult):
            result.update_context(
                {
                    "moderation_action": action_obj,
                    "moderation_type": "post_moderation",
                    "breadcrumbs": self.get_thread_breadcrumbs(request, thread),
                    "thread": thread,
                    "post": post,
                    "cancel_url": self.get_post_url(post),
                },
            )

        return result

    def get_thread_moderation_actions(
        self, request: HttpRequest, thread: Thread
    ) -> list[type[ThreadModerationAction]]:
        raise NotImplementedError()

    def get_posts_moderation_actions(
        self, request: HttpRequest, thread: Thread
    ) -> list[type[PostsModerationAction]]:
        raise NotImplementedError()

    def get_post_moderation_actions(
        self, request: HttpRequest, post: Post
    ) -> list[type[PostModerationAction]]:
        raise NotImplementedError()

    def get_selected_posts(self, request: HttpRequest, posts: list[Post]) -> list[Post]:
        posts_id = self.get_selected_posts_ids(request)
        selection: list[Post] = [post for post in posts if post.id in posts_id]

        if not selection:
            raise ValidationError(
                pgettext("posts moderation error", "No valid posts selected."),
            )

        return selection

    def get_selected_posts_ids(self, request: HttpRequest) -> set[int]:
        posts_id: set[int] = set()
        for post_id in request.POST.getlist("posts"):
            try:
                posts_id.add(int(post_id))
            except (TypeError, ValueError):
                pass
        return posts_id

    def get_selected_post(self, request: HttpRequest, thread: Thread) -> Post:
        try:
            post_id = request.POST.get("post")
            return self.get_post(request, thread, post_id)
        except (TypeError, ValueError, Http404):
            raise ValidationError(
                pgettext("posts moderation error", "No valid posts selected."),
            )

    def get_moderation_result_data(self, request: HttpRequest, thread: Thread) -> dict:
        return self.get_moderation_result_data_action(request, thread)

    def get_moderation_result_data_action(
        self, request: HttpRequest, thread: Thread
    ) -> dict:
        breadcrumbs = self.get_category_breadcrumbs(request, thread.category)
        shared_context = {"breadcrumbs": breadcrumbs}

        return {
            "moderation_actions": get_moderation_action_choices(
                self.get_thread_moderation_actions(request, thread)
            ),
            "header": self.get_header_data(request, thread, shared_context),
            "footer": self.get_footer_data(request, thread, shared_context),
            "status_bars": self.get_thread_status_bars_data(request, thread),
            "extra_components": [],
        }

    # Context data

    def get_context_data(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        return self.get_context_data_action(request, thread, page, kwargs)

    def get_context_data_action(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        posts_moderation_actions = self.get_posts_moderation_actions(request, thread)

        if request.user.is_authenticated:
            starter_is_current_user = request.user.id == thread.starter_id
        else:
            starter_is_current_user = False

        breadcrumbs = self.get_category_breadcrumbs(request, thread.category)
        shared_context = {"breadcrumbs": breadcrumbs}

        return {
            "starter_is_current_user": starter_is_current_user,
            "header": self.get_header_data(request, thread, shared_context),
            "footer": self.get_footer_data(request, thread, shared_context),
            "status_bars": self.get_thread_status_bars_data(request, thread),
            "thread": thread,
            "thread_url": self.get_thread_url(thread),
            "watch_thread": self.get_watch_thread_data(request, thread),
            "feed": self.get_post_feed_data(request, thread, page, kwargs),
            "reply": self.get_reply_context_data(request, thread),
            "posts_moderation_actions": get_moderation_action_choices(
                posts_moderation_actions
            ),
            "post_edits_modal_template": self.backend.post_edits_modal_template,
            "post_likes_modal_template": self.backend.post_likes_modal_template,
        }

    def get_header_data(
        self, request: HttpRequest, thread: Thread, context: dict | None
    ) -> dict:
        from random import randint

        dice_roll = randint(1, 6)

        meta_bar = {
            "id": "meta_bar",
            "template_name": self.meta_bar_template_name,
            "items": [
                TextMetaData(
                    id="first",
                    icon=f"tabler/dice-{dice_roll}.svg",
                    text=f"Dice roll: {dice_roll}",
                ),
            ],
        }

        if thread.is_locked:
            meta_bar["items"].append(
                TextMetaData(
                    id="locked",
                    icon="tabler/lock.svg",
                    text="Locked",
                )
            )

        final_context = {
            "id": "header",
            "template_name": self.header_template_name,
            "header": thread.title,
            "meta_bar": meta_bar,
        }

        if context:
            final_context.update(context)

        return final_context

    def get_footer_data(
        self, request: HttpRequest, thread: Thread, context: dict | None
    ) -> dict:
        final_context = {
            "id": "footer",
            "template_name": self.footer_template_name,
        }

        if context:
            final_context.update(context)

        return final_context

    def get_thread_status_bars_data(self, request: HttpRequest, thread: Thread) -> dict:
        items = []

        if thread.is_locked:
            items.append(self.get_locked_thread_status_bar_data())

        if thread.is_unapproved:
            items.append(self.get_unapproved_thread_status_bar_data())

        if (
            request.user_permissions.is_category_moderator(thread.category_id)
            and thread.has_unapproved_posts
        ):
            items.append(self.get_unapproved_posts_status_bar_data(thread))

        return {
            "id": "status_bars",
            "template_name": self.status_bars_template_name,
            "items": items,
        }

    def get_locked_thread_status_bar_data(self) -> dict:
        return {
            "id": "locked_thread",
            "template_name": self.locked_thread_status_bar_template_name,
        }

    def get_unapproved_thread_status_bar_data(self) -> dict:
        return {
            "id": "unapproved_thread",
            "template_name": self.unapproved_thread_status_bar_template_name,
        }

    def get_unapproved_posts_status_bar_data(self, thread: Thread) -> dict:
        return {
            "id": "unapproved_posts",
            "template_name": self.unapproved_posts_status_bar_template_name,
            "unapproved_post_url": self.backend.get_post_unapproved_url(thread),
        }

    def get_watch_thread_data(
        self, request: HttpRequest, thread: Thread
    ) -> dict | None:
        if request.user.is_anonymous:
            return None

        if watched_thread := get_watched_thread(request.user, thread):
            if watched_thread.send_emails:
                notifications = 2
            else:
                notifications = 1
        else:
            notifications = 0

        return {
            "template_name": self.watch_thread_template_name,
            "watch_thread_url": self.get_watch_thread_url(thread),
            "watched_with_email": notifications == 2,
            "watched": notifications == 1,
            "not_watched": notifications == 0,
        }

    def get_post_feed_data(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs,
    ) -> dict:
        page_obj = self.get_posts_page(request, thread, page)
        posts = list(page_obj.object_list)

        if thread.has_updates:
            thread_updates = self.get_thread_updates(request, thread, page_obj, posts)
        else:
            thread_updates = []

        post_feed = self.get_post_feed(request, thread, posts, thread_updates)
        post_feed.set_counter_start(page_obj.start_index() - 1)

        if animate_posts := kwargs.get("updated_posts"):
            post_feed.set_animated_posts(animate_posts)

        if selected_posts := self.get_selected_posts_ids(request):
            post_feed.set_selected_posts(selected_posts)

        unread = get_unread_posts(request, thread, posts)
        post_feed.set_unread_posts(unread)

        allow_edit_thread = self.allow_edit_thread(request, thread)
        post_feed.set_allow_edit_thread(allow_edit_thread)

        if unread:
            self.update_thread_read_time(request, thread, posts[-1].posted_at)

        if request.user.is_authenticated and request.user.unread_notifications:
            self.read_user_notifications(request.user, posts)

        return post_feed.get_context_data({"paginator": page_obj})

    def get_posts_page(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
    ):
        queryset = self.get_posts_queryset(request, thread)
        paginator = self.get_posts_paginator(request, queryset)

        if page and page > paginator.num_pages:
            if not request.is_htmx:
                raise PageOutOfRangeError(
                    self.get_thread_url(thread, paginator.num_pages)
                )

            page = paginator.num_pages

        return paginator.get_page(page)

    def get_thread_updates(
        self,
        request: HttpRequest,
        thread: Thread,
        page: ThreadPostsPaginator,
        posts: list[Post],
    ) -> list[ThreadUpdate]:
        queryset = self.get_thread_updates_queryset(request, thread)
        if page.number > 1:
            queryset = queryset.filter(created_at__gt=posts[0].posted_at)
        if page.next_page_first_item:
            queryset = queryset.filter(
                created_at__lt=page.next_page_first_item.posted_at
            )
        return list(reversed(queryset[: request.settings.thread_updates_per_page]))

    def get_reply_context_data(self, request: HttpRequest, thread: Thread) -> dict:
        try:
            self.check_reply_thread_permission(request, thread)
        except PermissionDenied as exc:
            return {
                "permission": False,
                "template_name": self.reply_error_template_name,
                "error": exc,
            }

        return {
            "permission": True,
            "template_name": self.reply_template_name,
            "formset": self.get_reply_formset(request, thread),
            "url": self.get_reply_url(request, thread),
        }

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ThreadReplyFormset:
        raise NotImplementedError

    # Read tracker

    def update_thread_read_time(
        self,
        request: HttpRequest,
        thread: Thread,
        read_time: datetime,
    ):
        mark_thread_read(request.user, thread, read_time)
        update_watched_thread_read_time(request.user, thread, read_time)

        if self.is_category_read(
            request, thread.category, thread.user_readcategory_time
        ):
            self.mark_category_read(
                request.user,
                thread.category,
                force_update=bool(thread.user_readcategory_time),
            )

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        raise NotImplementedError()

    def mark_category_read(
        self,
        user: "User",
        category: Category,
        *,
        force_update: bool,
    ):
        mark_category_read(user, category, force_update=force_update)

    def read_user_notifications(self, user: "User", posts: list[Post]):
        updated_notifications = user.notification_set.filter(
            post__in=posts, is_read=False
        ).update(is_read=True)

        if updated_notifications:
            new_unread_notifications = max(
                [0, user.unread_notifications - updated_notifications]
            )

            if user.unread_notifications != new_unread_notifications:
                user.unread_notifications = new_unread_notifications
                user.save(update_fields=["unread_notifications"])

    # Permissions

    def allow_edit_thread(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def check_reply_thread_permission(self, request: HttpRequest, thread: Thread):
        raise NotImplementedError()

    # Urls

    def get_watch_thread_url(self, thread: Thread) -> str:
        raise NotImplementedError()

    def get_reply_url(self, request: HttpRequest, thread: Thread) -> str:
        raise NotImplementedError()


class ThreadDetailView(DetailView):
    backend = thread_backend

    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/partial.html"
    header_template_name: str = "misago/thread/header.html"
    footer_template_name: str = "misago/thread/footer.html"

    # Dispatch

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        page: int | None = None,
        **kwargs,
    ) -> HttpResponse:
        if request.is_htmx:
            if poll_response := dispatch_thread_poll_view(request, thread_id):
                return poll_response

        return super().get(request, thread_id, slug, page, **kwargs)

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        if request.GET.get("poll"):
            if poll_response := dispatch_thread_poll_view(request, thread_id):
                return poll_response

        return super().post(request, thread_id, slug, page)

    # Moderation

    def get_thread_moderation_actions(
        self, request: HttpRequest, thread: Thread
    ) -> list[type[ThreadModerationAction]]:
        return get_thread_moderation_actions(request.user_permissions, thread, request)

    def get_posts_moderation_actions(
        self, request: HttpRequest, thread: Thread
    ) -> list[type[PostsModerationAction]]:
        return get_thread_posts_moderation_actions(
            request.user_permissions, thread, request
        )

    def get_post_moderation_actions(
        self, request: HttpRequest, post: Post
    ) -> list[type[PostModerationAction]]:
        return get_thread_post_moderation_actions(
            request.user_permissions, post, request
        )

    def get_moderation_result_data(self, request: HttpRequest, thread: Thread) -> dict:
        return get_thread_detail_view_moderation_result_data_hook(
            self.get_moderation_result_data_action, request, thread
        )

    # Context data

    def get_context_data(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        return get_thread_detail_view_context_data_hook(
            self.get_context_data_action, request, thread, page, kwargs
        )

    def get_context_data_action(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        context = super().get_context_data_action(request, thread, page, kwargs)

        context.update(
            {
                "category": thread.category,
                "thread_moderation_actions": get_moderation_action_choices(
                    self.get_thread_moderation_actions(request, thread)
                ),
            }
        )

        poll = self.get_poll(request, thread)
        if poll:
            context["poll"] = self.get_poll_context_data(request, thread, poll)
            context["allow_start_poll"] = False
        else:
            with check_permissions() as allow_start_poll:
                check_start_thread_poll_permission(
                    request.user_permissions, thread.category, thread
                )

            context["allow_start_poll"] = allow_start_poll

        return context

    def get_thread_breadcrumbs(
        self, request: HttpRequest, thread: Thread
    ) -> list[dict]:
        return get_thread_breadcrumbs(request, thread)

    def get_watch_thread_url(self, thread: Thread) -> str:
        return reverse(
            "misago:thread-watch", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )

    def get_posts_queryset(self, request: HttpRequest, thread: Thread) -> QuerySet:
        return get_thread_detail_view_posts_queryset_hook(
            super().get_posts_queryset, request, thread
        )

    def allow_edit_thread(self, request: HttpRequest, thread: Thread) -> bool:
        if request.user.is_anonymous:
            return False

        with check_permissions() as can_edit_thread:
            check_edit_thread_permission(
                request.user_permissions, thread.category, thread
            )

        return can_edit_thread

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        return is_category_read(request, category, category_read_time)

    def check_reply_thread_permission(self, request: HttpRequest, thread: Thread):
        check_reply_thread_permission(request.user_permissions, thread.category, thread)

    def get_reply_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ThreadReplyFormset:
        return get_thread_reply_formset(request, thread)

    def get_poll(self, request: HttpRequest, thread: Thread) -> Poll | None:
        if thread.has_poll:
            return Poll.objects.filter(thread=thread).first()

        return None

    def get_poll_context_data(
        self,
        request: HttpRequest,
        thread: Thread,
        poll: Poll,
    ) -> dict:
        user_poll_votes = get_user_poll_votes(request.user, poll)
        context = get_poll_context_data(
            request,
            thread,
            poll,
            user_poll_votes,
            fetch_voters=request.GET.get("poll") == "voters",
        )

        template_name = PollTemplate.RESULTS
        if (
            context["allow_vote"]
            and request.GET.get("poll") not in ("results", "voters")
            and (request.GET.get("poll") == "vote" or not user_poll_votes)
        ):
            template_name = PollTemplate.VOTE

        context["template_name"] = template_name
        return context
