from importlib import import_module

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ThreadTypeBase(object):
    type_name = 'undefined'

    def get_forum_name(self, forum):
        return forum.name


def load_types(types_list):
    loaded_types = {}
    for path in types_list:
        module = import_module('.'.join(path.split('.')[:-1]))
        type_obj = getattr(module, path.split('.')[-1])()
        loaded_types[type_obj.type_name] = type_obj
    return loaded_types


THREAD_TYPES = load_types(settings.MISAGO_THREAD_TYPES)


def get(thread_type):
    try:
        return THREAD_TYPES[thread_type]
    except KeyError:
        raise KeyError("thread type %s is undefined" % thread_type)
