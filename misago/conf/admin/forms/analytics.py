import re

from django import forms
from django.utils.translation import pgettext_lazy

from .base import SettingsForm

GOOGLE_SITE_VERIFICATION = re.compile(
    r"^google-site-verification: google([0-9a-z]+)\.html$"
)


class AnalyticsSettingsForm(SettingsForm):
    settings = ["google_tracking_id", "google_site_verification"]

    google_tracking_id = forms.CharField(
        label=pgettext_lazy("admin analytics settings form", "Tracking ID"),
        help_text=pgettext_lazy(
            "admin analytics settings form",
            "Setting the Tracking ID will result in gtag.js file being included in your site's HTML markup, enabling Google Analytics integration.",
        ),
        required=False,
    )
    google_site_verification = forms.CharField(
        label=pgettext_lazy("admin analytics settings form", "Site verification code"),
        help_text=pgettext_lazy(
            "admin analytics settings form",
            "This code was extracted from the uploaded site verification file. To change it, upload new verification file.",
        ),
        required=False,
        disabled=True,
    )
    google_site_verification_file = forms.FileField(
        label=pgettext_lazy(
            "admin analytics settings form", "Upload site verification file"
        ),
        help_text=pgettext_lazy(
            "admin analytics settings form",
            'Site verification file can be downloaded from Search Console\'s "Ownership verification" page.',
        ),
        required=False,
    )

    def clean_google_site_verification_file(self):
        upload = self.cleaned_data.get("google_site_verification_file")
        if not upload:
            return None

        if upload.content_type != "text/html":
            raise forms.ValidationError(
                pgettext_lazy(
                    "admin analytics settings form", "Uploaded file type is not HTML."
                )
            )

        file_content = upload.read().decode("utf-8")
        content_match = GOOGLE_SITE_VERIFICATION.match(file_content)
        if not content_match:
            raise forms.ValidationError(
                pgettext_lazy(
                    "admin analytics settings form",
                    "Uploaded file doesn't contain a verification code.",
                )
            )

        return content_match.group(1)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("google_site_verification_file"):
            new_verification = cleaned_data.pop("google_site_verification_file")
            cleaned_data["google_site_verification"] = new_verification
        return cleaned_data
