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


def get_disallowed_category_choices(
    user_permissions: UserPermissionsProxy,
    categories: CategoriesProxy,
) -> set[int]:
    choices: set[int] = set()

    categories_start = user_permissions.categories[CategoryPermission.START]

    for category in categories.categories_list:
        if category["is_vanilla"] or category["id"] not in categories_start:
            choices.add(category["id"])

    return choices


class HideForm(forms.Form):
    request: HttpRequest

    hidden_reason = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, request: HttpRequest, **kwargs):
        super().__init__(*args, **kwargs)


class MoveThreadForm(forms.Form):
    request: HttpRequest

    category = forms.TypedChoiceField(coerce=int, choices=[])
    disallowed_categories: set[int]

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
    request: HttpRequest
    conflicts: dict[str, list[Model]]

    category = forms.TypedChoiceField(coerce=int, choices=[])
    title = forms.CharField(max_length=255)
    is_locked = forms.BooleanField(required=False)
    is_hidden = forms.BooleanField(required=False)

    disallowed_categories: set[int]
    conflicts_fields: list[str]

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
    request: HttpRequest
    thread: Thread

    other_thread = forms.CharField(max_length=500)
    direction = forms.ChoiceField(
        choices=(
            (
                "other",
                pgettext(
                    "moderation form thread merge direction", "Keep the other thread"
                ),
            ),
            (
                "this",
                pgettext("moderation form thread merge direction", "Keep this thread"),
            ),
        ),
        initial="other",
        widget=forms.RadioSelect,
    )

    thread_urls = ("misago:thread",)

    def __init__(self, *args, request: HttpRequest, thread: Thread, **kwargs):
        self.request = request
        self.thread = thread

        super().__init__(*args, **kwargs)

    def clean_other_thread(self):
        data = self.cleaned_data["other_thread"]

        try:
            parsed_url = urllib.parse.urlsplit(data)
        except ValueError:
            parsed_url = None

        if not parsed_url or not parsed_url.netloc or not parsed_url.path:
            raise forms.ValidationError("Parser error")

        try:
            resolved_url = resolve(parsed_url.path)
        except Resolver404:
            raise forms.ValidationError("Resolver error")

        url_name = resolved_url.url_name
        if resolved_url.namespaces:
            namespace = ":".join(resolved_url.namespaces)
            url_name = f"{namespace}:{url_name}"

        if url_name not in self.thread_urls:
            raise forms.ValidationError("URL error")

        try:
            thread_id = int(resolved_url.kwargs.get("thread_id"))
        except (TypeError, ValueError):
            thread_id = None

        if not thread_id:
            raise forms.ValidationError("Thread ID error")
        if thread_id == self.thread.id:
            raise forms.ValidationError("Can't merge thread with itself")

        return self.get_other_thread(thread_id)

    def get_other_thread(self, thread_id: int):
        from ..threads.views.backend import thread_backend

        try:
            thread = thread_backend.get_thread(self.request, thread_id)
        except (Http404, PermissionDenied):
            raise forms.ValidationError("Thread doesn't exist or can't see it")

        is_moderator = thread_backend.has_moderator_permission(
            self.request.user_permissions, thread
        )
        if not is_moderator:
            raise forms.ValidationError("Must be moderator")

        return thread


class SplitPostsForm(forms.Form):
    request: HttpRequest

    category = forms.TypedChoiceField(
        label=pgettext_lazy("moderation split posts form", "Category"),
        coerce=int,
        choices=[],
    )
    title = forms.CharField(
        label=pgettext_lazy("moderation split posts form", "Title"),
        max_length=255,
    )

    def __init__(
        self,
        *args,
        request: HttpRequest,
        **kwargs,
    ):
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["category"].choices = request.categories.get_choices()
        self.disabled_choices = get_disallowed_category_choices(
            request.user_permissions, request.categories
        )
