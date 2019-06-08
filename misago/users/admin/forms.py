from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from ...acl.models import Role
from ...admin.forms import IsoDateTimeField, YesNoSwitch
from ...conf.admin.forms import ChangeSettingsForm
from ...core.validators import validate_sluggable
from ...search.filter_queryset import filter_queryset
from ..models import Ban, DataDownload, Rank
from ..profilefields import profilefields
from ..utils import hash_email
from ..validators import validate_email, validate_username

User = get_user_model()


class UserBaseForm(forms.ModelForm):
    username = forms.CharField(label=_("Username"))
    title = forms.CharField(label=_("Custom title"), required=False)
    email = forms.EmailField(label=_("E-mail address"))

    class Meta:
        model = User
        fields = ["username", "email", "title"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.settings = self.request.settings

        super().__init__(*args, **kwargs)

    def clean_username(self):
        data = self.cleaned_data["username"]
        validate_username(self.settings, data, exclude=self.instance)
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        validate_email(data, exclude=self.instance)
        return data

    def clean_new_password(self):
        data = self.cleaned_data["new_password"]
        if data:
            validate_password(data, user=self.instance)
        return data

    def clean_roles(self):
        data = self.cleaned_data["roles"]

        for role in data:
            if role.special_role == "authenticated":
                break
        else:
            message = _('All registered members must have a "Member" role.')
            raise forms.ValidationError(message)

        return data


class NewUserForm(UserBaseForm):
    new_password = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "title"]


class EditUserForm(UserBaseForm):
    IS_STAFF_LABEL = _("Is administrator")
    IS_STAFF_HELP_TEXT = _(
        "Designates whether the user can log into admin sites. "
        "If Django admin site is enabled, this user will need "
        "additional permissions assigned within it to admin "
        "Django modules."
    )

    IS_SUPERUSER_LABEL = _("Is superuser")
    IS_SUPERUSER_HELP_TEXT = _(
        "Only administrators can access admin sites. "
        "In addition to admin site access, superadmins "
        "can also change other members admin levels."
    )

    IS_ACTIVE_LABEL = _("Is active")
    IS_ACTIVE_HELP_TEXT = _(
        "Designates whether this user should be treated as active. "
        "Turning this off is non-destructible way to remove user accounts."
    )

    IS_ACTIVE_STAFF_MESSAGE_LABEL = _("Staff message")
    IS_ACTIVE_STAFF_MESSAGE_HELP_TEXT = _(
        "Optional message for forum team members explaining "
        "why user's account has been disabled."
    )

    new_password = forms.CharField(
        label=_("Change password to"),
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )

    is_avatar_locked = YesNoSwitch(
        label=_("Lock avatar"),
        help_text=_(
            "Setting this to yes will stop user from changing "
            "his/her avatar, and will reset his/her avatar to "
            "procedurally generated one."
        ),
    )
    avatar_lock_user_message = forms.CharField(
        label=_("User message"),
        help_text=_(
            "Optional message for user explaining "
            "why he/she is banned form changing avatar."
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    avatar_lock_staff_message = forms.CharField(
        label=_("Staff message"),
        help_text=_(
            "Optional message for forum team members explaining "
            "why user is banned form changing avatar."
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    signature = forms.CharField(
        label=_("Signature contents"),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    is_signature_locked = YesNoSwitch(
        label=_("Lock signature"),
        help_text=_(
            "Setting this to yes will stop user from "
            "making changes to his/her signature."
        ),
    )
    signature_lock_user_message = forms.CharField(
        label=_("User message"),
        help_text=_(
            "Optional message to user explaining why his/hers signature is locked."
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    signature_lock_staff_message = forms.CharField(
        label=_("Staff message"),
        help_text=_(
            "Optional message to team members explaining why user signature is locked."
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    is_hiding_presence = YesNoSwitch(label=_("Hides presence"))

    limits_private_thread_invites_to = forms.TypedChoiceField(
        label=_("Who can add user to private threads"),
        coerce=int,
        choices=User.LIMIT_INVITES_TO_CHOICES,
    )

    subscribe_to_started_threads = forms.TypedChoiceField(
        label=_("Started threads"), coerce=int, choices=User.SUBSCRIPTION_CHOICES
    )
    subscribe_to_replied_threads = forms.TypedChoiceField(
        label=_("Replid threads"), coerce=int, choices=User.SUBSCRIPTION_CHOICES
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "title",
            "is_avatar_locked",
            "avatar_lock_user_message",
            "avatar_lock_staff_message",
            "signature",
            "is_signature_locked",
            "is_hiding_presence",
            "limits_private_thread_invites_to",
            "signature_lock_user_message",
            "signature_lock_staff_message",
            "subscribe_to_started_threads",
            "subscribe_to_replied_threads",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profilefields.add_fields_to_admin_form(self.request, self.instance, self)

    def get_profile_fields_groups(self):
        profile_fields_groups = []
        for group in self._profile_fields_groups:
            fields_group = {"name": group["name"], "fields": []}

            for fieldname in group["fields"]:
                fields_group["fields"].append(self[fieldname])

            profile_fields_groups.append(fields_group)
        return profile_fields_groups

    def clean_signature(self):
        data = self.cleaned_data["signature"]

        length_limit = self.settings.signature_length_max
        if len(data) > length_limit:
            message = ngettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit,
            )
            raise forms.ValidationError(message % {"limit": length_limit})

        return data

    def clean(self):
        data = super().clean()
        return profilefields.clean_form(self.request, self.instance, self, data)


def UserFormFactory(FormType, instance):
    extra_fields = {}

    extra_fields["rank"] = forms.ModelChoiceField(
        label=_("Rank"),
        help_text=_(
            "Ranks are used to group and distinguish users. They are "
            "also used to add permissions to groups of users."
        ),
        queryset=Rank.objects.order_by("name"),
        initial=instance.rank,
    )

    roles = Role.objects.order_by("name")

    extra_fields["roles"] = forms.ModelMultipleChoiceField(
        label=_("Roles"),
        help_text=_(
            'Individual roles of this user. All users must have a "Member" role.'
        ),
        queryset=roles,
        initial=instance.roles.all() if instance.pk else None,
        widget=forms.CheckboxSelectMultiple,
    )

    return type("UserFormFinal", (FormType,), extra_fields)


def StaffFlagUserFormFactory(FormType, instance):
    staff_fields = {
        "is_staff": YesNoSwitch(
            label=EditUserForm.IS_STAFF_LABEL,
            help_text=EditUserForm.IS_STAFF_HELP_TEXT,
            initial=instance.is_staff,
        ),
        "is_superuser": YesNoSwitch(
            label=EditUserForm.IS_SUPERUSER_LABEL,
            help_text=EditUserForm.IS_SUPERUSER_HELP_TEXT,
            initial=instance.is_superuser,
        ),
    }

    return type("StaffUserForm", (FormType,), staff_fields)


def UserIsActiveFormFactory(FormType, instance):
    is_active_fields = {
        "is_active": YesNoSwitch(
            label=EditUserForm.IS_ACTIVE_LABEL,
            help_text=EditUserForm.IS_ACTIVE_HELP_TEXT,
            initial=instance.is_active,
        ),
        "is_active_staff_message": forms.CharField(
            label=EditUserForm.IS_ACTIVE_STAFF_MESSAGE_LABEL,
            help_text=EditUserForm.IS_ACTIVE_STAFF_MESSAGE_HELP_TEXT,
            initial=instance.is_active_staff_message,
            widget=forms.Textarea(attrs={"rows": 3}),
            required=False,
        ),
    }

    return type("UserIsActiveForm", (FormType,), is_active_fields)


def EditUserFormFactory(
    FormType, instance, add_is_active_fields=False, add_admin_fields=False
):
    FormType = UserFormFactory(FormType, instance)

    if add_is_active_fields:
        FormType = UserIsActiveFormFactory(FormType, instance)

    if add_admin_fields:
        FormType = StaffFlagUserFormFactory(FormType, instance)

    return FormType


class BaseFilterUsersForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=False)
    email = forms.CharField(label=_("E-mail"), required=False)
    profilefields = forms.CharField(label=_("Profile fields contain"), required=False)
    is_inactive = forms.BooleanField(label=_("Requires activation"))
    is_disabled = forms.BooleanField(label=_("Account disabled"))
    is_staff = forms.BooleanField(label=_("Administrator"))
    is_deleting_account = forms.BooleanField(label=_("Deletes their account"))

    def filter_queryset(self, criteria, queryset):
        if criteria.get("username"):
            queryset = filter_queryset(
                queryset, "slug", criteria.get("username").lower()
            )

        if criteria.get("email"):
            queryset = filter_queryset(
                queryset, "email", criteria.get("email"), case_sensitive=False
            )

        if criteria.get("rank"):
            queryset = queryset.filter(rank_id=criteria.get("rank"))

        if criteria.get("role"):
            queryset = queryset.filter(roles__id=criteria.get("role"))

        if criteria.get("is_inactive"):
            queryset = queryset.filter(requires_activation__gt=0)

        if criteria.get("is_disabled"):
            queryset = queryset.filter(is_active=False)

        if criteria.get("is_staff"):
            queryset = queryset.filter(is_staff=True)

        if criteria.get("is_deleting_account"):
            queryset = queryset.filter(is_deleting_account=True)

        if criteria.get("profilefields", "").strip():
            queryset = profilefields.search_users(
                criteria.get("profilefields").strip(), queryset
            )

        return queryset


def create_filter_users_form():
    """
    Factory that uses cache for ranks and roles,
    and makes those ranks and roles typed choice fields that play nice
    with passing values via GET
    """
    ranks_choices = [("", _("All ranks"))]
    for rank in Rank.objects.order_by("name").iterator():
        ranks_choices.append((rank.pk, rank.name))

    roles_choices = [("", _("All roles"))]
    for role in Role.objects.order_by("name").iterator():
        roles_choices.append((role.pk, role.name))

    extra_fields = {
        "rank": forms.TypedChoiceField(
            label=_("Has rank"), coerce=int, required=False, choices=ranks_choices
        ),
        "role": forms.TypedChoiceField(
            label=_("Has role"), coerce=int, required=False, choices=roles_choices
        ),
    }

    return type("FilterUsersForm", (BaseFilterUsersForm,), extra_fields)


class RankForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        validators=[validate_sluggable()],
        help_text=_(
            "Short and descriptive name of all users with this rank. "
            '"The Team" or "Game Masters" are good examples.'
        ),
    )
    title = forms.CharField(
        label=_("User title"),
        required=False,
        help_text=_(
            "Optional, singular version of rank name displayed by user names. "
            'For example "GM" or "Dev".'
        ),
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_(
            "Optional description explaining function or status of "
            "members distincted with this rank."
        ),
    )
    roles = forms.ModelMultipleChoiceField(
        label=_("User roles"),
        widget=forms.CheckboxSelectMultiple,
        queryset=Role.objects.order_by("name"),
        required=False,
        help_text=_("Rank can give additional roles to users with it."),
    )
    css_class = forms.CharField(
        label=_("CSS class"),
        required=False,
        help_text=_(
            "Optional css class added to content belonging to this rank owner."
        ),
    )
    is_tab = YesNoSwitch(
        label=_("Give rank dedicated tab on users list"),
        required=False,
        help_text=_(
            "Selecting this option will make users with this rank easily discoverable "
            "by others through dedicated page on forum users list."
        ),
    )

    class Meta:
        model = Rank
        fields = ["name", "description", "css_class", "title", "roles", "is_tab"]

    def clean_name(self):
        data = self.cleaned_data["name"]
        self.instance.set_name(data)

        unique_qs = Rank.objects.filter(slug=self.instance.slug)
        if self.instance.pk:
            unique_qs = unique_qs.exclude(pk=self.instance.pk)

        if unique_qs.exists():
            raise forms.ValidationError(_("This name collides with other rank."))

        return data


class BanUsersForm(forms.Form):
    ban_type = forms.MultipleChoiceField(
        label=_("Values to ban"), widget=forms.CheckboxSelectMultiple, choices=[]
    )
    user_message = forms.CharField(
        label=_("User message"),
        required=False,
        max_length=1000,
        help_text=_("Optional message displayed to users instead of default one."),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": _("Message can't be longer than 1000 characters.")
        },
    )
    staff_message = forms.CharField(
        label=_("Team message"),
        required=False,
        max_length=1000,
        help_text=_("Optional ban message for moderators and administrators."),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": _("Message can't be longer than 1000 characters.")
        },
    )
    expires_on = IsoDateTimeField(label=_("Expiration date"), required=False)

    def __init__(self, *args, **kwargs):
        users = kwargs.pop("users")

        super().__init__(*args, **kwargs)

        self.fields["ban_type"].choices = [
            ("usernames", _("Usernames")),
            ("emails", _("E-mails")),
            ("domains", _("E-mail domains")),
        ]

        enable_ip_bans = list(filter(None, [u.joined_from_ip for u in users]))
        if enable_ip_bans:
            self.fields["ban_type"].choices += [
                ("ip", _("IP addresses")),
                ("ip_first", _("First segment of IP addresses")),
                ("ip_two", _("First two segments of IP addresses")),
            ]


class BanForm(forms.ModelForm):
    check_type = forms.TypedChoiceField(
        label=_("Check type"), coerce=int, choices=Ban.CHOICES
    )
    registration_only = YesNoSwitch(
        label=_("Restrict this ban to registrations"),
        help_text=_(
            "Changing this to yes will make this ban check be only performed on "
            "registration step. This is good if you want to block certain "
            "registrations like ones from recently comprimised e-mail providers, "
            "without harming existing users."
        ),
    )
    banned_value = forms.CharField(
        label=_("Banned value"),
        max_length=250,
        help_text=_(
            "This value is case-insensitive and accepts asterisk (*) "
            "for rought matches. For example, making IP ban for value "
            '"83.*" will ban all IP addresses beginning with "83.".'
        ),
        error_messages={
            "max_length": _("Banned value can't be longer than 250 characters.")
        },
    )
    user_message = forms.CharField(
        label=_("User message"),
        required=False,
        max_length=1000,
        help_text=_("Optional message displayed to user instead of default one."),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": _("Message can't be longer than 1000 characters.")
        },
    )
    staff_message = forms.CharField(
        label=_("Team message"),
        required=False,
        max_length=1000,
        help_text=_("Optional ban message for moderators and administrators."),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": _("Message can't be longer than 1000 characters.")
        },
    )
    expires_on = IsoDateTimeField(label=_("Expiration date"), required=False)

    class Meta:
        model = Ban
        fields = [
            "check_type",
            "registration_only",
            "banned_value",
            "user_message",
            "staff_message",
            "expires_on",
        ]

    def clean_banned_value(self):
        data = self.cleaned_data["banned_value"]
        while "**" in data:
            data = data.replace("**", "*")

        if data == "*":
            raise forms.ValidationError(_("Banned value is too vague."))

        return data


class FilterBansForm(forms.Form):
    check_type = forms.ChoiceField(
        label=_("Type"),
        required=False,
        choices=[
            ("", _("All bans")),
            ("names", _("Usernames")),
            ("emails", _("E-mails")),
            ("ips", _("IPs")),
        ],
    )
    value = forms.CharField(label=_("Banned value begins with"), required=False)
    registration_only = forms.ChoiceField(
        label=_("Registration only"),
        required=False,
        choices=[("", _("Any")), ("only", _("Yes")), ("exclude", _("No"))],
    )
    state = forms.ChoiceField(
        label=_("State"),
        required=False,
        choices=[("", _("Any")), ("used", _("Active")), ("unused", _("Expired"))],
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("check_type") == "names":
            queryset = queryset.filter(check_type=0)

        if criteria.get("check_type") == "emails":
            queryset = queryset.filter(check_type=1)

        if criteria.get("check_type") == "ips":
            queryset = queryset.filter(check_type=2)

        if criteria.get("value"):
            queryset = queryset.filter(
                banned_value__startswith=criteria.get("value").lower()
            )

        if criteria.get("state") == "used":
            queryset = queryset.filter(is_checked=True)

        if criteria.get("state") == "unused":
            queryset = queryset.filter(is_checked=False)

        if criteria.get("registration_only") == "only":
            queryset = queryset.filter(registration_only=True)

        if criteria.get("registration_only") == "exclude":
            queryset = queryset.filter(registration_only=False)

        return queryset


class RequestDataDownloadsForm(forms.Form):
    user_identifiers = forms.CharField(
        label=_("Usernames or emails"),
        help_text=_(
            "Enter every item in new line. Duplicates will be ignored. "
            "This field is case insensitive. Depending on site configuration and "
            "amount of data to archive it may take up to few days for requests to "
            "complete. E-mail will notification will be sent to every user once their "
            "download is ready."
        ),
        widget=forms.Textarea,
    )

    def clean_user_identifiers(self):
        user_identifiers = self.cleaned_data["user_identifiers"].lower().splitlines()
        user_identifiers = list(filter(bool, user_identifiers))
        user_identifiers = list(set(user_identifiers))

        if len(user_identifiers) > 20:
            raise forms.ValidationError(
                _(
                    "You may not enter more than 20 items at a single time "
                    "(You have entered %(show_value)s)."
                )
                % {"show_value": len(user_identifiers)}
            )

        return user_identifiers

    def clean(self):
        data = super().clean()

        if data.get("user_identifiers"):
            username_match = Q(slug__in=data["user_identifiers"])
            email_match = Q(email_hash__in=map(hash_email, data["user_identifiers"]))

            data["users"] = list(User.objects.filter(username_match | email_match))

            if len(data["users"]) != len(data["user_identifiers"]):
                raise forms.ValidationError(
                    _("One or more specified users could not be found.")
                )

        return data


class FilterDataDownloadsForm(forms.Form):
    status = forms.ChoiceField(
        label=_("Status"), required=False, choices=DataDownload.STATUS_CHOICES
    )
    user = forms.CharField(label=_("User"), required=False)
    requested_by = forms.CharField(label=_("Requested by"), required=False)

    def filter_queryset(self, criteria, queryset):
        if criteria.get("status") is not None:
            queryset = queryset.filter(status=criteria["status"])

        if criteria.get("user"):
            queryset = queryset.filter(user__slug__istartswith=criteria["user"])

        if criteria.get("requested_by"):
            queryset = queryset.filter(
                requester__slug__istartswith=criteria["requested_by"]
            )

        return queryset
