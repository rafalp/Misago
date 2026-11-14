from enum import IntEnum


class SearchMode(IntEnum):
    EQUAL = 0
    CONTAINS = 1
    STARTS_WITH = 2
    ENDS_WITH = 3


def search_queryset(
    queryset, field_name: str, search_query: str, case_sensitive: bool = False
):
    mode = get_search_mode(search_query)
    search_query = search_query.strip("*")

    if not search_query:
        return queryset

    queryset_filter = get_queryset_filter(
        mode, field_name, search_query, case_sensitive
    )
    return queryset.filter(**queryset_filter)


def get_search_mode(search_query: str) -> SearchMode:
    if search_query.startswith("*") and search_query.endswith("*"):
        return SearchMode.CONTAINS
    if search_query.endswith("*"):
        return SearchMode.STARTS_WITH
    if search_query.startswith("*"):
        return SearchMode.ENDS_WITH
    return SearchMode.EQUAL


def get_queryset_filter(
    mode: SearchMode,
    field_name: str,
    search_query: str,
    case_sensitive: bool = False,
) -> dict[str, str]:
    if mode is SearchMode.STARTS_WITH:
        if case_sensitive:
            return {"%s__startswith" % field_name: search_query}
        return {"%s__istartswith" % field_name: search_query}

    if mode is SearchMode.ENDS_WITH:
        if case_sensitive:
            return {"%s__endswith" % field_name: search_query}
        return {"%s__iendswith" % field_name: search_query}

    if mode is SearchMode.CONTAINS:
        if case_sensitive:
            return {"%s__contains" % field_name: search_query}
        return {"%s__icontains" % field_name: search_query}

    if case_sensitive:
        return {field_name: search_query}

    return {"%s__iexact" % field_name: search_query}
