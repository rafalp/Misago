from django import forms
from django.core.validators import validate_slug
from django.utils.translation import pgettext, pgettext_lazy

from ...core.validators import validate_color_hex, validate_css_name, validate_sluggable
from ...parser.factory import create_parser
from ...parser.html import render_tokens_to_html
from ...parser.metadata import get_tokens_metadata
from ...parser.plaintext import render_tokens_to_plaintext
from ...parser.tokenizer import tokenize
from ...permissions.enums import (
    CanHideOwnPostEdits,
    CanSeePostEdits,
    CanSeePostLikes,
    CanUploadAttachments,
)
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

    # Permissions

    can_edit_own_threads = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can edit own threads"),
    )
    own_threads_edit_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for editing own threads"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user starts a thread during which they can still edit it. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )

    can_edit_own_posts = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can edit own posts"),
    )
    own_posts_edit_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for editing own posts"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user posts a message during which they can still edit it. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )

    can_see_others_post_edits = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin group permissions form", "Can see other users post edits"
        ),
        choices=CanSeePostEdits.get_choices(),
        widget=forms.RadioSelect(),
        coerce=int,
    )
    can_hide_own_post_edits = forms.TypedChoiceField(
        label=pgettext_lazy("admin group permissions form", "Can hide own post edits"),
        choices=CanHideOwnPostEdits.get_choices(),
        widget=forms.RadioSelect(),
        coerce=int,
    )
    own_post_edits_hide_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for hiding own post edits"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user edits a post during which they can still hide the edit record. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )
    own_delete_post_edits_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for deleting own post edits"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user edits a post during which they can still delete the edit record. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )

    exempt_from_flood_control = YesNoSwitch(
        label=pgettext_lazy(
            "admin group permissions form", "Exempt from flood control"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enable this option to disable the flood control for members of this group.",
        ),
    )

    can_use_private_threads = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can use private threads"),
    )
    can_start_private_threads = YesNoSwitch(
        label=pgettext_lazy(
            "admin group permissions form", "Can start new private threads"
        ),
    )
    private_thread_members_limit = forms.IntegerField(
        label=pgettext_lazy("admin group permissions form", "Members limit"),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the maximum number of other members that can be added to private threads started by members of this group.",
        ),
        min_value=1,
    )

    can_upload_attachments = forms.TypedChoiceField(
        label=pgettext_lazy("admin group permissions form", "Can upload attachments"),
        choices=CanUploadAttachments.get_choices(),
        widget=forms.RadioSelect(),
        coerce=int,
    )
    attachment_storage_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Total attachment storage limit"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Maximum total storage space, in megabytes, that each member of this group can to use for their attachments. Enter 0 to remove this limit.",
        ),
        min_value=0,
    )
    unused_attachments_storage_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Unused attachments storage limit"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Maximum total storage space, in megabytes, for member's attachments that have been uploaded but are not associated with any posts. Enter 0 to remove this limit.",
        ),
        min_value=0,
    )
    attachment_size_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Attachment file size limit"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Maximum file size of an attachment in kilobytes. Enter 0 to remove this limit. Note: Server and Django request body size limits will still apply.",
        ),
        min_value=0,
    )
    can_always_delete_own_attachments = YesNoSwitch(
        label=pgettext_lazy(
            "admin group permissions form", "Can always delete own attachments"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "This permission allows users to delete their own attachments, even if they no longer have permission to edit or view the post they are associated with.",
        ),
    )

    can_start_polls = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can start polls"),
    )
    can_edit_own_polls = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can edit own polls"),
    )
    own_polls_edit_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for editing own polls"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user starts a poll during which they can still edit it. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )
    can_close_own_polls = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can close own polls"),
    )
    own_polls_close_time_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Time limit for closing own polls"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of minutes after a user starts a poll during which they can still edit it. Enter 0 to remove this time limit.",
        ),
        min_value=0,
    )
    can_vote_in_polls = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can vote in polls"),
        help_text=pgettext_lazy(
            "admin group permissions form", "Users can always vote in their own polls."
        ),
    )

    can_like_posts = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can like posts"),
    )
    can_see_own_post_likes = forms.TypedChoiceField(
        label=pgettext_lazy("admin group permissions form", "Can see own posts likes"),
        choices=CanSeePostLikes.get_choices(),
        widget=forms.RadioSelect(),
        coerce=int,
    )
    can_see_others_post_likes = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin group permissions form", "Can see other users post likes"
        ),
        choices=CanSeePostLikes.get_choices(),
        widget=forms.RadioSelect(),
        coerce=int,
    )

    can_change_username = YesNoSwitch(
        label=pgettext_lazy("admin group permissions form", "Can change username"),
    )
    username_changes_limit = forms.IntegerField(
        label=pgettext_lazy("admin group permissions form", "Limit username changes"),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter 0 to don't limit username changes.",
        ),
        min_value=0,
    )
    username_changes_expire = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Expire old username changes after"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the number of hours since the change after which it no longer counts towards the limit, or enter 0 for old username changes to always count.",
        ),
        min_value=0,
    )
    username_changes_span = forms.IntegerField(
        label=pgettext_lazy(
            "admin group permissions form", "Minimum time between changes"
        ),
        help_text=pgettext_lazy(
            "admin group permissions form",
            "Enter the minimum time between changes in hours, or enter 0 to not limit the time between changes.",
        ),
        min_value=0,
    )

    can_see_user_profiles = YesNoSwitch(
        label=pgettext_lazy(
            "admin group permissions form", "Can see other users' profiles"
        ),
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
            "can_edit_own_threads",
            "own_threads_edit_time_limit",
            "can_edit_own_posts",
            "own_posts_edit_time_limit",
            "can_see_others_post_edits",
            "can_hide_own_post_edits",
            "own_post_edits_hide_time_limit",
            "own_delete_post_edits_time_limit",
            "exempt_from_flood_control",
            "can_use_private_threads",
            "can_start_private_threads",
            "private_thread_members_limit",
            "can_upload_attachments",
            "attachment_storage_limit",
            "unused_attachments_storage_limit",
            "attachment_size_limit",
            "can_always_delete_own_attachments",
            "can_start_polls",
            "can_edit_own_polls",
            "own_polls_edit_time_limit",
            "can_close_own_polls",
            "own_polls_close_time_limit",
            "can_vote_in_polls",
            "can_like_posts",
            "can_see_own_post_likes",
            "can_see_others_post_likes",
            "can_change_username",
            "username_changes_limit",
            "username_changes_expire",
            "username_changes_span",
            "can_see_user_profiles",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["copy_permissions"].queryset = Group.objects.exclude(
            id=kwargs["instance"].id
        )

    def clean(self):
        data = super().clean()

        attachment_storage_limit = data.get("attachment_storage_limit")
        unused_attachments_storage_limit = data.get("unused_attachments_storage_limit")
        if (
            attachment_storage_limit
            and unused_attachments_storage_limit
            and unused_attachments_storage_limit > attachment_storage_limit
        ):
            self.add_error(
                "unused_attachments_storage_limit",
                forms.ValidationError(
                    message=pgettext(
                        "admin group form",
                        "Unused attachments limit cannot exceed total attachments limit.",
                    ),
                ),
            )

        return data


class EditGroupDescriptionForm(forms.ModelForm):
    markdown = forms.CharField(
        label=pgettext_lazy("admin group form", "Description"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional. Group's description in Markdown that will be parsed into HTML displayed on the group's page.",
        ),
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    meta = forms.CharField(
        label=pgettext_lazy("admin group form", "Meta description"),
        help_text=pgettext_lazy(
            "admin group form",
            "Optional. Will be used verbatim for the group page's meta description. Leave empty to generate one from the group's description.",
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

    def __init__(self, *args, request, **kwargs):
        self.request = request

        self.tokens = None
        self.metadata = None

        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()

        if data.get("markdown"):
            parser = create_parser()
            tokens = tokenize(parser, data["markdown"])
            metadata = get_tokens_metadata(tokens)

            data["html"] = render_tokens_to_html(parser, tokens)

            if not data.get("meta"):
                data["meta"] = render_tokens_to_plaintext(tokens)

            self.tokens = tokens
            self.metadata = metadata
        else:
            data.update({"markdown": None, "html": None})

        if not data.get("meta"):
            data["meta"] = None

        return data
