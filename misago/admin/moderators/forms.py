from django import forms
from django.utils.translation import pgettext_lazy

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...permissions.models import Moderator
from ...users.models import Group
from ..forms import YesNoSwitch


class NewModeratorModalForm(forms.Form):
    moderator_type = forms.ChoiceField(
        label=pgettext_lazy("admin moderators form", "Moderator type"),
        choices=[
            ("group", pgettext_lazy("admin moderators form type choice", "User group")),
            (
                "user",
                pgettext_lazy("admin moderators form type choice", "Individual user"),
            ),
        ],
    )
    group = forms.TypedChoiceField(
        label=pgettext_lazy("admin moderators form", "Group"),
        choices=[],
        coerce=int,
        required=False,
    )
    user = forms.CharField(
        label=pgettext_lazy("admin moderators form", "User"),
        required=False,
    )

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

        self.fields["group"].choices = []
        for group in Group.objects.all():
            self.fields["group"].choices.append((group.id, str(group)))


class ModeratorForm(forms.ModelForm):
    is_global = YesNoSwitch(
        label=pgettext_lazy("admin moderators form", "Is global moderator"),
        help_text=pgettext_lazy(
            "admin moderators form",
            "Global moderators can moderate all content they have access to. Other options have no effect if this setting is enabled.",
        ),
    )
    categories = forms.TypedMultipleChoiceField(
        label=pgettext_lazy("admin moderators form", "Moderated categories"),
        coerce=int,
        required=False,
    )
    private_threads = YesNoSwitch(
        label=pgettext_lazy("admin moderators form", "Is private threads moderator"),
    )

    class Meta:
        model = Moderator
        fields = ["is_global", "categories", "private_threads"]

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

        self.fields["categories"].choices = get_categories_choices()


def get_categories_choices():
    categories_queryset = Category.objects.filter(
        level__gt=0, tree_id=CategoryTree.THREADS
    ).values_list("id", "name", "level")

    categories_choices = []
    for category_id, category_name, category_level in categories_queryset:
        prefix = ""
        if category_level > 1:
            prefix = " → " * (category_level - 1)

        categories_choices.append((category_id, f"{prefix}{category_name}"))

    return categories_choices
