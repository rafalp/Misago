from django.template import RequestContext
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.models import Forum, Thread, Post
from misago.apps.threads.views.base import BaseView

class KarmaVotesView(BaseView):
    def fetch_target(self, kwargs):
        self.thread = Thread.objects.get(pk=kwargs['thread'])
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        self.post = Post.objects.select_related('user').get(pk=kwargs['post'], thread=self.thread.pk)
        self.post.thread = self.thread
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_post_votes_view(self.forum)

    def __call__(self, request, **kwargs):
        self.request = request
        self.forum = None
        self.thread = None
        self.post = None
        try:
            self.fetch_target(kwargs)
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        return request.theme.render_to_response('threads/karmas.html',
                                                {
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'post': self.post,
                                                 'upvotes': self.post.karma_set.filter(score=1),
                                                 'downvotes': self.post.karma_set.filter(score=-1),
                                                 },
                                                context_instance=RequestContext(request))