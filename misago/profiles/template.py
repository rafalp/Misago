from django.conf import settings
from django.template import RequestContext as DjangoRequestContext
from django.utils.importlib import import_module

def RequestContext(request, context=None):
    if not context:
        context = {}
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
