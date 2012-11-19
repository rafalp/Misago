from misago.acl.models import Role
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

def load_fixture():
    role_admin = Role(
                      name=_("Administrator").message,
                      token='admin'
                      )
    role_mod = Role(
                    name=_("Moderator").message,
                    token='mod'
                    )
    role_registered = Role(
                           name=_("Registered").message,
                           token='registered'
                           )
    role_guest = Role(
                      name=_("Guest").message,
                      token='guest'
                      )
    
    role_admin.save(force_insert=True)
    role_mod.save(force_insert=True)
    role_registered.save(force_insert=True)
    role_guest.save(force_insert=True)    