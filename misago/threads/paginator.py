from math import ceil

from django.core.paginator import Paginator, Page


class ThreadPostsPaginator(Paginator):
    def get_item_page(self, offset: int) -> int:
        item_page = ceil((offset + 1) / self.per_page)
        return min(item_page, self.num_pages)

    def page(self, number) -> "ThreadPostsPaginatorPage":
        number = self.validate_number(number)

        next_page_first_item = None
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
            object_list = self.object_list[bottom:top]
        elif number == self.num_pages:
            object_list = self.object_list[bottom:top]
        else:
            object_list = list(self.object_list[bottom : top + 1])
            object_list, next_page_first_item = object_list[:-1], object_list[-1]

        return ThreadPostsPaginatorPage(object_list, next_page_first_item, number, self)


class ThreadPostsPaginatorPage(Page):
    def __init__(self, object_list, next_page_first_item, number, paginator):
        self.object_list = object_list
        self.next_page_first_item = next_page_first_item
        self.number = number
        self.paginator = paginator
