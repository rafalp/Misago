from django.utils.translation import pgettext_lazy

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


class SearchLogsList(SearchLogAdmin, generic.ListView):
    items_per_page = 40
    ordering = [
        ("-id", pgettext_lazy("admin search logs ordering choice", "From newest")),
        ("id", pgettext_lazy("admin search logs ordering choice", "From oldest")),
    ]
    filter_form = FilterSearchLogsForm
