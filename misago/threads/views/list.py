from django.core.urlresolvers import reverse
from django.db.models import Q
from django import forms
from django.forms import ValidationError
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import Form, FormLayout, FormFields
from misago.forums.models import Forum
from misago.messages import Message
from misago.readstracker.trackers import ForumsTracker, ThreadsTracker
from misago.threads.forms import MoveThreadsForm, MergeThreadsForm
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination, slugify

class ThreadsView(BaseView):
    def fetch_forum(self, forum):
        self.forum = Forum.objects.get(pk=forum, type='forum')
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.parents = Forum.objects.forum_parents(self.forum.pk)
        if self.forum.lft + 1 != self.forum.rght:
            self.forum.subforums = Forum.objects.treelist(self.request.acl.forums, self.forum, tracker=ForumsTracker(self.request.user))
        self.tracker = ThreadsTracker(self.request, self.forum)

    def fetch_threads(self, page):
        self.count = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum).filter(weight__lt=2)).count()
        self.pagination = make_pagination(page, self.count, self.request.settings.threads_per_page)
        self.threads = []
        ignored_users = []
        queryset_anno = Thread.objects.filter(Q(forum=Forum.objects.token_to_pk('annoucements')) | (Q(forum=self.forum) & Q(weight=2)))
        queryset_threads = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum).filter(weight__lt=2)).order_by('-weight', '-last')
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                queryset_threads = queryset_threads.extra(where=["`threads_thread`.`start_poster_id` IS NULL OR `threads_thread`.`start_poster_id` NOT IN (%s)" % ','.join([str(i) for i in ignored_users])])
        if self.request.settings.avatars_on_threads_list:
            queryset_anno = queryset_anno.prefetch_related('start_poster', 'last_post')
            queryset_threads = queryset_threads.prefetch_related('start_poster', 'last_poster')
        for thread in queryset_anno:
            self.threads.append(thread)
        for thread in queryset_threads:
            self.threads.append(thread)
        if self.request.settings.threads_per_page < self.count:
            self.threads = self.threads[self.pagination['start']:self.pagination['stop']]
        for thread in self.threads:
            thread.is_read = self.tracker.is_read(thread)
            thread.last_poster_ignored = thread.last_poster_id in ignored_users
            

    def get_thread_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            if acl['can_approve']:
                actions.append(('accept', _('Accept threads')))
            if acl['can_pin_threads'] == 2:
                actions.append(('annouce', _('Change to annoucements')))
            if acl['can_pin_threads'] > 0:
                actions.append(('sticky', _('Change to sticky threads')))
            if acl['can_pin_threads'] > 0:
                actions.append(('normal', _('Change to standard thread')))
            if acl['can_move_threads_posts']:
                actions.append(('move', _('Move threads')))
                actions.append(('merge', _('Merge threads')))
            if acl['can_close_threads']:
                actions.append(('open', _('Open threads')))
                actions.append(('close', _('Close threads')))
            if acl['can_delete_threads']:
                actions.append(('undelete', _('Undelete threads')))
                actions.append(('soft', _('Soft delete threads')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Hard delete threads')))
        except KeyError:
            pass
        return actions

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
                        self.message = Message(e.messages[0], 'error')
                else:
                    self.message = Message(_("You have to select at least one thread."), 'error')
            else:
                if 'list_action' in self.form.errors:
                    self.message = Message(_("Action requested is incorrect."), 'error')
                else:
                    self.message = Message(form.non_field_errors()[0], 'error')
        else:
            self.form = self.form(request=self.request)

    def action_accept(self, ids):
        accepted = 0
        last_posts = []
        users = []
        for thread in self.threads:
            if thread.pk in ids and thread.moderated:
                accepted += 1
                # Sync thread and post
                thread.moderated = False
                thread.replies_moderated -= 1
                thread.save(force_update=True)
                thread.start_post.moderated = False
                thread.start_post.save(force_update=True)
                thread.last_post.set_checkpoint(self.request, 'accepted')
                last_posts.append(thread.last_post.pk)
                # Sync user
                if thread.last_post.user:
                    thread.start_post.user.threads += 1
                    thread.start_post.user.posts += 1
                    users.append(thread.start_post.user)
        if accepted:
            Post.objects.filter(id__in=last_posts).update(checkpoints=True)
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + accepted
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + accepted
            self.forum.sync()
            self.forum.save(force_update=True)
            for user in users:
                user.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected threads have been marked as reviewed and made visible to other members.')), 'success', 'threads')

    def action_annouce(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        annouced = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight < 2:
                annouced.append(thread.pk)
        if annouced:
            Thread.objects.filter(id__in=annouced).update(weight=2)
            self.request.messages.set_flash(Message(_('Selected threads have been turned into annoucements.')), 'success', 'threads')

    def action_sticky(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        sticky = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight != 1 and (acl['can_pin_threads'] == 2 or thread.weight < 2):
                sticky.append(thread.pk)
        if sticky:
            Thread.objects.filter(id__in=sticky).update(weight=1)
            self.request.messages.set_flash(Message(_('Selected threads have been sticked to the top of list.')), 'success', 'threads')

    def action_normal(self, ids):
        normalised = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight > 0:
                normalised.append(thread.pk)
        if normalised:
            Thread.objects.filter(id__in=normalised).update(weight=0)
            self.request.messages.set_flash(Message(_('Selected threads weight has been removed.')), 'success', 'threads')

    def action_move(self, ids):
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'move_form':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                for thread in threads:
                    thread.move_to(new_forum)
                    thread.save(force_update=True)
                new_forum.sync()
                new_forum.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                self.request.messages.set_flash(Message(_('Selected threads have been moved to "%(forum)s".') % {'forum': new_forum.name}), 'success', 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return self.request.theme.render_to_response('threads/move_threads.html',
                                                     {
                                                      'message': self.message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'threads': threads,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def action_merge(self, ids):
        if len(ids) < 2:
            raise ValidationError(_("You have to pick two or more threads to merge."))
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'merge_form':
            form = MergeThreadsForm(self.request.POST, request=self.request, threads=threads)
            if form.is_valid():
                new_thread = Thread.objects.create(
                                                   forum=form.cleaned_data['new_forum'],
                                                   name=form.cleaned_data['thread_name'],
                                                   slug=slugify(form.cleaned_data['thread_name']),
                                                   start=timezone.now(),
                                                   last=timezone.now()
                                                   )
                last_merge = 0
                last_thread = None
                merged = []
                for i in range(0, len(threads)):
                    thread = form.merge_order[i]
                    merged.append(thread.pk)
                    if last_thread and last_thread.last > thread.start:
                        last_merge += thread.merges + 1
                    thread.merge_with(new_thread, last_merge=last_merge)
                    last_thread = thread
                Thread.objects.filter(id__in=merged).delete()
                new_thread.sync()
                new_thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                if form.cleaned_data['new_forum'].pk != self.forum.pk:
                    form.cleaned_data['new_forum'].sync()
                    form.cleaned_data['new_forum'].save(force_update=True)
                self.request.messages.set_flash(Message(_('Selected threads have been merged into new one.')), 'success', 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MergeThreadsForm(request=self.request, threads=threads)
        return self.request.theme.render_to_response('threads/merge.html',
                                                     {
                                                      'message': self.message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'threads': threads,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def action_open(self, ids):
        opened = []
        last_posts = []
        for thread in self.threads:
            if thread.pk in ids and thread.closed:
                opened.append(thread.pk)
                thread.last_post.set_checkpoint(self.request, 'opened')
                last_posts.append(thread.last_post.pk)
        if opened:
            Post.objects.filter(id__in=last_posts).update(checkpoints=True)
            Thread.objects.filter(id__in=opened).update(closed=False)
            self.request.messages.set_flash(Message(_('Selected threads have been opened.')), 'success', 'threads')

    def action_close(self, ids):
        closed = []
        last_posts = []
        for thread in self.threads:
            if thread.pk in ids and not thread.closed:
                closed.append(thread.pk)
                thread.last_post.set_checkpoint(self.request, 'closed')
                last_posts.append(thread.last_post.pk)
        if closed:
            Post.objects.filter(id__in=last_posts).update(checkpoints=True)
            Thread.objects.filter(id__in=closed).update(closed=True)
            self.request.messages.set_flash(Message(_('Selected threads have been closed.')), 'success', 'threads')

    def action_undelete(self, ids):
        undeleted = []
        last_posts = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids and thread.deleted:
                undeleted.append(thread.pk)
                posts += thread.replies + 1
                thread.start_post.deleted = False
                thread.start_post.save(force_update=True)
                thread.last_post.set_checkpoint(self.request, 'undeleted')
        if undeleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + len(undeleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + posts
            self.forum.sync()
            self.forum.save(force_update=True)
            Post.objects.filter(id__in=last_posts).update(checkpoints=True)
            Thread.objects.filter(id__in=undeleted).update(deleted=False)
            self.request.messages.set_flash(Message(_('Selected threads have been undeleted.')), 'success', 'threads')

    def action_soft(self, ids):
        deleted = []
        last_posts = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids and not thread.deleted:
                deleted.append(thread.pk)
                posts += thread.replies + 1
                thread.start_post.deleted = True
                thread.start_post.save(force_update=True)
                thread.last_post.set_checkpoint(self.request, 'deleted')
                last_posts.append(thread.last_post.pk)
        if deleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) - len(deleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) - posts
            self.forum.sync()
            self.forum.save(force_update=True)
            Post.objects.filter(id__in=last_posts).update(checkpoints=True)
            Thread.objects.filter(id__in=deleted).update(deleted=True)
            self.request.messages.set_flash(Message(_('Selected threads have been softly deleted.')), 'success', 'threads')

    def action_hard(self, ids):
        deleted = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids:
                deleted.append(thread.pk)
                posts += thread.replies + 1
                thread.delete()
        if deleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) - len(deleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) - posts
            self.forum.sync()
            self.forum.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected threads have been deleted.')), 'success', 'threads')

    def __call__(self, request, slug=None, forum=None, page=0):
        self.request = request
        self.pagination = None
        self.parents = None
        self.message = request.messages.get_message('threads')
        try:
            self.fetch_forum(forum)
            self.fetch_threads(page)
            self.make_form()
            if self.form:
                response = self.handle_form()
                if response:
                    return response
        except Forum.DoesNotExist:
            return error404(request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        # Merge proxy into forum
        self.forum.closed = self.proxy.closed
        return request.theme.render_to_response('threads/list.html',
                                                {
                                                 'message': self.message,
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'count': self.count,
                                                 'list_form': FormFields(self.form).fields if self.form else None,
                                                 'threads': self.threads,
                                                 'pagination': self.pagination,
                                                 },
                                                context_instance=RequestContext(request));
