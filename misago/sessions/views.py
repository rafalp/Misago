from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import ListWidget
from misago.sessions.forms import SearchSessionsForm

class List(ListWidget):
    admin = site.get_action('online')
    id = 'list'
    columns=(
             ('owner', _("Session Owner")),
             ('start', _("Session Start"), 25),
             ('last', _("Last Click"), 25),
             )
    default_sorting = 'start'
    sortables={
               'start': 0,
               'last': 0,
              }
    hide_actions = True
    pagination = 50
    search_form = SearchSessionsForm
    empty_message = _('Looks like nobody is currently online on forums.')
    
    def set_filters(self, model, filters):
        if 'username' in filters:
            model = model.filter(user__username__istartswith=filters['username'])
        if 'ip_address' in filters:
            model = model.filter(ip__startswith=filters['ip_address'])
        if 'useragent' in filters:
            model = model.filter(agent__icontains=filters['useragent'])
        if filters['type'] == 'registered':
            model = model.filter(user__isnull=False)
        if filters['type'] == 'hidden':
            model = model.filter(hidden=True)
        if filters['type'] == 'guest':
            model = model.filter(user__isnull=True)
        if filters['type'] == 'crawler':
            model = model.filter(crawler__isnull=False)
        return model
    
    def prefetch_related(self, items):
        return items.prefetch_related('user')
    
    def select_items(self, items):
        return items.filter(matched=1).filter(admin=0)