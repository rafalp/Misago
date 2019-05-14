from django import forms
from django.utils.translation import gettext_lazy as _

from ...admin.forms import YesNoSwitch
from ...conf.admin.forms import ChangeSettingsForm


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
