from misago.roles.models import Role
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

def load_fixtures():
    role = Role(name=_("Administrator").message, token='admin', protected=True)
    role.set_permissions({
                          'name_changes_allowed': 5,
                          'changes_expire': 7,
                          'can_use_acp': True,
                          'can_use_signature': True,
                          'allow_signature_links': True,
                          'allow_signature_images': True,
                          'can_search_users': True,
                          'can_see_users_emails': True,
                          'can_see_users_trails': True,
                          'can_see_hidden_users': True,
                          'forums': {5: 1, 6: 1, 7: 1},
                          })
    role.save(force_insert=True)
    
    role = Role(name=_("Moderator").message, token='mod', protected=True)
    role.set_permissions({
                          'name_changes_allowed': 3,
                          'changes_expire': 14,
                          'can_use_signature': True,
                          'allow_signature_links': True,
                          'can_search_users': True,
                          'can_see_users_emails': True,
                          'can_see_users_trails': True,
                          'can_see_hidden_users': True,
                          'forums': {5: 1, 6: 1, 7: 1},
                          })
    role.save(force_insert=True)
    
    role = Role(name=_("Registered").message, token='registered')
    role.set_permissions({
                          'name_changes_allowed': 2,
                          'can_use_signature': False,
                          'can_search_users': True,
                          'forums': {5: 3, 6: 3, 7: 3},
                          })
    role.save(force_insert=True)
    
    role = Role(name=_("Guest").message, token='guest')
    role.set_permissions({
                          'can_search_users': True,
                          'forums': {5: 6, 6: 6, 7: 6},
                          })
    role.save(force_insert=True)