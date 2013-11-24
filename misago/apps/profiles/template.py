from datetime import timedelta
from django.conf import settings
from django.template import RequestContext as DjangoRequestContext
from django.utils import timezone
from django.utils.importlib import import_module
from misago.models import User

def RequestContext(request, context=None):
    if not context:
        context = {}
    context['fallback'] = request.path
        
    # Find out if we ignore or follow this user
    context['follows'] = False
    context['ignores'] = False
    if request.user.is_authenticated() and request.user.pk != context['profile'].pk:
        context['follows'] = request.user.is_following(context['profile'])
        context['ignores'] = request.user.is_ignoring(context['profile'])
    
    # Find out if this user allows us to see his activity
    if request.user.pk != context['profile'].pk:
        if context['profile'].hide_activity == 2:
            context['hidden'] = True
        if context['profile'].hide_activity == 1:
            context['hidden'] = context['profile'].is_following(request.user)
    else:
        context['hidden'] = False

    # Find out if this user is online:
    if request.user.pk != context['profile'].pk:
        try:
            context['online'] = context['profile'].sessions.filter(admin=False).filter(last__gt=(timezone.now() - timedelta(minutes=10))).order_by('-last')[0:1][0]
        except IndexError:
            context['online'] = False
    else:
        # Fake "right now" time
        context['online'] = {'last': timezone.now()}

    # Sync member
    if context['profile'].sync_profile():
        context['profile'].save(force_update=True)

    context['tabs'] = []
    for extension in settings.PROFILE_EXTENSIONS:
        profile_module = import_module(extension + '.profile')
        try:
            append_links = profile_module.register_profile_extension(request)
            if append_links:
                for link in append_links:
                    link = list(link)
                    token = link[0][link[0].find('_') + 1:]
                    context['tabs'].append({
                                            'route': link[0],
                                            'active': context['tab'] == token,
                                            'name': link[1],
                                            })
        except AttributeError:
            pass
    return DjangoRequestContext(request, context)
