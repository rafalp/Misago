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
from ..threads.merge import get_thread_merge_form_fields
from ..threads.models import Thread

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


def get_disallowed_category_choices(
    user_permissions: UserPermissionsProxy,
    categories: CategoriesProxy,
) -> set[int]:
    choices: set[int] = set()

    browse_categories = user_permissions.categories[CategoryPermission.BROWSE]

    for category in categories.categories_list:
        if (
            category["is_vanilla"]
            or category["id"] not in browse_categories
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


def get_valid_thread(request: HttpRequest, thread_id: int) -> Thread:
    from ..threads.views.backend import thread_backend

    try:
        thread = thread_backend.get_thread(request, thread_id)
    except (Http404, PermissionDenied) as exc:
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


class HideForm(forms.Form):
    hidden_reason = forms.CharField(max_length=255, required=False)

    request: HttpRequest

    def __init__(self, *args, request: HttpRequest, **kwargs):
        super().__init__(*args, **kwargs)


class MoveThreadsForm(forms.Form):
    category = forms.TypedChoiceField(coerce=int, choices=[])

    disallowed_categories: set[int]

    request: HttpRequest

    def __init__(self, *args, request: HttpRequest, **kwargs):
        self.request = request

        self.disallowed_categories = set(kwargs.pop("disallowed_categories") or [])
        self.disallowed_categories.update(
            get_disallowed_category_choices(
                request.user_permissions, request.categories
            )
        )

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()

    def clean_category(self):
        data = self.cleaned_data["category"]
        if data in self.disallowed_categories:
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


class MergeForm(forms.Form):
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
        resolutions: dict[str, Model] = {}
        for conflict, objects in self.conflicts.items():
            if len(objects) > 1:
                choices = {obj.id: obj for obj in objects}
                resolutions[conflict] = choices[self.cleaned_data[conflict]]
            else:
                resolutions[conflict] = objects[0]
        return resolutions


class MergeThreadsForm(MergeForm):
    category = forms.TypedChoiceField(coerce=int, choices=[])
    title = forms.CharField(max_length=255)
    is_locked = forms.BooleanField(required=False)
    is_hidden = forms.BooleanField(required=False)

    disallowed_categories: set[int]
    conflicts_fields: list[str]

    request: HttpRequest
    conflicts: dict[str, list[Model]]

    def __init__(
        self,
        *args,
        request: HttpRequest,
        conflicts: dict[str, list[Model]],
        **kwargs,
    ):
        super().__init__(*args, request=request, conflicts=conflicts, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()
        self.disallowed_categories = get_disallowed_category_choices(
            request.user_permissions, request.categories
        )

        if request.user_permissions.is_global_moderator:
            self.fields["pin"] = forms.TypedChoiceField(
                coerce=int,
                choices=ThreadPinned.get_choices(),
                initial=ThreadPinned.NONE,
                required=False,
            )

    def clean_category(self):
        data = self.cleaned_data["category"]
        if data in self.disallowed_categories:
            raise forms.ValidationError(
                message=pgettext(
                    "moderation form category validation", "Select a valid choice."
                ),
                code="invalid",
            )
        return data

    def clean_title(self):
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

    def clean_other_thread(self):
        data = self.cleaned_data["other_thread"]
        thread_id = parse_thread_url(data, self.request, self.valid_urls)

        if thread_id == self.thread.id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form thread validation",
                    "Enter a different thread link.",
                ),
                code="invalid",
            )

        return self.get_other_thread(thread_id)

    def get_other_thread(self, thread_id: int):
        return get_valid_thread(self.request, thread_id)


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

    disallowed_categories: set[int]
    conflicts_fields: list[str]

    request: HttpRequest

    def __init__(
        self,
        *args,
        request: HttpRequest,
        **kwargs,
    ):
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()
        self.disallowed_categories = get_disallowed_category_choices(
            request.user_permissions, request.categories
        )

        if request.user_permissions.is_global_moderator:
            self.fields["pin"] = forms.TypedChoiceField(
                coerce=int,
                choices=ThreadPinned.get_choices(),
                initial=ThreadPinned.NONE,
                required=False,
            )

    def clean_category(self):
        data = self.cleaned_data["category"]
        if data in self.disallowed_categories:
            raise forms.ValidationError(
                message=pgettext(
                    "moderation form category validation", "Select a valid choice."
                ),
                code="invalid",
            )
        return data

    def clean_title(self):
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

    def clean_target_thread(self):
        data = self.cleaned_data["target_thread"]
        thread_id = parse_thread_url(data, self.request, self.valid_urls)

        if thread_id == self.current_thread.id:
            raise forms.ValidationError(
                pgettext(
                    "moderation form thread validation",
                    "Enter a different thread link.",
                ),
                code="invalid",
            )

        return self.get_target_thread(thread_id)

    def get_target_thread(self, thread_id: int):
        return get_valid_thread(self.request, thread_id)
