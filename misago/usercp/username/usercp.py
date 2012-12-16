from django.utils.translation import ugettext_lazy as _

def register_usercp_extension(request):
    if request.acl.usercp.show_username_change():
        return (('usercp_username', _('Change Username')),)