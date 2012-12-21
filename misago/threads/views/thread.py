from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forums.models import Forum
from misago.threads.models import Thread, Post

class Thread(object):
    def __call__(self, request, slug=None, forum=None, page=0):
        return request.theme.render_to_response('threads/thread.html',
                                        context_instance=RequestContext(request));