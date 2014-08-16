from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from misago.threads.views.prefixesadmin import (PrefixesList, NewPrefix,
                                                EditPrefix, DeletePrefix)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # Threads Prefixes
        urlpatterns.namespace(r'^prefixes/', 'prefixes', 'forums')
        urlpatterns.patterns('forums:prefixes',
            url(r'^$', PrefixesList.as_view(), name='index'),
            url(r'^new/$', NewPrefix.as_view(), name='new'),
            url(r'^edit/(?P<prefix_id>\d+)/$', EditPrefix.as_view(), name='edit'),
            url(r'^delete/(?P<prefix_id>\d+)/$', DeletePrefix.as_view(), name='delete'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(name=_("Thread prefixes"),
                      icon='fa fa-tags',
                      parent='misago:admin:forums',
                      after='misago:admin:forums:nodes:index',
                      namespace='misago:admin:forums:prefixes',
                      link='misago:admin:forums:prefixes:index')
