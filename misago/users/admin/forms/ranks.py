from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import pgettext, pgettext_lazy

from ....acl.models import Role
from ....admin.forms import YesNoSwitch
from ....core.validators import validate_sluggable
from ...models import Rank

User = get_user_model()


class RankForm(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin rank form", "Name"),
        validators=[validate_sluggable()],
        help_text=pgettext_lazy(
            "admin rank form",
            'Short and descriptive name of all users with this rank. "The Team" or "Game Masters" are good examples.',
        ),
    )
    title = forms.CharField(
        label=pgettext_lazy("admin rank form", "User title"),
        required=False,
        help_text=pgettext_lazy(
            "admin rank form",
            'Optional, singular version of rank name displayed by user names. For example "GM" or "Dev".',
        ),
    )
    description = forms.CharField(
        label=pgettext_lazy("admin rank form", "Description"),
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=pgettext_lazy(
            "admin rank form",
            "Optional description explaining function or status of members distincted with this rank.",
        ),
    )
    roles = forms.ModelMultipleChoiceField(
        label=pgettext_lazy("admin rank form", "User roles"),
        widget=forms.CheckboxSelectMultiple,
        queryset=Role.objects.order_by("name"),
        required=False,
        help_text=pgettext_lazy(
            "admin rank form", "Rank can give additional roles to users with it."
        ),
    )
    css_class = forms.CharField(
        label=pgettext_lazy("admin rank form", "CSS class"),
        required=False,
        help_text=pgettext_lazy(
            "admin rank form",
            "Optional css class added to content belonging to this rank owner.",
        ),
    )
    is_tab = YesNoSwitch(
        label=pgettext_lazy("admin rank form", "Give rank dedicated tab on users list"),
        required=False,
        help_text=pgettext_lazy(
            "admin rank form",
            "Selecting this option will make users with this rank easily discoverable by others through dedicated page on forum users list.",
        ),
    )

    class Meta:
        model = Rank
        fields = ["name", "description", "css_class", "title", "roles", "is_tab"]

    def clean_name(self):
        data = self.cleaned_data["name"]
        self.instance.set_name(data)

        unique_qs = Rank.objects.filter(slug=self.instance.slug)
        if self.instance.pk:
            unique_qs = unique_qs.exclude(pk=self.instance.pk)

        if unique_qs.exists():
            raise forms.ValidationError(
                pgettext(
                    "admin rank form",
                    "There's already an other rank with this name.",
                )
            )

        return data
