from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import pgettext, pgettext_lazy

from ...models import DataDownload
from ...utils import hash_email

User = get_user_model()


class RequestDataDownloadsForm(forms.Form):
    user_identifiers = forms.CharField(
        label=pgettext_lazy("admin data download request form", "Usernames or emails"),
        help_text=pgettext_lazy(
            "admin data download request form",
            "Enter every item in new line. Duplicates will be ignored. This field is case insensitive. Depending on site configuration and amount of data to archive it may take up to few days for requests to complete. E-mail will notification will be sent to every user once their download is ready.",
        ),
        widget=forms.Textarea,
    )

    def clean_user_identifiers(self):
        user_identifiers = self.cleaned_data["user_identifiers"].lower().splitlines()
        user_identifiers = list(filter(bool, user_identifiers))
        user_identifiers = list(set(user_identifiers))

        if len(user_identifiers) > 20:
            raise forms.ValidationError(
                pgettext(
                    "admin data download request form",
                    "You may not enter more than 20 items at a single time (You have entered %(show_value)s).",
                )
                % {"show_value": len(user_identifiers)}
            )

        return user_identifiers

    def clean(self):
        data = super().clean()

        if data.get("user_identifiers"):
            username_match = Q(slug__in=data["user_identifiers"])
            email_match = Q(email_hash__in=map(hash_email, data["user_identifiers"]))

            data["users"] = list(User.objects.filter(username_match | email_match))

            if len(data["users"]) != len(data["user_identifiers"]):
                raise forms.ValidationError(
                    pgettext(
                        "admin data download request form",
                        "One or more specified users could not be found.",
                    )
                )

        return data


class FilterDataDownloadsForm(forms.Form):
    status = forms.ChoiceField(
        label=pgettext_lazy("admin data download requests filter form", "Status"),
        required=False,
        choices=DataDownload.STATUS_CHOICES,
    )
    user = forms.CharField(
        label=pgettext_lazy("admin data download requests filter form", "User"),
        required=False,
    )
    requested_by = forms.CharField(
        label=pgettext_lazy("admin data download requests filter form", "Requested by"),
        required=False,
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("status") is not None:
            queryset = queryset.filter(status=criteria["status"])

        if criteria.get("user"):
            queryset = queryset.filter(user__slug__istartswith=criteria["user"])

        if criteria.get("requested_by"):
            queryset = queryset.filter(
                requester__slug__istartswith=criteria["requested_by"]
            )

        return queryset
