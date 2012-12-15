from django.conf import settings
from django.utils.importlib import import_module
from misago.forms import Form
from misago.forums.models import Forum
from misago.forumroles.models import ForumRole

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


class ACL(object):
    def __init__(self, version):
        self.version = version
        self.team = False


def build_acl(request, roles):
    acl = ACL(request.monitor['acl_version'])
    forums = Forum.objects.get(token='root').get_descendants().order_by('lft')
    perms = []
    forum_roles = {}
    
    for role in roles:
        perms.append(role.get_permissions())
    
    for role in ForumRole.objects.all():
        forum_roles[role.pk] = role.get_permissions()
    
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.build(acl, perms)
        except AttributeError:
            pass
        try:
            app_module.build_forums(acl, perms, forums, forum_roles)
        except AttributeError:
            pass
        
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.cleanup(acl, perms, forums)
        except AttributeError:
            pass

    return acl