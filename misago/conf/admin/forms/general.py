from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeGeneralSettingsForm(ChangeSettingsForm):
    settings = [
        "forum_name",
        "forum_address",
        "index_header",
        "index_title",
        "index_meta_description",
        "logo",
        "logo_small",
        "logo_text",
        "og_image",
        "og_image_avatar_on_profile",
        "og_image_avatar_on_thread",
        "forum_footnote",
        "email_footer",
    ]

    forum_name = forms.CharField(label=_("Forum name"), min_length=2, max_length=255)
    forum_address = forms.URLField(label=_("Forum address"), max_length=255)

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
    logo_delete = forms.BooleanField(label=_("Delete logo image"), required=False)
    logo_small = forms.ImageField(
        label=_("Small logo"),
        help_text=_(
            "Image that will be displayed in compact forum navbar. "
            "When set, it will replace icon pointing to forum index."
        ),
        required=False,
    )
    logo_small_delete = forms.BooleanField(
        label=_("Delete small logo image"), required=False
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        address = self.request.build_absolute_uri("/")
        self["forum_address"].help_text = _(
            "Misago uses this setting to build links in e-mails sent to site "
            'users. Address under which site is running appears to be "%(address)s".'
        ) % {"address": address}

    def clean_forum_address(self):
        return self.cleaned_data["forum_address"].lower()
