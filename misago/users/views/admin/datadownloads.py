from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.users.datadownload import expire_user_data_download
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
    selection_label = _('With data downloads: 0')
    empty_selection_label = _('Select data downloads')
    mass_actions = [
        {
            'action': 'expire',
            'name': _("Expire downloads"),
            'icon': 'fa fa-ban',
            'confirmation': _("Are you sure you want to set selected data downloads as expired?"),
        },
        {
            'action': 'delete',
            'name': _("Delete downloads"),
            'icon': 'fa fa-times-circle',
            'confirmation': _("Are you sure you want to delete selected data downloads?"),
        },
    ]

    def get_queryset(self):
        qs = super(DataDownloadsList, self).get_queryset()
        return qs.select_related('user', 'requester')
        
    def get_search_form(self, request):
        return SearchDataDownloadsForm

    def action_expire(self, request, data_downloads):
        for data_download in data_downloads:
            expire_user_data_download(data_download)

        messages.success(request, _("Selected data downloads have been set as expired."))

    def action_delete(self, request, data_downloads):
        for data_download in data_downloads:
            data_download.delete()

        messages.success(request, _("Selected data downloads have been deleted."))
