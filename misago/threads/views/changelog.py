import difflib
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.markdown import post_markdown
from misago.messages import Message
from misago.threads.models import Thread, Post, Change
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination, slugify

class ChangelogBaseView(BaseView):
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
        self.request.acl.threads.allow_changelog_view(self.request.user, self.forum, self.post)

    def dispatch(self, request, **kwargs):
        raise NotImplementedError('ChangelogBaseView cannot be called directly. Did you forget to define custom "dispatch" method?')

    def __call__(self, request, **kwargs):
        self.request = request
        self.forum = None
        self.thread = None
        self.post = None
        try:
            self.fetch_target(kwargs)
            if not request.user.is_authenticated():
                raise ACLError403(_("Guest, you have to sign-in in order to see posts changelogs."))
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist, Change.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        return self.dispatch(request, **kwargs)


class ChangelogView(ChangelogBaseView):
    def dispatch(self, request, **kwargs):
        return request.theme.render_to_response('threads/changelog.html',
                                                {
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'post': self.post,
                                                 'edits': self.post.change_set.prefetch_related('user').order_by('-id')
                                                 },
                                                context_instance=RequestContext(request))


class ChangelogDiffView(ChangelogBaseView):
    def fetch_target(self, kwargs):
        super(ChangelogDiffView, self).fetch_target(kwargs)
        self.change = self.post.change_set.get(pk=kwargs['change'])

    def dispatch(self, request, **kwargs):
        try:
            next = self.post.change_set.filter(id__gt=self.change.pk)[:1][0]
        except IndexError:
            next = None
        try:
            prev = self.post.change_set.filter(id__lt=self.change.pk).order_by('-id')[:1][0]
        except IndexError:
            prev = None
        self.forum.closed = self.proxy.closed
        return request.theme.render_to_response('threads/changelog_diff.html',
                                                {
                                                 'forum': self.forum,
                                                 'parents': self.parents,
                                                 'thread': self.thread,
                                                 'post': self.post,
                                                 'change': self.change,
                                                 'next': next,
                                                 'prev': prev,
                                                 'message': request.messages.get_message('changelog'),
                                                 'l': 1,
                                                 'diff': difflib.ndiff(self.change.post_content.splitlines(), self.post.post.splitlines()),
                                                 },
                                                context_instance=RequestContext(request))


class ChangelogRevertView(ChangelogDiffView):
    def fetch_target(self, kwargs):
        super(ChangelogDiffView, self).fetch_target(kwargs)
        self.change = self.post.change_set.get(pk=kwargs['change'])
        self.request.acl.threads.allow_revert(self.proxy, self.thread)

    def dispatch(self, request, **kwargs):
        if ((not self.change.thread_name_old or self.thread.name == self.change.thread_name_old)
            and (self.change.post_content == self.post.post)):
            request.messages.set_flash(Message(_("No changes to revert.")), 'error', 'changelog')
            return redirect(reverse('changelog_diff', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'post': self.post.pk, 'change': self.change.pk}))

        if self.change.thread_name_old and self.change.thread_name_old != self.thread.name:
            self.thread.name = self.change.thread_name_old
            self.thread.slug = slugify(self.change.thread_name_old)
            self.thread.save(force_update=True)

            if self.forum.last_thread_id == self.thread.pk:
                self.forum.last_thread_name = self.change.thread_name_old
                self.forum.last_thread_slug = slugify(self.change.thread_name_old)
                self.forum.save(force_update=True)

        if self.change.post_content != self.post.post:
            self.post.post = self.change.post_content
            md, self.post.post_preparsed = post_markdown(request, self.change.post_content)
            self.post.save(force_update=True)

        request.messages.set_flash(Message(_("Post has been reverted previous state.")), 'success', 'threads_%s' % self.post.pk)
        pagination = make_pagination(0, request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set).filter(id__lte=self.post.pk).count(), self.request.settings.posts_per_page)
        if pagination['total'] > 1:
            return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % self.post.pk))
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))
