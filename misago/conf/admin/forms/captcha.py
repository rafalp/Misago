from django import forms
from django.utils.translation import pgettext_lazy

from ....admin.forms import YesNoSwitch
from .base import SettingsForm


class CaptchaSettingsForm(SettingsForm):
    settings = [
        "captcha_type",
        "recaptcha_site_key",
        "recaptcha_secret_key",
        "qa_question",
        "qa_help_text",
        "qa_answers",
        "enable_stop_forum_spam",
        "stop_forum_spam_confidence",
    ]

    captcha_type = forms.ChoiceField(
        label=pgettext_lazy("admin captcha settings form", "Enable CAPTCHA"),
        choices=[
            ("no", pgettext_lazy("admin captcha type field choice", "No CAPTCHA")),
            ("re", pgettext_lazy("admin captcha type field choice", "reCaptcha")),
            (
                "qa",
                pgettext_lazy("admin captcha type field choice", "Question and answer"),
            ),
        ],
        widget=forms.RadioSelect(),
    )

    recaptcha_site_key = forms.CharField(
        label=pgettext_lazy("admin captcha settings form", "Site key"),
        max_length=100,
        required=False,
    )
    recaptcha_secret_key = forms.CharField(
        label=pgettext_lazy("admin captcha settings form", "Secret key"),
        max_length=100,
        required=False,
    )

    qa_question = forms.CharField(
        label=pgettext_lazy("admin captcha settings form", "Test question"),
        max_length=100,
        required=False,
    )
    qa_help_text = forms.CharField(
        label=pgettext_lazy("admin captcha settings form", "Question help text"),
        max_length=250,
        required=False,
    )
    qa_answers = forms.CharField(
        label=pgettext_lazy("admin captcha settings form", "Valid answers"),
        help_text=pgettext_lazy(
            "admin captcha settings form",
            "Enter each answer in new line. Answers are case-insensitive.",
        ),
        widget=forms.Textarea({"rows": 4}),
        max_length=250,
        required=False,
    )

    enable_stop_forum_spam = YesNoSwitch(
        label=pgettext_lazy(
            "admin captcha settings form",
            "Validate new registrations against SFS database",
        ),
        help_text=pgettext_lazy(
            "admin captcha settings form",
            "Turning this option on will result in Misago validating new user's e-mail and IP address against SFS database.",
        ),
    )
    stop_forum_spam_confidence = forms.IntegerField(
        label=pgettext_lazy(
            "admin captcha settings form", "Minimum SFS confidence required"
        ),
        help_text=pgettext_lazy(
            "admin captcha settings form",
            "SFS compares user e-mail and IP address with database of known spammers and assigns the confidence score in range of 0 to 100 that user is a spammer themselves. If this score is equal or higher than specified, Misago will block user from registering and ban their IP address for 24 hours.",
        ),
        min_value=0,
        max_value=100,
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("captcha_type") == "re":
            if not cleaned_data.get("recaptcha_site_key"):
                self.add_error(
                    "recaptcha_site_key",
                    pgettext_lazy(
                        "admin captcha settings form",
                        "You need to enter site key if selected CAPTCHA type is reCaptcha.",
                    ),
                )

            if not cleaned_data.get("recaptcha_secret_key"):
                self.add_error(
                    "recaptcha_secret_key",
                    pgettext_lazy(
                        "admin captcha settings form",
                        "You need to enter secret key if selected CAPTCHA type is reCaptcha.",
                    ),
                )

        if cleaned_data.get("captcha_type") == "qa":
            if not cleaned_data.get("qa_question"):
                self.add_error(
                    "qa_question",
                    pgettext_lazy(
                        "admin captcha settings form",
                        "You need to set question if selected CAPTCHA type is Q&A.",
                    ),
                )

            if not cleaned_data.get("qa_answers"):
                self.add_error(
                    "qa_answers",
                    pgettext_lazy(
                        "admin captcha settings form",
                        "You need to set question answers if selected CAPTCHA type is Q&A.",
                    ),
                )

        return cleaned_data
