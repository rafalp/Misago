from django import forms
from django.utils.translation import pgettext_lazy

from ....admin.forms import YesNoSwitch
from ....core.validators import validate_sluggable
from ...models import Group


class NewGroupForm(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin group form", "Name"),
        validators=[validate_sluggable()],
    )
    copy_permissions = forms.ModelChoiceField(
        label=pgettext_lazy("admin group form", "Copy permissions from"),
        help_text=pgettext_lazy(
            "admin group form",
            "You can speed up a new group setup process by copying its permissions from another group. Aadministrator and moderator permissions are not copied.",
        ),
        queryset=Group.objects,
        required=False,
        empty_label=pgettext_lazy("admin group form", "(Don't copy permissions)"),
    )

    class Meta:
        model = Group
        fields = ["name"]


class EditGroupForm(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin group form", "Name"),
        validators=[validate_sluggable()],
    )
    slug = forms.CharField(
        label=pgettext_lazy("admin group form", "Slug"),
        required=False,
    )

    is_page = YesNoSwitch(
        label=pgettext_lazy("admin group form", "Page"),
    )
    is_hidden = YesNoSwitch(
        label=pgettext_lazy("admin group form", "Hidden"),
    )
    copy_permissions = forms.ModelChoiceField(
        label=pgettext_lazy("admin group form", "Copy permissions from"),
        help_text=pgettext_lazy(
            "admin group form",
            "You can replace this group's permissions with those copied from another group. Administrator and moderator permissions are not copied.",
        ),
        queryset=Group.objects,
        required=False,
        empty_label=pgettext_lazy("admin group form", "(Don't copy permissions)"),
    )

    class Meta:
        model = Group
        fields = [
            "name",
            "slug",
            "css_suffix",
            "user_title",
            "user_icon",
            "is_page",
            "is_hidden",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["copy_permissions"].queryset = Group.objects.exclude(
            id=kwargs["instance"].id
        )
