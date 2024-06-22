from django import forms
from django.utils.translation import pgettext_lazy

from ....admin.forms import YesNoSwitch
from ....forumindex.views import index_views
from .base import SettingsForm


class GeneralSettingsForm(SettingsForm):
    settings = [
        "forum_name",
        "forum_address",
        "index_header",
        "index_view",
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

    forum_name = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Forum name"),
        min_length=2,
        max_length=255,
    )
    forum_address = forms.URLField(
        label=pgettext_lazy("admin general settings form", "Forum address"),
        max_length=255,
    )

    index_title = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Page title"),
        max_length=255,
        required=False,
    )
    index_meta_description = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Meta Description"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Short description of your forum that search and social sites may display next to link to your forum's index.",
        ),
        max_length=255,
        required=False,
    )
    index_header = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Header text"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "This text will be displayed in page header on forum index.",
        ),
        max_length=255,
        required=False,
    )
    index_message = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Header message"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "This message will be displayed in page header on forum index, under the header text.",
        ),
        max_length=2048,
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    logo = forms.ImageField(
        label=pgettext_lazy("admin general settings form", "Large logo"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Image that will be displayed in forum navbar instead of a small logo or text.",
        ),
        required=False,
    )
    logo_delete = forms.BooleanField(
        label=pgettext_lazy("admin general settings form", "Delete large logo image"),
        required=False,
    )
    logo_small = forms.ImageField(
        label=pgettext_lazy("admin general settings form", "Small logo"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Image that will be displayed in the forum navbar next to the logo text if a large logo was not uploaded.",
        ),
        required=False,
    )
    logo_small_delete = forms.BooleanField(
        label=pgettext_lazy("admin general settings form", "Delete small logo image"),
        required=False,
    )
    logo_text = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Text logo"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Text displayed in forum navbar. If a small logo image was uploaded, this text will be displayed right next to it. If a large logo was uploaded, it will replace both the small logo and the text.",
        ),
        max_length=255,
        required=False,
    )

    og_image = forms.ImageField(
        label=pgettext_lazy("admin general settings form", "Image"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Custom image that will appear next to links to your forum posted on social sites. Facebook recommends that this image should be 1200 pixels wide and 630 pixels tall.",
        ),
        required=False,
    )
    og_image_delete = forms.BooleanField(
        label=pgettext_lazy("admin general settings form", "Delete image"),
        required=False,
    )
    og_image_avatar_on_profile = YesNoSwitch(
        label=pgettext_lazy(
            "admin general settings form", "Replace image with avatar on user profiles"
        )
    )
    og_image_avatar_on_thread = YesNoSwitch(
        label=pgettext_lazy(
            "admin general settings form", "Replace image with avatar on threads"
        )
    )

    forum_footnote = forms.CharField(
        label=pgettext_lazy("admin general settings form", "Forum footnote"),
        help_text=pgettext_lazy(
            "admin general settings form", "Short message displayed in forum footer."
        ),
        max_length=300,
        required=False,
    )
    email_footer = forms.CharField(
        label=pgettext_lazy("admin general settings form", "E-mails footer"),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Optional short message included at the end of e-mails sent by forum.",
        ),
        max_length=255,
        required=False,
    )

    show_admin_panel_link_in_ui = YesNoSwitch(
        label=pgettext_lazy(
            "admin general settings form",
            "Display the link to the Admin Control Panel in the administrator's user menu",
        ),
        help_text=pgettext_lazy(
            "admin general settings form",
            "Hiding the link to the ACP from user menus reduces risk of malicious actors gaining access to admin session for admin users who are sharing their device with others or who are logging in to the site in public spaces.",
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add index_view choice field
        self.fields["index_view"] = forms.CharField(
            label=pgettext_lazy("admin general settings form", "Index page"),
            help_text=pgettext_lazy(
                "admin general settings form",
                "Select the page to display on the forum index.",
            ),
            widget=forms.RadioSelect(choices=index_views.get_choices()),
            required=True,
        )

        # Set help text with accurate forum address from request on forum_address field
        address = self.request.build_absolute_uri("/").rstrip("/")
        self["forum_address"].help_text = pgettext_lazy(
            "admin general settings form",
            'Misago uses this setting to build links in e-mails sent to site users. Address under which site is running appears to be "%(address)s".',
        ) % {"address": address}

    def clean_forum_address(self):
        return self.cleaned_data["forum_address"].lower().rstrip("/")
