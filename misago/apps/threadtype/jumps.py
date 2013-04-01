from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.decorators import block_guest, check_csrf
from misago.messages import Message
from misago.models import Forum, Thread, Post, Karma, WatchedThread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.utils.views import json_response
from misago.apps.threadtype.base import ViewBase

class JumpView(ViewBase):
    def fetch_thread(self, thread):
        self.thread = Thread.objects.get(pk=thread)
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

    def fetch_post(self, post):
        self.post = self.thread.post_set.get(pk=post)
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)

    def make_jump(self):
        raise NotImplementedError('JumpView cannot be called directly.')

    def __call__(self, request, slug=None, thread=None, post=None):
        self.request = request
        self.parents = []
        try:
            self._type_available()
            self.fetch_thread(thread)
            if self.forum.level:
                self.parents = Forum.objects.forum_parents(self.forum.pk, True)
            self.check_forum_type()
            self._check_permissions()
            if post:
                self.fetch_post(post)
            return self.make_jump()
        except (Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e)
        except ACLError404 as e:
            return error404(request, e)


class LastReplyBaseView(JumpView):
    def make_jump(self):
        return self.redirect_to_post(self.thread.post_set.order_by('-id')[:1][0])


class FindReplyBaseView(JumpView):
    def make_jump(self):
        return self.redirect_to_post(self.post)


class NewReplyBaseView(JumpView):
    def make_jump(self):
        if not self.request.user.is_authenticated():
            return self.redirect_to_post(self.thread.post_set.order_by('-id')[:1][0])
        tracker = ThreadsTracker(self.request, self.forum)
        read_date = tracker.read_date(self.thread)
        post = self.thread.post_set.filter(date__gt=read_date).order_by('id')[:1]
        if not post:
            return self.redirect_to_post(self.thread.post_set.order_by('-id')[:1][0])
        return self.redirect_to_post(post[0])


class FirstModeratedBaseView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_approve(self.forum):
            raise ACLError404()
        try:
            return self.redirect_to_post(
                self.thread.post_set.get(moderated=True))
        except Post.DoesNotExist:
            return error404(self.request)


class FirstReportedBaseView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_mod_posts(self.forum):
            raise ACLError404()
        try:
            return self.redirect_to_post(
                self.thread.post_set.get(reported=True))
        except Post.DoesNotExist:
            return error404(self.request)


class ShowHiddenRepliesBaseView(JumpView):
    def make_jump(self):
        @block_guest
        @check_csrf
        def view(request):
            ignored_exclusions = request.session.get('unignore_threads', [])
            ignored_exclusions.append(self.thread.pk)
            request.session['unignore_threads'] = ignored_exclusions
            request.messages.set_flash(Message(_('Replies made to this thread by members on your ignore list have been revealed.')), 'success', 'threads')
            return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
        return view(self.request)


class WatchThreadBaseView(JumpView):
    def get_retreat(self):
        return redirect(self.request.POST.get('retreat', reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug})))

    def update_watcher(self, request, watcher):
        request.messages.set_flash(Message(_('This thread has been added to your watched threads list.')), 'success', 'threads')

    def make_jump(self):
        @block_guest
        @check_csrf
        def view(request):
            try:
                watcher = WatchedThread.objects.get(user=request.user, thread=self.thread)
            except WatchedThread.DoesNotExist:
                watcher = WatchedThread()
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


class WatchEmailThreadBaseView(WatchThreadBaseView):
    def update_watcher(self, request, watcher):
        watcher.email = True
        if watcher.pk:
            request.messages.set_flash(Message(_('You will now receive e-mail with notification when somebody replies to this thread.')), 'success', 'threads')
        else:
            request.messages.set_flash(Message(_('This thread has been added to your watched threads list. You will also receive e-mail with notification when somebody replies to it.')), 'success', 'threads')


class UnwatchThreadBaseView(WatchThreadBaseView):
    def update_watcher(self, request, watcher):
        watcher.deleted = True
        watcher.delete()
        if watcher.email:
            request.messages.set_flash(Message(_('This thread has been removed from your watched threads list. You will no longer receive e-mails with notifications when somebody replies to it.')), 'success', 'threads')
        else:
            request.messages.set_flash(Message(_('This thread has been removed from your watched threads list.')), 'success', 'threads')


class UnwatchEmailThreadBaseView(WatchThreadBaseView):
    def update_watcher(self, request, watcher):
        watcher.email = False
        request.messages.set_flash(Message(_('You will no longer receive e-mails with notifications when somebody replies to this thread.')), 'success', 'threads')


class UpvotePostBaseView(JumpView):
    def make_jump(self):
        @block_guest
        @check_csrf
        def view(request):
            if self.post.user_id == request.user.id:
                return error404(request)
            self.check_acl(request)
            try:
                vote = Karma.objects.get(user=request.user, post=self.post)
                if self.thread.start_post_id == self.post.pk:
                    if vote.score > 0:
                        self.thread.upvotes -= 1
                    else:
                        self.thread.downvotes -= 1
                if vote.score > 0:
                    self.post.upvotes -= 1
                    request.user.karma_given_p -= 1
                    if self.post.user_id:
                        self.post.user.karma_p -= 1
                else:
                    self.post.downvotes -= 1
                    request.user.karma_given_n -= 1
                    if self.post.user_id:
                        self.post.user.karma_n -= 1
            except Karma.DoesNotExist:
                vote = Karma()
            vote.forum = self.forum
            vote.thread = self.thread
            vote.post = self.post
            vote.user = request.user
            vote.user_name = request.user.username
            vote.user_slug = request.user.username_slug
            vote.date = timezone.now()
            vote.ip = request.session.get_ip(request)
            vote.agent = request.META.get('HTTP_USER_AGENT')
            self.make_vote(request, vote)
            if vote.pk:
                vote.save(force_update=True)
            else:
                vote.save(force_insert=True)
            if self.thread.start_post_id == self.post.pk:
                if vote.score > 0:
                    self.thread.upvotes += 1
                else:
                    self.thread.downvotes += 1
                self.thread.save(force_update=True)
            if vote.score > 0:
                self.post.upvotes += 1
                request.user.karma_given_p += 1
                if self.post.user_id:
                    self.post.user.karma_p += 1
                    self.post.user.score += request.settings['score_reward_karma_positive']
            else:
                self.post.downvotes += 1
                request.user.karma_given_n += 1
                if self.post.user_id:
                    self.post.user.karma_n += 1
                    self.post.user.score -= request.settings['score_reward_karma_negative']
            self.post.save(force_update=True)
            request.user.save(force_update=True)
            if self.post.user_id:
                self.post.user.save(force_update=True)
            if request.is_ajax():
                return json_response(request, {
                                               'score_total': self.post.upvotes - self.post.downvotes,
                                               'score_upvotes': self.post.upvotes,
                                               'score_downvotes': self.post.downvotes,
                                               'user_vote': vote.score,
                                              })
            request.messages.set_flash(Message(_('Your vote has been saved.')), 'success', 'threads_%s' % self.post.pk)
            return self.redirect_to_post(self.post)
        return view(self.request)
    
    def check_acl(self, request):
        request.acl.threads.allow_post_upvote(self.forum)
    
    def make_vote(self, request, vote):
        vote.score = 1


class DownvotePostBaseView(UpvotePostBaseView):
    def check_acl(self, request):
        request.acl.threads.allow_post_downvote(self.forum)
    
    def make_vote(self, request, vote):
        vote.score = -1
