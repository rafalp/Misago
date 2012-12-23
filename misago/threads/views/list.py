from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.readstracker.trackers import ForumsTracker, ThreadsTracker
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination

class ThreadsView(BaseView):
    def fetch_forum(self, forum):
        self.forum = Forum.objects.get(pk=forum, type='forum')
        self.request.acl.forums.allow_forum_view(self.forum)
        self.parents = self.forum.get_ancestors().filter(level__gt=1)
        self.forum.subforums = Forum.objects.treelist(self.request.acl.forums, self.forum, tracker=ForumsTracker(self.request.user))
        self.tracker = ThreadsTracker(self.request.user, self.forum)
                
    def fetch_threads(self, page):
        self.count = Thread.objects.filter(forum=self.forum).count()
        self.threads = Thread.objects.filter(forum=self.forum).order_by('-weight', '-last').all()
        self.pagination = make_pagination(page, self.count, self.request.settings.threads_per_page)
        if self.request.settings.threads_per_page < self.count:
            self.threads = self.threads[self.pagination['start']:self.pagination['stop']]
        for thread in self.threads:
            thread.is_read = self.tracker.is_read(thread)
    
    def __call__(self, request, slug=None, forum=None, page=0):
        self.request = request
        self.pagination = None
        self.parents = None
        try:
            self.fetch_forum(forum)
            self.fetch_threads(page)
        except Forum.DoesNotExist:
            return error404(self.request)
        except ACLError403 as e:
            return error403(args[0], e.message)
        except ACLError404 as e:
            return error404(args[0], e.message)
        return request.theme.render_to_response('threads/list.html',
                                                {
                                                 'message': request.messages.get_message('threads'),
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'count': self.count,
                                                 'threads': self.threads,
                                                 'pagination': self.pagination,
                                                 },
                                                context_instance=RequestContext(request));