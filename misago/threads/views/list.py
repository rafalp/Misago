from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import FormLayout, FormFields
from misago.forums.models import Forum
from misago.messages import Message
from misago.readstracker.trackers import ForumsTracker, ThreadsTracker
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.threads.views.mixins import ThreadsFormMixin
from misago.views import error403, error404
from misago.utils import make_pagination

class ThreadsView(BaseView, ThreadsFormMixin):
    def fetch_forum(self, forum):
        self.forum = Forum.objects.get(pk=forum, type='forum')
        self.request.acl.forums.allow_forum_view(self.forum)
        self.parents = self.forum.get_ancestors().filter(level__gt=1)
        if self.forum.lft + 1 != self.forum.rght:
            self.forum.subforums = Forum.objects.treelist(self.request.acl.forums, self.forum, tracker=ForumsTracker(self.request.user))
        self.tracker = ThreadsTracker(self.request.user, self.forum)
                
    def fetch_threads(self, page):
        self.count = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum)).count()
        self.threads = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum)).order_by('-weight', '-last')
        self.pagination = make_pagination(page, self.count, self.request.settings.threads_per_page)
        if self.request.settings.threads_per_page < self.count:
            self.threads = self.threads[self.pagination['start']:self.pagination['stop']]
        for thread in self.threads:
            thread.is_read = self.tracker.is_read(thread)
    
    def get_thread_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            if acl['can_approve']:
               actions.append(('accept', _('Accept threads')))
            if acl['can_make_annoucements']:
               actions.append(('annouce', _('Change to annoucements')))
            if acl['can_pin_threads']:
               actions.append(('sticky', _('Change to sticky threads')))
            if acl['can_make_annoucements'] or acl['can_pin_threads']:
               actions.append(('normal', _('Change to standard thread')))
            if acl['can_move_threads_posts']:
               actions.append(('move', _('Move threads')))
               actions.append(('merge', _('Merge threads')))
            if acl['can_close_threads']:
               actions.append(('open', _('Open threads')))
               actions.append(('close', _('Close threads')))
            if acl['can_delete_threads']:
               actions.append(('undelete', _('Undelete threads')))
            if acl['can_delete_threads']:
               actions.append(('soft', _('Soft delete threads')))
            if acl['can_delete_threads'] == 2:
               actions.append(('hard', _('Hard delete threads')))
        except KeyError:
            pass
        return actions
    
    def action_accept(self, ids, threads):
        accepted = 0
        users = []
        for thread in self.threads.prefetch_related('last_post', 'last_post__user').all():
            if thread.pk in ids and thread.moderated:
                accepted += 1
                # Sync thread and post
                thread.moderated = False
                thread.replies_moderated -= 1
                thread.save(force_update=True)
                thread.last_post.moderated = False
                thread.last_post.save(force_update=True)
                # Sync user
                if thread.last_post.user:
                    thread.last_post.user.threads += 1
                    thread.last_post.user.posts += 1
                    users.append(thread.last_post.user)
                # Sync forum
                self.forum.threads += 1
                self.forum.threads_delta += 1
                self.forum.posts += 1
                self.forum.posts_delta += 1
                if not self.forum.last_thread_date or self.forum.last_thread_date < thread.last:
                    self.forum.last_thread = thread
                    self.forum.last_thread_name = thread.name
                    self.forum.last_thread_slug = thread.slug
                    self.forum.last_thread_date = thread.last
                    self.forum.last_poster = thread.last_poster
                    self.forum.last_poster_name = thread.last_poster_name
                    self.forum.last_poster_slug = thread.last_poster_slug
                    self.forum.last_poster_style = thread.last_poster_style
        if accepted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + accepted
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + accepted
            self.forum.save(force_update=True)
            for user in users:
                user.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected threads have been marked as reviewed and made visible to other members.')), 'success', 'threads')
    
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