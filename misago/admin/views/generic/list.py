from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.six.moves.urllib.parse import urlencode
from django.utils.translation import ugettext_lazy as _

from misago.core.exceptions import ExplicitFirstPage

from .base import AdminView


class MassActionError(Exception):
    pass


class ListView(AdminView):
    """
    Admin items list view

    Uses following attributes:

    template = template name used to render items list
    items_per_page = number of items displayed on single page
                     (enter 0 or don't define for no pagination)
    ordering = tuple of tuples defining allowed orderings
               typles should follow this format: (name, order_by)
    """
    template = 'list.html'

    items_per_page = 0
    ordering = None

    extra_actions = None
    mass_actions = None

    selection_label = _('Selected: 0')
    empty_selection_label = _('Select items')

    @classmethod
    def add_mass_action(cls, action, name, icon, confirmation=None):
        if not cls.mass_actions:
            cls.mass_actions = []

        cls.extra_actions.append({
            'action': action,
            'name': name,
            'icon': icon,
            'confirmation': confirmation
        })

    @classmethod
    def add_item_action(cls, name, icon, link, style=None):
        if not cls.extra_actions:
            cls.extra_actions = []

        cls.extra_actions.append({
            'name': name,
            'icon': icon,
            'link': link,
            'style': style,
        })

    def get_queryset(self):
        return self.get_model().objects.all()

    def dispatch(self, request, *args, **kwargs):
        mass_actions_list = self.mass_actions or []
        extra_actions_list = self.extra_actions or []

        refresh_querystring = False

        context = {
            'items': self.get_queryset(),
            'paginator': None,
            'page': None,
            'order_by': [],
            'order': None,
            'search_form': None,
            'active_filters': {},
            'querystring': '',
            'query_order': {},
            'query_filters': {},
            'selected_items': [],
            'selection_label': self.selection_label,
            'empty_selection_label': self.empty_selection_label,
            'mass_actions': mass_actions_list,
            'extra_actions': extra_actions_list,
            'extra_actions_len': len(extra_actions_list),
        }

        if request.method == 'POST' and mass_actions_list:
            try:
                response = self.handle_mass_action(request, context)
                if response:
                    return response
                else:
                    return redirect(request.path_info)
            except MassActionError as e:
                messages.error(request, e.args[0])

        if self.ordering:
            ordering_methods = self.get_ordering_methods(request)
            used_method = self.get_ordering_method_to_use(ordering_methods)
            self.set_ordering_in_context(context, used_method)

            if (ordering_methods['GET'] and ordering_methods['GET'] != ordering_methods['session']):
                # Store GET ordering in session for future requests
                session_key = self.ordering_session_key
                request.session[session_key] = ordering_methods['GET']

            if context['order_by'] and not ordering_methods['GET']:
                # Make view redirect to itself with querystring,
                # So address ball contains copy-friendly link
                refresh_querystring = True

        SearchForm = self.get_search_form(request)
        if SearchForm:
            filtering_methods = self.get_filtering_methods(request)
            active_filters = self.get_filtering_method_to_use(filtering_methods)
            if request.GET.get('clear_filters'):
                # Clear filters from querystring
                request.session.pop(self.filters_session_key, None)
                active_filters = {}
            self.apply_filtering_on_context(context, active_filters, SearchForm)

            if (filtering_methods['GET'] and
                    filtering_methods['GET'] != filtering_methods['session']):
                # Store GET filters in session for future requests
                session_key = self.filters_session_key
                request.session[session_key] = filtering_methods['GET']
            if request.GET.get('set_filters'):
                # Force store filters in session
                session_key = self.filters_session_key
                request.session[session_key] = context['active_filters']
                refresh_querystring = True

            if context['active_filters'] and not filtering_methods['GET']:
                # Make view redirect to itself with querystring,
                # so address bar contains copy-friendly link
                refresh_querystring = True

        self.make_querystring(context)

        if self.items_per_page:
            try:
                self.paginate_items(context, kwargs.get('page', 0))
            except EmptyPage:
                return redirect('%s%s' % (reverse(self.root_link), context['querystring']))

        if refresh_querystring and not request.GET.get('redirected'):
            return redirect('%s%s' % (request.path_info, context['querystring']))

        return self.render(request, context)

    def paginate_items(self, context, page):
        try:
            page = int(page)
            if page == 1:
                raise ExplicitFirstPage()
            elif page == 0:
                page = 1
        except ValueError:
            page = 1

        context['paginator'] = Paginator(
            context['items'], self.items_per_page, allow_empty_first_page=True
        )
        context['page'] = context['paginator'].page(page)
        context['items'] = context['page'].object_list

    # Filter list items
    search_form = None

    def get_search_form(self, request):
        return self.search_form

    @property
    def filters_session_key(self):
        return 'misago_admin_%s_filters' % self.root_link

    def get_filters_from_GET(self, search_form, request):
        form = search_form(request.GET)
        form.is_valid()
        return self.clean_filtering_data(form.cleaned_data)

    def get_filters_from_session(self, search_form, request):
        session_filters = request.session.get(self.filters_session_key, {})
        form = search_form(session_filters)
        form.is_valid()
        return self.clean_filtering_data(form.cleaned_data)

    def clean_filtering_data(self, data):
        for key, value in list(data.items()):
            if not value:
                del data[key]
        return data

    def get_filtering_methods(self, request):
        SearchForm = self.get_search_form(request)
        methods = {
            'GET': self.get_filters_from_GET(SearchForm, request),
            'session': self.get_filters_from_session(SearchForm, request),
        }

        if request.GET.get('set_filters'):
            methods['session'] = {}

        return methods

    def get_filtering_method_to_use(self, methods):
        for method in ('GET', 'session'):
            if methods.get(method):
                return methods.get(method)
        else:
            return {}

    def apply_filtering_on_context(self, context, active_filters, search_form):
        context['active_filters'] = active_filters
        context['search_form'] = search_form(initial=context['active_filters'])

        if context['active_filters']:
            context['items'] = context['search_form'].filter_queryset(
                active_filters, context['items']
            )

    # Order list items
    @property
    def ordering_session_key(self):
        return 'misago_admin_%s_order_by' % self.root_link

    def get_ordering_from_GET(self, request):
        sort = request.GET.get('sort')

        if request.GET.get('direction') == 'desc':
            new_ordering = '-%s' % sort
        elif request.GET.get('direction') == 'asc':
            new_ordering = sort
        else:
            new_ordering = '?nope'

        return self.clean_ordering(new_ordering)

    def get_ordering_from_session(self, request):
        new_ordering = request.session.get(self.ordering_session_key)
        return self.clean_ordering(new_ordering)

    def clean_ordering(self, new_ordering):
        for order_by, _ in self.ordering:
            if order_by == new_ordering:
                return order_by
        else:
            return None

    def get_ordering_methods(self, request):
        return {
            'GET': self.get_ordering_from_GET(request),
            'session': self.get_ordering_from_session(request),
            'default': self.clean_ordering(self.ordering[0][0]),
        }

    def get_ordering_method_to_use(self, methods):
        for method in ('GET', 'session', 'default'):
            if methods.get(method):
                return methods.get(method)

    def set_ordering_in_context(self, context, method):
        for order_by, name in self.ordering:
            order_as_dict = {
                'type': 'desc' if order_by[0] == '-' else 'asc',
                'order_by': order_by,
                'name': name,
            }

            if order_by == method:
                context['order'] = order_as_dict
                context['items'] = context['items'].order_by(order_as_dict['order_by'])
            elif order_as_dict['name']:
                if order_as_dict['type'] == 'desc':
                    order_as_dict['order_by'] = order_as_dict['order_by'][1:]
                context['order_by'].append(order_as_dict)

    # Mass actions
    def handle_mass_action(self, request, context):
        limit = self.items_per_page or 64
        action = self.select_mass_action(request.POST.get('action'))
        items = [x for x in request.POST.getlist('selected_items')[:limit]]

        context['selected_items'] = items
        if not context['selected_items']:
            raise MassActionError(_("You have to select one or more items."))

        action_queryset = context['items'].filter(pk__in=items)

        if not action_queryset.exists():
            raise MassActionError(_("You have to select one or more items."))

        action_callable = getattr(self, 'action_%s' % action['action'])

        if action.get('is_atomic', True):
            with transaction.atomic():
                return action_callable(request, action_queryset)
        else:
            return action_callable(request, action_queryset)

    def select_mass_action(self, action):
        for definition in self.mass_actions:
            if definition['action'] == action:
                return definition
        else:
            raise MassActionError(_("Action is not allowed."))

    # Querystring builder
    def make_querystring(self, context):
        values = {}
        filter_values = {}
        order_values = {}

        if context['active_filters']:
            filter_values = context['active_filters']
            values.update(filter_values)

        if context['order_by']:
            order_values = {
                'sort': context['order']['order_by'],
                'direction': context['order']['type'],
            }

            if order_values['sort'][0] == '-':
                # We don't start sorting criteria with minus in querystring
                order_values['sort'] = order_values['sort'][1:]

            values.update(order_values)

        if values:
            values['redirected'] = 1
            context['querystring'] = '?%s' % urlencode(values, 'utf-8')
        if order_values:
            context['query_order'] = order_values
        if filter_values:
            context['query_filters'] = filter_values
