from django.utils.translation import ugettext_lazy as _

def register_profile_extension(request):
    return (('user_threads', _('Threads')),)
