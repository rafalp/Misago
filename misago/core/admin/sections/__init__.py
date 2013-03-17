from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection

ADMIN_SECTIONS = (
    AdminSection(
                 id='overview',
                 name=_("Overview"),
                 icon='signal',
                 ),
)

"""
AdminSection(
             id='users',
             name=_("Users"),
             icon='user',
             ),
AdminSection(
             id='forums',
             name=_("Forums"),
             icon='comment',
             ),
AdminSection(
             id='perms',
             name=_("Permissions"),
             icon='adjust',
             ),
AdminSection(
             id='system',
             name=_("System"),
             icon='cog',
             ),
"""
