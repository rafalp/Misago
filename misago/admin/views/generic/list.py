from urllib import urlencode
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect
from misago.core.exceptions import ExplicitFirstPage
from misago.admin.views.generic.base import AdminView


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

    def paginate_items(self, context, page):
        try:
            page = int(page)
            if page == 1:
                raise ExplicitFirstPage()
            elif page == 0:
                page = 1
        except ValueError:
            page_no = 1

        context['paginator'] = Paginator(context['items'],
                                         self.items_per_page,
                                         allow_empty_first_page=True)
        context['page'] = context['paginator'].page(page)
        context['items'] = context['page'].object_list

    """
    Filter list items
    """
    @property
    def filters_token(self):
        return '%s:filters' % self.root_link

    def search_form(self, request, context):
        pass

    def filter_items(self, context):
        pass

    """
    Order list items
    """
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
        for order_by, name in self.ordering:
            if order_by == new_ordering:
                return order_by
        else:
            return None

    def get_ordering_methods(self, request):
        methods = {
            'GET': self.get_ordering_from_GET(request),
            'session': self.get_ordering_from_session(request),
            'default': self.clean_ordering(self.ordering[0][0]),
        }

        if methods['GET'] and methods['GET'] != methods['session']:
            request.session[self.ordering_session_key] = methods['GET']

        return methods

    def get_ordering_method(self, methods):
        for method in ('GET', 'session', 'default'):
            if methods.get(method):
                return methods.get(method)

    def order_items(self, method, context):
        for order_by, name in self.ordering:
            order_as_dict = {
                'type': 'desc' if order_by[0] == '-' else 'asc',
                'order_by': order_by,
                'name': name,
            }

            if order_by == method:
                context['order'] = order_as_dict
                context['items'] = context['items'].order_by(
                    order_as_dict['order_by'])
            elif order_as_dict['name']:
                if order_as_dict['type'] == 'desc':
                    order_as_dict['order_by'] = order_as_dict['order_by'][1:]
                context['order_by'].append(order_as_dict)

    """
    Dispatch response
    """
    def make_querystrings(self, request, context):
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
            context['querystring'] = '?%s' % urlencode(values)
        if order_values:
            context['querystring_order'] = '?%s' % urlencode(order_values)
        if filter_values:
            context['querystring_filter'] = '?%s' % urlencode(filter_values)

    def dispatch(self, request, *args, **kwargs):
        active_filters = request.session.get(self.filters_token, None)
        extra_actions_list = self.extra_actions or []

        set_querystring = False

        context = {
            'items': self.get_queryset(),
            'paginator': None,
            'page': None,
            'order_by': [],
            'order': None,
            'search_form': None,
            'active_filters': active_filters,
            'querystring': '',
            'querystring_order': '',
            'querystring_filter': '',
            'extra_actions': extra_actions_list,
            'extra_actions_len': len(extra_actions_list),
        }

        if self.ordering:
            ordering_methods = self.get_ordering_methods(request)
            current_method = self.get_ordering_method(ordering_methods)
            self.order_items(current_method, context)

            if context['order_by'] and not ordering_methods.get('GET'):
                set_querystring = True

        self.search_form(request, context)
        if active_filters:
            self.filter_items(context)

        if self.items_per_page:
            self.paginate_items(context, kwargs.get('page', 0))

        self.make_querystrings(request, context)
        if set_querystring:
            return redirect('%s%s' % (request.path, context['querystring']))

        return self.render(request, context)
