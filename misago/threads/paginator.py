from math import ceil

from django.core.paginator import Paginator
from django.utils.functional import cached_property


class PostsPaginator(Paginator):
    """
    Paginator that returns that makes last item on page
    repeat as first item on next page.
    """
    @cached_property
    def num_pages(self):
        """
        Returns the total number of pages.
        """
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count - self.orphans)
        hits += int(ceil(hits / float(self.per_page)))
        return int(ceil(hits / float(self.per_page)))

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        if number > 1:
            bottom -= number - 1
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self._get_page(self.object_list[bottom:top], number, self)
