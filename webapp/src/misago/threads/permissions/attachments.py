from django import forms
from django.utils.translation import gettext_lazy as _

from ...acl import algebra
from ...acl.models import Role
from ...admin.forms import YesNoSwitch
from ..models import Attachment

# Admin Permissions Forms
class PermissionsForm(forms.Form):
    legend = _("Attachments")

    max_attachment_size = forms.IntegerField(
        label=_("Max attached file size (in kb)"),
        help_text=_("Enter 0 to don't allow uploading end deleting attachments."),
        initial=500,
        min_value=0,
    )

    can_download_other_users_attachments = YesNoSwitch(
        label=_("Can download other users attachments")
    )
    can_delete_other_users_attachments = YesNoSwitch(
        label=_("Can delete other users attachments")
    )


class AnonymousPermissionsForm(forms.Form):
    legend = _("Attachments")

    can_download_other_users_attachments = YesNoSwitch(
        label=_("Can download attachments")
    )


def change_permissions_form(role):
    if isinstance(role, Role):
        if role.special_role == "anonymous":
            return AnonymousPermissionsForm
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {
        "max_attachment_size": 0,
        "can_download_other_users_attachments": False,
        "can_delete_other_users_attachments": False,
    }
    new_acl.update(acl)

    return algebra.sum_acls(
        new_acl,
        roles=roles,
        key=key_name,
        max_attachment_size=algebra.greater,
        can_download_other_users_attachments=algebra.greater,
        can_delete_other_users_attachments=algebra.greater,
    )


def add_acl_to_attachment(user_acl, attachment):
    if user_acl["is_authenticated"] and user_acl["user_id"] == attachment.uploader_id:
        attachment.acl.update({"can_delete": True})
    else:
        user_can_delete = user_acl["can_delete_other_users_attachments"]
        attachment.acl.update(
            {"can_delete": user_acl["is_authenticated"] and user_can_delete}
        )


def register_with(registry):
    registry.acl_annotator(Attachment, add_acl_to_attachment)
