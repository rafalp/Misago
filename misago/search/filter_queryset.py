EQUAL = 0
CONTAINS = 1
STARTS_WITH = 2
ENDS_WITH = 3


def filter_queryset(queryset, attr, search, *, case_sensitive=False):
    mode = get_mode(search)
    search = search.strip("*")

    if not search:
        return queryset

    queryset_filter = get_queryset_filter(
        attr, mode, search, case_sensitive=case_sensitive
    )
    return queryset.filter(**queryset_filter)


def get_mode(search):
    if search.startswith("*") and search.endswith("*"):
        return CONTAINS
    if search.endswith("*"):
        return STARTS_WITH
    if search.startswith("*"):
        return ENDS_WITH
    return EQUAL


def get_queryset_filter(attr, mode, search, *, case_sensitive=False):
    if mode is STARTS_WITH:
        if case_sensitive:
            return {"%s__startswith" % attr: search}
        return {"%s__istartswith" % attr: search}

    if mode is ENDS_WITH:
        if case_sensitive:
            return {"%s__endswith" % attr: search}
        return {"%s__iendswith" % attr: search}

    if mode is CONTAINS:
        if case_sensitive:
            return {"%s__contains" % attr: search}
        return {"%s__icontains" % attr: search}

    if case_sensitive:
        return {attr: search}

    return {"%s__iexact" % attr: search}
