from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.threads.views.generic.threads import ThreadsFiltering


__all__ = ['ForumFiltering']


class ForumFiltering(ThreadsFiltering):
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
