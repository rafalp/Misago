from django import forms
from django.utils.translation import pgettext_lazy

from ..search import search_queryset


class FilterSearchLogsForm(forms.Form):
    search_query = forms.CharField(
        label=pgettext_lazy("admin search logs filter form", "Search query contains"),
        required=False,
    )
    ip_address = forms.CharField(
        label=pgettext_lazy("admin search logs filter form", "IP address"),
        required=False,
    )

    def filter_queryset(self, criteria, queryset):
        if search_query := criteria.get("search_query"):
            queryset = queryset.filter(search_query__icontains=search_query)
        if ip_address := criteria.get("ip_address"):
            queryset = search_queryset(
                queryset, "ip_address", ip_address, case_sensitive=True
            )
        return queryset
