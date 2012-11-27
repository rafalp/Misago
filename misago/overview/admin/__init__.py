from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection, AdminAction
from misago.sessions.models import Session

ADMIN_SECTIONS=(
    AdminSection(
                 id='overview',
                 name=_("Overview"),
                 icon='signal',
                 ),
)

ADMIN_ACTIONS=(
   AdminAction(
               section='overview',
               id='home',
               name=_("Home"),
               help=_("Your forums right now"),
               icon='home',
               route='admin_overview_home',
               urlpatterns=patterns('misago.overview.admin.views',
                        url(r'^$', 'overview_home', name='admin_overview_home'),
                    ),
               ),
   AdminAction(
               section='overview',
               id='stats',
               name=_("Stats"),
               help=_("Create Statistics Reports"),
               icon='signal',
               route='admin_overview_stats',
               urlpatterns=patterns('misago.overview.admin.views',
                        url(r'^$', 'overview_stats', name='admin_overview_stats'),
                        url(r'^(?P<model>[a-z0-9]+)/(?P<date_start>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])/(?P<date_end>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])/(?P<precision>\w+)$', 'overview_graph', name='admin_overview_graph'),
                    ),
               ),
   AdminAction(
               section='overview',
               id='online',
               name=_("Online"),
               help=_("See who is currently online on forums."),
               icon='fire',
               model=Session,
               actions=[
                        {
                         'id': 'list',
                         'icon': 'list-alt',
                         'name': _("Browse Users"),
                         'help': _("Browse all registered user accounts"),
                         'route': 'admin_overview_online'
                         },
                        ],
               route='admin_overview_online', 
               urlpatterns=patterns('misago.overview.admin.views',
                        url(r'^$', 'OnlineList', name='admin_overview_online'),
                        url(r'^(?P<page>\d+)/$', 'OnlineList', name='admin_overview_online'),
                    ),
               ),
   AdminAction(
               section='overview',
               id='staff',
               name=_("Forum Team"),
               help=_("List of all forum team members"),
               icon='user',
               route='admin_overview_staff',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_overview_staff'),
                    ),
               ),
)