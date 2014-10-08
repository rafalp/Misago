from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


__all__ = ['ForumFiltering']


class ForumFiltering(object):
    def __init__(self, forum, link_name, link_params):
        self.forum = forum
        self.link_name = link_name
        self.link_params = link_params.copy()

        self.filters = self.get_available_filters()

    def get_available_filters(self):
        filters = []

        if self.forum.acl['can_see_all_threads']:
            filters.append({
                'type': 'my-threads',
                'name': _("My threads"),
                'is_label': False,
            })

        if self.forum.acl['can_see_reports']:
            filters.append({
                'type': 'reported',
                'name': _("With reported posts"),
                'is_label': False,
            })

        if self.forum.acl['can_review_moderated_content']:
            filters.extend(({
                'type': 'moderated-threads',
                'name': _("Moderated threads"),
                'is_label': False,
            },
            {
                'type': 'moderated-posts',
                'name': _("With moderated posts"),
                'is_label': False,
            }))

        for label in self.forum.labels:
            filters.append({
                'type': label.slug,
                'name': label.name,
                'is_label': True,
                'css_class': label.css_class,
            })

        return filters

    def clean_kwargs(self, kwargs):
        show = kwargs.get('show')
        if show:
            available_filters = [method['type'] for method in self.filters]
            if show in available_filters:
                self.show = show
            else:
                kwargs.pop('show')
        else:
            self.show = None

        return kwargs

    def filter(self, threads):
        threads.filter(self.show)

    def get_filtering_dics(self):
        try:
            return self._dicts
        except AttributeError:
            self._dicts = self.create_dicts()
            return self._dicts

    def create_dicts(self):
        dicts = []

        if self.forum.acl['can_see_all_threads']:
            default_name = _("All threads")
        else:
            default_name = _("Your threads")

        self.link_params.pop('show', None)
        dicts.append({
            'type': None,
            'url': reverse(self.link_name, kwargs=self.link_params),
            'name': default_name,
            'is_label': False,
        })

        for filtering in self.filters:
            self.link_params['show'] = filtering['type']
            filtering['url'] = reverse(self.link_name, kwargs=self.link_params)
            dicts.append(filtering)

        return dicts

    @property
    def is_active(self):
        return bool(self.show)

    @property
    def current(self):
        try:
            return self._current
        except AttributeError:
            for filtering in self.get_filtering_dics():
                if filtering['type'] == self.show:
                    self._current = filtering
                    return filtering

    def choices(self):
        if self.show:
            choices = []
            for filtering in self.get_filtering_dics():
                if filtering['type'] != self.show:
                    choices.append(filtering)
            return choices
        else:
            return self.get_filtering_dics()[1:]
