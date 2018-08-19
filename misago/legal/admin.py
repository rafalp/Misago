from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views.admin import (
    AgreementsList, DeleteAgreement, EditAgreement, NewAgreement, SetAgreementAsActive
)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # Legal Agreements
        urlpatterns.namespace(r'^agreements/', 'agreements', 'users')
        urlpatterns.patterns(
            'users:agreements',
            url(r'^$', AgreementsList.as_view(), name='index'),
            url(r'^(?P<page>\d+)/$', AgreementsList.as_view(), name='index'),
            url(r'^new/$', NewAgreement.as_view(), name='new'),
            url(r'^edit/(?P<pk>\d+)/$', EditAgreement.as_view(), name='edit'),
            url(r'^delete/(?P<pk>\d+)/$', DeleteAgreement.as_view(), name='delete'),
            url(r'^set-as-active/(?P<pk>\d+)/$', SetAgreementAsActive.as_view(), name='set-as-active'),
        )
        
    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Agreements"),
            icon='fa fa-check-square-o',
            parent='misago:admin:users',
            after='misago:admin:users:data-downloads:index',
            namespace='misago:admin:users:agreements',
            link='misago:admin:users:agreements:index',
        )