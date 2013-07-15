from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    form.base_fields['can_search_forums'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['search_cooldown'] = forms.IntegerField(initial=25, min_value=0)
    form.layout.append((_("Searching"),
                        (
                         ('can_search_forums', {'label': _("Can search community")}),
                         ('search_cooldown', {'label': _("Minimum delay between searches"), 'help_text': _("Forum search can be resources intensive operation, and so its usually good idea to limit frequency of searches by requiring members to wait certain number of seconds before they can perform next search. Enter 0 to disable this requirement.")}),
                         )
                        ))


class SearchACL(BaseACL):
    def can_search(self):
        return self.acl['can_search_forums']

    def search_cooldown(self):
        return self.acl['search_cooldown']


def build(acl, roles):
    acl.search = SearchACL()
    acl.search.acl['can_search_forums'] = False
    acl.search.acl['search_cooldown'] = 25

    for role in roles:
        try:
            if role['can_search_forums']:
                acl.search.acl['can_search_forums'] = True
            if role['search_cooldown'] < acl.search.acl['search_cooldown']:
                acl.search.acl['search_cooldown'] = role['search_cooldown']
        except KeyError:
            pass
