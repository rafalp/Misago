from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import acl_errors
from misago.forums.models import Forum
from misago.threads.models import Thread, Post

@acl_errors
def threads(request, slug=None, forum=None, page=0):
    request.acl.forums.check_forum(forum)
    return request.theme.render_to_response('threads/list.html',
                                            context_instance=RequestContext(request));
    

@acl_errors
def thread(request, slug=None, thread=None, page=0):
    return request.theme.render_to_response('threads/thread.html',
                                            context_instance=RequestContext(request));
    

@acl_errors
def reply(request, slug=None, thread=None):
    return request.theme.render_to_response('threads/reply.html',
                                            context_instance=RequestContext(request));