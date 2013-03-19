from django.core.urlresolvers import reverse
from django import forms
from django.db.models import F
from django.forms import ValidationError
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import Form, FormLayout, FormFields
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, Thread, Post, Karma, Change, Checkpoint, WatchedThread
from misago.readstrackers import ThreadsTracker
from misago.utils.strings import slugify
from misago.utils.pagination import make_pagination
from misago.apps.threads.forms import MoveThreadsForm, SplitThreadForm, MovePostsForm, QuickReplyForm
from misago.apps.threads.views.base import BaseView

class ThreadView(BaseView):
    def fetch_thread(self, thread):
        self.thread = Thread.objects.get(pk=thread)
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        self.tracker = ThreadsTracker(self.request, self.forum)
        if self.request.user.is_authenticated():
            try:
                self.watcher = WatchedThread.objects.get(user=self.request.user, thread=self.thread)
            except WatchedThread.DoesNotExist:
                pass

    def fetch_posts(self, page):
        self.count = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).count()
        self.posts = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).prefetch_related('checkpoint_set', 'user', 'user__rank')
        if self.thread.merges > 0:
            self.posts = self.posts.order_by('merge', 'pk')
        else:
            self.posts = self.posts.order_by('pk')
        self.pagination = make_pagination(page, self.count, self.request.settings.posts_per_page)
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
            self.tracker.set_read(self.thread, last_post)
            self.tracker.sync()
        if self.watcher and last_post.date > self.watcher.last_read:
            self.watcher.last_read = timezone.now()
            self.watcher.save(force_update=True)
        if self.request.user.is_authenticated():
            for karma in Karma.objects.filter(post_id__in=posts_dict.keys()).filter(user=self.request.user):
                posts_dict[karma.post_id].karma_vote = karma

    def get_post_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_approve'] and self.thread.replies_moderated > 0:
                actions.append(('accept', _('Accept posts')))
            if acl['can_move_threads_posts']:
                actions.append(('merge', _('Merge posts into one')))
                actions.append(('split', _('Split posts to new thread')))
                actions.append(('move', _('Move posts to other thread')))
            if acl['can_protect_posts']:
                actions.append(('protect', _('Protect posts')))
                actions.append(('unprotect', _('Remove posts protection')))
            if acl['can_delete_posts']:
                if self.thread.replies_deleted > 0:
                    actions.append(('undelete', _('Undelete posts')))
                actions.append(('soft', _('Soft delete posts')))
            if acl['can_delete_posts'] == 2:
                actions.append(('hard', _('Hard delete posts')))
        except KeyError:
            pass
        return actions

    def make_posts_form(self):
        self.posts_form = None
        list_choices = self.get_post_actions();
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

    def post_action_accept(self, ids):
        accepted = 0
        for post in self.posts:
            if post.pk in ids and post.moderated:
                accepted += 1
        if accepted:
            self.thread.post_set.filter(id__in=ids).update(moderated=False)
            self.thread.sync()
            self.thread.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected posts have been accepted and made visible to other members.')), 'success', 'threads')

    def post_action_merge(self, ids):
        users = []
        posts = []
        for post in self.posts:
            if post.pk in ids:
                posts.append(post)
                if not post.user_id in users:
                    users.append(post.user_id)
                if len(users) > 1:
                    raise forms.ValidationError(_("You cannot merge replies made by different members!"))
        if len(posts) < 2:
            raise forms.ValidationError(_("You have to select two or more posts you want to merge."))
        new_post = posts[0]
        for post in posts[1:]:
            post.merge_with(new_post)
            post.delete()
        md, new_post.post_preparsed = post_markdown(self.request, new_post.post)
        new_post.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)
        self.request.messages.set_flash(Message(_('Selected posts have been merged into one message.')), 'success', 'threads')

    def post_action_split(self, ids):
        for id in ids:
            if id == self.thread.start_post_id:
                raise forms.ValidationError(_("You cannot split first post from thread."))
        message = None
        if self.request.POST.get('do') == 'split':
            form = SplitThreadForm(self.request.POST, request=self.request)
            if form.is_valid():
                new_thread = Thread()
                new_thread.forum = form.cleaned_data['thread_forum']
                new_thread.name = form.cleaned_data['thread_name']
                new_thread.slug = slugify(form.cleaned_data['thread_name'])
                new_thread.start = timezone.now()
                new_thread.last = timezone.now()
                new_thread.start_poster_name = 'n'
                new_thread.start_poster_slug = 'n'
                new_thread.last_poster_name = 'n'
                new_thread.last_poster_slug = 'n'
                new_thread.save(force_insert=True)
                prev_merge = -1
                merge = -1
                for post in self.posts:
                    if post.pk in ids:
                        if prev_merge != post.merge:
                            prev_merge = post.merge
                            merge += 1
                        post.merge = merge
                        post.move_to(new_thread)
                        post.save(force_update=True)
                new_thread.sync()
                new_thread.save(force_update=True)
                self.thread.sync()
                self.thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                if new_thread.forum != self.forum:
                    new_thread.forum.sync()
                    new_thread.forum.save(force_update=True)
                self.request.messages.set_flash(Message(_("Selected posts have been split to new thread.")), 'success', 'threads')
                return redirect(reverse('thread', kwargs={'thread': new_thread.pk, 'slug': new_thread.slug}))
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = SplitThreadForm(request=self.request, initial={
                                                                  'thread_name': _('[Split] %s') % self.thread.name,
                                                                  'thread_forum': self.forum,
                                                                  })
        return self.request.theme.render_to_response('threads/split.html',
                                                     {
                                                      'message': message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'thread': self.thread,
                                                      'posts': ids,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def post_action_move(self, ids):
        message = None
        if self.request.POST.get('do') == 'move':
            form = MovePostsForm(self.request.POST, request=self.request, thread=self.thread)
            if form.is_valid():
                thread = form.cleaned_data['thread_url']
                prev_merge = -1
                merge = -1
                for post in self.posts:
                    if post.pk in ids:
                        if prev_merge != post.merge:
                            prev_merge = post.merge
                            merge += 1
                        post.merge = merge + thread.merges
                        post.move_to(thread)
                        post.save(force_update=True)
                if self.thread.post_set.count() == 0:
                    self.thread.delete()
                else:
                    self.thread.sync()
                    self.thread.save(force_update=True)
                thread.sync()
                thread.save(force_update=True)
                thread.forum.sync()
                thread.forum.save(force_update=True)
                if self.forum.pk != thread.forum.pk:
                    self.forum.sync()
                    self.forum.save(force_update=True)
                self.request.messages.set_flash(Message(_("Selected posts have been moved to new thread.")), 'success', 'threads')
                return redirect(reverse('thread', kwargs={'thread': thread.pk, 'slug': thread.slug}))
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MovePostsForm(request=self.request)
        return self.request.theme.render_to_response('threads/move_posts.html',
                                                     {
                                                      'message': message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'thread': self.thread,
                                                      'posts': ids,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def post_action_undelete(self, ids):
        undeleted = []
        for post in self.posts:
            if post.pk in ids and post.deleted:
                undeleted.append(post.pk)
        if undeleted:
            self.thread.post_set.filter(id__in=undeleted).update(deleted=False)
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected posts have been restored.')), 'success', 'threads')

    def post_action_protect(self, ids):
        protected = 0
        for post in self.posts:
            if post.pk in ids and not post.protected:
                protected += 1
        if protected:
            self.thread.post_set.filter(id__in=ids).update(protected=True)
            self.request.messages.set_flash(Message(_('Selected posts have been protected from edition.')), 'success', 'threads')

    def post_action_unprotect(self, ids):
        unprotected = 0
        for post in self.posts:
            if post.pk in ids and post.protected:
                unprotected += 1
        if unprotected:
            self.thread.post_set.filter(id__in=ids).update(protected=False)
            self.request.messages.set_flash(Message(_('Protection from editions has been removed from selected posts.')), 'success', 'threads')

    def post_action_soft(self, ids):
        deleted = []
        for post in self.posts:
            if post.pk in ids and not post.deleted:
                if post.pk == self.thread.start_post_id:
                    raise forms.ValidationError(_("You cannot delete first post of thread using this action. If you want to delete thread, use thread moderation instead."))
                deleted.append(post.pk)
        if deleted:
            self.thread.post_set.filter(id__in=deleted).update(deleted=True)
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected posts have been deleted.')), 'success', 'threads')

    def post_action_hard(self, ids):
        deleted = []
        for post in self.posts:
            if post.pk in ids:
                if post.pk == self.thread.start_post_id:
                    raise forms.ValidationError(_("You cannot delete first post of thread using this action. If you want to delete thread, use thread moderation instead."))
                deleted.append(post.pk)
        if deleted:
            for post in self.posts:
                if post.pk in deleted:
                    post.delete()
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected posts have been deleted.')), 'success', 'threads')

    def get_thread_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_approve'] and self.thread.moderated:
                actions.append(('accept', _('Accept this thread')))
            if acl['can_pin_threads'] == 2 and self.thread.weight < 2:
                actions.append(('annouce', _('Change this thread to announcement')))
            if acl['can_pin_threads'] > 0 and self.thread.weight != 1:
                actions.append(('sticky', _('Change this thread to sticky')))
            if acl['can_pin_threads'] > 0:
                if self.thread.weight == 2:
                    actions.append(('normal', _('Change this thread to normal')))
                if self.thread.weight == 1:
                    actions.append(('normal', _('Unpin this thread')))
            if acl['can_move_threads_posts']:
                actions.append(('move', _('Move this thread')))
            if acl['can_close_threads']:
                if self.thread.closed:
                    actions.append(('open', _('Open this thread')))
                else:
                    actions.append(('close', _('Close this thread')))
            if acl['can_delete_threads']:
                if self.thread.deleted:
                    actions.append(('undelete', _('Undelete this thread')))
                else:
                    actions.append(('soft', _('Soft delete this thread')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Hard delete this thread')))
        except KeyError:
            pass
        return actions

    def make_thread_form(self):
        self.thread_form = None
        list_choices = self.get_thread_actions();
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

    def thread_action_accept(self):
        # Sync thread and post
        self.thread.moderated = False
        self.thread.replies_moderated -= 1
        self.thread.save(force_update=True)
        self.thread.start_post.moderated = False
        self.thread.start_post.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'accepted')
        # Sync user
        if self.thread.last_post.user:
            self.thread.start_post.user.threads += 1
            self.thread.start_post.user.posts += 1
            self.thread.start_post.user.save(force_update=True)
        # Sync forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) + self.thread.replies + 1
        self.request.messages.set_flash(Message(_('Thread has been marked as reviewed and made visible to other members.')), 'success', 'threads')

    def thread_action_annouce(self):
        self.thread.weight = 2
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread has been turned into announcement.')), 'success', 'threads')

    def thread_action_sticky(self):
        self.thread.weight = 1
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread has been turned into sticky.')), 'success', 'threads')

    def thread_action_normal(self):
        self.thread.weight = 0
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread weight has been changed to normal.')), 'success', 'threads')

    def thread_action_move(self):
        message = None
        if self.request.POST.get('do') == 'move':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                self.thread.move_to(new_forum)
                self.thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                new_forum.sync()
                new_forum.save(force_update=True)
                self.request.messages.set_flash(Message(_('Thread has been moved to "%(forum)s".') % {'forum': new_forum.name}), 'success', 'threads')
                return None
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return self.request.theme.render_to_response('threads/move_thread.html',
                                                     {
                                                      'message': message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'thread': self.thread,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def thread_action_open(self):
        self.thread.closed = False
        self.thread.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'opened')
        self.request.messages.set_flash(Message(_('Thread has been opened.')), 'success', 'threads')

    def thread_action_close(self):
        self.thread.closed = True
        self.thread.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'closed')
        self.request.messages.set_flash(Message(_('Thread has been closed.')), 'success', 'threads')

    def thread_action_undelete(self):
        # Update thread
        self.thread.deleted = False
        self.thread.replies_deleted -= 1
        self.thread.save(force_update=True)
        # Update first post in thread
        self.thread.start_post.deleted = False
        self.thread.start_post.save(force_update=True)
        # Set checkpoint
        self.thread.last_post.set_checkpoint(self.request, 'undeleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) + self.thread.replies + 1
        self.request.messages.set_flash(Message(_('Thread has been undeleted.')), 'success', 'threads')

    def thread_action_soft(self):
        # Update thread
        self.thread.deleted = True
        self.thread.replies_deleted += 1
        self.thread.save(force_update=True)
        # Update first post in thread
        self.thread.start_post.deleted = True
        self.thread.start_post.save(force_update=True)
        # Set checkpoint
        self.thread.last_post.set_checkpoint(self.request, 'deleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) - 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) - self.thread.replies - 1
        self.request.messages.set_flash(Message(_('Thread has been deleted.')), 'success', 'threads')

    def thread_action_hard(self):
        # Delete thread
        self.thread.delete()
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) - 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) - self.thread.replies - 1
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
        return redirect(reverse('forum', kwargs={'forum': self.forum.pk, 'slug': self.forum.slug}))

    def __call__(self, request, slug=None, thread=None, page=0):
        self.request = request
        self.pagination = None
        self.parents = None
        self.ignored = False
        self.watcher = None
        try:
            self.fetch_thread(thread)
            self.fetch_posts(page)
            self.message = request.messages.get_message('threads')
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
        except Thread.DoesNotExist:
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        # Merge proxy into forum
        self.forum.closed = self.proxy.closed
        return request.theme.render_to_response('threads/thread.html',
                                                {
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
                                                 },
                                                context_instance=RequestContext(request));
