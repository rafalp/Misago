from django.core.paginator import Paginator


class PostsPaginator(Paginator):
    """paginator that returns that makes last item on page repeat as first item on next page."""

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        per_page = int(per_page) - 1
        if orphans:
            orphans += 1
        super(PostsPaginator,
              self).__init__(object_list, per_page, orphans, allow_empty_first_page)

    def page(self, number):
        """returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        if top < self.count:
            top += 1
        return self._get_page(self.object_list[bottom:top], number, self)
