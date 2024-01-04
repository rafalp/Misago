import re

from django.forms import ValidationError
from django.utils.translation import pgettext, pgettext_lazy

from . import basefields


class BioField(basefields.UrlifiedTextareaProfileField):
    fieldname = "bio"
    label = pgettext_lazy("bio profile field", "Bio")


class RealNameField(basefields.TextProfileField):
    fieldname = "real_name"
    label = pgettext_lazy("real_name profile field", "Real name")


class LocationField(basefields.TextProfileField):
    fieldname = "location"
    label = pgettext_lazy("location profile field", "Location")


class GenderField(basefields.ChoiceProfileField):
    fieldname = "gender"
    label = pgettext_lazy("gender profile field", "Gender")

    choices = (
        ("", pgettext_lazy("gender profile field choice", "Not specified")),
        ("secret", pgettext_lazy("gender profile field choice", "Not telling")),
        ("female", pgettext_lazy("gender profile field choice", "Female")),
        ("male", pgettext_lazy("gender profile field choice", "Male")),
        ("enby", pgettext_lazy("gender profile field choice", "Non-binary")),
    )


class WebsiteField(basefields.UrlProfileField):
    fieldname = "website"
    label = pgettext_lazy("website profile field", "Website")
    help_text = pgettext_lazy(
        "website profile field",
        'If you own a website you wish to share on your profile, you may enter its address here. Remember that, for it to be valid, it should start with either "http://" or "https://".',
    )


class SkypeIdField(basefields.TextProfileField):
    fieldname = "skype"
    label = pgettext_lazy("skype id profile field", "Skype ID")


class TwitterHandleField(basefields.TextProfileField):
    fieldname = "twitter"
    label = pgettext_lazy("twitter handle profile field", "X (formerly Twitter) handle")

    def get_help_text(self, user):
        return pgettext_lazy(
            "twitter handle profile field",
            'If you own an X account, here you may enter your X handle for other users to find you. Starting your handle with "@" sign is optional. Either "@%(slug)s" or "%(slug)s" are valid values.',
        ) % {"slug": user.slug}

    def get_value_display_data(self, request, user, value):
        return {"text": "@%s" % value, "url": "https://twitter.com/%s" % value}

    def clean(self, request, user, data):
        data = data.lstrip("@")
        if data and not re.search(r"^[A-Za-z0-9_]+$", data):
            raise ValidationError(
                pgettext(
                    "twitter handle profile field",
                    "This is not a valid X handle.",
                )
            )
        return data


class JoinIpField(basefields.TextProfileField):
    fieldname = "join_ip"
    label = pgettext_lazy("join ip profile field", "Join IP")
    readonly = True

    def get_value_display_data(self, request, user, value):
        if not request.user_acl.get("can_see_users_ips"):
            return None

        if not user.joined_from_ip:
            return None

        return {"text": user.joined_from_ip}
