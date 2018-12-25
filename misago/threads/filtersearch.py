from django.utils.module_loading import import_string

from ..conf import settings

filters_list = settings.MISAGO_POST_SEARCH_FILTERS
SEARCH_FILTERS = list(map(import_string, filters_list))


def filter_search(search, filters=None):
    filters = filters or SEARCH_FILTERS
    for search_filter in filters:
        search = search_filter(search) or search
    return search
