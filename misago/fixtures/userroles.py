from misago.models import Role
from misago.utils.translation import ugettext_lazy as _

def load():
    role = Role(name=_("Administrator").message, _special='admin', protected=True)
    role.permissions = {
                        'name_changes_allowed': 5,
                        'changes_expire': 7,
                        'can_use_acp': True,
                        'can_use_mcp': True,
                        'can_use_signature': True,
                        'allow_signature_links': True,
                        'allow_signature_images': True,
                        'can_search_users': True,
                        'can_see_users_emails': True,
                        'can_see_users_trails': True,
                        'can_see_hidden_users': True,
                        'forums': {1: 1, 2: 1, 3: 1, 5: 1, 6: 1},
                       }
    role.save(force_insert=True)
    
    role = Role(name=_("Moderator").message, _special='mod', protected=True)
    role.permissions = {
                        'name_changes_allowed': 3,
                        'changes_expire': 14,
                        'can_use_mcp': True,
                        'can_use_signature': True,
                        'allow_signature_links': True,
                        'can_search_users': True,
                        'can_see_users_emails': True,
                        'can_see_users_trails': True,
                        'can_see_hidden_users': True,
                        'forums': {1: 1, 2: 1, 3: 1, 5: 1, 6: 1},
                       }
    role.save(force_insert=True)
    
    role = Role(name=_("Registered").message, _special='registered')
    role.permissions = {
                        'name_changes_allowed': 2,
                        'can_use_signature': False,
                        'can_search_users': True,
                        'forums': {1: 3, 4: 3, 5: 3, 6: 3},
                       }
    role.save(force_insert=True)
    
    role = Role(name=_("Guest").message, _special='guest')
    role.permissions = {
                        'can_search_users': True,
                        'forums': {4: 6, 5: 6, 6: 6},
                       }
    role.save(force_insert=True)