from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection, AdminAction

ADMIN_SECTIONS=(
    AdminSection(
                 id='forums',
                 name=_("Forums"),
                 icon='comment',
                 after='users',
                 ),
)

ADMIN_ACTIONS=(
   AdminAction(
               section='forums',
               id='forums',
               name=_("Forums List"),
               help=_("Create, edit and delete forums."),
               icon='comment',
               route='admin_forums',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='attachments',
               name=_("Attachments"),
               help=_("Manage allowed attachment types."),
               icon='download-alt',
               route='admin_forums_attachments',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_attachments'),
                    ),
               ),
)