from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_forum_form(request, role, form):
    form.base_fields['can_see_forum'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_forum_contents'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.layout.append((
                        _("Forums Permissions"),
                        (
                         ('can_see_forum', {'label': _("Can see this forum")}),
                         ('can_see_forum_contents', {'label': _("Can see this forum's contents")}),
                        ),
                       ))
    

class ForumsACL(BaseACL):
    def can_see(self, forum):
        try:
            return forum.pk in self.acl['can_see']
        except AttributeError:
            return forum in self.acl['can_see']
        
    def can_browse(self, forum):
        if self.can_see(forum):
            try:
                return forum.pk in self.acl['can_see']
            except AttributeError:
                return forum in self.acl['can_see']
        return False


def build_forums(acl, perms, forums, forum_roles):
    acl.forums = ForumsACL()
    acl.forums.acl['can_see'] = []
    acl.forums.acl['can_browse'] = []
    
    for forum in forums:
        for perm in perms:
            try:
                role = forum_roles[perm['forums'][forum.pk]]
                if role['can_see_forum'] and forum.pk not in acl.forums.acl['can_see']:
                    acl.forums.acl['can_see'].append(forum.pk)
                if role['can_see_forum_contents'] and forum.pk not in acl.forums.acl['can_browse']:
                    acl.forums.acl['can_browse'].append(forum.pk)
            except KeyError:
                pass


def cleanup(acl, perms, forums):
    for forum in forums:
        if forum.pk in acl.forums.acl['can_browse'] and not forum.pk in acl.forums.acl['can_see']:
            # First burp: we can read forum but we cant see forum
            del acl.forums.acl['can_browse'][acl.forums.acl['can_browse'].index(forum.pk)]
            
        if forum.level > 1:
            if forum.parent_id not in acl.forums.acl['can_see'] or forum.parent_id not in acl.forums.acl['can_browse']:
                # Second burp: we cant see or read parent forum
                try:
                    del acl.forums.acl['can_see'][acl.forums.acl['can_see'].index(forum.pk)]
                except ValueError:
                    pass
                try:
                    del acl.forums.acl['can_browse'][acl.forums.acl['can_browse'].index(forum.pk)]
                except ValueError:
                    pass            