from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import ListWidget

class List(ListWidget):
    admin = site.get_action('team')
    id = 'list'
    columns=(
             ('username', _("Team Member")),
             )
    default_sorting = 'username_slug'
    hide_actions = True
    pagination = 50
    
    def select_items(self, items):
        return items.filter(is_team=1)