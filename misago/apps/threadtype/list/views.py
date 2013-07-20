from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import Form
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.readstrackers import ForumsTracker
from misago.shortcuts import render_to_response
from misago.apps.threadtype.base import ViewBase

class ThreadsListBaseView(ViewBase):
    template = 'list'

    def _fetch_forum(self):
        self.fetch_forum()
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)
        self.check_forum_type()
        if self.forum.lft + 1 != self.forum.rght:
            self.forum.subforums = Forum.objects.treelist(self.request.acl.forums, self.forum, tracker=ForumsTracker(self.request.user))

    def threads_actions(self):
        pass

    def make_form(self):
        self.form = None
        list_choices = self.threads_actions();
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

        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices, widget=forms.CheckboxSelectMultiple)
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
                    try:
                        response = form_action(checked_items)
                        if response:
                            return response
                        return redirect(self.request.path)
                    except forms.ValidationError as e:
                        self.message = Message(e.messages[0], messages.ERROR)
                else:
                    self.message = Message(_("You have to select at least one thread."), messages.ERROR)
            else:
                if 'list_action' in self.form.errors:
                    self.message = Message(_("Requested action is incorrect."), messages.ERROR)
                else:
                    self.message = Message(self.form.non_field_errors()[0], messages.ERROR)
        else:
            self.form = self.form(request=self.request)

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.pagination = {}
        self.parents = []
        self.threads = []
        self.message = request.messages.get_message('threads')
        try:
            self._type_available()
            self._fetch_forum()
            self._check_permissions()
            response = self.fetch_threads()
            if response:
                return response
            self.form = None
            self.make_form()
            if self.form:
                response = self.handle_form()
                if response:
                    return response
        except (Forum.DoesNotExist, Thread.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

        # Merge proxy into forum
        self.forum.closed = self.proxy.closed

        return render_to_response('%ss/%s.html' % (self.type_prefix, self.template),
                                  self.template_vars({
                                      'type_prefix': self.type_prefix,
                                      'message': self.message,
                                      'forum': self.forum,
                                      'parents': self.parents,
                                      'count': self.count,
                                      'list_form': self.form or None,
                                      'threads': self.threads,
                                      'pagination': self.pagination,
                                      }),
                                  context_instance=RequestContext(request));