from django.conf import settings
from django.template import RequestContext as DjangoRequestContext
from django.utils.importlib import import_module
from misago.users.models import User

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
