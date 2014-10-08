from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


__all__ = ['Sorting']


class Sorting(object):
    sortings = (
        {
            'method': 'recently-replied',
            'name': _("Recently replied"),
            'order_by': '-last_post_on',
        },
        {
            'method': 'last-replied',
            'name': _("Last replied"),
            'order_by': 'last_post_on',
        },
        {
            'method': 'most-replied',
            'name': _("Most replied"),
            'order_by': '-replies',
        },
        {
            'method': 'least-replied',
            'name': _("Least replied"),
            'order_by': 'replies',
        },
        {
            'method': 'newest',
            'name': _("Newest"),
            'order_by': '-id',
        },
        {
            'method': 'oldest',
            'name': _("Oldest"),
            'order_by': 'id',
        },
    )

    def __init__(self, link_name, link_params):
        self.link_name = link_name
        self.link_params = link_params.copy()

        self.default_method = self.sortings[0]['method']

    def clean_kwargs(self, kwargs):
        sorting = kwargs.get('sort')

        if sorting:
            if sorting == self.default_method:
                kwargs.pop('sort')
                return kwargs

            available_sortings = [method['method'] for method in self.sortings]
            if sorting not in available_sortings:
                kwargs.pop('sort')
                return kwargs
        else:
            sorting = self.default_method

        self.set_sorting(sorting)
        return kwargs

    def set_sorting(self, method):
        for sorting in self.sortings:
            if sorting['method'] == method:
                self.sorting = sorting
                break

    @property
    def name(self):
        return self.sorting['name']

    def choices(self):
        choices = []
        for sorting in self.sortings:
            if sorting['method'] != self.sorting['method']:
                if sorting['method'] == self.default_method:
                    self.link_params.pop('sort', None)
                else:
                    self.link_params['sort'] = sorting['method']

                url = reverse(self.link_name, kwargs=self.link_params)
                choices.append({
                    'name': sorting['name'],
                    'url': url,
                })
        return choices

    def sort(self, threads):
        threads.sort(self.sorting['order_by'])
