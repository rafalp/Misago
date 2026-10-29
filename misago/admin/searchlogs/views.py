import csv

from django.http import HttpRequest, StreamingHttpResponse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import pgettext_lazy

from ...core.utils import slugify
from ...search.models import SearchLog
from ..views import generic
from .forms import FilterSearchLogsForm


class SearchLogAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:searchlogs:index"
    model = SearchLog
    templates_dir = "misago/admin/searchlogs"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_public=True).prefetch_related("user")


class ListView(SearchLogAdmin, generic.ListView):
    items_per_page = 40
    ordering = [
        ("-id", pgettext_lazy("admin search logs ordering choice", "From newest")),
        ("id", pgettext_lazy("admin search logs ordering choice", "From oldest")),
    ]
    filter_form = FilterSearchLogsForm


class EchoBuffer:
    def write(self, value: str) -> str:
        return value


class DownloadView(SearchLogAdmin, generic.AdminView):
    def post(self, request: HttpRequest) -> StreamingHttpResponse:
        filename = self.get_filename()
        queryset = self.get_queryset()

        pseudo_buffer = EchoBuffer()
        csv_writer = csv.writer(pseudo_buffer)

        def generate_csv():
            yield csv_writer.writerow(
                [
                    "Search",
                    "Searched",
                    "User",
                    "IP address",
                ]
            )

            for search_query, searched_at, username, ip_address in queryset:
                yield csv_writer.writerow(
                    [
                        search_query,
                        searched_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        username or "",
                        ip_address,
                    ]
                )

        response = StreamingHttpResponse(
            generate_csv(),
            content_type="text/csv",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .values_list("search_query", "searched_at", "user__username", "ip_address")
            .iterator(chunk_size=100)
        )

    def get_filename(self) -> str:
        timestamp = slugify(timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        return f"search-logs-{timestamp}.csv"
