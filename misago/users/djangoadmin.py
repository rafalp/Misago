"""
Defines `UserAdminModel` for registration of Misago `User` model in django
admin panel.

The model supposed to be used for interaction of third party django apps with
Misago `User` model, i.e. assignment to a `User` permissions or groups.

Registration call is placed in :mod:`misago.users.admin`.

Test for the model is placed in :mod:`misago.users.tests.test_djangoadmin_user`.
"""
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _


# Misago user model
UserModel = get_user_model()


class UserAdminForm(forms.ModelForm):
    """
    This form adds `edit_from_misago_link` pseudo-field, that renders
    itself like an html hyperlink to a user edit page in misago admin panel.

    This could be done with `User` edit template overwrite, but
    it is kind of overkill - overwrite the whole template just to add one
    button - isn't it?
    """
    edit_from_misago_link = forms.Field()

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.init_edit_from_misago_link_field()

    def init_edit_from_misago_link_field(self):
        """init for the pseudo-field, and replace it's widget `render`"""
        field = self.fields['edit_from_misago_link']
        field.required = False
        field.label = ''
        field.widget.render = self.render_edit_from_misago_link

    def render_edit_from_misago_link(self, *args, **kwargs):
        """composes an html hyperlink for the pseudo-field render"""
        text = _('Edit this user in Misago admin panel')
        link_html_template = ('<a href="{}" target="blank">' + text + '</a>')
        link_url = reverse(
            viewname='misago:admin:users:accounts:edit',
            kwargs={'pk': self.instance.pk},
        )
        link_html = format_html(link_html_template, link_url)

        return link_html

    class Meta:
        model = UserModel
        fields = ['edit_from_misago_link']


class UserAdmin(admin.ModelAdmin):
    """
    Redeclare most of the model fields like read-only.
    Prevents new/delete actions (users should use misago admin panel for
    that).
    Replaces default form with custom `UserAdminForm`.
    """
    list_display = ['username', 'email', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    list_filter = ['groups', 'is_staff', 'is_superuser']

    form = UserAdminForm
    actions = None
    readonly_fields = [
        'username', 'email', 'rank', 'last_login', 'joined_on', 'is_staff', 'is_superuser'
    ]
    fieldsets = [
        [
            _('Misago user data'),
            {
                'fields': (
                    'username', 'email', 'rank', 'last_login', 'joined_on', 'is_staff',
                    'is_superuser', 'edit_from_misago_link',
                )
            },
        ],
        [
            _('Edit permissions and groups'),
            {
                'fields': ('groups', 'user_permissions', )
            },
        ],
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
