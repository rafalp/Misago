from django.template import RequestContext
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import FormFields
from misago.models import Forum
from misago.readstrackers import ForumsTracker, ThreadsTracker

class ThreadsListBaseView(object):
    def _fetch_forum(self):
        self.fetch_forum()
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)
        if self.forum.lft + 1 != self.forum.rght:
            self.forum.subforums = Forum.objects.treelist(self.request.acl.forums, self.forum, tracker=ForumsTracker(self.request.user))
        self.tracker = ThreadsTracker(self.request, self.forum)
    
    def __new__(cls, request, **kwargs):
        obj = super(ThreadsListBaseView, cls).__new__(cls)
        return obj(request, **kwargs)

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.pagination = {}
        self.parents = []
        self.message = request.messages.get_message('threads')
        try:
            self._fetch_forum()
            self.fetch_threads()
            self.form = None
            #self.make_form()
            #if self.form:
            #    response = self.handle_form()
            #    if response:
            #        return response
        except Forum.DoesNotExist:
            return error404(request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        # Merge proxy into forum
        self.forum.closed = self.proxy.closed
        return request.theme.render_to_response(('%s/list.html' % self.templates_prefix),
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