from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.models import Session, User

ADMIN_ACTIONS = (
   AdminAction(
               section='overview',
               id='index',
               name=_("Home"),
               help=_("Your forums right now"),
               icon='home',
               route='admin_home',
               urlpatterns=patterns('misago.core.admin.index',
                        url(r'^$', 'index', name='admin_home'),
                    ),
               ),
    AdminAction(
               section='overview',
               id='stats',
               name=_("Stats"),
               help=_("Create Statistics Reports"),
               icon='signal',
               route='admin_stats',
               urlpatterns=patterns('misago.core.admin.stats.views',
                        url(r'^$', 'form', name='admin_stats'),
                        url(r'^(?P<model>[a-z0-9]+)/(?P<date_start>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])/(?P<date_end>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])/(?P<precision>\w+)$', 'graph', name='admin_stats_graph'),
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
                         'name': _("Browse Users"),
                         'help': _("Browse all registered user accounts"),
                         'route': 'admin_online'
                         },
                        ],
               route='admin_online',
               urlpatterns=patterns('misago.core.admin.online.views',
                        url(r'^$', 'List', name='admin_online'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_online'),
                    ),
               ),
)
"""
AdminAction(
           section='overview',
           id='team',
           name=_("Forum Team"),
           help=_("List of all forum team members"),
           icon='user',
           model=User,
           actions=[
                    {
                     'id': 'list',
                     'name': _("Forum Team Members"),
                     'help': _("List of all forum team members"),
                     'route': 'admin_team'
                     },
                    ],
           route='admin_team',
           urlpatterns=patterns('misago.team.views',
                    url(r'^$', 'List', name='admin_team'),
                ),
           ),
"""
