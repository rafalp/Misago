from django.core.paginator import EmptyPage, InvalidPage


class CursorPaginator:
    def __init__(self, queryset, order_by, per_page):
        self.queryset = queryset
        self.per_page = int(per_page)

        if order_by.startswith("-"):
            self.order_by = order_by[1:]
            self.desc = True
        else:
            self.order_by = order_by
            self.desc = False

    def get_page(self, start=0):
        if start < 0:
            raise InvalidPage()

        object_list = list(self._get_slice(start))
        if start and not object_list:
            raise EmptyPage()

        next_cursor = None
        if len(object_list) > self.per_page:
            next_slice_first_item = object_list.pop(-1)
            next_cursor = getattr(next_slice_first_item, self.order_by)

        return Page(start, object_list, next_cursor)

    def _get_slice(self, start):
        page_len = self.per_page + 1
        if start:
            print(start)
            if self.desc:
                filter_name = "%s__lte" % self.order_by
            else:
                filter_name = "%s__gte" % self.order_by
            print({filter_name: start})
            return self.queryset.filter(**{filter_name: start})[:page_len]
        return self.queryset[:page_len]


class Page:
    def __init__(self, start, object_list, next_):
        self.start = start or 0
        self.object_list = object_list
        self.next = next_

    def __len__(self):
        return len(self.object_list)

    def has_next(self):
        return bool(self.next)
