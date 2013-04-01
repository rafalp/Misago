from django import forms
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import Form, FormLayout, FormFields
from misago.messages import Message
from misago.models import Forum, Thread, Post, Karma, WatchedThread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.threadtype.base import ViewBase
from misago.apps.threadtype.thread.forms import QuickReplyForm

class ThreadBaseView(ViewBase):
    def fetch_thread(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk, True)

        self.tracker = ThreadsTracker(self.request, self.forum)
        if self.request.user.is_authenticated():
            try:
                self.watcher = WatchedThread.objects.get(user=self.request.user, thread=self.thread)
            except WatchedThread.DoesNotExist:
                pass

    def fetch_posts(self):
        self.count = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).count()
        self.posts = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).prefetch_related('checkpoint_set', 'user', 'user__rank')
        
        if self.thread.merges > 0:
            self.posts = self.posts.order_by('merge', 'pk')
        else:
            self.posts = self.posts.order_by('pk')

        self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.posts_per_page)
        if self.request.settings.posts_per_page < self.count:
            self.posts = self.posts[self.pagination['start']:self.pagination['stop']]

        self.read_date = self.tracker.read_date(self.thread)

        ignored_users = []
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()

        posts_dict = {}
        for post in self.posts:
            posts_dict[post.pk] = post
            post.message = self.request.messages.get_message('threads_%s' % post.pk)
            post.is_read = post.date <= self.read_date or (post.pk != self.thread.start_post_id and post.moderated)
            post.karma_vote = None
            post.ignored = self.thread.start_post_id != post.pk and not self.thread.pk in self.request.session.get('unignore_threads', []) and post.user_id in ignored_users
            if post.ignored:
                self.ignored = True

        last_post = self.posts[len(self.posts) - 1]

        if not self.tracker.is_read(self.thread):
            self.tracker_update(last_post)

        if self.watcher and last_post.date > self.watcher.last_read:
            self.watcher.last_read = timezone.now()
            self.watcher.save(force_update=True)

        if self.request.user.is_authenticated():
            for karma in Karma.objects.filter(post_id__in=posts_dict.keys()).filter(user=self.request.user):
                posts_dict[karma.post_id].karma_vote = karma

    def tracker_update(self, last_post):
        self.tracker.set_read(self.thread, last_post)
        try:
            self.tracker.sync(self.tracker_queryset())
        except AttributeError:
            self.tracker.sync()

    def thread_actions(self):
        pass

    def make_thread_form(self):
        self.thread_form = None
        list_choices = self.thread_actions();
        if (not self.request.user.is_authenticated()
            or not list_choices):
            return
        form_fields = {'thread_action': forms.ChoiceField(choices=list_choices)}
        self.thread_form = type('ThreadViewForm', (Form,), form_fields)

    def handle_thread_form(self):
        if self.request.method == 'POST' and self.request.POST.get('origin') == 'thread_form':
            self.thread_form = self.thread_form(self.request.POST, request=self.request)
            if self.thread_form.is_valid():
                form_action = getattr(self, 'thread_action_' + self.thread_form.cleaned_data['thread_action'])
                try:
                    response = form_action()
                    if response:
                        return response
                    return redirect(self.request.path)
                except forms.ValidationError as e:
                    self.message = Message(e.messages[0], 'error')
            else:
                if 'thread_action' in self.thread_form.errors:
                    self.message = Message(_("Action requested is incorrect."), 'error')
                else:
                    self.message = Message(form.non_field_errors()[0], 'error')
        else:
            self.thread_form = self.thread_form(request=self.request)

    def posts_actions(self):
        pass

    def make_posts_form(self):
        self.posts_form = None
        list_choices = self.posts_actions();
        if (not self.request.user.is_authenticated()
            or not list_choices):
            return

        form_fields = {}
        form_fields['list_action'] = forms.ChoiceField(choices=list_choices)
        list_choices = []
        for item in self.posts:
            list_choices.append((item.pk, None))
        if not list_choices:
            return
        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices, widget=forms.CheckboxSelectMultiple)
        self.posts_form = type('PostsViewForm', (Form,), form_fields)
    
    def handle_posts_form(self):
        if self.request.method == 'POST' and self.request.POST.get('origin') == 'posts_form':
            self.posts_form = self.posts_form(self.request.POST, request=self.request)
            if self.posts_form.is_valid():
                checked_items = []
                for post in self.posts:
                    if str(post.pk) in self.posts_form.cleaned_data['list_items']:
                        checked_items.append(post.pk)
                if checked_items:
                    form_action = getattr(self, 'post_action_' + self.posts_form.cleaned_data['list_action'])
                    try:
                        response = form_action(checked_items)
                        if response:
                            return response
                        return redirect(self.request.path)
                    except forms.ValidationError as e:
                        self.message = Message(e.messages[0], 'error')
                else:
                    self.message = Message(_("You have to select at least one post."), 'error')
            else:
                if 'list_action' in self.posts_form.errors:
                    self.message = Message(_("Action requested is incorrect."), 'error')
                else:
                    self.message = Message(posts_form.non_field_errors()[0], 'error')
        else:
            self.posts_form = self.posts_form(request=self.request)

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.parents = []
        self.ignored = False
        self.watcher = False
        self.message = request.messages.get_message('threads')
        try:
            self._type_available()
            self.fetch_thread()
            self.check_forum_type()
            self._check_permissions()
            self.fetch_posts()
            self.make_thread_form()
            if self.thread_form:
                response = self.handle_thread_form()
                if response:
                    return response
            self.make_posts_form()
            if self.posts_form:
                response = self.handle_posts_form()
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

        return request.theme.render_to_response('%ss/thread.html' % self.type_prefix,
                                                self.template_vars({
                                                 'type_prefix': self.type_prefix,
                                                 'message': self.message,
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'is_read': self.tracker.is_read(self.thread),
                                                 'count': self.count,
                                                 'posts': self.posts,
                                                 'ignored_posts': self.ignored,
                                                 'watcher': self.watcher,
                                                 'pagination': self.pagination,
                                                 'quick_reply': FormFields(QuickReplyForm(request=request)).fields,
                                                 'thread_form': FormFields(self.thread_form).fields if self.thread_form else None,
                                                 'posts_form': FormFields(self.posts_form).fields if self.posts_form else None,
                                                 }),
                                                context_instance=RequestContext(request));