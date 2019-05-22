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
            if setting_obj.python_type == "image":
                if new_value and new_value != self.initial.get(setting):
                    self.save_image(setting_obj, new_value)
                elif self.cleaned_data.get("%s_delete" % setting):
                    self.delete_image(setting_obj)
            else:
                self.save_setting(setting_obj, new_value)

    def delete_image(self, setting):
        if setting.image:
            setting.image.delete()

    def save_image(self, setting, value):
        if setting.image:
            setting.image.delete(save=False)
        setting.value = value
        setting.save()

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
        "index_header",
        "index_title",
        "index_meta_description",
        "logo",
        "logo_small",
        "logo_text",
        "forum_footnote",
        "email_footer",
    ]

    forum_name = forms.CharField(label=_("Forum name"), min_length=2, max_length=255)

    index_header = forms.CharField(
        label=_("Header text"),
        help_text=_("This text will replace forum name in page header."),
        max_length=255,
        required=False,
    )
    index_title = forms.CharField(label=_("Page title"), max_length=255, required=False)
    index_meta_description = forms.CharField(
        label=_("Meta Description"),
        help_text=_(
            "Short description of your forum that search and social sites may "
            "display next to link to your forum's index."
        ),
        max_length=255,
        required=False,
    )

    logo = forms.ImageField(
        label=_("Logo"),
        help_text=_("Image that will displayed in forum navbar."),
        required=False,
    )
    logo_delete = forms.BooleanField(label=_("Delete current logo"), required=False)
    logo_small = forms.ImageField(
        label=_("Small logo"),
        help_text=_(
            "Image that will be displayed in compact forum navbar. "
            "When set, it will replace icon pointing to forum index."
        ),
        required=False,
    )
    logo_small_delete = forms.BooleanField(
        label=_("Delete current small logo"), required=False
    )
    logo_text = forms.CharField(
        label=_("Text"),
        help_text=_(
            "Text displayed in forum navbar. If logo image was uploaded, text will "
            "be displayed right next to it. Never displayed by the compact navbar."
        ),
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


class ChangeThreadsSettingsForm(ChangeSettingsForm):
    settings = [
        "post_length_max",
        "post_length_min",
        "thread_title_length_max",
        "thread_title_length_min",
    ]

    post_length_max = forms.IntegerField(
        label=_("Maximum allowed post length"), min_value=0
    )
    post_length_min = forms.IntegerField(
        label=_("Minimum required post length"), min_value=1
    )
    thread_title_length_max = forms.IntegerField(
        label=_("Maximum allowed thread title length"), min_value=2, max_value=255
    )
    thread_title_length_min = forms.IntegerField(
        label=_("Minimum required thread title length"), min_value=2, max_value=255
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
