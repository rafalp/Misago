from django.contrib import messages
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ...datadownloads import (
    expire_user_data_download,
    request_user_data_download,
    user_has_data_download_request,
)
from ...models import DataDownload
from ..forms.datadownloads import RequestDataDownloadsForm, FilterDataDownloadsForm


class DataDownloadAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:users:data-downloads:index"
    templates_dir = "misago/admin/datadownloads"
    model = DataDownload


class DataDownloadsList(DataDownloadAdmin, generic.ListView):
    items_per_page = 30
    ordering = [
        ("-id", pgettext_lazy("admin data downloads ordering choice ", "From newest")),
        ("id", pgettext_lazy("admin data downloads ordering choice ", "From oldest")),
    ]
    selection_label = pgettext_lazy("admin data downloads", "With data downloads: 0")
    empty_selection_label = pgettext_lazy(
        "admin data downloads", "Select data downloads"
    )
    mass_actions = [
        {
            "action": "expire",
            "name": pgettext_lazy("admin data downloads", "Expire downloads"),
            "confirmation": pgettext_lazy(
                "admin data downloads",
                "Are you sure you want to set selected data downloads as expired?",
            ),
        },
        {
            "action": "delete",
            "name": pgettext_lazy("admin data downloads", "Delete downloads"),
            "confirmation": pgettext_lazy(
                "admin data downloads",
                "Are you sure you want to delete selected data downloads?",
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
            request,
            pgettext(
                "admin data downloads",
                "Selected data downloads have been set as expired.",
            ),
        )

    def action_delete(self, request, data_downloads):
        for data_download in data_downloads:
            data_download.delete()

        messages.success(
            request,
            pgettext(
                "admin data downloads", "Selected data downloads have been deleted."
            ),
        )


class RequestDataDownloads(DataDownloadAdmin, generic.FormView):
    form_class = RequestDataDownloadsForm

    def handle_form(self, form, request):
        for user in form.cleaned_data["users"]:
            if not user_has_data_download_request(user):
                request_user_data_download(user, requester=request.user)

        messages.success(
            request,
            pgettext(
                "admin data downloads",
                "Data downloads have been requested for specified users.",
            ),
        )
