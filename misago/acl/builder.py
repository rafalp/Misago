from django.conf import settings
from django.core.cache import cache, InvalidCacheBackendError
from django.utils.importlib import import_module
from misago.forms import Form
from misago.models import Forum, ForumRole

def build_form(request, role):
    form_type = type('ACLForm', (Form,), dict(layout=[]))
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.make_form(request, role, form_type)
        except AttributeError:
            pass
    return form_type


def build_forum_form(request, role):
    form_type = type('ACLForm', (Form,), dict(layout=[]))
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.make_forum_form(request, role, form_type)
        except AttributeError:
            pass
    return form_type


class BaseACL(object):
    def __init__(self):
        self.acl = {}

    def __repr__(self):
        return '%s (%s)' % (self.__class__.__name__[0:-3],
                            self.__class__.__module__)


class ACL(object):
    def __init__(self, version):
        self.version = version
        self.team = False

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__") and attr not in ['team', 'version']:
                yield self.__dict__[attr]


def acl(request, user):
    acl_key = user.make_acl_key()
    try:
        user_acl = cache.get(acl_key)
        if user_acl.version != request.monitor['acl_version']:
            raise InvalidCacheBackendError()
    except (AttributeError, InvalidCacheBackendError):
        user_acl = build_acl(request, request.user.get_roles())
        cache.set(acl_key, user_acl, 2592000)
    return user_acl


def build_acl(request, roles):
    new_acl = ACL(request.monitor['acl_version'])
    forums = Forum.objects.get(special='root').get_descendants().order_by('lft')
    perms = []
    forum_roles = {}

    for role in roles:
        perms.append(role.permissions)

    for role in ForumRole.objects.all():
        forum_roles[role.pk] = role.permissions

    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.build(new_acl, perms)
        except AttributeError:
            pass
        try:
            app_module.build_forums(new_acl, perms, forums, forum_roles)
        except AttributeError:
            pass

    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.cleanup(new_acl, perms, forums)
        except AttributeError:
            pass

    return new_acl
