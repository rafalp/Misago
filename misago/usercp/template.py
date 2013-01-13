from django.conf import settings
from django.template import RequestContext as DjangoRequestContext
from django.utils.importlib import import_module

def RequestContext(request, context=None):
    if not context:
        context = {}
    context['tabs'] = []

    for extension in settings.USERCP_EXTENSIONS:
        usercp_module = import_module(extension + '.usercp')
        try:
            append_links = usercp_module.register_usercp_extension(request)
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
