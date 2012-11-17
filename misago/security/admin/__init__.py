from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.security.models import QATest

ADMIN_ACTIONS=(
   AdminAction(
               section='system',
               id='qa',
               name=_("Q&A Tests"),
               help=_("Question & Answer Tests"),
               icon='question-sign',
               model=QATest,
               actions=[
                        {
                         'id': 'list',
                         'icon': 'list-alt',
                         'name': _("Browse Tests"),
                         'help': _("Browse all Question & Answer Tests"),
                         'route': 'admin_qa'
                         },
                        {
                         'id': 'new',
                         'icon': 'plus',
                         'name': _("New Test"),
                         'help': _("Crete new Q&A Test"),
                         'route': 'admin_qa_new'
                         },
                        ],
               route='admin_qa',
               urlpatterns=patterns('misago.security.admin.qatest.views',
                        url(r'^$', 'List', name='admin_qa'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_qa'),
                        url(r'^new/$', 'New', name='admin_qa_new'),
                        url(r'^edit/(?P<slug>([a-zA-Z0-9]|-)+)\.(?P<target>\d+)/$', 'Edit', name='admin_qa_edit'),
                        url(r'^delete/(?P<slug>([a-zA-Z0-9]|-)+)\.(?P<target>\d+)/$', 'Delete', name='admin_qa_delete'),
                    ),
               after='settings',
               ),
   AdminAction(
               section='system',
               id='api',
               name=_("API Keys"),
               help=_("Connect other apps with your forums"),
               icon='barcode',
               route='admin_api',
               urlpatterns=patterns('misago.security.admin.views',
                        url(r'^$', 'api_list', name='admin_api'),
                    ),
               ),
)