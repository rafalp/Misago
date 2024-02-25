from django import forms
from django.core.validators import validate_slug
from django.utils.translation import pgettext_lazy

from ...core.validators import validate_color_hex, validate_css_name, validate_sluggable
from ...parser.context import create_parser_context
from ...users.models import Group, GroupDescription
from ..forms import YesNoSwitch


class NewGroupForm(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin group form", "Name"),
        validators=[validate_sluggable()],
    )
    copy_permissions = forms.ModelChoiceField(
        label=pgettext_lazy("admin group form", "Copy permissions from"),
        help_text=pgettext_lazy(
            "admin group form",
            "You can speed up a new group setup process by copying its permissions from another group. Aadministrator and moderator permissions are not copied.",
        ),
        queryset=Group.objects,
        required=False,
        empty_label=pgettext_lazy("admin group form", "(Don't copy permissions)"),
    )

    class Meta:
        model = Group
        fields = ["name"]


class EditGroupForm(forms.ModelForm):
    name = forms.CharField(
        label=pgettext_lazy("admin group form", "Name"),
        validators=[validate_sluggable()],
    )
    slug = forms.CharField(
        label=pgettext_lazy("admin group form", "Slug"),
        help_text=pgettext_lazy(
            "admin group form",
            "Leave this field empty to set a default slug from the group's name.",
        ),
        validators=[validate_slug],
        required=False,
    )

    user_title = forms.CharField(
        label=pgettext_lazy("admin group form", "User title"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional user title displayed instead of the group's name next to group members in the interface.",
        ),
        required=False,
    )
    color = forms.CharField(
        label=pgettext_lazy("admin group form", "Color"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional. Should be in hex format, eg. #F5A9B8.",
        ),
        required=False,
        validators=[validate_color_hex],
    )
    icon = forms.CharField(
        label=pgettext_lazy("admin group form", "Icon"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional icon displayed next to the group's name (or member titles) in the interface.",
        ),
        required=False,
    )
    css_suffix = forms.CharField(
        label=pgettext_lazy("admin group form", "CSS suffix"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional CSS suffix added to various interface elements, enabling customization of how content from group members is displayed.",
        ),
        validators=[validate_css_name],
        required=False,
    )

    is_page = YesNoSwitch(
        label=pgettext_lazy(
            "admin group form", "Give this group a dedicated section on the Users page"
        ),
        help_text=pgettext_lazy(
            "admin group form",
            "Enabling this option will allow users to view all members of this group on a dedicated section of the Users page.",
        ),
    )
    is_hidden = YesNoSwitch(
        label=pgettext_lazy("admin group form", "Hide this group on user details"),
        help_text=pgettext_lazy(
            "admin group form",
            "Enabling this option will prevent this group from appearing on members' cards, profiles, and postbits.",
        ),
    )

    copy_permissions = forms.ModelChoiceField(
        label=pgettext_lazy("admin group form", "Copy permissions from"),
        help_text=pgettext_lazy(
            "admin group form",
            "You can replace this group's permissions with those copied from another group. Administrator and moderator permissions are not copied.",
        ),
        queryset=Group.objects,
        required=False,
        empty_label=pgettext_lazy("admin group form", "(Don't copy permissions)"),
    )

    can_see_user_profiles = YesNoSwitch(
        label=pgettext_lazy("admin group form", "Can see other users profiles"),
    )

    class Meta:
        model = Group
        fields = [
            "name",
            "slug",
            "user_title",
            "color",
            "icon",
            "css_suffix",
            "is_page",
            "is_hidden",
            "can_see_user_profiles",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["copy_permissions"].queryset = Group.objects.exclude(
            id=kwargs["instance"].id
        )


class EditGroupDescriptionForm(forms.ModelForm):
    markdown = forms.CharField(
        label=pgettext_lazy("admin group form", "Markdown"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional. Should be in hex format, eg. #F5A9B8.",
        ),
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    meta = forms.CharField(
        label=pgettext_lazy("admin group form", "Meta"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional. Should be in hex format, eg. #F5A9B8.",
        ),
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )

    class Meta:
        model = GroupDescription
        fields = [
            "markdown",
            "meta",
        ]

    def clean(self):
        data = super().clean()
        return data
