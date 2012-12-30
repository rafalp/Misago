from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import FormFields
from misago.forums.models import Forum
from misago.readstracker.trackers import ThreadsTracker
from misago.threads.forms import QuickReplyForm
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination

class ThreadView(BaseView):
    def fetch_thread(self, thread):
        self.thread = Thread.objects.get(pk=thread)
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        self.tracker = ThreadsTracker(self.request.user, self.forum)
    
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
        self.read_date = self.tracker.get_read_date(self.thread) 
        for post in self.posts:
            post.message = self.request.messages.get_message('threads_%s' % post.pk)
            post.is_read = post.date <= self.read_date
        last_post = self.posts[len(self.posts) - 1]
        if not self.tracker.is_read(self.thread):
            self.tracker.set_read(self.thread, last_post)
            self.tracker.sync()
     
    def __call__(self, request, slug=None, thread=None, page=0):
        self.request = request
        self.pagination = None
        self.parents = None
        try:
            self.fetch_thread(thread)
            self.fetch_posts(page)
        except Thread.DoesNotExist:
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        return request.theme.render_to_response('threads/thread.html',
                                                {
                                                 'message': request.messages.get_message('threads'),
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'is_read': self.tracker.is_read(self.thread),
                                                 'count': self.count,
                                                 'posts': self.posts,
                                                 'pagination': self.pagination,
                                                 'quick_reply': FormFields(QuickReplyForm(request=request)).fields
                                                 },
                                                context_instance=RequestContext(request));