from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forums.models import Forum
from misago.threads.models import Thread, Post

class List(object):
    def fetch_forum(self, forum):
        pass
    
    def __call__(self, request, slug=None, forum=None, page=0):
        self.request = request
        try:
            self.fetch_forum(forum)
            self.fetch_threads(forum, page)
        except MehEception as e:
            pass
        return request.theme.render_to_response('threads/list.html',
                                        context_instance=RequestContext(request));