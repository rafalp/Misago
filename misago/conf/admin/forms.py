from django import forms
from django.utils.translation import gettext_lazy as _

from ...admin.forms import YesNoSwitch
from ..cache import clear_settings_cache


class ChangeSettingsForm(forms.Form):
    settings = []

    def save(self, settings):
        self.save_settings(settings)
        self.clear_cache()

    def save_settings(self, settings):
        for setting in self.settings:
            setting_obj = settings[setting]
            new_value = self.cleaned_data.get(setting)
            self.save_setting(setting_obj, new_value)

    def save_setting(self, setting, value):
        setting.value = value
        setting.save()

    def clear_cache(self):
        clear_settings_cache()


class ChangeCaptchaSettingsForm(ChangeSettingsForm):
    settings = [
        "captcha_type",
        "recaptcha_site_key",
        "recaptcha_secret_key",
        "qa_question",
        "qa_help_text",
        "qa_answers",
    ]

    captcha_type = forms.ChoiceField(
        label=_("Enable CAPTCHA"),
        choices=[
            ("no", _("No CAPTCHA")),
            ("re", _("reCaptcha")),
            ("qa", _("Question and answer")),
        ],
        widget=forms.RadioSelect(),
    )
    recaptcha_site_key = forms.CharField(
        label=_("Site key"), max_length=100, required=False
    )
    recaptcha_secret_key = forms.CharField(
        label=_("Secret key"), max_length=100, required=False
    )
    qa_question = forms.CharField(
        label=_("Test question"), max_length=100, required=False
    )
    qa_help_text = forms.CharField(
        label=_("Question help text"), max_length=250, required=False
    )
    qa_answers = forms.CharField(
        label=_("Valid answers"),
        help_text=_("Enter each answer in new line. Answers are case-insensitive."),
        widget=forms.Textarea({"rows": 4}),
        max_length=250,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("captcha_type") == "re":
            if not cleaned_data.get("recaptcha_site_key"):
                self.add_error(
                    "recaptcha_site_key",
                    _(
                        "You need to enter site key if "
                        "selected CAPTCHA type is reCaptcha."
                    ),
                )

            if not cleaned_data.get("recaptcha_secret_key"):
                self.add_error(
                    "recaptcha_secret_key",
                    _(
                        "You need to enter secret key if "
                        "selected CAPTCHA type is reCaptcha."
                    ),
                )

        if cleaned_data.get("captcha_type") == "qa":
            if not cleaned_data.get("qa_question"):
                self.add_error(
                    "qa_question",
                    _("You need to set question if selected CAPTCHA type is Q&A."),
                )

            if not cleaned_data.get("qa_answers"):
                self.add_error(
                    "qa_answers",
                    _(
                        "You need to set question answers if "
                        "selected CAPTCHA type is Q&A."
                    ),
                )

        return cleaned_data


class ChangeGeneralSettingsForm(ChangeSettingsForm):
    settings = [
        "forum_name",
        "forum_index_title",
        "forum_index_meta_description",
        "forum_branding_display",
        "forum_branding_text",
        "forum_footnote",
        "email_footer",
    ]

    forum_name = forms.CharField(label=_("Forum name"), min_length=2, max_length=255)
    forum_index_title = forms.CharField(
        label=_("Title"),
        help_text=_("You may set a custom title on forum index by typing it here."),
        max_length=255,
        required=False,
    )
    forum_index_meta_description = forms.CharField(
        label=_("Meta Description"),
        help_text=_("Short description of your forum for internet crawlers."),
        max_length=255,
        required=False,
    )
    forum_branding_display = YesNoSwitch(
        label=_("Display branding"), help_text=_("Switch branding in forum's navbar.")
    )
    forum_branding_text = forms.CharField(
        label=_("Branding text"),
        help_text=_("Optional text displayed besides brand image in navbar."),
        max_length=255,
        required=False,
    )
    forum_footnote = forms.CharField(
        label=_("Forum footnote"),
        help_text=_("Short message displayed in forum footer."),
        max_length=300,
        required=False,
    )
    email_footer = forms.CharField(
        label=_("E-mails footer"),
        help_text=_(
            "Optional short message included at the end of e-mails sent by forum."
        ),
        max_length=255,
        required=False,
    )


class ChangeUsersSettingsForm(ChangeSettingsForm):
    settings = [
        "account_activation",
        "allow_custom_avatars",
        "avatar_upload_limit",
        "default_avatar",
        "default_gravatar_fallback",
        "signature_length_max",
        "subscribe_reply",
        "subscribe_start",
        "username_length_max",
        "username_length_min",
    ]

    account_activation = forms.ChoiceField(
        label=_("Require new accounts activation"),
        choices=[
            ("none", _("No activation required")),
            ("user", _("Activation token sent to user e-mail")),
            ("admin", _("Activation by administrator")),
            ("closed", _("Disable new registrations")),
        ],
        widget=forms.RadioSelect(),
    )
    username_length_min = forms.IntegerField(
        label=_("Minimum allowed username length"), min_value=2, max_value=20
    )
    username_length_max = forms.IntegerField(
        label=_("Maximum allowed username length"), min_value=2, max_value=20
    )
    allow_custom_avatars = YesNoSwitch(
        label=_("Allow custom avatar uploads"),
        help_text=_(
            "Turning this option off will forbid forum users from uploading custom "
            "avatars. Good for forums adressed at young users."
        ),
    )
    avatar_upload_limit = forms.IntegerField(
        label=_("Maximum size of uploaded avatar"),
        help_text=_("Enter maximum allowed file size (in KB) for avatar uploads."),
        min_value=0,
    )
    default_avatar = forms.ChoiceField(
        label=_("Default avatar"),
        choices=[
            ("dynamic", _("Individual")),
            ("gravatar", _("Gravatar")),
            ("gallery", _("Random avatar from gallery")),
        ],
        widget=forms.RadioSelect(),
    )
    default_gravatar_fallback = forms.ChoiceField(
        label=_("Fallback for default gravatar"),
        help_text=_(
            "Select which avatar to use when user has no gravatar associated with "
            "their e-mail address."
        ),
        choices=[
            ("dynamic", _("Individual")),
            ("gallery", _("Random avatar from gallery")),
        ],
        widget=forms.RadioSelect(),
    )
    signature_length_max = forms.IntegerField(
        label=_("Maximum allowed signature length"), min_value=10, max_value=5000
    )
    subscribe_start = forms.ChoiceField(
        label=_("Started threads"),
        choices=[
            ("no", _("Don't watch")),
            ("watch", _("Put on watched threads list")),
            (
                "watch_email",
                _("Put on watched threads list and e-mail user when somebody replies"),
            ),
        ],
        widget=forms.RadioSelect(),
    )
    subscribe_reply = forms.ChoiceField(
        label=_("Replied threads"),
        choices=[
            ("no", _("Don't watch")),
            ("watch", _("Put on watched threads list")),
            (
                "watch_email",
                _("Put on watched threads list and e-mail user when somebody replies"),
            ),
        ],
        widget=forms.RadioSelect(),
    )
