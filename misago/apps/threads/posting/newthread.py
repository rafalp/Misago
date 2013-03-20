from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from itertools import chain
from misago.apps.forumbase.mixins import RedirectToPostMixin
from misago.apps.forumbase.posting import PostingBaseView
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.utils.strings import slugify
from misago.apps.threads.forms import NewThreadForm
from misago.apps.threads.mixins import TypeMixin

class NewThreadView(PostingBaseView, TypeMixin, RedirectToPostMixin):
    action = 'new_thread'
    form_type = NewThreadForm

    def set_context(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')
        self.request.acl.forums.allow_forum_view(self.forum)
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.threads.allow_new_threads(self.proxy)

    def post_form(self, form):
        now = timezone.now()
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
                                            score=self.request.settings['thread_ranking_initial_score'],
                                            replies=1,
                                            replies_moderated=int(moderation),
                                            )

        # Create our post
        md, post_preparsed = post_markdown(self.request, form.cleaned_data['post'])
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
            self.thread.closed = True
        if 'thread_weight' in form.cleaned_data:
            self.thread.weight = form.cleaned_data['thread_weight']

        # Finally save complete thread
        self.thread.save(force_update=True)

        # Reward user for posting new thread?
        if (not self.request.user.last_post
                or self.request.user.last_post < timezone.now() - timedelta(seconds=self.request.settings['score_reward_new_post_cooldown'])):
            self.request.user.score += self.request.settings['score_reward_new_thread']

        # Update forum monitor
        if not moderation:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + 1
            self.forum.threads += 1
            self.forum.posts += 1
            self.forum.new_last_thread(self.thread)
            self.forum.save(force_update=True)

        # Update user
        if not moderation:
            self.request.user.threads += 1
            self.request.user.posts += 1
            self.request.user.last_post = now
            self.request.user.save(force_update=True)

        # Notify mentioned
        if md.mentions:
            self.post.notify_mentioned(self.request, md.mentions)
            self.post.save(force_update=True)

        # Set thread watch status
        self.watch_thread()

        # Set flash and redirect user to his post
        if moderation:
            self.request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))
