from typing import Type

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.translation import npgettext, pgettext, pgettext_lazy

from ....acl.models import Role
from ....admin.forms import IsoDateTimeField, YesNoSwitch
from ....notifications.threads import ThreadNotifications
from ....search.filter_queryset import filter_queryset
from ...enums import DefaultGroupId
from ...models import Group, Rank
from ...profilefields import profilefields
from ...utils import slugify_username
from ...validators import validate_email, validate_username

User = get_user_model()


class BaseUserForm(forms.ModelForm):
    groups_dict: dict[int, Group]

    username = forms.CharField(label=pgettext_lazy("admin user form", "Username"))
    title = forms.CharField(
        label=pgettext_lazy("admin user form", "Custom title"),
        required=False,
    )
    email = forms.EmailField(label=pgettext_lazy("admin user form", "E-mail address"))

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

    def clean_group(self):
        data = self.cleaned_data["group"]
        return self.groups_dict[data]

    def clean_secondary_groups(self):
        data = self.cleaned_data["secondary_groups"]
        return [self.groups_dict[item] for item in data]

    def clean_roles(self):
        data = self.cleaned_data["roles"]

        for role in data:
            if role.special_role == "authenticated":
                break
        else:
            message = pgettext(
                "admin user form", 'All registered members must have a "Member" role.'
            )
            raise forms.ValidationError(message)

        return data


class NewUserForm(BaseUserForm):
    new_password = forms.CharField(
        label=pgettext_lazy("admin user form", "Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["username", "email", "title"]

    def clean_group(self):
        data = self.cleaned_data["group"]
        group = self.groups_dict[data]

        if not self.request.user.is_misago_root and data == DefaultGroupId.ADMINS:
            raise forms.ValidationError(
                pgettext(
                    "admin user form",
                    "You must be a root administrator to set this user's main group to the %(group)s.",
                )
                % {"group": group}
            )

        return group

    def clean_secondary_groups(self):
        data = self.cleaned_data["secondary_groups"]

        if not self.request.user.is_misago_root and DefaultGroupId.ADMINS in data:
            admins_group = self.groups_dict[DefaultGroupId.ADMINS]
            raise forms.ValidationError(
                pgettext(
                    "admin user form",
                    "You must be a root administrator to add this user to the %(group)s group.",
                )
                % {"group": admins_group}
            )

        return [self.groups_dict[item] for item in data]


class EditUserForm(BaseUserForm):
    new_password = forms.CharField(
        label=pgettext_lazy("admin user form", "New password"),
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )

    is_misago_root = YesNoSwitch(
        label=pgettext_lazy("admin user form", "Is root administrator"),
        help_text=pgettext_lazy(
            "admin user form",
            "Root administrators can sign in to the Misago Admin Control Panel and change other users' admin status. You need to be a root administrator to change this field.",
        ),
        disabled=True,
    )

    is_active = YesNoSwitch(
        label=pgettext_lazy("admin user form", "Is active"),
        help_text=pgettext_lazy(
            "admin user form",
            "Designates whether this user should be treated as active. Turning this off is non-destructible way to remove user accounts.",
        ),
    )
    is_active_staff_message = forms.CharField(
        label=pgettext_lazy("admin user form", "Staff message"),
        help_text=pgettext_lazy(
            "admin user form",
            "Optional message for forum team members explaining why user's account has been disabled.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    is_avatar_locked = YesNoSwitch(
        label=pgettext_lazy("admin user form", "Lock avatar changes"),
        help_text=pgettext_lazy(
            "admin user form",
            "Setting this to yes will stop user from changing their avatar, and will reset their avatar to procedurally generated one.",
        ),
    )
    avatar_lock_user_message = forms.CharField(
        label=pgettext_lazy("admin user form", "User message"),
        help_text=pgettext_lazy(
            "admin user form",
            "Optional message for user explaining why they are banned form changing avatar.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    avatar_lock_staff_message = forms.CharField(
        label=pgettext_lazy("admin user form", "Staff message"),
        help_text=pgettext_lazy(
            "admin user form",
            "Optional message for forum team members explaining why user is banned form changing avatar.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    signature = forms.CharField(
        label=pgettext_lazy("admin user form", "Signature contents"),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    is_signature_locked = YesNoSwitch(
        label=pgettext_lazy("admin user form", "Lock signature changes"),
        help_text=pgettext_lazy(
            "admin user form",
            "Setting this to yes will stop user from making changes to his/her signature.",
        ),
    )
    signature_lock_user_message = forms.CharField(
        label=pgettext_lazy("admin user form", "User message"),
        help_text=pgettext_lazy(
            "admin user form",
            "Optional message to user explaining why his/hers signature is locked.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    signature_lock_staff_message = forms.CharField(
        label=pgettext_lazy("admin user form", "Staff message"),
        help_text=pgettext_lazy(
            "admin user form",
            "Optional message to team members explaining why user signature is locked.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    is_hiding_presence = YesNoSwitch(
        label=pgettext_lazy("admin user form", "Hides presence")
    )

    limits_private_thread_invites_to = forms.TypedChoiceField(
        label=pgettext_lazy("admin user form", "Who can add user to private threads"),
        coerce=int,
        choices=User.LIMIT_INVITES_TO_CHOICES,
    )

    watch_started_threads = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Automatically watch threads that the user has started",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )
    watch_replied_threads = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Automatically watch threads that the user has replied to",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )
    watch_new_private_threads_by_followed = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Automatically watch private threads that the user was invited to by users they are following",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )
    watch_new_private_threads_by_other_users = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Automatically watch private threads that the user was invited to by other users",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )
    notify_new_private_threads_by_followed = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Notify about new private thread invitations from users this user is following",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )
    notify_new_private_threads_by_other_users = forms.TypedChoiceField(
        label=pgettext_lazy(
            "admin user form",
            "Notify about new private thread invitations from other users",
        ),
        coerce=int,
        choices=ThreadNotifications.choices,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "title",
            "is_misago_root",
            "is_active",
            "is_active_staff_message",
            "is_avatar_locked",
            "avatar_lock_user_message",
            "avatar_lock_staff_message",
            "signature",
            "is_signature_locked",
            "is_hiding_presence",
            "limits_private_thread_invites_to",
            "signature_lock_user_message",
            "signature_lock_staff_message",
            "watch_started_threads",
            "watch_replied_threads",
            "watch_new_private_threads_by_followed",
            "watch_new_private_threads_by_other_users",
            "notify_new_private_threads_by_followed",
            "notify_new_private_threads_by_other_users",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request_user = kwargs["request"].user

        if request_user.is_misago_root and request_user != self.instance:
            self.fields["is_misago_root"].disabled = False

        if self.instance.is_misago_admin and not (
            request_user.is_misago_root or request_user == self.instance
        ):
            self.credentials_require_root = True
            self.fields["new_password"].disabled = True
            self.fields["email"].disabled = True
        else:
            self.credentials_require_root = False

        if (
            self.instance.is_deleting_account
            or request_user == self.instance
            or (self.instance.is_misago_admin and not request_user.is_misago_root)
        ):
            self.fields["is_active"].disabled = True
            self.fields["is_active_staff_message"].disabled = True

        profilefields.add_fields_to_admin_form(self.request, self.instance, self)

    def get_profile_fields_groups(self):
        profile_fields_groups = []
        for group in self._profile_fields_groups:
            fields_group = {"name": group["name"], "fields": []}

            for fieldname in group["fields"]:
                fields_group["fields"].append(self[fieldname])

            profile_fields_groups.append(fields_group)
        return profile_fields_groups

    def clean_group(self):
        group = super().clean_group()

        if self.request.user.is_misago_root:
            return group

        if group.id != self.instance.group.id:
            if self.instance.group.id == DefaultGroupId.ADMINS:
                raise forms.ValidationError(
                    pgettext(
                        "admin user form",
                        "You must be a root administrator to change this user's main group from the %(group)s.",
                    )
                    % {"group": self.instance.group}
                )

            if group.id == DefaultGroupId.ADMINS:
                raise forms.ValidationError(
                    pgettext(
                        "admin user form",
                        "You must be a root administrator to change this user's main group to the %(group)s.",
                    )
                    % {"group": group}
                )

        return group

    def clean_secondary_groups(self):
        secondary_groups = super().clean_secondary_groups()

        if self.request.user.is_misago_root:
            return secondary_groups

        admins_id = DefaultGroupId.ADMINS.value
        initial_secondary_groups_ids = [
            group_id
            for group_id in self.instance.groups_ids
            if group_id != self.instance.group_id
        ]
        updated_secondary_groups_ids = [group.id for group in secondary_groups]

        if (
            admins_id in initial_secondary_groups_ids
            and admins_id not in updated_secondary_groups_ids
        ):
            raise forms.ValidationError(
                pgettext(
                    "admin user form",
                    "You must be a root administrator to remove this user from the %(group)s group.",
                )
                % {"group": self.groups_dict[admins_id]}
            )

        if (
            admins_id not in initial_secondary_groups_ids
            and admins_id in updated_secondary_groups_ids
        ):
            raise forms.ValidationError(
                pgettext(
                    "admin user form",
                    "You must be a root administrator to add this user to the %(group)s group.",
                )
                % {"group": self.groups_dict[admins_id]}
            )

        return secondary_groups

    def clean_signature(self):
        data = self.cleaned_data["signature"]

        length_limit = self.settings.signature_length_max
        if len(data) > length_limit:
            message = npgettext(
                "signature length validator",
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit,
            )
            raise forms.ValidationError(message % {"limit": length_limit})

        return data

    def clean(self):
        data = super().clean()
        return profilefields.clean_form(self.request, self.instance, self, data)


def user_form_factory(base_form_type: Type[BaseUserForm], instance: User):
    groups = list(Group.objects.all())
    groups_data = {group.id: group for group in groups}

    groups_choices = []
    for group in groups:
        if group.id == DefaultGroupId.ADMINS:
            groups_choices.append((group.id, f"{group}*"))
        else:
            groups_choices.append((group.id, str(group)))

    if instance.group_id:
        instance.group = groups_data[instance.group_id]

    secondary_groups_initial = instance.groups_ids[:]
    if instance.group_id in secondary_groups_initial:
        secondary_groups_initial.remove(instance.group_id)

    form_attrs = {
        "groups_dict": groups_data,
        "group": forms.TypedChoiceField(
            label=pgettext_lazy("admin user form", "Main group"),
            help_text=pgettext_lazy(
                "admin user form",
                "An asterisk (*) after the group's name signifies the administrators group.",
            ),
            coerce=int,
            choices=groups_choices,
            initial=instance.group_id,
        ),
        "secondary_groups": forms.TypedMultipleChoiceField(
            label=pgettext_lazy("admin user form", "Secondary groups"),
            help_text=pgettext_lazy(
                "admin user form",
                "Optional, other groups this user should be a member of. An asterisk (*) after the group's name signifies the administrators group.",
            ),
            coerce=int,
            choices=groups_choices,
            initial=secondary_groups_initial,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        ),
        "rank": forms.ModelChoiceField(
            label=pgettext_lazy("admin user form", "Rank"),
            help_text=pgettext_lazy(
                "admin user form",
                "Ranks are used to group and distinguish users. They are also used to add permissions to groups of users.",
            ),
            queryset=Rank.objects.order_by("name"),
            initial=instance.rank,
        ),
    }

    roles = Role.objects.order_by("name")

    form_attrs["roles"] = forms.ModelMultipleChoiceField(
        label=pgettext_lazy("admin user form", "Roles"),
        help_text=pgettext_lazy(
            "admin user form",
            'Individual roles of this user. All users must have a "Member" role.',
        ),
        queryset=roles,
        initial=instance.roles.all() if instance.pk else None,
        widget=forms.CheckboxSelectMultiple,
    )

    return type("UserForm", (base_form_type,), form_attrs)


class BaseFilterUsersForm(forms.Form):
    username = forms.CharField(
        label=pgettext_lazy("admin users filter form", "Username"),
        required=False,
    )
    email = forms.CharField(
        label=pgettext_lazy("admin users filter form", "E-mail"),
        required=False,
    )
    profilefields = forms.CharField(
        label=pgettext_lazy("admin users filter form", "Profile fields contain"),
        required=False,
    )
    is_inactive = forms.BooleanField(
        label=pgettext_lazy("admin users filter form", "Requires activation")
    )
    is_deactivated = forms.BooleanField(
        label=pgettext_lazy("admin users filter form", "Account deactivated")
    )
    is_admin = forms.BooleanField(
        label=pgettext_lazy("admin users filter form", "Administrator")
    )
    is_deleting_account = forms.BooleanField(
        label=pgettext_lazy("admin users filter form", "Deletes their account")
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("username"):
            queryset = filter_queryset(
                queryset, "slug", slugify_username(criteria["username"])
            )

        if criteria.get("email"):
            queryset = filter_queryset(
                queryset, "email", criteria["email"], case_sensitive=False
            )

        if criteria.get("main_group"):
            queryset = queryset.filter(group_id=criteria["main_group"])

        if criteria.get("group"):
            queryset = queryset.filter(groups_ids__contains=[criteria["group"]])

        if criteria.get("rank"):
            queryset = queryset.filter(rank_id=criteria["rank"])

        if criteria.get("role"):
            queryset = queryset.filter(roles__id=criteria["role"])

        if criteria.get("is_inactive"):
            queryset = queryset.filter(requires_activation__gt=0)

        if criteria.get("is_deactivated"):
            queryset = queryset.filter(is_active=False)

        if criteria.get("is_admin"):
            queryset = queryset.filter(
                Q(is_misago_root=True) | Q(groups_ids__contains=[DefaultGroupId.ADMINS])
            )

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
    groups_choices = [
        ("", pgettext_lazy("admin users group filter choice", "All groups"))
    ]
    for group in Group.objects.order_by("name").iterator(chunk_size=50):
        groups_choices.append((group.pk, str(group)))

    ranks_choices = [("", pgettext_lazy("admin users rank filter choice", "All ranks"))]
    for rank in Rank.objects.order_by("name").iterator(chunk_size=50):
        ranks_choices.append((rank.pk, str(rank)))

    roles_choices = [("", pgettext_lazy("admin users role filter choice", "All roles"))]
    for role in Role.objects.order_by("name").iterator(chunk_size=50):
        roles_choices.append((role.pk, str(role)))

    extra_fields = {
        "main_group": forms.TypedChoiceField(
            label=pgettext_lazy("admin users filter form", "Main group"),
            coerce=int,
            required=False,
            choices=groups_choices,
        ),
        "group": forms.TypedChoiceField(
            label=pgettext_lazy("admin users filter form", "Has group"),
            coerce=int,
            required=False,
            choices=groups_choices,
        ),
        "rank": forms.TypedChoiceField(
            label=pgettext_lazy("admin users filter form", "Has rank"),
            coerce=int,
            required=False,
            choices=ranks_choices,
        ),
        "role": forms.TypedChoiceField(
            label=pgettext_lazy("admin users filter form", "Has role"),
            coerce=int,
            required=False,
            choices=roles_choices,
        ),
    }

    return type("FilterUsersForm", (BaseFilterUsersForm,), extra_fields)


class BanUsersForm(forms.Form):
    ban_type = forms.MultipleChoiceField(
        label=pgettext_lazy("admin ban users form", "Values to ban"),
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )
    user_message = forms.CharField(
        label=pgettext_lazy("admin ban users form", "User message"),
        required=False,
        max_length=1000,
        help_text=pgettext_lazy(
            "admin ban users form",
            "Optional message displayed to users instead of default one.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": pgettext_lazy(
                "admin ban users form", "Message can't be longer than 1000 characters."
            )
        },
    )
    staff_message = forms.CharField(
        label=pgettext_lazy("admin ban users form", "Team message"),
        required=False,
        max_length=1000,
        help_text=pgettext_lazy(
            "admin ban users form",
            "Optional ban message for moderators and administrators.",
        ),
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "max_length": pgettext_lazy(
                "admin ban users form", "Message can't be longer than 1000 characters."
            )
        },
    )
    expires_on = IsoDateTimeField(
        label=pgettext_lazy("admin ban users form", "Expiration date"), required=False
    )

    def __init__(self, *args, **kwargs):
        users = kwargs.pop("users")

        super().__init__(*args, **kwargs)

        self.fields["ban_type"].choices = [
            ("usernames", pgettext_lazy("admin ban users form", "Usernames")),
            ("emails", pgettext_lazy("admin ban users form", "E-mails")),
            ("domains", pgettext_lazy("admin ban users form", "E-mail domains")),
        ]

        enable_ip_bans = list(filter(None, [u.joined_from_ip for u in users]))
        if enable_ip_bans:
            self.fields["ban_type"].choices += [
                ("ip", pgettext_lazy("admin ban users form", "IP addresses")),
                (
                    "ip_first",
                    pgettext_lazy(
                        "admin ban users form", "First segment of IP addresses"
                    ),
                ),
                (
                    "ip_two",
                    pgettext_lazy(
                        "admin ban users form", "First two segments of IP addresses"
                    ),
                ),
            ]
