from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from ....admin.views import generic
from ...datadownloads import (
    expire_user_data_download,
    request_user_data_download,
    user_has_data_download_request,
)
from ...models import DataDownload
from ..forms import RequestDataDownloadsForm, FilterDataDownloadsForm


class DataDownloadAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:users:data-downloads:index"
    templates_dir = "misago/admin/datadownloads"
    model = DataDownload


class DataDownloadsList(DataDownloadAdmin, generic.ListView):
    items_per_page = 30
    ordering = [("-id", _("From newest")), ("id", _("From oldest"))]
    selection_label = _("With data downloads: 0")
    empty_selection_label = _("Select data downloads")
    mass_actions = [
        {
            "action": "expire",
            "name": _("Expire downloads"),
            "confirmation": _(
                "Are you sure you want to set selected data downloads as expired?"
            ),
        },
        {
            "action": "delete",
            "name": _("Delete downloads"),
            "confirmation": _(
                "Are you sure you want to delete selected data downloads?"
            ),
        },
    ]
    filter_form = FilterDataDownloadsForm

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("user", "requester")

    def action_expire(self, request, data_downloads):
        for data_download in data_downloads:
            expire_user_data_download(data_download)

        messages.success(
            request, _("Selected data downloads have been set as expired.")
        )

    def action_delete(self, request, data_downloads):
        for data_download in data_downloads:
            data_download.delete()

        messages.success(request, _("Selected data downloads have been deleted."))


class RequestDataDownloads(DataDownloadAdmin, generic.FormView):
    form_class = RequestDataDownloadsForm

    def handle_form(self, form, request):
        for user in form.cleaned_data["users"]:
            if not user_has_data_download_request(user):
                request_user_data_download(user, requester=request.user)

        messages.success(
            request, _("Data downloads have been requested for specified users.")
        )
