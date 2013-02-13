from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.themes.models import ThemeAdjustment

ADMIN_ACTIONS = (
   AdminAction(
               section='system',
               id='settings',
               name=_("Settings"),
               help=_("Change your forum configuration"),
               icon='wrench',
               route='admin_settings',
               urlpatterns=patterns('misago.settings.views',
                        url(r'^$', 'settings', name='admin_settings'),
                        url(r'^search/$', 'settings_search', name='admin_settings_search'),
                        url(r'^(?P<group_slug>([a-z0-9]|-)+)-(?P<group_id>\d+)/$', 'settings', name='admin_settings')
                    ),
               ),
   AdminAction(
               section='system',
               id='clients',
               name=_("Clients"),
               help=_("Adjust presentation layer to clients"),
               icon='tint',
               model=ThemeAdjustment,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Browse Clients"),
                         'help': _("Browse all existing clients"),
                         'route': 'admin_clients'
                         },
                        {
                         'id': 'new',
                         'name': _("Add New Adjustment"),
                         'help': _("Create new client adjustment"),
                         'route': 'admin_clients_new'
                         },
                        ],
               route='admin_clients',
               urlpatterns=patterns('misago.themes.views',
                        url(r'^$', 'List', name='admin_clients'),
                        url(r'^new/$', 'New', name='admin_clients_new'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_clients_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_clients_delete'),
                    ),
               ),
)
