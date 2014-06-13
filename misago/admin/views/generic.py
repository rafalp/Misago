from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from misago.core.exceptions import ExplicitFirstPage
from misago.admin import site
from misago.admin.views import render


class AdminBaseMixin(object):
    """
    Admin mixin abstraciton used for configuring admin CRUD views.

    Takes following attributes:

    Model = Model instance
    root_link = name of link leading to root action (eg. list of all items
    templates_dir = directory with templates
    message_404 = string used in "requested item not found" messages
    """
    Model = None
    root_link = None
    templates_dir = None
    message_404 = None

    def get_model(self):
        """
        Basic method for retrieving Model, used in cases such as User model.
        """
        return self.Model


class AdminView(View):
    def final_template(self):
        return '%s/%s' % (self.templates_dir, self.template)

    def current_link(self, request):
        matched_url = request.resolver_match.url_name
        return '%s:%s' % (request.resolver_match.namespace, matched_url)

    def process_context(self, request, context):
        """
        Simple hook for extending and manipulating template context.
        """
        return context

    def render(self, request, context=None):
        context = context or {}

        context['root_link'] = self.root_link
        context['current_link'] = self.current_link(request)

        context = self.process_context(request, context)

        return render(request, self.final_template(), context)


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

    def set_filters(self, request):
        pass

    def filter_items(self, request, context):
        context['is_filtering'] = False

    def ordering_session_key(self):
        return 'misago_admin_%s_order_by' % self.root_link

    def set_ordering(self, request, new_order):
        for order_by, name in self.ordering:
            if order_by == new_order:
                request.session[self.ordering_session_key()] = order_by
                return redirect(self.current_link(request))
        else:
            messages.error(request, _("New sorting method is incorrect."))
            raise ValueError()

    def order_items(self, request, context):
        current_ordering = request.session.get(self.ordering_session_key())

        for order_by, name in self.ordering:
            order_as_dict = {
                'order_by': order_by,
                'type': 'desc' if order_by[0] == '-' else 'asc',
                'name': name,
            }

            if order_by == current_ordering:
                context['order'] = order_as_dict
                context['items'] = context['items'].order_by(
                    order_as_dict['order_by'])
            else:
                context['order_by'].append(order_as_dict)

        if not context['order']:
            current_ordering = context['order_by'].pop(0)
            context['order'] = current_ordering
            context['items'] = context['items'].order_by(
                current_ordering['order_by'])

    def dispatch(self, request, *args, **kwargs):
        extra_actions_list = self.extra_actions or []

        context = {
            'items': self.get_queryset(),
            'paginator': None,
            'page': None,
            'order_by': [],
            'order': None,
            'extra_actions': extra_actions_list,
            'extra_actions_len': len(extra_actions_list),
        }

        if self.ordering:
            if request.method == 'POST' and 'order_by' in request.POST:
                try:
                    return self.set_ordering(request,
                                             request.POST.get('order_by'))
                except ValueError:
                    pass
            self.order_items(request, context)

        if self.items_per_page:
            self.paginate_items(context, kwargs.get('page', 0))

        return self.render(request, context)


class TargetedView(AdminView):
    def check_permissions(self, request, target):
        pass

    def get_target(self, kwargs):
        if len(kwargs) == 1:
            select_for_update = self.get_model().objects.select_for_update()
            return select_for_update.get(pk=kwargs[kwargs.keys()[0]])
        else:
            return self.get_model()()

    def get_target_or_none(self, request, kwargs):
        try:
            return self.get_target(kwargs)
        except self.get_model().DoesNotExist:
            return None

    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            target = self.get_target_or_none(request, kwargs)
            if not target:
                messages.error(request, self.message_404)
                return redirect(self.root_link)

            error = self.check_permissions(request, target)
            if error:
                messages.error(request, error)
                return redirect(self.root_link)

            return self.real_dispatch(request, target)

    def real_dispatch(self, request, target):
        pass


class FormView(TargetedView):
    Form = None
    template = 'form.html'

    def create_form_type(self, request):
        return self.Form

    def initialize_form(self, FormType, request):
        if request.method == 'POST':
            return FormType(request.POST, request.FILES)
        else:
            return FormType()

    def handle_form(self, form, request):
        raise NotImplementedError(
            "You have to define your own handle_form method to handle "
            "form submissions.")

    def real_dispatch(self, request, target):
        FormType = self.create_form_type(request)
        form = self.initialize_form(FormType, request)

        if request.method == 'POST' and form.is_valid():
            response = self.handle_form(form, request)

            if response:
                return response
            elif 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(request, {'form': form})


class ModelFormView(FormView):
    message_submit = None

    def create_form_type(self, request, target):
        return self.Form

    def initialize_form(self, FormType, request, target):
        if request.method == 'POST':
            return FormType(request.POST, request.FILES, instance=target)
        else:
            return FormType(instance=target)

    def handle_form(self, form, request, target):
        form.instance.save()
        if self.message_submit:
            messages.success(request, self.message_submit % target.name)

    def real_dispatch(self, request, target):
        FormType = self.create_form_type(request, target)
        form = self.initialize_form(FormType, request, target)

        if request.method == 'POST' and form.is_valid():
            response = self.handle_form(form, request, target)

            if response:
                return response
            elif 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(request, {'form': form, 'target': target})


class ButtonView(TargetedView):
    def real_dispatch(self, request, target):
        if request.method == 'POST':
            new_response = self.button_action(request, target)
            if new_response:
                return new_response
        return redirect(self.root_link)

    def button_action(self, request, target):
        raise NotImplementedError("You have to define custom button_action.")
