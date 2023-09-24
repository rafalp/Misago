import re

from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import pgettext_lazy
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from ...admin.forms import YesNoSwitch
from ...core.validators import validate_sluggable
from ...threads.threadtypes import trees_map
from .. import THREADS_ROOT_NAME
from ..models import Category, CategoryRole


class AdminCategoryFieldMixin:
    def __init__(self, *args, **kwargs):
        self.base_level = kwargs.pop("base_level", 1)
        kwargs["level_indicator"] = kwargs.get("level_indicator", "- - ")

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        queryset = Category.objects.filter(tree_id=threads_tree_id)
        if not kwargs.pop("include_root", False):
            queryset = queryset.exclude(special_role="root_category")

        kwargs.setdefault("queryset", queryset)

        super().__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr) - self.base_level
        if level > 0:
            return mark_safe(conditional_escape(self.level_indicator) * level)
        return ""


class AdminCategoryChoiceField(AdminCategoryFieldMixin, TreeNodeChoiceField):
    pass


class AdminCategoryMultipleChoiceField(
    AdminCategoryFieldMixin, TreeNodeMultipleChoiceField
):
    pass


class CategoryFormBase(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin category form", "Name"),
        validators=[validate_sluggable()],
    )
    short_name = forms.CharField(
        label=pgettext_lazy("admin category form", "Short name"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Optional, alternative or abbreviated name (eg. abbreviation) used on threads list.",
        ),
        validators=[validate_sluggable()],
    )
    color = forms.CharField(
        label=pgettext_lazy("admin category form", "Color"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Optional but recommended, should be in hex format, eg. #F5A9B8.",
        ),
        validators=[
            RegexValidator(
                r"^#[0-9a-f][0-9a-f][0-9a-f]([0-9a-f][0-9a-f][0-9a-f]?)$",
                flags=re.MULTILINE | re.IGNORECASE,
                message=pgettext_lazy(
                    "admin category form", "Entered value is not a valid color."
                ),
            ),
        ],
    )
    description = forms.CharField(
        label=pgettext_lazy("admin category form", "Description"),
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=pgettext_lazy(
            "admin category form",
            "Optional description explaining category intented purpose.",
        ),
    )
    css_class = forms.CharField(
        label=pgettext_lazy("admin category form", "CSS class"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Optional CSS class used to customize this category's appearance from themes.",
        ),
    )
    is_closed = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Closed category"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Only members with valid permissions can post in closed categories.",
        ),
    )
    require_threads_approval = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Threads"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "All threads started in this category will require moderator approval.",
        ),
    )
    require_replies_approval = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Replies"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "All replies posted in this category will require moderator approval.",
        ),
    )
    require_edits_approval = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Edits"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Will make all edited replies return to unapproved state for moderator to review.",
        ),
    )
    prune_started_after = forms.IntegerField(
        label=pgettext_lazy("admin category form", "Thread age"),
        min_value=0,
        help_text=pgettext_lazy(
            "admin category form",
            "Prune thread if number of days since its creation is greater than specified. Enter 0 to disable this pruning criteria.",
        ),
    )
    prune_replied_after = forms.IntegerField(
        label=pgettext_lazy("admin category form", "Last reply"),
        min_value=0,
        help_text=pgettext_lazy(
            "admin category form",
            "Prune thread if number of days since last reply is greater than specified. Enter 0 to disable this pruning criteria.",
        ),
    )

    class Meta:
        model = Category
        fields = [
            "name",
            "short_name",
            "color",
            "description",
            "css_class",
            "is_closed",
            "require_threads_approval",
            "require_replies_approval",
            "require_edits_approval",
            "prune_started_after",
            "prune_replied_after",
            "archive_pruned_in",
        ]

    def clean_copy_permissions(self):
        data = self.cleaned_data["copy_permissions"]
        if data and data.pk == self.instance.pk:
            message = pgettext_lazy(
                "admin category form",
                "Permissions cannot be copied from category into itself.",
            )
            raise forms.ValidationError(message)
        return data

    def clean_archive_pruned_in(self):
        data = self.cleaned_data["archive_pruned_in"]
        if data and data.pk == self.instance.pk:
            message = pgettext_lazy(
                "admin category form", "Category cannot act as archive for itself."
            )
            raise forms.ValidationError(message)
        return data

    def clean(self):
        data = super().clean()
        self.instance.set_name(data.get("name"))
        return data


def CategoryFormFactory(instance):
    parent_queryset = Category.objects.all_categories(True).order_by("lft")
    if instance.pk:
        not_siblings = models.Q(lft__lt=instance.lft)
        not_siblings = not_siblings | models.Q(rght__gt=instance.rght)
        parent_queryset = parent_queryset.filter(not_siblings)

    return type(
        "CategoryFormFinal",
        (CategoryFormBase,),
        {
            "new_parent": AdminCategoryChoiceField(
                label=pgettext_lazy("admin category form", "Parent category"),
                queryset=parent_queryset,
                initial=instance.parent,
                empty_label=None,
            ),
            "copy_permissions": AdminCategoryChoiceField(
                label=pgettext_lazy("admin category form", "Copy permissions"),
                help_text=pgettext_lazy(
                    "admin category form",
                    "You can replace this category permissions with permissions copied from category selected here.",
                ),
                queryset=Category.objects.all_categories(),
                empty_label=pgettext_lazy(
                    "admin category form", "Don't copy permissions"
                ),
                required=False,
            ),
            "archive_pruned_in": AdminCategoryChoiceField(
                label=pgettext_lazy("admin category form", "Archive"),
                help_text=pgettext_lazy(
                    "admin category form",
                    "Instead of being deleted, pruned threads can be moved to designated category.",
                ),
                queryset=Category.objects.all_categories(),
                empty_label=pgettext_lazy(
                    "admin category form", "Don't archive pruned threads"
                ),
                required=False,
            ),
        },
    )


class DeleteCategoryFormBase(forms.ModelForm):
    class Meta:
        model = Category
        fields = []

    def clean(self):
        data = super().clean()

        if data.get("move_threads_to"):
            if data["move_threads_to"].pk == self.instance.pk:
                message = pgettext_lazy(
                    "admin category form",
                    "You are trying to move this category threads to itself.",
                )
                raise forms.ValidationError(message)

            moving_to_child = self.instance.has_child(data["move_threads_to"])
            if moving_to_child and not data.get("move_children_to"):
                message = pgettext_lazy(
                    "admin category form",
                    "You are trying to move this category threads to a child category that will also be deleted.",
                )
                raise forms.ValidationError(message)

        return data


def DeleteFormFactory(instance):
    content_queryset = Category.objects.all_categories().order_by("lft")
    fields = {
        "move_threads_to": AdminCategoryChoiceField(
            label=pgettext_lazy("admin category form", "Move category threads to"),
            queryset=content_queryset,
            initial=instance.parent,
            empty_label=pgettext_lazy("admin category form", "Delete with category"),
            required=False,
        )
    }

    not_siblings = models.Q(lft__lt=instance.lft)
    not_siblings = not_siblings | models.Q(rght__gt=instance.rght)
    children_queryset = Category.objects.all_categories(True)
    children_queryset = children_queryset.filter(not_siblings).order_by("lft")

    if children_queryset.exists():
        fields["move_children_to"] = AdminCategoryChoiceField(
            label=pgettext_lazy("admin category form", "Move child categories to"),
            queryset=children_queryset,
            empty_label=pgettext_lazy("admin category form", "Delete with category"),
            required=False,
        )

    return type("DeleteCategoryFormFinal", (DeleteCategoryFormBase,), fields)


class CategoryRoleForm(forms.ModelForm):
    name = forms.CharField(label=pgettext_lazy("admin category role form", "Role name"))

    class Meta:
        model = CategoryRole
        fields = ["name"]


def RoleCategoryACLFormFactory(category, category_roles, selected_role):
    attrs = {
        "category": category,
        "role": forms.ModelChoiceField(
            label=pgettext_lazy("admin permissions form", "Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=pgettext_lazy("admin permissions form", "No access"),
        ),
    }

    return type("RoleCategoryACLForm", (forms.Form,), attrs)


def CategoryRolesACLFormFactory(role, category_roles, selected_role):
    attrs = {
        "role": role,
        "category_role": forms.ModelChoiceField(
            label=pgettext_lazy("admin permissions form", "Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=pgettext_lazy("admin permissions form", "No access"),
        ),
    }

    return type("CategoryRolesACLForm", (forms.Form,), attrs)
