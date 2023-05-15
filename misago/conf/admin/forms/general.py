from django import forms
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from ....admin.forms import YesNoSwitch
from .base import SettingsForm


class GeneralSettingsForm(SettingsForm):
    settings = [
        "forum_name",
        "forum_address",
        "index_header",
        "index_title",
        "index_message",
        "index_meta_description",
        "logo",
        "logo_small",
        "logo_text",
        "og_image",
        "og_image_avatar_on_profile",
        "og_image_avatar_on_thread",
        "forum_footnote",
        "email_footer",
        "show_admin_panel_link_in_ui",
    ]

    forum_name = forms.CharField(label=_("Forum name"), min_length=2, max_length=255)
    forum_address = forms.URLField(label=_("Forum address"), max_length=255)

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
    index_header = forms.CharField(
        label=_("Header text"),
        help_text=_("This text will be displayed in page header on forum index."),
        max_length=255,
        required=False,
    )
    index_message = forms.CharField(
        label=_("Header message"),
        help_text=_(
            "This message will be displayed in page header on forum index, "
            "under the header text."
        ),
        max_length=2048,
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    logo = forms.ImageField(
        label=pgettext_lazy("admin general", "Large logo"),
        help_text=_(
            "Image that will be displayed in forum navbar instead of a small "
            "logo or text."
        ),
        required=False,
    )
    logo_delete = forms.BooleanField(label=_("Delete large logo image"), required=False)
    logo_small = forms.ImageField(
        label=pgettext_lazy("admin general", "Small logo"),
        help_text=_(
            "Image that will be displayed in the forum navbar next to the logo "
            "text if a large logo was not uploaded."
        ),
        required=False,
    )
    logo_small_delete = forms.BooleanField(
        label=_("Delete small logo image"), required=False
    )
    logo_text = forms.CharField(
        label=pgettext_lazy("admin general", "Text logo"),
        help_text=_(
            "Text displayed in forum navbar. If a small logo image was uploaded, "
            "this text will be displayed right next to it. If a large logo was "
            "uploaded, it will replace both the small logo and the text."
        ),
        max_length=255,
        required=False,
    )

    og_image = forms.ImageField(
        label=_("Image"),
        help_text=_(
            "Custom image that will appear next to links to your forum posted on "
            "social sites. Facebook recommends that this image should be "
            "1200 pixels wide and 630 pixels tall."
        ),
        required=False,
    )
    og_image_delete = forms.BooleanField(label=_("Delete image"), required=False)
    og_image_avatar_on_profile = YesNoSwitch(
        label=_("Replace image with avatar on user profiles")
    )
    og_image_avatar_on_thread = YesNoSwitch(
        label=_("Replace image with avatar on threads")
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

    show_admin_panel_link_in_ui = YesNoSwitch(
        label=_(
            "Display the link to the Admin Control Panel in "
            "the administrator's user menu"
        ),
        help_text=_(
            "Hiding the link to the ACP from user menus reduces risk of malicious "
            "actors gaining access to admin session for admin users who are sharing "
            "their PC with others or who are logging in to the site in public spaces."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        address = self.request.build_absolute_uri("/")
        self["forum_address"].help_text = _(
            "Misago uses this setting to build links in e-mails sent to site "
            'users. Address under which site is running appears to be "%(address)s".'
        ) % {"address": address}

    def clean_forum_address(self):
        return self.cleaned_data["forum_address"].lower()
