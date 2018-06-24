from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.users.forms.admin import SearchDataDownloadsForm
from misago.users.models import DataDownload


class DataDownloadAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:data-downloads:index'
    templates_dir = 'misago/admin/datadownloads'
    model = DataDownload


class DataDownloadsList(DataDownloadAdmin, generic.ListView):
    items_per_page = 30
    ordering = [
        ('-id', _("From newest")),
        ('id', _("From oldest")),
    ]

    def get_queryset(self):
        qs = super(DataDownloadsList, self).get_queryset()
        return qs.select_related('user', 'requester')
        
    def get_search_form(self, request):
        return SearchDataDownloadsForm