from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.models import Role
from misago.users.models import User, Rank
from misago.users.validators import validate_password, validate_email
from misago.forms import Form, YesNoSwitch

class UserForm(Form):
    username = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255,required=False)
    rank = forms.ModelChoiceField(queryset=Rank.objects.order_by('order').all(),required=False,empty_label=_('No rank assigned'))
    roles = False
    email = forms.EmailField(max_length=255)
    new_password = forms.CharField(max_length=255,required=False,widget=forms.PasswordInput)
    
    layout = [
              [
               _("Basic Account Settings"),
               [
                ('username', {'label': _("Username"), 'help_text': _("Username is name under which user is known to other users. Between 3 and 15 characters, only letters and digits are allowed.")}),
                ('title', {'label': _("User Title"), 'help_text': _("To override user title with custom one, enter it here.")}),
                ('rank', {'label': _("User Rank"), 'help_text': _("This users's rank.")}),
                ('roles', {'label': _("User Roles"), 'help_text': _("This user's roles. Roles are sets of user permissions")}),
                ],
               ],
              [
               _("Sign-in Credentials"),
               [
                ('email', {'label': _("E-mail Address"), 'help_text': _("Username is name under which user is known to other users.")}),
                ('new_password', {'label': _("Change User Password"), 'help_text': _("If you wish to change user's password, enter here new password. Otherwhise leave this field blank"), 'has_value': False}),
                ],
               ],
              ]
        
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs['request']
        self.user = user
        
        # Roles list
        if self.request.user.is_god():
            self.base_fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.order_by('name').all(),error_messages={'required': _("User must have at least one role assigned.")})
        else:
            self.base_fields['roles'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Role.objects.filter(protected__exact=False).order_by('name').all(),required=False)
            
        # Keep non-gods from editing protected members sign-in credentials
        if user.is_protected() and not self.request.user.is_god() and user.pk != self.request.user.pk:
            del self.base_fields['email']
            del self.base_fields['new_password']
            del self.layout[1]
            
        super(UserForm, self).__init__(*args, **kwargs)
    
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

class SearchUsersForm(Form):
    username = forms.CharField(max_length=255, required=False)
    email = forms.CharField(max_length=255, required=False)
    activation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(('0', _("Already Active")), ('1', _("By User")), ('2', _("By Administrator")), ('3', _("Sign-In Credentials Change"))), required=False)
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
    