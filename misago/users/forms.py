from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.ranks.models import Rank
from misago.roles.models import Role
from misago.users.models import User
from misago.users.validators import validate_password, validate_email
from misago.forms import Form, YesNoSwitch

class UserForm(Form):
    username = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255,required=False)
    rank = forms.ModelChoiceField(queryset=Rank.objects.order_by('order').all(),required=False,empty_label=_('No rank assigned'))
    roles = False
    email = forms.EmailField(max_length=255)
    new_password = forms.CharField(max_length=255,required=False,widget=forms.PasswordInput)
    signature = forms.CharField(widget=forms.Textarea,required=False)
    avatar_custom = forms.CharField(max_length=255,required=False)
    avatar_ban = forms.BooleanField(widget=YesNoSwitch,required=False)
    avatar_ban_reason_user = forms.CharField(widget=forms.Textarea,required=False)
    avatar_ban_reason_admin = forms.CharField(widget=forms.Textarea,required=False)
    signature_ban = forms.BooleanField(widget=YesNoSwitch,required=False)
    signature_ban_reason_user = forms.CharField(widget=forms.Textarea,required=False)
    signature_ban_reason_admin = forms.CharField(widget=forms.Textarea,required=False)
            
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs['request']
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
    
    def finalize_form(self):
        self.layout = [
                       [
                        _("Basic Account Settings"),
                        [
                         ('username', {'label': _("Username"), 'help_text': _("Username is name under which user is known to other users. Between 3 and 15 characters, only letters and digits are allowed.")}),
                         ('title', {'label': _("User Title"), 'help_text': _("To override user title with custom one, enter it here.")}),
                         ('rank', {'label': _("User Rank"), 'help_text': _("This user rank.")}),
                         ('roles', {'label': _("User Roles"), 'help_text': _("This user roles. Roles are sets of user permissions")}),
                         ],
                        ],
                       [
                        _("Sign-in Credentials"),
                        [
                         ('email', {'label': _("E-mail Address"), 'help_text': _("Member e-mail address.")}),
                         ('new_password', {'label': _("Change User Password"), 'help_text': _("If you wish to change user password, enter here new password. Otherwhise leave this field blank."), 'has_value': False}),
                         ],
                        ],
                       [
                        _("User Avatar"),
                        [
                         ('avatar_custom', {'label': _("Set Non-Standard Avatar"), 'help_text': _("You can make this member use special avatar by entering name of image file located in avatars directory here.")}),
                         ('avatar_ban', {'label': _("Lock Member's Avatar"), 'help_text': _("If you set this field to yes, this member's avatar will be deleted and replaced with random one selected from _removed gallery and member will not be able to change his avatar.")}),
                         ('avatar_ban_reason_user', {'label': _("User-visible reason for lock"), 'help_text': _("You can leave message to member explaining why he or she is unable to change his avatar anymore. This message will be displayed to member in his control panel.")}),
                         ('avatar_ban_reason_admin', {'label': _("Forum Team-visible reason for lock"), 'help_text': _("You can leave message to other forum team members exmplaining why this member's avatar has been locked.")}),
                         ],
                        ],
                       [
                        _("User Signature"),
                        [
                         ('signature', {'label': _("Signature"), 'help_text': _("Signature is short message attached at end of member's messages.")}),
                         ('signature_ban', {'label': _("Lock Member's Signature"), 'help_text': _("If you set this field to yes, this member will not be able to change his signature.")}),
                         ('signature_ban_reason_user', {'label': _("User-visible reason for lock"), 'help_text': _("You can leave message to member explaining why he or she is unable to edit his signature anymore. This message will be displayed to member in his control panel.")}),
                         ('signature_ban_reason_admin', {'label': _("Forum Team-visible reason for lock"), 'help_text': _("You can leave message to other forum team members exmplaining why this member's signature has been locked.")}),
                         ],
                        ],
                       ]
        
        # Roles list
        if self.request.user.is_god():
            self.fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.order_by('name').all(),error_messages={'required': _("User must have at least one role assigned.")})
        else:
            self.fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.filter(protected__exact=False).order_by('name').all(),required=False)
            
        # Keep non-gods from editing protected members sign-in credentials
        if self.user.is_protected() and not self.request.user.is_god() and self.user.pk != self.request.user.pk:
            del self.fields['email']
            del self.fields['new_password']
            del self.layout[1]
    
    def clean_username(self):
        self.user.set_username(self.cleaned_data['username'])
        try:
            self.user.full_clean()
        except ValidationError as e:
            self.user.is_username_valid(e)
        return self.cleaned_data['username']
        
    def clean_email(self):
        self.user.set_email(self.cleaned_data['email'])
        try:
            self.user.full_clean()
        except ValidationError as e:
            self.user.is_email_valid(e)
        return self.cleaned_data['email']
        
    def clean_new_password(self):
        if self.cleaned_data['new_password']:
            self.user.set_password(self.cleaned_data['new_password'])
            try:
                self.user.full_clean()
            except ValidationError as e:
                self.user.is_password_valid(e)
            validate_password(self.cleaned_data['new_password'])
            return self.cleaned_data['new_password']
        return ''

    def clean_avatar_custom(self):
        if self.cleaned_data['avatar_custom']:
            try:
                avatar_image = Image.open('%s/avatars/%s' % (settings.STATICFILES_DIRS[0], self.cleaned_data['avatar_custom']))
            except IOError:
                raise ValidationError(_("Avatar does not exist or is not image file."))
            return self.cleaned_data['avatar_custom']            
        return ''


class NewUserForm(Form):
    username = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255,required=False)
    rank = forms.ModelChoiceField(queryset=Rank.objects.order_by('order').all(),required=False,empty_label=_('No rank assigned'))
    roles = False
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255,widget=forms.PasswordInput)
    
    layout = [
              [
               _("Basic Account Settings"),
               [
                ('username', {'label': _("Username"), 'help_text': _("Username is name under which user is known to other users. Between 3 and 15 characters, only letters and digits are allowed.")}),
                ('title', {'label': _("User Title"), 'help_text': _("To override user title with custom one, enter it here.")}),
                ('rank', {'label': _("User Rank"), 'help_text': _("This user rank.")}),
                ('roles', {'label': _("User Roles"), 'help_text': _("This user roles. Roles are sets of user permissions")}),
                ],
               ],
              [
               _("Sign-in Credentials"),
               [
                ('email', {'label': _("E-mail Address"), 'help_text': _("Member e-mail address.")}),
                ('password', {'label': _("User Password"), 'help_text': _("Member password."), 'has_value': False}),
                ],
               ],
              ]
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs['request']
        
        # Roles list
        if self.request.user.is_god():
            self.base_fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.order_by('name').all(),error_messages={'required': _("User must have at least one role assigned.")})
        else:
            self.base_fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.filter(protected__exact=False).order_by('name').all(),required=False)
        
        super(NewUserForm, self).__init__(*args, **kwargs)
        
    def clean_username(self):
        new_user = User.objects.get_blank_user()
        new_user.set_username(self.cleaned_data['username'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_username_valid(e)
        return self.cleaned_data['username']
        
    def clean_email(self):
        new_user = User.objects.get_blank_user()
        new_user.set_email(self.cleaned_data['email'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_email_valid(e)
        return self.cleaned_data['email']
        
    def clean_password(self):
        new_user = User.objects.get_blank_user()
        new_user.set_password(self.cleaned_data['password'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_password_valid(e)
        validate_password(self.cleaned_data['password'])
        return self.cleaned_data['password']


class SearchUsersForm(Form):
    username = forms.CharField(max_length=255, required=False)
    email = forms.CharField(max_length=255, required=False)
    activation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(('0', _("Already Active")), ('1', _("By User")), ('2', _("By Administrator"))), required=False)
    rank = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('order').all(), required=False)
    role = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), required=False)
    
    layout = (
              (
               _("Search Users"),
               (
                ('username', {'label': _("Username"), 'attrs': {'placeholder': _("Username contains...")}}),
                ('email', {'label': _("E-mail Address"), 'attrs': {'placeholder': _("E-mail address contains...")}}),
                ('activation', {'label': _("Activation Requirement")}),
                ('rank', {'label': _("Rank is")}),
                ('role', {'label': _("Has Role")}),
               ),
              ),
             )
    