from django.core.paginator import EmptyPage, InvalidPage


def get_page(queryset, order_by, per_page, start=0):
    if start < 0:
        raise InvalidPage()

    object_list = list(_slice_queryset(queryset, order_by, per_page, start))
    if start and not object_list:
        raise EmptyPage()

    next_cursor = None
    if len(object_list) > per_page:
        next_slice_first_item = object_list.pop(-1)
        attr_name = order_by.lstrip("-")
        next_cursor = getattr(next_slice_first_item, attr_name)

    return CursorPage(start, object_list, next_cursor)


def _slice_queryset(queryset, order_by, per_page, start):
    page_len = int(per_page) + 1
    if start:
        if order_by.startswith("-"):
            filter_name = "%s__lte" % order_by[1:]
        else:
            filter_name = "%s__gte" % order_by
        return queryset.filter(**{filter_name: start})[:page_len]
    return queryset[:page_len]


class CursorPage:
    def __init__(self, start, object_list, next_=None):
        self.start = start or 0
        self.first = self.start == 0
        self.object_list = object_list
        self.next = next_

    def __len__(self):
        return len(self.object_list)

    def has_next(self):
        return bool(self.next)
