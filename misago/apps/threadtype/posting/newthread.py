from datetime import timedelta
from django.utils import timezone
from misago.apps.threadtype.posting.base import PostingBaseView
from misago.apps.threadtype.posting.forms import NewThreadForm
from misago.conf import settings
from misago.markdown import post_markdown
from misago.models import Forum, Thread, Post
from misago.monitor import monitor, UpdatingMonitor
from misago.utils.strings import slugify

class NewThreadBaseView(PostingBaseView):
    action = 'new_thread'
    form_type = NewThreadForm

    def set_context(self):
        self.set_forum_context()
        self.request.acl.forums.allow_forum_view(self.forum)
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.threads.allow_new_threads(self.proxy)

    def post_form(self, form):
        now = timezone.now()

        if self.force_moderation():
            moderation = True
        else:
            moderation = (not self.request.acl.threads.acl[self.forum.pk]['can_approve']
                          and self.request.acl.threads.acl[self.forum.pk]['can_start_threads'] == 1)

        # Create empty thread
        self.thread = Thread.objects.create(
                                            forum=self.forum,
                                            name=form.cleaned_data['thread_name'],
                                            slug=slugify(form.cleaned_data['thread_name']),
                                            start=now,
                                            last=now,
                                            moderated=moderation,
                                            score=settings.thread_ranking_initial_score,
                                            )

        # Create our post
        self.md, post_preparsed = post_markdown(form.cleaned_data['post'])
        self.post = Post.objects.create(
                                        forum=self.forum,
                                        thread=self.thread,
                                        user=self.request.user,
                                        user_name=self.request.user.username,
                                        ip=self.request.session.get_ip(self.request),
                                        agent=self.request.META.get('HTTP_USER_AGENT'),
                                        post=form.cleaned_data['post'],
                                        post_preparsed=post_preparsed,
                                        date=now,
                                        moderated=moderation,
                                        )

        # Update thread stats to contain this post
        self.thread.new_start_post(self.post)
        self.thread.new_last_post(self.post)

        # Set thread status
        if 'close_thread' in form.cleaned_data:
            self.thread.closed = form.cleaned_data['close_thread']
        if 'thread_weight' in form.cleaned_data:
            self.thread.weight = form.cleaned_data['thread_weight']

        # Finally save complete thread
        self.thread.save(force_update=True)

        # Update forum monitor
        if not moderation:
            with UpdatingMonitor() as cm:
                monitor.increase('threads')
                monitor.increase('posts')
            self.forum.threads += 1
            self.forum.posts += 1
            self.forum.new_last_thread(self.thread)
            self.forum.save(force_update=True)

        # Reward user for posting new thread?
        if not moderation and (not self.request.user.last_post
                or self.request.user.last_post < timezone.now() - timedelta(seconds=settings.score_reward_new_post_cooldown)):
            self.request.user.score += settings.score_reward_new_thread

        # Update user
        if not moderation:
            self.request.user.threads += 1
            self.request.user.posts += 1
        self.request.user.last_post = now
        self.request.user.save(force_update=True)

    def watch_thread(self):
        if self.request.user.subscribe_start:
            self.start_watching_thread(
                self.request.user.subscribe_start == 2)