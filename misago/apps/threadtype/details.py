from django.template import RequestContext
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.models import Forum, Thread, Post
from misago.shortcuts import render_to_response
from misago.apps.threadtype.base import ViewBase

class ExtraBaseView(ViewBase):
    def fetch_target(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        self.check_forum_type()
        self.post = Post.objects.select_related('user').get(pk=self.kwargs.get('post'), thread=self.thread.pk)
        self.post.thread = self.thread
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.forum = None
        self.thread = None
        self.post = None
        self.parents = []
        try:
            self._type_available()
            self.fetch_target()
            self.check_acl()
            self._check_permissions()
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e)
        except ACLError404 as e:
            return error404(request, e)
        return self.response()


class DetailsBaseView(ExtraBaseView):
    def check_acl(self):
        self.request.acl.users.allow_details_view()

    def response(self):
        return render_to_response('%ss/details.html' % self.type_prefix,
                                  self.template_vars({
                                      'type_prefix': self.type_prefix,
                                      'forum': self.forum,
                                      'parents': self.parents,
                                      'thread': self.thread,
                                      'post': self.post,
                                      }),
                                  context_instance=RequestContext(self.request))


class KarmaVotesBaseView(ExtraBaseView):
    def check_acl(self):
        self.request.acl.threads.allow_post_votes_view(self.forum)

    def response(self):
        return render_to_response('%ss/karmas.html' % self.type_prefix,
                                  self.template_vars({
                                      'type_prefix': self.type_prefix,
                                      'forum': self.forum,
                                      'parents': self.parents,
                                      'thread': self.thread,
                                      'post': self.post,
                                      'upvotes': self.post.karma_set.filter(score=1),
                                      'downvotes': self.post.karma_set.filter(score=-1),
                                      }),
                                  context_instance=RequestContext(self.request))