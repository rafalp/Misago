from django.utils.translation import ugettext_lazy as _

def register_usercp_extension(request):
    if request.acl.usercp.can_use_signature():
        return (('usercp_signature', _('Edit Signature')),)
