from django import forms
from django.utils.translation import pgettext_lazy

from ...users.models import Group


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
