import re

from django.forms import ValidationError
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from . import basefields


class BioField(basefields.UrlifiedTextareaProfileField):
    fieldname = "bio"
    label = _("Bio")


class RealNameField(basefields.TextProfileField):
    fieldname = "real_name"
    label = _("Real name")


class LocationField(basefields.TextProfileField):
    fieldname = "location"
    label = _("Location")


class GenderField(basefields.ChoiceProfileField):
    fieldname = "gender"
    label = _("Gender")

    choices = (
        ("", _("Not specified")),
        ("secret", _("Not telling")),
        ("female", _("Female")),
        ("male", _("Male")),
    )


class WebsiteField(basefields.UrlProfileField):
    fieldname = "website"
    label = _("Website")
    help_text = _(
        "If you own website in the internet you wish to share on your profile "
        "you may enter its address here. Remember to for it to be valid http "
        'address starting with either "http://" or "https://".'
    )


class SkypeIdField(basefields.TextProfileField):
    fieldname = "skype"
    label = _("Skype ID")
    help_text = _(
        "Entering your Skype ID in this field may invite other users to "
        "contact you over the Skype instead of via private threads."
    )


class TwitterHandleField(basefields.TextProfileField):
    fieldname = "twitter"
    label = _("Twitter handle")

    def get_help_text(self, user):
        return _(
            "If you own Twitter account, here you may enter your Twitter handle for "
            'other users to find you. Starting your handle with "@" sign is optional. '
            'Either "@%(slug)s" or "%(slug)s" are valid values.'
        ) % {"slug": user.slug}

    def get_value_display_data(self, request, user, value):
        return {"text": "@%s" % value, "url": "https://twitter.com/%s" % value}

    def clean(self, request, user, data):
        data = data.lstrip("@")
        if data and not re.search("^[A-Za-z0-9_]+$", data):
            raise ValidationError(gettext("This is not a valid twitter handle."))
        return data


class JoinIpField(basefields.TextProfileField):
    fieldname = "join_ip"
    label = _("Join IP")
    readonly = True

    def get_value_display_data(self, request, user, value):
        if not request.user_acl.get("can_see_users_ips"):
            return None

        if not user.joined_from_ip:
            return None

        return {"text": user.joined_from_ip}
