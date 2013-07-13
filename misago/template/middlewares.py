from django.conf import settings
from django.utils.importlib import import_module
from misago.thread import local

__all__ = ('merge_contexts', 'process_context', 'process_templates')

def load_middlewares():
    """
    Populate _middlewares with list of template middlewares instances
    """
    middlewares = []
    for extension in settings.TEMPLATE_MIDDLEWARES:
        module = '.'.join(extension.split('.')[:-1])
        extension = extension.split('.')[-1]
        module = import_module(module)
        middleware = getattr(module, extension)
        middlewares += (middleware(), )
    return tuple(middlewares)

_middlewares = load_middlewares()

def merge_contexts(dictionary=None, context_instance=None):
    dictionary = dictionary or {}
    if not context_instance:
        return dictionary
    context_instance.update(dictionary)
    return context_instance


_thread_local = local()


def process_context(templates, dictionary=None, context_instance=None):
    context = merge_contexts(dictionary, context_instance)
    """
    Put template context trough template middlewares
    """
    if _thread_local.template_mutex:
        return context
    _thread_local.template_mutex = True

    for middleware in _middlewares:
        try:
            new_context = middleware.process_context(templates, context)
            if new_context:
                context = new_context
        except AttributeError:
            pass

    _thread_local.template_mutex = None
    return context


def process_templates(templates, context):
    for middleware in _middlewares:
        try:
            new_templates = middleware.process_template(templates, context)
            if new_templates:
                return new_templates
        except AttributeError:
            pass
    return templates
