from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms, threadstore
from misago.core.validators import validate_sluggable
from misago.acl.models import Role

from misago.users.models import (AUTO_SUBSCRIBE_CHOICES,
                                 PRIVATE_THREAD_INVITES_LIMITS_CHOICES,
                                 BANS_CHOICES, RESTRICTIONS_CHOICES,
                                 Ban, Rank, WarningLevel)
from misago.users.validators import (validate_username, validate_email,
                                     validate_password)


"""
Users
"""
class UserBaseForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"))
    title = forms.CharField(
        label=_("Custom title"), required=False)
    email = forms.EmailField(
        label=_("E-mail address"))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']

    def clean_username(self):
        data = self.cleaned_data['username']
        validate_username(data, exclude=self.instance)
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        validate_email(data, exclude=self.instance)
        return data

    def clean_new_password(self):
        data = self.cleaned_data['new_password']
        if data:
            validate_password(data)
        return data

    def clean_roles(self):
        data = self.cleaned_data['roles']

        for role in data:
            if role.special_role == 'authenticated':
                break
        else:
            message = _('All registered members must have "Member" role.')
            raise forms.ValidationError(message)

        return data


class NewUserForm(UserBaseForm):
    new_password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']


class EditUserForm(UserBaseForm):
    new_password = forms.CharField(
        label=_("Change password to"),
        widget=forms.PasswordInput,
        required=False)

    is_avatar_locked = forms.YesNoSwitch(
        label=_("Lock avatar"),
        help_text=_("Setting this to yes will stop user from "
                    "changing his/her avatar, and will reset "
                    "his/her avatar to procedurally generated one."))
    avatar_lock_user_message = forms.CharField(
        label=_("User message"),
        help_text=_("Optional message for user explaining "
                    "why he/she is banned form changing avatar."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    avatar_lock_staff_message = forms.CharField(
        label=_("Staff message"),
        help_text=_("Optional message for forum team members explaining "
                    "why user is banned form changing avatar."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)

    signature = forms.CharField(
        label=_("Signature contents"),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    is_signature_locked = forms.YesNoSwitch(
        label=_("Lock signature"),
        help_text=_("Setting this to yes will stop user from "
                    "making changes to his/her signature."))
    signature_lock_user_message = forms.CharField(
        label=_("User message"),
        help_text=_("Optional message to user explaining "
                    "why his/hers signature is locked."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    signature_lock_staff_message = forms.CharField(
        label=_("Staff message"),
        help_text=_("Optional message to team members explaining "
                    "why user signature is locked."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)

    is_hiding_presence = forms.YesNoSwitch(label=_("Hides presence"))
    limits_private_thread_invites_to = forms.TypedChoiceField(
        label=_("Who can add user to private threads"),
        coerce=int,
        choices=PRIVATE_THREAD_INVITES_LIMITS_CHOICES)

    subscribe_to_started_threads = forms.TypedChoiceField(
        label=_("Started threads"), coerce=int, choices=AUTO_SUBSCRIBE_CHOICES)
    subscribe_to_replied_threads = forms.TypedChoiceField(
        label=_("Replid threads"), coerce=int,
        choices=AUTO_SUBSCRIBE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'title',
            'is_avatar_locked',
            'avatar_lock_user_message',
            'avatar_lock_staff_message',
            'signature',
            'is_signature_locked',
            'is_hiding_presence',
            'limits_private_thread_invites_to',
            'signature_lock_user_message',
            'signature_lock_staff_message',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'

        ]

    def clean_signature(self):
        data = self.cleaned_data['signature']

        length_limit = settings.signature_length_max
        if len(data) > length_limit:
            raise forms.ValidationError(ungettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit) % {'limit': length_limit})

        return data


def UserFormFactory(FormType, instance):
    extra_fields = {}

    extra_fields['rank'] = forms.ModelChoiceField(
        label=_("Rank"),
        help_text=_("Ranks are used to group and distinguish users. "
                    "They are also used to add permissions to groups of "
                    "users."),
        queryset=Rank.objects.order_by('name'),
        initial=instance.rank)

    roles = Role.objects.order_by('name')
    extra_fields['roles'] = forms.ModelMultipleChoiceField(
        label=_("Roles"),
        help_text=_('Individual roles of this user. '
                    'All users must have "member" role.'),
        queryset=roles,
        initial=instance.roles.all() if instance.pk else None,
        widget=forms.CheckboxSelectMultiple)

    return type('UserFormFinal', (FormType,), extra_fields)


def StaffFlagUserFormFactory(FormType, instance, add_staff_field):
    FormType = UserFormFactory(FormType, instance)

    if add_staff_field:
        staff_levels = (
            (0, _("No access")),
            (1, _("Administrator")),
            (2, _("Superadmin")),
        )

        staff_fields = {
            'staff_level': forms.TypedChoiceField(
                label=_("Admin level"),
                help_text=_('Only administrators can access admin sites. '
                            'In addition to admin site access, superadmins '
                            'can also change other members admin levels.'),
                coerce=int,
                choices=staff_levels,
                initial=instance.staff_level),
        }

        return type('StaffUserForm', (FormType,), staff_fields)
    else:
        return FormType


class SearchUsersFormBase(forms.Form):
    username = forms.CharField(label=_("Username starts with"), required=False)
    email = forms.CharField(label=_("E-mail starts with"), required=False)
    inactive = forms.YesNoSwitch(label=_("Inactive only"))
    is_staff = forms.YesNoSwitch(label=_("Admins only"))

    def filter_queryset(self, search_criteria, queryset):
        criteria = search_criteria
        if criteria.get('username'):
            queryset = queryset.filter(
                slug__startswith=criteria.get('username').lower())

        if criteria.get('email'):
            queryset = queryset.filter(
                email__istartswith=criteria.get('email'))

        if criteria.get('rank'):
            queryset = queryset.filter(
                rank_id=criteria.get('rank'))

        if criteria.get('role'):
            queryset = queryset.filter(
                roles__id=criteria.get('role'))

        if criteria.get('inactive'):
            queryset = queryset.filter(requires_activation__gt=0)

        if criteria.get('is_staff'):
            queryset = queryset.filter(is_staff=True)

        return queryset


def SearchUsersForm(*args, **kwargs):
    """
    Factory that uses cache for ranks and roles,
    and makes those ranks and roles typed choice fields that play nice
    with passing values via GET
    """
    ranks_choices = threadstore.get('misago_admin_ranks_choices', 'nada')
    if ranks_choices == 'nada':
        ranks_choices = [('', _("All ranks"))]
        for rank in Rank.objects.order_by('name').iterator():
            ranks_choices.append((rank.pk, rank.name))
        threadstore.set('misago_admin_ranks_choices', ranks_choices)

    roles_choices = threadstore.get('misago_admin_roles_choices', 'nada')
    if roles_choices == 'nada':
        roles_choices = [('', _("All roles"))]
        for role in Role.objects.order_by('name').iterator():
            roles_choices.append((role.pk, role.name))
        threadstore.set('misago_admin_roles_choices', roles_choices)

    extra_fields = {
        'rank': forms.TypedChoiceField(label=_("Has rank"),
                                       coerce=int,
                                       required=False,
                                       choices=ranks_choices),
        'role': forms.TypedChoiceField(label=_("Has role"),
                                       coerce=int,
                                       required=False,
                                       choices=roles_choices)
    }

    FinalForm = type('SearchUsersFormFinal',
                     (SearchUsersFormBase,),
                     extra_fields)
    return FinalForm(*args, **kwargs)


"""
Ranks
"""
class RankForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        validators=[validate_sluggable()],
        help_text=_('Short and descriptive name of all users with this rank. '
                    '"The Team" or "Game Masters" are good examples.'))
    title = forms.CharField(
        label=_("User title"), required=False,
        help_text=_('Optional, singular version of rank name displayed by '
                    'user names. For example "GM" or "Dev".'))
    description = forms.CharField(
        label=_("Description"), max_length=2048, required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Optional description explaining function or status of "
                    "members distincted with this rank."))
    roles = forms.ModelMultipleChoiceField(
        label=_("User roles"), queryset=Role.objects.order_by('name'),
        required=False,  widget=forms.CheckboxSelectMultiple,
        help_text=_('Rank can give additional roles to users with it.'))
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
        help_text=_("Optional css class added to content belonging to this "
                    "rank owner."))
    is_tab = forms.BooleanField(
        label=_("Give rank dedicated tab on users list"), required=False,
        help_text=_("Selecting this option will make users with this rank "
                    "easily discoverable by others trough dedicated page on "
                    "forum users list."))
    is_on_index = forms.BooleanField(
        label=_("Show users online on forum index"), required=False,
        help_text=_("Selecting this option will make forum inform other "
                    "users of their availability by displaying them on forum "
                    "index page."))

    class Meta:
        model = Rank
        fields = [
            'name',
            'description',
            'css_class',
            'title',
            'roles',
            'is_tab',
            'is_on_index',
        ]

    def clean_name(self):
        data = self.cleaned_data['name']
        self.instance.set_name(data)

        unique_qs = Rank.objects.filter(slug=self.instance.slug)
        if self.instance.pk:
            unique_qs = unique_qs.exclude(pk=self.instance.pk)

        if unique_qs.exists():
            raise forms.ValidationError(
                _("This name collides with other rank."))

        return data


"""
Bans
"""
class BanUsersForm(forms.Form):
    ban_type = forms.MultipleChoiceField(
        label=_("Values to ban"), widget=forms.CheckboxSelectMultiple,
        choices=(
            ('usernames', _('Usernames')),
            ('emails', _('E-mails')),
            ('domains', _('E-mail domains')),
            ('ip', _('IP addresses')),
            ('ip_first', _('First segment of IP addresses')),
            ('ip_two', _('First two segments of IP addresses'))
        ))
    user_message = forms.CharField(
        label=_("User message"), required=False, max_length=1000,
        help_text=_("Optional message displayed to users "
                    "instead of default one."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    staff_message = forms.CharField(
        label=_("Team message"), required=False, max_length=1000,
        help_text=_("Optional ban message for moderators and administrators."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    expires_on = forms.IsoDateTimeField(
        label=_("Expires on"), required=False,
        help_text=_('Leave this field empty for set bans to never expire.'))


class BanForm(forms.ModelForm):
    check_type = forms.TypedChoiceField(
        label=_("Check type"),
        coerce=int,
        choices=BANS_CHOICES)
    banned_value = forms.CharField(
        label=_("Banned value"), max_length=250,
        help_text=_('This value is case-insensitive and accepts asterisk (*) '
                    'for rought matches. For example, making IP ban for value '
                    '"83.*" will ban all IP addresses beginning with "83.".'),
        error_messages={
            'max_length': _("Banned value can't be longer "
                            "than 250 characters.")
        })
    user_message = forms.CharField(
        label=_("User message"), required=False, max_length=1000,
        help_text=_("Optional message displayed to user "
                    "instead of default one."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    staff_message = forms.CharField(
        label=_("Team message"), required=False, max_length=1000,
        help_text=_("Optional ban message for moderators and administrators."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    expires_on = forms.IsoDateTimeField(
        label=_("Expires on"), required=False,
        help_text=_('Leave this field empty for this ban to never expire.'))

    class Meta:
        model = Ban
        fields = [
            'check_type',
            'banned_value',
            'user_message',
            'staff_message',
            'expires_on',
        ]

    def clean_banned_value(self):
        data = self.cleaned_data['banned_value']
        while '**' in data:
            data = data.replace('**', '*')

        if data == '*':
            raise forms.ValidationError(_("Banned value is too vague."))

        return data


SARCH_BANS_CHOICES = (
    ('', _('All bans')),
    ('names', _('Usernames')),
    ('emails', _('E-mails')),
    ('ips', _('IPs')),
)


class SearchBansForm(forms.Form):
    check_type = forms.ChoiceField(
        label=_("Type"), required=False,
        choices=SARCH_BANS_CHOICES)
    value = forms.CharField(
        label=_("Banned value begins with"),
        required=False)
    state = forms.ChoiceField(
        label=_("State"), required=False,
        choices=(
            ('', _('Any')),
            ('used', _('Active')),
            ('unused', _('Expired')),
        ))

    def filter_queryset(self, search_criteria, queryset):
        criteria = search_criteria
        if criteria.get('check_type') == 'names':
            queryset = queryset.filter(check_type=0)

        if criteria.get('check_type') == 'emails':
            queryset = queryset.filter(check_type=1)

        if criteria.get('check_type') == 'ips':
            queryset = queryset.filter(check_type=2)

        if criteria.get('value'):
            queryset = queryset.filter(
                banned_value__startswith=criteria.get('value').lower())

        if criteria.get('state') == 'used':
            queryset = queryset.filter(is_checked=True)

        if criteria.get('state') == 'unused':
            queryset = queryset.filter(is_checked=False)

        return queryset


"""
Warning levels
"""
class WarningLevelForm(forms.ModelForm):
    name = forms.CharField(label=_("Level name"), max_length=255)
    length_in_minutes = forms.IntegerField(
        label=_("Length in minutes"), min_value=0,
        help_text=_("Enter number of minutes since this warning level was "
                    "imposed on member until it's reduced, or 0 to make "
                    "this warning level permanent."))
    restricts_posting_replies = forms.TypedChoiceField(
        label=_("Posting replies"),
        coerce=int, choices=RESTRICTIONS_CHOICES)
    restricts_posting_threads = forms.TypedChoiceField(
        label=_("Posting threads"),
        coerce=int, choices=RESTRICTIONS_CHOICES)

    class Meta:
        model = WarningLevel
        fields = [
            'name',
            'length_in_minutes',
            'restricts_posting_replies',
            'restricts_posting_threads',
        ]
