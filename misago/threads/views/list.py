from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404

class List(BaseView):
    def fetch_forum(self, forum):
        self.forum = Forum.objects.get(pk=forum, type='forum')
        self.request.acl.forums.check_forum(self.forum)
        
    def fetch_threads(self, page):
        self.threads = Thread.objects.filter(forum=self.forum).order_by('-last').all()
    
    def __call__(self, request, slug=None, forum=None, page=0):
        self.request = request
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
                                                 'threads': self.threads,
                                                 },
                                                context_instance=RequestContext(request));