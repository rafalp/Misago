from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forums.models import Forum
from misago.threads.models import Thread, Post

class Posting(object):
    def __call__(self, request):
        return request.theme.render_to_response('threads/posting.html',
                                            context_instance=RequestContext(request));