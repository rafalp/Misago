from django import forms
from django.db.models import Model
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from ..posting.validators import validate_thread_title
from ..threads.enums import ThreadPinned
from ..threads.merge import (
    get_thread_merge_form_fields,
)


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
                message=pgettext("moderation move thread form", "Invalid choice."),
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

        self.fields.update(get_thread_merge_form_fields(self, conflicts, request))

    @property
    def conflicts_fields(self):
        return [self[field_name] for field_name in self.conflicts]

    def get_conflicts_resolutions(self):
        resolutions: dict[str, Model] = {}
        for conflict, objects in self.conflicts.items():
            choices = {obj.id: obj for obj in objects}
            resolutions[conflict] = choices[self.cleaned_data[conflict]]
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
