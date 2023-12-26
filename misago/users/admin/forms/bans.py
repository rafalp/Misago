from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.forms import IsoDateTimeField, YesNoSwitch
from ...models import Ban

User = get_user_model()


class BanForm(forms.ModelForm):
    check_type = forms.TypedChoiceField(
        label=pgettext_lazy("admin ban form", "Check type"),
        coerce=int,
        choices=Ban.CHOICES,
    )
    registration_only = YesNoSwitch(
        label=pgettext_lazy("admin ban form", "Restrict this ban to registrations"),
        help_text=pgettext_lazy(
            "admin ban form",
            "Changing this to yes will make this ban check be only performed on registration step. This is good if you want to block certain registrations like ones from recently compromised e-mail providers, without harming existing users.",
        ),
    )
    banned_value = forms.CharField(
        label=pgettext_lazy("admin ban form", "Banned value"),
        max_length=250,
        help_text=pgettext_lazy(
            "admin ban form",
            'This value is case-insensitive and accepts asterisk (*) for partial matches. For example, making IP ban for value "83.*" will ban all IP addresses beginning with "83.".',
        ),
        error_messages={
            "max_length": pgettext_lazy(
                "admin ban form", "Banned value can't be longer than 250 characters."
            )
        },
    )
    user_message = forms.CharField(
        label=pgettext_lazy("admin ban form", "User message"),
        required=False,
        max_length=1000,
        help_text=pgettext_lazy(
            "admin ban form",
            "Optional message displayed to user instead of default one.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": pgettext_lazy(
                "admin ban form", "Message can't be longer than 1000 characters."
            )
        },
    )
    staff_message = forms.CharField(
        label=pgettext_lazy("admin ban form", "Team message"),
        required=False,
        max_length=1000,
        help_text=pgettext_lazy(
            "admin ban form", "Optional ban message for moderators and administrators."
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": pgettext_lazy(
                "admin ban form", "Message can't be longer than 1000 characters."
            )
        },
    )
    expires_on = IsoDateTimeField(
        label=pgettext_lazy("admin ban form", "Expiration date"),
        required=False,
    )

    class Meta:
        model = Ban
        fields = [
            "check_type",
            "registration_only",
            "banned_value",
            "user_message",
            "staff_message",
            "expires_on",
        ]

    def clean_banned_value(self):
        data = self.cleaned_data["banned_value"]
        while "**" in data:
            data = data.replace("**", "*")

        if data == "*":
            raise forms.ValidationError(
                pgettext("admin ban form", "Banned value is too vague.")
            )

        return data


class FilterBansForm(forms.Form):
    check_type = forms.ChoiceField(
        label=pgettext_lazy("admin bans filter form", "Type"),
        required=False,
        choices=[
            ("", pgettext_lazy("admin bans type filter choice", "All bans")),
            ("names", pgettext_lazy("admin bans type filter choice", "Usernames")),
            ("emails", pgettext_lazy("admin bans filter form", "E-mails")),
            ("ips", pgettext_lazy("admin bans type filter choice", "IPs")),
        ],
    )
    value = forms.CharField(
        label=pgettext_lazy("admin bans filter form", "Banned value begins with"),
        required=False,
    )
    registration_only = forms.ChoiceField(
        label=pgettext_lazy("admin bans filter form", "Registration only"),
        required=False,
        choices=[
            ("", pgettext_lazy("admin bans registration filter choice", "Any")),
            ("only", pgettext_lazy("admin bans registration filter choice", "Yes")),
            ("exclude", pgettext_lazy("admin bans registration filter choice", "No")),
        ],
    )
    state = forms.ChoiceField(
        label=pgettext_lazy("admin bans filter form", "State"),
        required=False,
        choices=[
            ("", pgettext_lazy("admin bans state filter choice", "Any")),
            ("used", pgettext_lazy("admin bans state filter choice", "Active")),
            ("unused", pgettext_lazy("admin bans state filter choice", "Expired")),
        ],
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("check_type") == "names":
            queryset = queryset.filter(check_type=0)

        if criteria.get("check_type") == "emails":
            queryset = queryset.filter(check_type=1)

        if criteria.get("check_type") == "ips":
            queryset = queryset.filter(check_type=2)

        if criteria.get("value"):
            queryset = queryset.filter(
                banned_value__startswith=criteria.get("value").lower()
            )

        if criteria.get("state") == "used":
            queryset = queryset.filter(is_checked=True)

        if criteria.get("state") == "unused":
            queryset = queryset.filter(is_checked=False)

        if criteria.get("registration_only") == "only":
            queryset = queryset.filter(registration_only=True)

        if criteria.get("registration_only") == "exclude":
            queryset = queryset.filter(registration_only=False)

        return queryset
