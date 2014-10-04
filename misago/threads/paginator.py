from django.core.paginator import Paginator as DjangoPaginator, Page, EmptyPage
from django.http import Http404


class Paginator(DjangoPaginator):
    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.

        If its not last page, it will also contain one element of last page
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        else:
            top += 1
        return self._get_page(self.object_list[bottom:top], number, self)

    def _get_page(self, *args, **kwargs):
        page = Page(*args, **kwargs)
        if page.has_next():
           page.next_page_first_item = page[-1]
           page.object_list = page.object_list[:-1]
        else:
           page.next_page_first_item = None
        return page


def paginate(object_list, page, per_page, orphans=0):
    from misago.core.exceptions import ExplicitFirstPage

    if page in (1, "1"):
        raise ExplicitFirstPage()
    elif not page:
        page = 1

    try:
        return Paginator(
            object_list, per_page, orphans=orphans,
            allow_empty_first_page=False).page(page)
    except EmptyPage:
        raise Http404()
