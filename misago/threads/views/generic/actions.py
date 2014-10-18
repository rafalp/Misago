from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from misago.core.exceptions import AjaxError

from misago.threads.moderation import ModerationError


__all__ = ['ActionsBase']


class ActionsBase(object):
    query_key = 'action'
    invalid_action_message = _("Requested action is invalid.")

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
        action_name = request.POST.get(self.query_key)

        for action in self.available_actions:
            if action['action'] == action_name:
                if ':' in action_name:
                    action_bits = action_name.split(':')
                    action_name = action_bits[0]
                    action_arg = action_bits[1]
                else:
                    action_arg = None

                action_callable = 'action_%s' % action_name
                return getattr(self, action_callable), action_arg
        else:
            raise ModerationError(self.invalid_action_message)

    def clean_selection(self, data):
        filtered_data = []
        for pk in data[:50]: # a tiny fail-safe to avoid too big workloads
            try:
                filtered_data.append(int(pk))
            except ValueError:
                pass

        if not filtered_data:
            raise ModerationError(self.select_items_message)

        return filtered_data

    def handle_post(self, request, target):
        try:
            if self.is_mass_action:
                return self.handle_mass_action(request, target)
            else:
                return self.handle_single_action(request, target)
        except ModerationError as e:
            if request.is_ajax():
                raise AjaxError(e.message, 406)
            else:
                messages.error(request, e.message)
                return False

    def handle_mass_action(self, request, queryset):
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
            elif request.is_ajax():
                raise AjaxError(self.invalid_action_message, 406)
            else:
                # prepare default response: page reload
                return redirect(request.path)
        else:
            raise ModerationError(self.select_items_message)

    def handle_single_action(self, request, target):
        action, action_arg = self.resolve_action(request)

        if action_arg:
            response = action(request, target, action_arg)
        else:
            response = action(request, target)

        if response:
            return response
        elif request.is_ajax():
            raise AjaxError(self.invalid_action_message, 406)
        else:
            # prepare default response: page reload
            return redirect(request.path)

    def get_list(self):
        return self.available_actions

    def get_selected_ids(self):
        return self.selected_ids
