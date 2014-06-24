from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.acl.models import Role
from misago.users.models import Rank
from misago.users.validators import (validate_username, validate_email,
                                     validate_password)


class UserBaseForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"))
    title = forms.CharField(
        label=_("Custom title"),
        required=False)
    email = forms.EmailField(
        label=_("E-mail address"))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']

    def clean_username(self):
        data = self.cleaned_data['username']
        validate_username(data)
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        validate_email(data)
        return data

    def clean_new_password(self):
        data = self.cleaned_data['new_password']
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
        label=_("Password"),
        widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']


class EditUserForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("Change password to"),
        widget=forms.PasswordInput,
        required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']


def UserFormFactory(FormType, instance):
    extra_fields = {}


    ranks = Rank.objects.order_by('name')
    if ranks.exists():
        extra_fields['rank'] = forms.ModelChoiceField(
            label=_("Rank"),
            help_text=_("Ranks are used to group and distinguish users. "
                        "They are also used to add permissions to groups of "
                        "users."),
            queryset=ranks,
            initial=instance.rank,
            required=False,
            empty_label=_("No rank"))

    roles = Role.objects.order_by('name')
    extra_fields['roles'] = forms.ModelMultipleChoiceField(
        label=_("Roles"),
        help_text=_("Individual roles of this user."),
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
        help_text=_('Rank can give users with it additional roles.'))
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

    def clean(self):
        data = super(RankForm, self).clean()

        self.instance.set_name(data.get('name'))
        return data
