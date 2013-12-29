from django.utils.translation import ugettext_lazy as _

def register_profile_extension(request, user):
    return (('user_threads', _('Warnings')),)
