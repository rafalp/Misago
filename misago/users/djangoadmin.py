# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _


def _change_field_short_description(short_desc_new):
    def func_wrapper(func):
        func.short_description = short_desc_new
        return func
    return func_wrapper


class UserAdminModel(ModelAdmin):
    """
    Removes `new` and `delete` actions (use misago admin panel for that).
    The registration call is placed in `misago.users.admin`.
    """
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_superuser',
        'rank',
        'show_edit_from_misago_url',
    )
    search_fields = ('username', 'email')
    list_filter = ('groups', 'is_staff', 'is_superuser', 'rank')

    actions = None
    readonly_fields = (
        'username',
        'email',
        'rank',
        'last_login',
        'joined_on',
        'is_staff',
        'is_superuser',
        'show_edit_from_misago_url',
    )
    fieldsets = (
        (
            _("Misago user data"),
            {'fields': (
                'username',
                'email',
                'rank',
                'last_login',
                'joined_on',
                'is_staff',
                'is_superuser',
                'show_edit_from_misago_url',
            )},
        ),
        (
            _("Edit permissions and groups"),
            {'fields': (
                'groups',
                'user_permissions',
            )},
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    @_change_field_short_description(_("Edit the user from Misago admin panel"))
    def show_edit_from_misago_url(self, user_instance):
        return format_html(
            '<a href="{link}" class="{cls}" target="blank">{text}</a>',
            link=reverse(
                viewname='misago:admin:users:accounts:edit',
                kwargs={'pk': user_instance.pk},
            ),
            cls='changelink',
            text=_("Edit"),
        )
