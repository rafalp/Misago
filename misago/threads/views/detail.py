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
from django.template.defaultfilters import date as format_date
from django.urls import reverse
from django.utils.translation import npgettext, pgettext

from ...categories.models import Category
from ...metadata import NumberMetadata, UserDatetimeMetadata
from ...metatags.metatag import MetaTag
from ...moderation.actions import (
    ModerationActionTemplateResult,
    ModerationResult,
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
    get_moderation_result_response,
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
from ...readtracker.threads import is_category_read
from ...readtracker.tracker import (
    get_unread_posts,
    mark_category_read,
    mark_thread_read,
)
from ...threadevents.models import ThreadEvent
from ..breadcrumbs import get_thread_breadcrumbs
from ..models import Post, Thread
from ..paginator import ThreadPostsPaginator
from ..statusmessages import (
    hidden_thread_status_message,
    locked_thread_status_message,
    require_reply_approval_thread_status_message,
    unapproved_posts_thread_status_message,
    unapproved_thread_status_message,
)
from ..threadtypes import thread_type
from .base import BaseThreadView

if TYPE_CHECKING:
    from ...users.models import User


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class DetailView(BaseThreadView):
    template_name: str
    template_partial_name: str
    header_template_name: str
    header_meta_template_name: str = "misago/header_meta.html"
    footer_template_name: str

    status_messages_template_name: str = "misago/thread/status_messages.html"
    reply_error_template_name: str = "misago/thread/reply_error.html"
    reply_template_name: str = "misago/quick_reply/form.html"
    watch_thread_template_name: str = "misago/thread/watch_thread.html"

    moderation_modal_template_name: str = "misago/moderation_thread/modal.html"
    moderation_page_template_name: str = "misago/moderation_thread/page.html"
    moderation_result_template_name: str = "misago/moderation_thread/result.html"

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
        return super().get_thread(
            *args,
            annotate_read_time=True,
            select_related=("category", "starter"),
            **kwargs,
        )

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

            messages.error(request, e.messages[0])
            return self.get(request, thread_id, slug, page)

        if isinstance(result, ModerationActionTemplateResult):
            if request.is_htmx:
                template_name = self.moderation_modal_template_name
            else:
                template_name = self.moderation_page_template_name

            return result.render(request, template_name)

        if response := get_moderation_result_response(request, result):
            return response

        if thread in result.deleted_items:
            parent_url = self.get_thread_parent_url(request, thread)
            if not request.is_htmx:
                return redirect(parent_url)

            response = HttpResponse(status=201)
            response.headers["hx-redirect"] = parent_url
            return response

        if not request.is_htmx:
            return redirect(request.get_full_path())

        context_data = self.get_moderation_result_data(request, thread, result)

        if thread_events := result.thread_updates:
            post_feed = self.get_post_feed(request, thread, [], thread_events)
            post_feed.set_animated_thread_events(
                [update.id for update in thread_events]
            )
            context_data[("thread_updates")] = post_feed.get_context_data()["items"]

        response = render(request, self.moderation_result_template_name, context_data)
        set_moderation_response_headers(
            request, response, "misago:afterThreadModeration"
        )

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

            messages.error(request, e.messages[0])
            return self.get(request, thread_id, slug, page)

        return self.get_posts_moderation_response(
            request, thread, result, "misago:afterPostsModeration"
        )

    def execute_posts_moderation_action(
        self, request: HttpRequest, thread: Thread, page: int | None
    ) -> ModerationResult:
        actions = self.get_posts_moderation_actions(request, thread)
        action: PostsModerationAction = get_moderation_action(
            actions, request.POST["posts_moderation"]
        )

        selected_posts = self.get_selected_posts(request, thread)

        for post in selected_posts:
            post.category = thread.category
            post.thread = thread

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

            messages.error(request, e.messages[0])
            return self.get(request, thread_id, slug, page)

        return self.get_posts_moderation_response(
            request, thread, result, "misago:afterPostModeration"
        )

    def execute_post_moderation_action(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> ModerationResult:
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
                    "selection": post,
                    "cancel_url": self.get_post_url(post),
                },
            )

        return result

    def get_posts_moderation_response(
        self,
        request: HttpRequest,
        thread: Thread,
        result: ModerationResult,
        htmx_event_name: str,
    ) -> HttpResponse:
        if isinstance(result, ModerationActionTemplateResult):
            if request.is_htmx:
                template_name = self.moderation_modal_template_name
            else:
                template_name = self.moderation_page_template_name

            return result.render(request, template_name)

        if response := get_moderation_result_response(request, result):
            return response

        if not request.is_htmx:
            if result.updated_items:
                post = result.updated_items[0]
                return self.get_post_redirect(request, post)

            return redirect(request.get_full_path())

        context_data = self.get_moderation_result_data(request, thread, result)

        if result.updated_items or result.thread_updates:
            updated_post_ids = [post.id for post in result.updated_items]
            post_feed = self.get_post_feed(
                request, thread, result.updated_items, result.thread_updates
            )

            if result.updated_items:
                post_feed.set_counter_start(
                    self.get_post_number(request, result.updated_items[0]) - 1
                )
                post_feed.set_animated_posts(updated_post_ids)

            if request.POST.get("posts_moderation"):
                post_feed.set_selected_posts(updated_post_ids)

            post_feed_data = post_feed.get_feed_data()
            context_data["update_posts"] = [
                item for item in post_feed_data if item["type"] == "post"
            ]
            context_data["thread_updates"] = [
                item for item in post_feed_data if item["type"] == "event"
            ]

        response = render(request, self.moderation_result_template_name, context_data)
        set_moderation_response_headers(
            request,
            response,
            htmx_event_name,
            self.get_moderation_event_context(result),
        )

        return response

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

    def get_selected_posts(self, request: HttpRequest, thread: Thread) -> list[Post]:
        posts_id = self.get_selected_posts_ids(request)

        limit = (
            request.settings.posts_per_page + request.settings.posts_per_page_orphans
        )

        if len(posts_id) > limit:
            raise ValidationError(
                message=npgettext(
                    "posts moderation error",
                    "You can't select more than %(limit)s post to moderate.",
                    "You can't select more than %(limit)s posts to moderate.",
                    limit,
                ),
                params={"limit": limit},
            )

        selection: list[Post] = self.get_posts_queryset(request, thread).filter(
            id__in=posts_id
        )

        if not selection:
            raise ValidationError(
                pgettext("posts moderation error", "No valid posts selected."),
            )

        for post in selection:
            post.category = thread.category
            post.thread = thread

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

    def get_moderation_result_data(
        self, request: HttpRequest, thread: Thread, result: ModerationResult
    ) -> dict:
        breadcrumbs = self.get_category_breadcrumbs(request, thread.category)
        shared_context = {"breadcrumbs": breadcrumbs}

        return {
            "moderation_actions": get_moderation_action_choices(
                self.get_thread_moderation_actions(request, thread)
            ),
            "header": self.get_header_data(request, thread, shared_context),
            "footer": self.get_footer_data(request, thread, shared_context),
            "status_messages": self.get_thread_status_messages(request, thread),
            "extra_components": [],
        }

    def get_moderation_event_context(self, result: ModerationResult) -> dict:
        event_context = {}

        if result.updated_items:
            event_context["updated"] = [item.id for item in result.updated_items]
        if result.deleted_items:
            event_context["deleted"] = [item.id for item in result.deleted_items]

        return event_context

    # Context data

    def get_context_data(
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

        return {
            "starter_is_current_user": starter_is_current_user,
            "metatags": self.get_metatags(thread),
            "canonical_link": self.get_canonical_link(thread),
            "breadcrumbs": self.get_category_breadcrumbs(request, thread.category),
            "header": self.get_header_data(request, thread),
            "footer": self.get_footer_data(request, thread),
            "status_messages": self.get_thread_status_messages(request, thread),
            "thread": thread,
            "thread_url": self.get_thread_url(thread),
            "watch_thread": self.get_watch_thread_data(request, thread),
            "feed": self.get_post_feed_data(request, thread, page, kwargs),
            "reply": self.get_reply_context_data(request, thread),
            "posts_moderation_actions": get_moderation_action_choices(
                posts_moderation_actions
            ),
            "post_edits_modal_template": self.thread_type.post_edits_modal_template,
            "post_likes_modal_template": self.thread_type.post_likes_modal_template,
        }

    def get_metatags(self, thread: Thread) -> dict:
        request = self.request

        description: list[str] = [
            pgettext(
                "thread description metatag", "Thread by %(user)s in %(category)s."
            )
            % {
                "user": thread.starter_name,
                "category": thread.category.name,
                "date": format_date(thread.started_at),
            },
        ]

        if thread.replies:
            description.append(
                npgettext(
                    "thread description metatag",
                    "%(replies)s reply.",
                    "%(replies)s replies.",
                    thread.replies,
                )
                % {"replies": thread.replies},
            )
            description.append(
                pgettext(
                    "thread description metatag",
                    "Last replied by %(user)s on %(date)s.",
                )
                % {
                    "user": thread.last_poster_name,
                    "date": format_date(thread.last_posted_at),
                },
            )

        metatags = {
            "url": MetaTag(
                name="twitter:url",
                property="og:url",
                content=request.build_absolute_uri(request.path),
            ),
            "title": MetaTag(
                name="twitter:title",
                property="og:title",
                content=thread.title,
            ),
            "description": MetaTag(
                name="twitter:description",
                property="og:description",
                content=" ".join(description),
            ),
        }

        if (
            request.settings.og_image_avatar_on_thread
            and thread.starter
            and thread.starter.avatars
        ):
            starter_avatar = thread.starter.avatars[0]
            metatags.update(
                {
                    "image": MetaTag(
                        name="twitter:image",
                        property="og:image",
                        content=request.build_absolute_uri(starter_avatar["url"]),
                    ),
                    "image:width": MetaTag(
                        name="twitter:image",
                        property="og:image",
                        content=starter_avatar["size"],
                    ),
                    "image:height": MetaTag(
                        name="twitter:image",
                        property="og:image",
                        content=starter_avatar["size"],
                    ),
                },
            )

        return metatags

    def get_canonical_link(self, thread: Thread) -> str:
        return self.request.path

    def get_header_data(self, request: HttpRequest, thread: Thread) -> dict:
        return {
            "id": "header",
            "template_name": self.header_template_name,
            "header": thread.title,
            "meta": self.get_header_meta(request, thread),
        }

    def get_header_meta(self, request: HttpRequest, thread: Thread) -> dict:
        items: list[dict] = [
            UserDatetimeMetadata(
                id="thread-started",
                user=thread.starter or thread.starter_name,
                datetime=thread.started_at,
                url=self.get_thread_url(thread) + f"#post-{thread.first_post_id}",
            ),
        ]

        if thread.replies:
            items.append(
                NumberMetadata(
                    id="thread-replies",
                    text=npgettext(
                        "thread header meta replies",
                        "%(number)s reply",
                        "%(number)s replies",
                        thread.replies,
                    ),
                    number=thread.replies,
                    icon="tabler/messages.svg",
                )
            )

        return {
            "id": "meta_bar",
            "template_name": self.header_meta_template_name,
            "items": items,
        }

    def get_footer_data(self, request: HttpRequest, thread: Thread) -> dict:
        return {
            "id": "footer",
            "template_name": self.footer_template_name,
        }

    def get_thread_status_messages(self, request: HttpRequest, thread: Thread) -> dict:
        messages = []

        if status_message := locked_thread_status_message(thread):
            messages.append(status_message)

        if status_message := hidden_thread_status_message(thread):
            messages.append(status_message)

        if status_message := unapproved_thread_status_message(thread):
            messages.append(status_message)

        if status_message := require_reply_approval_thread_status_message(thread):
            messages.append(status_message)

        if (
            request.user_permissions.is_category_moderator(thread.category_id)
            and thread.has_unapproved_posts
        ):
            messages.append(
                unapproved_posts_thread_status_message(thread, self.thread_type)
            )

        return {
            "id": "status_messages",
            "template_name": self.status_messages_template_name,
            "messages": messages,
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

        if thread.has_events:
            thread_events = self.get_thread_updates(request, thread, page_obj, posts)
        else:
            thread_events = []

        post_feed = self.get_post_feed(request, thread, posts, thread_events)
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
    ) -> list[ThreadEvent]:
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
    thread_type = thread_type

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

    # Context data

    def get_context_data(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None,
        kwargs: dict,
    ) -> dict:
        context = super().get_context_data(request, thread, page, kwargs)

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
