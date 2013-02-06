from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.authn.decorators import block_guest
from misago.csrf.decorators import check_csrf
from misago.forums.models import Forum
from misago.messages import Message
from misago.readstracker.trackers import ThreadsTracker
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination
from misago.watcher.models import ThreadWatch

class JumpView(BaseView):
    def fetch_thread(self, thread):
        self.thread = Thread.objects.get(pk=thread)
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

    def fetch_post(self, post):
        self.post = self.thread.post_set.get(pk=post)
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)

    def redirect(self, post):
        pagination = make_pagination(0, self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set.filter(date__lt=post.date)).count() + 1, self.request.settings.posts_per_page)
        if pagination['total'] > 1:
            return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % post.pk))
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))

    def make_jump(self):
        raise NotImplementedError('JumpView cannot be called directly.')

    def __call__(self, request, slug=None, thread=None, post=None):
        self.request = request
        try:
            self.fetch_thread(thread)
            if post:
                self.fetch_post(post)
            return self.make_jump()
        except (Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)


class LastReplyView(JumpView):
    def make_jump(self):
        return self.redirect(self.thread.post_set.order_by('-id')[:1][0])


class FindReplyView(JumpView):
    def make_jump(self):
        return self.redirect(self.post)


class NewReplyView(JumpView):
    def make_jump(self):
        if not self.request.user.is_authenticated():
            return self.redirect(self.thread.post_set.order_by('-id')[:1][0])
        tracker = ThreadsTracker(self.request, self.forum)
        read_date = tracker.get_read_date(self.thread)
        post = self.thread.post_set.filter(date__gt=read_date).order_by('id')[:1]
        if not post:
            return self.redirect(self.thread.post_set.order_by('-id')[:1][0])
        return self.redirect(post[0])


class FirstModeratedView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_approve(self.forum):
            raise ACLError404()
        try:
            return self.redirect(
                self.thread.post_set.get(moderated=True))
        except Post.DoesNotExist:
            return error404(self.request)


class FirstReportedView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_mod_posts(self.forum):
            raise ACLError404()
        try:
            return self.redirect(
                self.thread.post_set.get(reported=True))
        except Post.DoesNotExist:
            return error404(self.request)


class ShowHiddenRepliesView(JumpView):
    def make_jump(self):
        @block_guest
        @check_csrf
        def view(request):
            ignored_exclusions = request.session.get('unignore_threads', [])
            ignored_exclusions.append(self.thread.pk)
            request.session['unignore_threads'] = ignored_exclusions
            request.messages.set_flash(Message(_('Replies made to this thread by members on your ignore list have been revealed.')), 'success', 'threads')
            return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
        return view(self.request)


class WatchThreadView(JumpView):
    def get_retreat(self):
        return redirect(self.request.POST.get('retreat', reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug})))
    
    def update_watcher(self, request, watcher):
        request.messages.set_flash(Message(_('This thread has been added to your watched threads list.')), 'success', 'threads')
    
    def make_jump(self):
        @block_guest
        @check_csrf
        def view(request):
            try:
                watcher = ThreadWatch.objects.get(user=request.user, thread=self.thread)
            except ThreadWatch.DoesNotExist:
                watcher = ThreadWatch()
                watcher.user = request.user
                watcher.forum = self.forum
                watcher.thread = self.thread
                watcher.last_read = timezone.now()
            self.update_watcher(request, watcher)
            if watcher.pk:
                watcher.save(force_update=True)
            else:
                watcher.save(force_insert=True)
            return self.get_retreat()
        return view(self.request)


class WatchEmailThreadView(WatchThreadView):
    def update_watcher(self, request, watcher):
        watcher.email = True
        if watcher.pk:
            request.messages.set_flash(Message(_('You will now receive e-mail with notification when somebody replies to this thread.')), 'success', 'threads')
        else:
            request.messages.set_flash(Message(_('This thread has been added to your watched threads list. You will also receive e-mail with notification when somebody replies to it.')), 'success', 'threads')


class UnwatchThreadView(WatchThreadView):
    def update_watcher(self, request, watcher):
        watcher.deleted = True
        watcher.delete()
        if watcher.email:
            request.messages.set_flash(Message(_('This thread has been removed from your watched threads list. You will no longer receive e-mails with notifications when somebody replies to it.')), 'success', 'threads')
        else:
            request.messages.set_flash(Message(_('This thread has been removed from your watched threads list.')), 'success', 'threads')


class UnwatchEmailThreadView(WatchThreadView):
    def update_watcher(self, request, watcher):
        watcher.email = False
        request.messages.set_flash(Message(_('You will no longer receive e-mails with notifications when somebody replies to this thread.')), 'success', 'threads')
