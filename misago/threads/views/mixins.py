from django import forms
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.forms import Form
from misago.messages import Message

class ThreadsFormMixin(object):
    def make_form(self):
        self.form = None
        list_choices = self.get_thread_actions();
        if (not self.request.user.is_authenticated()
            or not list_choices):
            return
        
        form_fields = {}
        form_fields['list_action'] = forms.ChoiceField(choices=list_choices)
        list_choices = []
        for item in self.threads:
            list_choices.append((item.pk, None))
        if not list_choices:
            return
        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices,widget=forms.CheckboxSelectMultiple)
        self.form = type('ThreadsViewForm', (Form,), form_fields)
    
    def handle_form(self):
        if self.request.method == 'POST':
            self.form = self.form(self.request.POST, request=self.request)
            if self.form.is_valid():
                checked_items = []
                checked_ids = []
                for thread in self.threads:
                    if str(thread.pk) in self.form.cleaned_data['list_items']:
                        checked_ids.append(thread.pk)
                        checked_items.append(thread)
                if checked_items:
                    form_action = getattr(self, 'action_' + self.form.cleaned_data['list_action'])
                    response = form_action(checked_ids, checked_items)
                    if response:
                        return response
                    return redirect(self.request.path)
                else:
                    self.message = Message(_("You have to select at least one thread."), 'error')
            else:
                if 'list_action' in self.form.errors:
                    self.message = Message(_("Action requested is incorrect."), 'error')
                else:
                    self.message = Message(form.non_field_errors()[0], 'error')
        else:
            self.form = self.form(request=self.request)