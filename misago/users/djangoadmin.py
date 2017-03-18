from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _


class UserAdminModel(ModelAdmin):
    """
    The model should be used for interaction of third party django apps with
    Misago's `User`.
    
    Removes `new` and `delete` actions (use Misago admin for that).
    
    Registration call is placed in :mod:`misago.users.admin`.
    The tests are in :mod:`misago.users.tests.test_djangoadmin_user`.
    """

    list_display = (
        'username', 'email', 'rank', 'is_staff', 'is_superuser', 'get_edit_from_misago_url',
    )
    search_fields = ('username', 'email')
    list_filter = ('groups', 'rank', 'is_staff', 'is_superuser')

    actions = None
    readonly_fields = (
        'username', 'email', 'joined_on', 'last_login', 'rank', 'is_staff', 'is_superuser',
        'get_edit_from_misago_url',
    )
    fieldsets = ((
        _("Misago user data"), {
            'fields': (
                'username', 'email', 'joined_on', 'last_login', 'rank', 'is_staff', 'is_superuser',
                'get_edit_from_misago_url',
            )
        },
    ), (_("Edit permissions and groups"), {
        'fields': ('groups', 'user_permissions', )
    }, ), )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_edit_from_misago_url(self, user_instance):
        return format_html(
            '<a href="{link}" class="{cls}" target="blank">{text}</a>',
            link=reverse(
                viewname='misago:admin:users:accounts:edit',
                kwargs={'pk': user_instance.pk},
            ),
            cls='changelink',
            text=_("Edit"),
        )

    get_edit_from_misago_url.short_description = _("Edit the user from Misago admin panel")
