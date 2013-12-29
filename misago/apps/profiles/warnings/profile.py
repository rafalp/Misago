from django.utils.translation import ugettext_lazy as _

def register_profile_extension(request, user):
    if request.acl.warnings.can_see_member_warns(request.user, user):
        return (('user_warnings', _('Warnings')),)
