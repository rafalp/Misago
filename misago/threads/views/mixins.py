from django import forms
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.forms import Form
from misago.messages import Message
from misago.threads.models import Post

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
            if item.forum_id == self.forum.pk:
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
                posts = []
                for thread in self.threads:
                    if str(thread.pk) in self.form.cleaned_data['list_items'] and thread.forum_id == self.forum.pk:
                        posts.append(thread.start_post_id)
                        if thread.start_post_id != thread.last_post_id:
                            posts.append(thread.last_post_id)
                        checked_items.append(thread.pk)
                if checked_items:
                    if posts:
                        for post in Post.objects.filter(id__in=posts).prefetch_related('user'):
                            for thread in self.threads:
                                if thread.start_post_id == post.pk:
                                    thread.start_post = post
                                if thread.last_post_id == post.pk:
                                    thread.last_post = post
                                if thread.start_post_id == post.pk or thread.last_post_id == post.pk:
                                    break
                    form_action = getattr(self, 'action_' + self.form.cleaned_data['list_action'])
                    response = form_action(checked_items)
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