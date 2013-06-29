from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from jinja2 import TemplateNotFound
import math
from misago.forms import Form, FormLayout, FormFields, FormFieldsets
from misago.messages import Message
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination

"""
Class widgets
"""
class BaseWidget(object):
    """
    Admin Widget abstract class, providing widgets with common or shared functionality
    """
    admin = None
    id = None
    fallback = None
    name = None
    help = None
    notfound_message = None

    def __new__(cls, request, **kwargs):
        obj = super(BaseWidget, cls).__new__(cls)
        if not obj.name:
            obj.name = obj.get_name()
        if not obj.help:
            obj.help = obj.get_help()
        return obj(request, **kwargs)

    def get_token(self, token):
        return '%s_%s_%s' % (self.id, token, str('%s.%s' % (self.admin.id, self.admin.model.__name__)))

    def get_url(self):
        return reverse(self.admin.get_action_attr(self.id, 'route'))

    def get_name(self):
        return self.admin.get_action_attr(self.id, 'name')

    def get_help(self):
        return self.admin.get_action_attr(self.id, 'help')

    def get_id(self):
        return 'admin_%s' % self.id

    def get_template(self):
        return ('%s/%s.html' % (self.admin.id, self.template),
                'admin/%s.html' % self.template)

    def add_template_variables(self, variables):
        return variables

    def get_fallback_url(self):
        return reverse(self.fallback)

    def get_target(self, model):
        pass

    def get_target_name(self, model):
        try:
            if self.translate_target_name:
                return _(model.__dict__[self.target_name])
            return model.__dict__[self.target_name]
        except AttributeError:
            return None

    def get_and_validate_target(self, target):
        try:
            model = self.admin.model.objects.select_related().get(pk=target)
            self.get_target(model)
            return model
        except self.admin.model.DoesNotExist:
            self.request.messages.set_flash(Message(self.notfound_message), 'error', self.admin.id)
        except ValueError as e:
            self.request.messages.set_flash(Message(e.args[0]), 'error', self.admin.id)
        return None


class ListWidget(BaseWidget):
    """
    Items list widget
    """
    actions = []
    columns = []
    sortables = {}
    default_sorting = None
    search_form = None
    is_filtering = False
    pagination = None
    template = 'list'
    hide_actions = False
    table_form_button = _('Go')
    empty_message = _('There are no items to display')
    empty_search_message = _('Search has returned no items')
    nothing_checked_message = _('You have to select at least one item.')
    prompt_select = False

    def get_item_actions(self, item):
        """
        Provides request and item, should return list of tuples with item actions in following format:
        (id, name, help, icon, link)
        """
        return []

    def action(self, icon=None, name=None, url=None, post=False, prompt=None):
        """
        Function call to make hash with item actions
        """
        if prompt:
            self.prompt_select = True
        return {
                'icon': icon,
                'name': name,
                'link': url,
                'post': post,
                'prompt': prompt,
                }

    def get_search_form(self):
        """
        Build a form object with items search
        """
        return self.search_form

    def set_filters(self, model, filters):
        """
        Set filters on model using filters from session
        """
        return None

    def get_table_form(self, page_items):
        """
        Build a form object with list of all items fields
        """
        return None

    def table_action(self, page_items, cleaned_data):
        """
        Handle table form submission, return tuple containing message and redirect link/false
        """
        return None

    def get_actions_form(self, page_items):
        """
        Build a form object with list of all items actions
        """
        if not self.actions:
            return None # Dont build form
        form_fields = {}
        list_choices = []
        for action in self.actions:
            list_choices.append((action[0], action[1]))
        form_fields['list_action'] = forms.ChoiceField(choices=list_choices)
        list_choices = []
        for item in page_items:
            list_choices.append((item.pk, None))
        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices, widget=forms.CheckboxSelectMultiple)
        return type('AdminListForm', (Form,), form_fields)

    def get_sorting(self):
        """
        Return list sorting method.
        A list with three values:
        - Field we use to sort over
        - Sorting direction
        - order_by() argument
        """
        sorting_method = None
        if self.request.session.get(self.get_token('sort')) and self.request.session.get(self.get_token('sort'))[0] in self.sortables:
            sorting_method = self.request.session.get(self.get_token('sort'))

        if self.request.GET.get('sort') and self.request.GET.get('sort') in self.sortables:
            new_sorting = self.request.GET.get('sort')
            sorting_dir = int(self.request.GET.get('dir')) == 1
            sorting_method = [
                    new_sorting,
                    sorting_dir,
                    new_sorting if sorting_dir else '-%s' % new_sorting
                   ]
            self.request.session[self.get_token('sort')] = sorting_method

        if not sorting_method:
            if self.sortables:
                new_sorting = self.sortables.keys()[0]
                if self.default_sorting in self.sortables:
                    new_sorting = self.default_sorting
                sorting_method = [
                        new_sorting,
                        self.sortables[new_sorting] == True,
                        new_sorting if self.sortables[new_sorting] else '-%s' % new_sorting
                       ]
            else:
                sorting_method = [
                        id,
                        True,
                        '-id'
                       ]
        return sorting_method

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by(sorting_method[2])

    def get_pagination_url(self, page):
        return reverse(self.admin.get_action_attr(self.id, 'route'), kwargs={'page': page})

    def get_pagination(self, total, page):
        if not self.pagination or total < 0:
            # Dont do anything if we are not paging
            return None
        return make_pagination(page, total, self.pagination)

    def get_items(self):
        if self.request.session.get(self.get_token('filter')):
            self.is_filtering = True
            return self.set_filters(self.admin.model.objects, self.request.session.get(self.get_token('filter')))
        return self.admin.model.objects

    def __call__(self, request, page=0):
        """
        Use widget as view
        """
        self.request = request

        # Get basic list items
        items_total = self.get_items()

        # Set extra filters?
        try:
            items_total = self.select_items(items_total).count()
        except AttributeError:
            items_total = items_total.count()

        # Set sorting and paginating
        sorting_method = self.get_sorting()
        try:
            paginating_method = self.get_pagination(items_total, page)
        except Http404:
            return redirect(self.get_url())

        # List items
        items = self.get_items()
        if not request.session.get(self.get_token('filter')):
            items = items.all()

        # Set extra filters?
        try:
            items = self.select_items(items)
        except AttributeError:
            pass

        # Sort them
        items = self.sort_items(items, sorting_method);

        # Set pagination
        if self.pagination:
            items = items[paginating_method['start']:paginating_method['stop']]

        # Prefetch related?
        try:
            items = self.prefetch_related(items)
        except AttributeError:
            pass

        # Default message
        message = None

        # See if we should make and handle search form
        search_form = None
        SearchForm = self.get_search_form()
        if SearchForm:
            if request.method == 'POST':
                # New search
                if request.POST.get('origin') == 'search':
                    search_form = SearchForm(request.POST, request=request)
                    if search_form.is_valid():
                        search_criteria = {}
                        for field, criteria in search_form.cleaned_data.items():
                            if len(criteria) > 0:
                                search_criteria[field] = criteria
                        if not search_criteria:
                            message = Message(_("No search criteria have been defined."))
                        else:
                            request.session[self.get_token('filter')] = search_criteria
                            return redirect(self.get_url())
                    else:
                        message = Message(_("Search form contains errors."))
                    message.type = 'error'
                else:
                    search_form = SearchForm(request=request)

                # Kill search
                if request.POST.get('origin') == 'clear' and self.is_filtering and request.csrf.request_secure(request):
                    request.session[self.get_token('filter')] = None
                    request.messages.set_flash(Message(_("Search criteria have been cleared.")), 'info', self.admin.id)
                    return redirect(self.get_url())
            else:
                if self.is_filtering:
                    search_form = SearchForm(request=request, initial=request.session.get(self.get_token('filter')))
                else:
                    search_form = SearchForm(request=request)

        # See if we sould make and handle tab form
        table_form = None
        TableForm = self.get_table_form(items)
        if TableForm:
            if request.method == 'POST' and request.POST.get('origin') == 'table':
                table_form = TableForm(request.POST, request=request)
                if table_form.is_valid():
                    message, redirect_url = self.table_action(items, table_form.cleaned_data)
                    if redirect_url:
                        request.messages.set_flash(message, message.type, self.admin.id)
                        return redirect(redirect_url)
                else:
                    message = Message(table_form.non_field_errors()[0], 'error')
            else:
                table_form = TableForm(request=request)

        # See if we should make and handle list form
        list_form = None
        ListForm = self.get_actions_form(items)
        if ListForm:
            if request.method == 'POST' and request.POST.get('origin') == 'list':
                list_form = ListForm(request.POST, request=request)
                if list_form.is_valid():
                    try:
                        form_action = getattr(self, 'action_' + list_form.cleaned_data['list_action'])
                        message, redirect_url = form_action(items, [int(x) for x in list_form.cleaned_data['list_items']])
                        if redirect_url:
                            request.messages.set_flash(message, message.type, self.admin.id)
                            return redirect(redirect_url)
                    except AttributeError:
                        message = Message(_("Requested action is incorrect."))
                else:
                    if 'list_items' in list_form.errors:
                        message = Message(self.nothing_checked_message)
                    elif 'list_action' in list_form.errors:
                        message = Message(_("Requested action is incorrect."))
                    else:
                        message = Message(list_form.non_field_errors()[0])
                message.type = 'error'
            else:
                list_form = ListForm(request=request)

        # Little hax to keep counters correct 
        items_shown = len(items)
        if items_total < items_shown:
            items_total = items_shown

        # Render list
        return render_to_response(self.get_template(),
                                  self.add_template_variables({
                                   'admin': self.admin,
                                   'action': self,
                                   'request': request,
                                   'link': self.get_url(),
                                   'messages_log': request.messages.get_messages(self.admin.id),
                                   'message': message,
                                   'sorting': self.sortables,
                                   'sorting_method': sorting_method,
                                   'pagination': paginating_method,
                                   'list_form': FormLayout(list_form) if list_form else None,
                                   'search_form': FormLayout(search_form) if search_form else None,
                                   'table_form': FormFields(table_form).fields if table_form else None,
                                   'items': items,
                                   'items_total': items_total,
                                   'items_shown': items_shown,
                                  }),
                                  context_instance=RequestContext(request));


class FormWidget(BaseWidget):
    """
    Form page widget
    """
    template = 'form'
    submit_button = _("Save Changes")
    form = None
    layout = None
    tabbed = False
    target_name = None
    translate_target_name = False
    original_name = None
    submit_fallback = False

    def get_url(self, model):
        return reverse(self.admin.get_action_attr(self.id, 'route'))

    def get_form(self, target):
        return self.form

    def get_form_instance(self, form, target, initial, post=False):
        if post:
            return form(self.request.POST, request=self.request, initial=initial)
        return form(request=self.request, initial=initial)

    def get_layout(self, form, model):
        if self.layout:
            return self.layout
        return form.layout

    def get_initial_data(self, model):
        return {}

    def submit_form(self, form, model):
        """
        Handle form submission, ALWAYS return tuple with model and message
        """
        pass

    def __call__(self, request, target=None, slug=None):
        self.request = request

        # Fetch target?
        model = None
        if target:
            model = self.get_and_validate_target(target)
            self.original_name = self.get_target_name(model)
            if not model:
                return redirect(self.get_fallback_url())
        original_model = model

        # Get form type to instantiate
        FormType = self.get_form(model)

        #Submit form
        message = None
        if request.method == 'POST':
            form = self.get_form_instance(FormType, model, self.get_initial_data(model), True)
            if form.is_valid():
                try:
                    model, message = self.submit_form(form, model)
                    if message.type != 'error':
                        request.messages.set_flash(message, message.type, self.admin.id)
                        # Redirect back to right page
                        try:
                            if 'save_new' in request.POST and self.get_new_url:
                                return redirect(self.get_new_url(model))
                        except AttributeError:
                            pass
                        try:
                            if 'save_edit' in request.POST and self.get_edit_url:
                                return redirect(self.get_edit_url(model))
                        except AttributeError:
                            pass
                        try:
                            if self.get_submit_url:
                                return redirect(self.get_submit_url(model))
                        except AttributeError:
                            pass
                        return redirect(self.get_fallback_url())
                except ValidationError as e:
                    message = Message(e.messages[0], 'error')
            else:
                message = Message(form.non_field_errors()[0], 'error')
        else:
            form = self.get_form_instance(FormType, model, self.get_initial_data(model))

        # Render form
        return render_to_response(self.get_template(),
                                  self.add_template_variables({
                                   'admin': self.admin,
                                   'action': self,
                                   'request': request,
                                   'link': self.get_url(model),
                                   'fallback': self.get_fallback_url(),
                                   'messages_log': request.messages.get_messages(self.admin.id),
                                   'message': message,
                                   'tabbed': self.tabbed,
                                   'target': self.get_target_name(original_model),
                                   'target_model': original_model,
                                   'form': FormLayout(form, self.get_layout(form, target)),
                                  }),
                                  context_instance=RequestContext(request));


class ButtonWidget(BaseWidget):
    """
    Button Action Widget
    This widget handles most basic and common type of admin action - button press:
    - User presses button on list (for example "delete this user!")
    - Widget checks if request is CSRF-valid and POST
    - Widget optionally chcecks if target has been provided and action is allowed at all
    - Widget does action and redirects us back to fallback url
    """
    def __call__(self, request, target=None, slug=None):
        self.request = request

        # Fetch target?
        model = None
        if target:
            model = self.get_and_validate_target(target)
            if not model:
                return redirect(self.get_fallback_url())
        original_model = model

        # Crash if this is invalid request
        if not request.csrf.request_secure(request):
            request.messages.set_flash(Message(_("Action authorization is invalid.")), 'error', self.admin.id)
            return redirect(self.get_fallback_url())

        # Do something
        message, url = self.action(model)
        request.messages.set_flash(message, message.type, self.admin.id)
        if url:
            return redirect(url)
        return redirect(self.get_fallback_url())

    def action(self, target):
        """
        Action to be executed when button is pressed
        Define custom one in your Admin action.
        It should return response and message objects 
        """
        pass
