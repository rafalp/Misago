from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import FormFields
from misago.forums.models import Forum
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
        self.request.acl.threads.allow_thread_view(self.thread)
        self.parents = self.forum.get_ancestors(include_self=True).filter(level__gt=1)
    
    def fetch_posts(self, page):
        self.count = Post.objects.filter(thread=self.thread).count()
        self.posts = Post.objects.filter(thread=self.thread).order_by('pk').all()
        self.pagination = make_pagination(page, self.count, self.request.settings.posts_per_page)
        if self.request.settings.threads_per_page < self.count:
            self.posts = self.posts[self.pagination['start']:self.pagination['stop']]
        self.posts.prefetch_related('user', 'user__rank')
        
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
            return error403(args[0], e.message)
        except ACLError404 as e:
            return error404(args[0], e.message)
        return request.theme.render_to_response('threads/thread.html',
                                                {
                                                 'message': request.messages.get_message('threads'),
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'count': self.count,
                                                 'posts': self.posts,
                                                 'pagination': self.pagination,
                                                 'quick_reply': FormFields(QuickReplyForm(request=request)).fields
                                                 },
                                                context_instance=RequestContext(request));