from misago.roles.models import Role
from misago.utils import ugettext_lazy as _

def load_fixtures():
    role_admin = Role(
                      name=_("Administrator").message,
                      token='admin',
                      protected=True,
                      )
    role_admin.set_permissions({
                                'can_use_acp': True,
                                'can_use_signature': True,
                                })
    
    role_mod = Role(
                    name=_("Moderator").message,
                    token='mod',
                    protected=True,
                    )
    role_admin.set_permissions({
                                'can_use_signature': True,
                                })
    
    role_registered = Role(
                           name=_("Registered").message,
                           token='registered',
                           )
    role_registered.set_permissions({})
    
    role_guest = Role(
                      name=_("Guest").message,
                      token='guest',
                      )
    role_guest.set_permissions({})
    
    role_admin.save(force_insert=True)
    role_mod.save(force_insert=True)
    role_registered.save(force_insert=True)
    role_guest.save(force_insert=True)    