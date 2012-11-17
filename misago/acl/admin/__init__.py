from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection, AdminAction

ADMIN_SECTIONS=(
    AdminSection(
                 id='permissions',
                 name=_("Permissions"),
                 icon='adjust',
                 after='forums',
                 ),
)

ADMIN_ACTIONS=(
   AdminAction(
               section='permissions',
               id='permissions',
               name=_("Permissions"),
               help=_("trolololo permissions"),
               icon='adjust',
               route='admin_permissions',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_permissions'),
                    ),
               ),
)