from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.core.shortcuts import paginate
from misago.readtracker import threadstracker

from misago.threads.models import Label
from misago.threads.moderation import ModerationError
from misago.threads.views.generic.base import ViewBase


__all__ = ['Actions', 'Sorting', 'Threads', 'ThreadsView']


class Actions(object):
    select_threads_message = ugettext_lazy(
        "You have to select at least one thread")

    def __init__(self, **kwargs):
        if kwargs.get('user').is_authenticated():
            self.available_actions = self.get_available_actions(kwargs)
        else:
            self.available_actions = []
        self.selected_ids = []

    def get_available_actions(self, kwargs):
        raise NotImplementedError("get_available_actions has to return list "
                                  "of dicts with allowed actions")

    def resolve_action(self, request):
        action_name = request.POST.get('action')
        if ':' in action_name:
            action_bits = action_name.split(':')
            action_name = action_bits[0]
            action_arg = action_bits[1]
        else:
            action_arg = None

        for action in self.available_actions:
            if action['action'] == action_name:
                action_callable = 'action_%s' % action_name
                return getattr(self, action_callable), action_arg
        else:
            raise ModerationError(_("Requested action is invalid."))

    def clean_selection(self, data):
        filtered_data = []
        for pk in data[:50]: # a tiny fail-safe to avoid too big workloads
            try:
                filtered_data.append(int(pk))
            except ValueError:
                pass

        if not filtered_data:
            raise ModerationError(self.select_threads_message)

        return filtered_data

    def handle_post(self, request, queryset):
        try:
            action, action_arg = self.resolve_action(request)
            self.selected_ids = self.clean_selection(
                request.POST.getlist('thread', []))

            filtered_queryset = queryset.filter(pk__in=self.selected_ids)
            if filtered_queryset.exists():
                if action_arg:
                    response = action(request, filtered_queryset, action_arg)
                else:
                    response = action(request, filtered_queryset)
                if response:
                    return response
                else:
                    # prepare default response: page reload
                    return redirect(request.path)
            else:
                raise ModerationError(self.select_threads_message)
        except ModerationError as e:
            messages.error(request, e.message)
            return False

    def get_list(self):
        return self.available_actions

    def get_selected_ids(self):
        return self.selected_ids


class Sorting(object):
    sortings = (
        {
            'method': 'recently-replied',
            'name': ugettext_lazy("Recently replied"),
            'order_by': '-last_post_on',
        },
        {
            'method': 'last-replied',
            'name': ugettext_lazy("Last replied"),
            'order_by': 'last_post_on',
        },
        {
            'method': 'most-replied',
            'name': ugettext_lazy("Most replied"),
            'order_by': '-replies',
        },
        {
            'method': 'least-replied',
            'name': ugettext_lazy("Least replied"),
            'order_by': 'replies',
        },
        {
            'method': 'newest',
            'name': ugettext_lazy("Newest"),
            'order_by': '-id',
        },
        {
            'method': 'oldest',
            'name': ugettext_lazy("Oldest"),
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


class Threads(object):
    def __init__(self, user):
        self.user = user

    def sort(self, sort_by):
        self.queryset = self.queryset.order_by(sort_by)

    def label_threads(self, threads, labels=None):
        if labels:
            labels_dict = dict([(label.pk, label) for label in labels])
        else:
            labels_dict = Label.objects.get_cached_labels_dict()

        for thread in threads:
            thread.label = labels_dict.get(thread.label_id)

    def make_threads_read_aware(self, threads):
        threadstracker.make_read_aware(self.user, threads)


class ThreadsView(ViewBase):
    def get_threads(self, request, kwargs):
        queryset = self.get_threads_queryset(request, forum)
        queryset = threads_qs.order_by('-last_post_id')

        page = paginate(threads_qs, kwargs.get('page', 0), 30, 10)
        threads = [thread for thread in page.object_list]

        return page, threads

    def get_threads_queryset(self, request):
        return forum.thread_set.all().order_by('-last_post_id')

    def clean_kwargs(self, request, kwargs):
        cleaned_kwargs = kwargs.copy()
        if request.user.is_anonymous():
            """we don't allow sort/filter for guests"""
            cleaned_kwargs.pop('sort', None)
            cleaned_kwargs.pop('show', None)
        return cleaned_kwargs
