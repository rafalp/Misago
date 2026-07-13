import urllib

from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Model
from django.http import Http404, HttpRequest
from django.urls import Resolver404, resolve
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from ..posting.validators import validate_thread_title
from ..threads.enums import ThreadPinned
from ..threads.merge import get_post_merge_form_fields, get_thread_merge_form_fields
from ..threads.models import Post, Thread

THREAD_URLS = (
    "misago:thread",
    "misago:thread-post",
    "misago:thread-post-last",
    "misago:thread-post-unapproved",
    "misago:thread-post-unread",
    "misago:thread-post-solution",
    "misago:thread-post-edit",
    "misago:thread-post-edits",
    "misago:thread-post-likes",
    "misago:thread-reply",
    "misago:thread-edit",
)


def get_invalid_category_choices(
    user_permissions: UserPermissionsProxy,
    categories: CategoriesProxy,
) -> set[int]:
    valid_categories = user_permissions.categories[CategoryPermission.BROWSE]

    choices: set[int] = set()
    for category in categories.category_list:
        if (
            category["is_vanilla"]
            or category["id"] not in valid_categories
            or not user_permissions.is_category_moderator(category["id"])
        ):
            choices.add(category["id"])
    return choices


def parse_thread_url(value: str, request: HttpRequest, valid_urls: list[str]) -> int:
    try:
        parsed_url = urllib.parse.urlsplit(value)
    except ValueError:
        parsed_url = None

    if not parsed_url or not parsed_url.netloc or not parsed_url.path.strip("/"):
        raise forms.ValidationError(
            pgettext("moderation form thread url validation", "Enter a valid link."),
            code="invalid",
        )

    if parsed_url.netloc != request.get_host():
        raise forms.ValidationError(
            pgettext(
                "moderation form thread url validation",
                "Enter a link to this site.",
            ),
            code="invalid",
        )

    try:
        resolved_url = resolve(parsed_url.path)
    except Resolver404:
        raise forms.ValidationError(
            pgettext(
                "moderation form thread url validation",
                "Enter a valid thread link.",
            ),
            code="invalid",
        )

    url_name = resolved_url.url_name
    if resolved_url.namespaces:
        namespace = ":".join(resolved_url.namespaces)
        url_name = f"{namespace}:{url_name}"

    if url_name not in valid_urls:
        raise forms.ValidationError(
            pgettext(
                "moderation form thread url validation",
                "Enter a valid thread link.",
            ),
            code="invalid",
        )

    try:
        return int(resolved_url.kwargs.get("thread_id"))
    except (TypeError, ValueError):
        raise forms.ValidationError(
            pgettext(
                "moderation form thread url validation",
                "Enter a valid thread link.",
            ),
            code="invalid",
        )


def parse_thread_post_url(
    value: str,
    request: HttpRequest,
    valid_urls: list[str],
    current_thread_id: int,
) -> int:
    try:
        parsed_url = urllib.parse.urlsplit(value)
    except ValueError:
        parsed_url = None

    if not parsed_url or not parsed_url.netloc or not parsed_url.path.strip("/"):
        raise forms.ValidationError(
            pgettext("moderation form post url validation", "Enter a valid link."),
            code="invalid",
        )

    if parsed_url.netloc != request.get_host():
        raise forms.ValidationError(
            pgettext(
                "moderation form post url validation",
                "Enter a link to this site.",
            ),
            code="invalid",
        )

    try:
        resolved_url = resolve(parsed_url.path)
    except Resolver404:
        raise forms.ValidationError(
            pgettext(
                "moderation form post url validation",
                "Enter a valid post link.",
            ),
            code="invalid",
        )

    url_name = resolved_url.url_name
    if resolved_url.namespaces:
        namespace = ":".join(resolved_url.namespaces)
        url_name = f"{namespace}:{url_name}"

    if url_name not in valid_urls:
        raise forms.ValidationError(
            pgettext(
                "moderation form post url validation",
                "Enter a valid post link.",
            ),
            code="invalid",
        )

    try:
        post_int = int(resolved_url.kwargs.get("post_id"))
    except (TypeError, ValueError):
        raise forms.ValidationError(
            pgettext(
                "moderation form post url validation",
                "Enter a valid post link.",
            ),
            code="invalid",
        )

    if "thread_id" in resolved_url.kwargs:
        try:
            thread_id = int(resolved_url.kwargs.get("thread_id"))
        except (TypeError, ValueError):
            raise forms.ValidationError(
                pgettext(
                    "moderation form post url validation",
                    "Enter a valid thread post link.",
                ),
                code="invalid",
            )

        if thread_id != current_thread_id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form post url validation",
                    "Enter a link to a post in the current thread.",
                ),
                code="invalid",
            )

    return post_int


def get_valid_thread(request: HttpRequest, thread_id: int) -> Thread:
    from ..threads.views.backend import thread_backend

    try:
        thread = thread_backend.get_thread(request, thread_id)
    except (Http404, PermissionDenied):
        raise forms.ValidationError(
            pgettext(
                "moderation form thread validation",
                "Thread doesn't exist or you don't have permission to see it.",
            ),
            code="invalid",
        )

    is_moderator = thread_backend.has_moderator_permission(
        request.user_permissions, thread
    )
    if not is_moderator:
        raise forms.ValidationError(
            pgettext(
                "moderation form thread validation",
                "You can't moderate this thread.",
            ),
            code="permission_denied",
        )

    return thread


def get_conflicts_resolutions(
    conflicts: dict[str, list[Model]], cleaned_data: dict
) -> dict[str, int]:
    resolutions: dict[str, Model] = {}
    for conflict, objects in conflicts.items():
        if len(objects) > 1:
            choices = {obj.id: obj for obj in objects}
            resolutions[conflict] = choices[cleaned_data[conflict]]
        else:
            resolutions[conflict] = objects[0]
    return resolutions


class HideForm(forms.Form):
    hidden_reason = forms.CharField(max_length=255, required=False)

    request: HttpRequest

    def __init__(self, *args, request: HttpRequest, **kwargs):
        super().__init__(*args, **kwargs)


class MoveThreadsForm(forms.Form):
    category = forms.TypedChoiceField(coerce=int, choices=[])

    invalid_category_choices: set[int]

    request: HttpRequest

    def __init__(self, *args, request: HttpRequest, **kwargs):
        self.request = request

        self.invalid_category_choices = set(kwargs.pop("invalid_category_choices", []))
        self.invalid_category_choices.update(
            get_invalid_category_choices(request.user_permissions, request.categories)
        )

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()

    def clean_category(self) -> int:
        data = self.cleaned_data["category"]
        if data in self.invalid_category_choices:
            raise forms.ValidationError(
                message=pgettext(
                    "moderation form category validation", "Select a valid choice."
                ),
                code="invalid",
            )
        return data

    def clean(self):
        data = super().clean()
        if data.get("category"):
            data["category"] = Category.objects.get(id=data["category"])
        return data


class MergeThreadsForm(forms.Form):
    category = forms.TypedChoiceField(coerce=int, choices=[])
    title = forms.CharField(max_length=255)
    is_locked = forms.BooleanField(required=False)
    is_hidden = forms.BooleanField(required=False)

    invalid_category_choices: set[int]

    request: HttpRequest
    conflicts: dict[str, list[Model]]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        conflicts: dict[str, list[Model]],
        **kwargs,
    ):
        self.request = request
        self.conflicts = conflicts

        super().__init__(*args, **kwargs)

        self.fields.update(get_thread_merge_form_fields(conflicts, request))
        self.fields["category"].choices = request.categories.get_choices()

        self.invalid_category_choices = get_invalid_category_choices(
            request.user_permissions, request.categories
        )

        if request.user_permissions.is_global_moderator:
            self.fields["pin"] = forms.TypedChoiceField(
                coerce=int,
                choices=ThreadPinned.get_choices(),
                initial=ThreadPinned.NONE,
                required=False,
            )

    @property
    def conflicts_fields(self):
        return [
            self[field_name]
            for field_name, choices in self.conflicts.items()
            if len(choices) > 1
        ]

    def clean_category(self) -> int:
        data = self.cleaned_data["category"]
        if data in self.invalid_category_choices:
            raise forms.ValidationError(
                message=pgettext(
                    "moderation form category validation", "Select a valid choice."
                ),
                code="invalid",
            )
        return data

    def clean_title(self) -> str:
        data = self.cleaned_data["title"]
        validate_thread_title(
            data,
            self.request.settings.thread_title_length_min,
            self.request.settings.thread_title_length_max,
            self.request,
        )
        return data

    def clean(self):
        data = super().clean()
        if data.get("category"):
            data["category"] = Category.objects.get(id=data["category"])
        return data

    def get_conflicts_resolutions(self) -> dict[str, int]:
        return get_conflicts_resolutions(self.conflicts, self.cleaned_data)


class MergeThreadForm(forms.Form):
    other_thread = forms.CharField(max_length=500)
    direction = forms.ChoiceField(
        choices=(
            (
                "other",
                pgettext("moderation form thread merge direction", "Keep other thread"),
            ),
            (
                "current",
                pgettext(
                    "moderation form thread merge direction", "Keep current thread"
                ),
            ),
        ),
        initial="other",
        widget=forms.RadioSelect,
    )

    valid_urls = THREAD_URLS

    request: HttpRequest
    thread: Thread

    def __init__(self, *args, request: HttpRequest, thread: Thread, **kwargs):
        self.request = request
        self.thread = thread

        super().__init__(*args, **kwargs)

    def clean_other_thread(self) -> Thread:
        data = self.cleaned_data["other_thread"]
        thread_id = parse_thread_url(data, self.request, self.valid_urls)

        if thread_id == self.thread.id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form thread validation",
                    "Can't merge a thread with itself.",
                ),
                code="invalid",
            )

        return self.get_other_thread(thread_id)

    def get_other_thread(self, thread_id: int) -> Thread:
        return get_valid_thread(self.request, thread_id)


class MergeThreadConflictsForm(forms.Form):
    conflicts: dict[str, list[Model]]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        conflicts: dict[str, list[Model]],
        **kwargs,
    ):
        self.request = request
        self.conflicts = conflicts

        super().__init__(*args, **kwargs)

        self.fields.update(get_thread_merge_form_fields(conflicts, request))

    @property
    def conflicts_fields(self):
        return [
            self[field_name]
            for field_name, choices in self.conflicts.items()
            if len(choices) > 1
        ]

    def get_conflicts_resolutions(self):
        return get_conflicts_resolutions(self.conflicts, self.cleaned_data)


class SplitPostsForm(forms.Form):
    category = forms.TypedChoiceField(coerce=int, choices=[])
    title = forms.CharField(max_length=255)
    is_locked = forms.BooleanField(required=False)
    is_hidden = forms.BooleanField(required=False)
    redirect_to = forms.ChoiceField(
        choices=[
            ("new", pgettext_lazy("split posts form redirect to", "New thread")),
            (
                "current",
                pgettext_lazy("split posts form redirect to", "Current thread"),
            ),
        ],
        initial="new",
        widget=forms.RadioSelect,
    )

    request: HttpRequest
    invalid_category_choices: set[int]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        **kwargs,
    ):
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()
        self.invalid_category_choices = get_invalid_category_choices(
            request.user_permissions, request.categories
        )

        if request.user_permissions.is_global_moderator:
            self.fields["pin"] = forms.TypedChoiceField(
                coerce=int,
                choices=ThreadPinned.get_choices(),
                initial=ThreadPinned.NONE,
                required=False,
            )

    def clean_category(self) -> int:
        data = self.cleaned_data["category"]
        if data in self.invalid_category_choices:
            raise forms.ValidationError(
                message=pgettext(
                    "moderation form category validation", "Select a valid choice."
                ),
                code="invalid",
            )
        return data

    def clean_title(self) -> str:
        data = self.cleaned_data["title"]
        validate_thread_title(
            data,
            self.request.settings.thread_title_length_min,
            self.request.settings.thread_title_length_max,
            self.request,
        )
        return data

    def clean(self):
        data = super().clean()
        if data.get("category"):
            data["category"] = Category.objects.get(id=data["category"])
        return data


class MovePostsForm(forms.Form):
    target_thread = forms.CharField(max_length=500)
    redirect_to = forms.ChoiceField(
        choices=[
            ("target", pgettext_lazy("move posts form redirect to", "Target thread")),
            (
                "current",
                pgettext_lazy("move posts form redirect to", "Current thread"),
            ),
        ],
        initial="target",
        widget=forms.RadioSelect,
    )

    valid_urls = THREAD_URLS

    request: HttpRequest
    current_thread: Thread | None

    def __init__(
        self,
        *args,
        request: HttpRequest,
        current_thread: Thread | None = None,
        **kwargs,
    ):
        self.request = request
        self.current_thread = current_thread

        super().__init__(*args, **kwargs)

    def clean_target_thread(self) -> Thread:
        data = self.cleaned_data["target_thread"]
        thread_id = parse_thread_url(data, self.request, self.valid_urls)

        if thread_id == self.current_thread.id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form thread validation",
                    "Can't move posts to the same thread.",
                ),
                code="invalid",
            )

        return self.get_target_thread(thread_id)

    def get_target_thread(self, thread_id: int) -> Thread:
        return get_valid_thread(self.request, thread_id)


class MergePostsForm(forms.Form):
    edit_reason = forms.CharField(max_length=255, required=False)

    request: HttpRequest
    conflicts: dict[str, list[Model]]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        conflicts: dict[str, list[Model]],
        **kwargs,
    ):
        self.request = request
        self.conflicts = conflicts

        super().__init__(*args, **kwargs)

        self.fields.update(get_post_merge_form_fields(conflicts, request))

    @property
    def conflicts_fields(self):
        return [
            self[field_name]
            for field_name, choices in self.conflicts.items()
            if len(choices) > 1
        ]

    def get_conflicts_resolutions(self):
        return get_conflicts_resolutions(self.conflicts, self.cleaned_data)


class MergeThreadPostForm(forms.Form):
    other_post = forms.CharField(max_length=500)
    direction = forms.ChoiceField(
        choices=(
            (
                "other",
                pgettext("moderation form post merge direction", "Keep other post"),
            ),
            (
                "current",
                pgettext("moderation form post merge direction", "Keep current post"),
            ),
        ),
        initial="other",
        widget=forms.RadioSelect,
    )
    edit_reason = forms.CharField(max_length=255, required=False)

    valid_urls = (
        "misago:post",
        "misago:thread-post",
        "misago:thread-post-edit",
        "misago:thread-post-edits",
        "misago:thread-post-likes",
    )

    request: HttpRequest
    thread: Thread
    post: Post

    def __init__(self, *args, request: HttpRequest, post: Post, **kwargs):
        self.request = request
        self.thread = post.thread
        self.post = post

        super().__init__(*args, **kwargs)

        if post.id == post.thread.first_post_id:
            del self.fields["direction"]

    def clean_other_post(self) -> Post:
        data = self.cleaned_data["other_post"]
        post_id = parse_thread_post_url(
            data, self.request, self.valid_urls, self.post.thread_id
        )

        if post_id == self.post.id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form post validation",
                    "Can't merge a post with itself.",
                ),
                code="invalid",
            )

        try:
            post = self.get_other_post(post_id)
        except (Http404, PermissionDenied):
            raise forms.ValidationError(
                pgettext(
                    "moderation form post validation",
                    "Post doesn't exist in this thread or you don't have permission to see it.",
                ),
                code="invalid",
            )

        if (self.post.poster_id and self.post.poster_id != post.poster_id) or (
            not self.post.poster_id and post.poster_name != self.post.poster_name
        ):
            raise forms.ValidationError(
                pgettext(
                    "moderation form post validation",
                    "Merged posts must belong to the same user.",
                ),
                code="invalid",
            )

        return post

    def clean(self):
        data = super().clean()

        data.setdefault("direction", "current")

        other_post = data.get("other_post")
        if (
            other_post
            and other_post.id == self.thread.first_post_id
            and data["direction"] == "current"
        ):
            self.add_error(
                "direction",
                forms.ValidationError(
                    pgettext(
                        "moderation form post validation",
                        "Thread's first post can't be merged into another post.",
                    ),
                    code="invalid",
                ),
            )

        return data

    def get_other_post(self, post_id: int) -> Post:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_post(
            self.request, self.post.thread, post_id, for_content=True
        )


class MergePrivateThreadPostForm(MergeThreadPostForm):
    valid_urls = (
        "misago:post",
        "misago:private-thread-post",
        "misago:private-thread-post-edit",
        "misago:private-thread-post-edits",
        "misago:private-thread-post-likes",
    )

    def get_other_post(self, post_id: int):
        from ..privatethreads.views.backend import private_thread_backend

        return private_thread_backend.get_post(
            self.request, self.post.thread, post_id, for_content=True
        )


class MergePostConflictsForm(forms.Form):
    conflicts: dict[str, list[Model]]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        conflicts: dict[str, list[Model]],
        **kwargs,
    ):
        self.request = request
        self.conflicts = conflicts

        super().__init__(*args, **kwargs)

        self.fields.update(get_post_merge_form_fields(conflicts, request))

    @property
    def conflicts_fields(self):
        return [
            self[field_name]
            for field_name, choices in self.conflicts.items()
            if len(choices) > 1
        ]

    def get_conflicts_resolutions(self):
        return get_conflicts_resolutions(self.conflicts, self.cleaned_data)
