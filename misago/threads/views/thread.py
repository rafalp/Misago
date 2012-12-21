from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404

class Thread(BaseView):
    def __call__(self, request, slug=None, forum=None, page=0):
        return request.theme.render_to_response('threads/thread.html',
                                        context_instance=RequestContext(request));