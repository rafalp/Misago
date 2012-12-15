from django.conf import settings
from django.template import RequestContext as DjangoRequestContext
from django.utils.importlib import import_module

def RequestContext(request, context=None):
    print context
    if not context:
        context = {}
    context['tabs'] = []
    
    for extension in settings.USERCP_EXTENSIONS:
        usercp_module = import_module(extension + '.usercp')
        try:
            append_links = usercp_module.register_usercp_extension(request)
            for link in append_links:
                context['tabs'].append({
                                        'route': link[0],
                                        'active': context['tab'] == link[0][link[0].find('_') + 1:],
                                        'name': link[1],
                                        })
        except AttributeError:
            pass
    
    return DjangoRequestContext(request, context)
    