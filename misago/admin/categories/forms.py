from django import forms
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import pgettext, pgettext_lazy
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from ...admin.forms import YesNoSwitch
from ...categories.enums import CategoryTree, CategoryChildrenComponent
from ...categories.models import Category
from ...core.validators import validate_color_hex, validate_sluggable


class AdminCategoryFieldMixin:
    def __init__(self, *args, **kwargs):
        self.base_level = kwargs.pop("base_level", 1)
        kwargs["level_indicator"] = kwargs.get("level_indicator", "- - ")

        queryset = Category.objects.filter(tree_id=CategoryTree.THREADS)
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


class CategoryForm(forms.ModelForm):
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
        validators=[validate_color_hex],
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
    allow_polls = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Allow polls"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Controls if users can start new polls in this category.",
        ),
    )
    delay_browse_check = YesNoSwitch(
        label=pgettext_lazy(
            "admin category form",
            'Allow users without the "browse contents" permission to access category\'s threads list',
        ),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            'Enabling this option will allow users with permission to "see" this category to access it\'s threads list page. They will receive an error if they try to see threads replies.',
        ),
    )
    show_started_only = YesNoSwitch(
        label=pgettext_lazy(
            "admin category form", "Show users only threads that they started"
        ),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Enabling this option will limit users access to threads in this category to only the threads they have started. Moderators will still have access to all threads.",
        ),
    )
    is_closed = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Close category"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Only members with valid permissions can post in closed categories.",
        ),
    )
    is_vanilla = YesNoSwitch(
        label=pgettext_lazy("admin category form", "Make category vanilla"),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            'Vanilla categories behave like categories in "vanilla" forum software: users can\'t post threads directly in them. They are also displayed differently in the UI. Vanilla categories must have at least one visible subcategory to be shown to users.',
        ),
    )
    list_children_threads = YesNoSwitch(
        label=pgettext_lazy(
            "admin category form",
            "Include threads from child categories on threads list",
        ),
        required=False,
        help_text=pgettext_lazy(
            "admin category form",
            "Enabling this option will make this category's threads list also include threads from child categories. For vanilla categories disabling this option will remove threads list from category page.",
        ),
    )
    children_categories_component = forms.CharField(
        label=pgettext_lazy("admin category form", "Children categories UI component"),
        help_text=pgettext_lazy(
            "admin category form",
            "Select UI component to use for displaying category's subcategories on its page.",
        ),
        widget=forms.RadioSelect(
            choices=CategoryChildrenComponent.get_category_choices(),
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
            "allow_polls",
            "delay_browse_check",
            "show_started_only",
            "is_closed",
            "is_vanilla",
            "list_children_threads",
            "children_categories_component",
            "require_threads_approval",
            "require_replies_approval",
            "require_edits_approval",
            "prune_started_after",
            "prune_replied_after",
            "archive_pruned_in",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_new_parent_field()
        self.setup_copy_permissions_field()
        self.setup_archive_pruned_in_field()

    def setup_new_parent_field(self):
        parent_queryset = Category.objects.all_categories(True).order_by("lft")
        if self.instance.pk:
            not_siblings = models.Q(lft__lt=self.instance.lft)
            not_siblings = not_siblings | models.Q(rght__gt=self.instance.rght)
            parent_queryset = parent_queryset.filter(not_siblings)

        self.fields["new_parent"] = AdminCategoryChoiceField(
            label=pgettext_lazy("admin category form", "Parent category"),
            queryset=parent_queryset,
            initial=self.instance.parent,
            empty_label=None,
        )

    def setup_copy_permissions_field(self):
        self.fields["copy_permissions"] = AdminCategoryChoiceField(
            label=pgettext_lazy("admin category form", "Copy permissions"),
            help_text=pgettext_lazy(
                "admin category form",
                "You can replace this category permissions with permissions copied from the category selected here.",
            ),
            queryset=Category.objects.all_categories(),
            empty_label=pgettext_lazy("admin category form", "Don't copy permissions"),
            required=False,
        )

    def setup_archive_pruned_in_field(self):
        self.fields["archive_pruned_in"] = AdminCategoryChoiceField(
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
        )

    def clean_copy_permissions(self):
        data = self.cleaned_data["copy_permissions"]
        if data and data.pk == self.instance.pk:
            message = pgettext(
                "admin category form",
                "Permissions cannot be copied from category into itself.",
            )
            raise forms.ValidationError(message)
        return data

    def clean_archive_pruned_in(self):
        data = self.cleaned_data["archive_pruned_in"]
        if data and data.pk == self.instance.pk:
            message = pgettext(
                "admin category form", "Category cannot act as archive for itself."
            )
            raise forms.ValidationError(message)
        return data

    def clean(self):
        data = super().clean()
        self.instance.set_name(data.get("name"))

        if not self.errors and data["is_vanilla"]:
            self.validate_vanilla_invalid_values(data)

        return data

    def validate_vanilla_invalid_values(self, data: dict):
        new_parent = data.get("new_parent")

        if new_parent and new_parent.level != 0:
            self.add_error(
                "is_vanilla",
                forms.ValidationError(
                    pgettext(
                        "admin category form",
                        "Only top-level categories can be set as vanilla.",
                    )
                ),
            )

        elif (
            not data["list_children_threads"]
            and data["children_categories_component"]
            == CategoryChildrenComponent.DROPDOWN
        ):
            self.add_error(
                "children_categories_component",
                forms.ValidationError(
                    pgettext(
                        "admin category form",
                        "This choice is not available for vanilla categories with disabled listing of child category threads.",
                    )
                ),
            )


class DeleteCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_fields()

    def setup_fields(self):
        not_siblings = models.Q(lft__lt=self.instance.lft)
        not_siblings = not_siblings | models.Q(rght__gt=self.instance.rght)
        children_queryset = Category.objects.all_categories(True)
        children_queryset = children_queryset.filter(not_siblings).order_by("lft")

        if children_queryset.exists():
            self.fields["move_children_to"] = AdminCategoryChoiceField(
                label=pgettext_lazy("admin category form", "Move child categories to"),
                queryset=children_queryset,
                empty_label=pgettext_lazy(
                    "admin category form", "Delete with category"
                ),
                required=False,
            )

        content_queryset = Category.objects.all_categories().order_by("lft")
        self.fields["move_contents_to"] = AdminCategoryChoiceField(
            label=pgettext_lazy("admin category form", "Move contents to"),
            queryset=content_queryset,
            initial=self.instance.parent,
            empty_label=pgettext_lazy("admin category form", "Delete with category"),
            required=False,
        )

    def clean(self):
        data = super().clean()

        if data.get("move_contents_to"):
            if data["move_contents_to"].pk == self.instance.pk:
                message = pgettext_lazy(
                    "admin category form",
                    "You are trying to move this category threads to itself.",
                )
                raise forms.ValidationError(message)

            moving_to_child = self.instance.has_child(data["move_contents_to"])
            if moving_to_child and not data.get("move_children_to"):
                message = pgettext_lazy(
                    "admin category form",
                    "You are trying to move this category's contents to a child category that will also be deleted.",
                )
                raise forms.ValidationError(message)

        return data
