import difflib
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, Thread, Post, Change
from misago.shortcuts import render_to_response
from misago.utils.datesformats import reldate
from misago.utils.strings import slugify
from misago.apps.threadtype.base import ViewBase

class ChangelogBaseView(ViewBase):
    def fetch_target(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        self.check_forum_type()
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.post = Post.objects.select_related('user').get(pk=self.kwargs.get('post'), thread=self.thread.pk)
        self.post.thread = self.thread
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_changelog_view(self.request.user, self.forum, self.post)

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
            self._check_permissions()
            if not request.user.is_authenticated():
                raise ACLError403(_("Guest, you have to sign-in in order to see posts changelogs."))
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist, Change.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e)
        except ACLError404 as e:
            return error404(request, e)
        return self.dispatch(request)


class ChangelogChangesBaseView(ChangelogBaseView):
    def dispatch(self, request, **kwargs):
        return render_to_response('%ss/changelog.html' % self.type_prefix,
                                  self.template_vars({
                                      'type_prefix': self.type_prefix,
                                      'forum': self.forum,
                                      'parents': self.parents,
                                      'thread': self.thread,
                                      'post': self.post,
                                      'edits': self.post.change_set.prefetch_related('user').order_by('-id')
                                      }),
                                  context_instance=RequestContext(request))


class ChangelogDiffBaseView(ChangelogBaseView):
    def fetch_target(self):
        super(ChangelogDiffBaseView, self).fetch_target()
        self.change = self.post.change_set.get(pk=self.kwargs.get('change'))

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
        return render_to_response('%ss/changelog_diff.html' % self.type_prefix,
                                  self.template_vars({
                                      'type_prefix': self.type_prefix,
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
                                      }),
                                  context_instance=RequestContext(request))


class ChangelogRevertBaseView(ChangelogDiffBaseView):
    def fetch_target(self):
        super(ChangelogRevertBaseView, self).fetch_target()
        self.change = self.post.change_set.get(pk=self.kwargs.get('change'))
        self.request.acl.threads.allow_revert(self.proxy, self.thread)

    def dispatch(self, request, **kwargs):
        if ((not self.change.thread_name_old or self.thread.name == self.change.thread_name_old)
            and (self.change.post_content == self.post.post)):
            request.messages.set_flash(Message(_("No changes to revert.")), 'error', 'changelog')
            return redirect(reverse('%s_changelog_diff' % self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'post': self.post.pk, 'change': self.change.pk}))

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
            md, self.post.post_preparsed = post_markdown(self.change.post_content)
            self.post.save(force_update=True)

        request.messages.set_flash(Message(_("Post has been reverted to state from %(date)s.") % {'date': reldate(self.change.date).lower()}), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
