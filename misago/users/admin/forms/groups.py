from django import forms
from django.utils.translation import pgettext_lazy

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
            "You can speed up a new group setup process by copying its permissions from another group. The administrator and moderator permissions are never copied.",
        ),
        queryset=Group.objects,
        required=False,
        empty_label=pgettext_lazy("admin group form", "(Don't copy permissions)"),
    )

    class Meta:
        model = Group
        fields = ["name"]
