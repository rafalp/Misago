from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.markdown import post_markdown
from misago.models import Post
from misago.utils.datesformats import date
from misago.utils.translation import ugettext_lazy
from misago.apps.threadtype.posting.base import PostingBaseView
from misago.apps.threadtype.posting.forms import NewReplyForm

class NewReplyBaseView(PostingBaseView):
    action = 'new_reply'
    allow_quick_reply = True
    form_type = NewReplyForm

    def set_context(self):
        self.set_thread_context()
        self.request.acl.threads.allow_reply(self.proxy, self.thread)
        if self.kwargs.get('quote'):
            self.quote = Post.objects.get(id=self.kwargs.get('quote'))
            self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.quote)

    def form_initial_data(self):
        if self.quote:
            quote_post = []
            if self.quote.user:
                quote_post.append('@%s' % self.quote.user.username)
            else:
                quote_post.append('@%s' % self.quote.user_name)
            for line in self.quote.post.splitlines():
                quote_post.append('> %s' % line)
            quote_post.append('\r\n')
            return {'post': '\r\n'.join(quote_post)}
        return {}

    def post_form(self, form):
        now = timezone.now()
        moderation = (not self.request.acl.threads.acl[self.forum.pk]['can_approve']
                      and self.request.acl.threads.acl[self.forum.pk]['can_start_threads'] == 1)

        self.thread.previous_last = self.thread.last
        self.md, post_preparsed = post_markdown(self.request, form.cleaned_data['post'])

        # Count merge diff and see if we are merging
        merge_diff = (now - self.thread.last)
        merge_diff = (merge_diff.days * 86400) + merge_diff.seconds
        if (self.request.settings.post_merge_time
                and merge_diff < (self.request.settings.post_merge_time * 60)
                and self.thread.last_poster_id == self.request.user.id
                and self.thread.last_post.moderated == moderation):
            merged = True
            self.post = self.thread.last_post
            self.post.date = now
            self.post.post = '%s\n\n- - -\n**%s**\n%s' % (self.post.post, _("Added on %(date)s:") % {'date': date(now, 'SHORT_DATETIME_FORMAT')}, form.cleaned_data['post'])
            self.md, self.post.post_preparsed = post_markdown(self.request, self.post.post)
            self.post.save(force_update=True)
        else:
            # Create new post
            merged = False
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
                                            merge=self.thread.merges,
                                            moderated=moderation,
                                        )

        # Update thread data and score?
        if not merged:
            if not moderation:
                self.thread.new_last_post(self.post)
                self.thread.replies += 1
            else:
                self.thread.replies_moderated += 1

            # Increase thread score
            if self.thread.last_poster_id != self.request.user.pk:
                self.thread.score += self.request.settings['thread_ranking_reply_score']

        # Set thread status
        if 'close_thread' in form.cleaned_data:
            self.thread.closed = form.cleaned_data['close_thread']
        if 'thread_weight' in form.cleaned_data:
            self.thread.weight = form.cleaned_data['thread_weight']

        # Save updated thread
        self.thread.save(force_update=True)

        # Update forum and monitor
        if not moderation and not merged:
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + 1
            self.forum.posts += 1
            self.forum.new_last_thread(self.thread)
            self.forum.save(force_update=True)
        
        # Reward user for posting new reply?
        if not moderation and not merged and (not self.request.user.last_post
                or self.request.user.last_post < timezone.now() - timedelta(seconds=self.request.settings['score_reward_new_post_cooldown'])):
            self.request.user.score += self.request.settings['score_reward_new_post']

        # Update user
        if not moderation and not merged:
            self.request.user.threads += 1
            self.request.user.posts += 1
        self.request.user.last_post = now
        self.request.user.save(force_update=True)

        # Set "closed" checkpoint, either due to thread limit or posters wish
        if (self.request.settings.thread_length > 0
                and not merged and not moderation and not self.thread.closed
                and self.thread.replies >= self.request.settings.thread_length):
            self.thread.closed = True
            self.post.set_checkpoint(self.request, 'limit')
        elif 'close_thread' in form.cleaned_data and form.cleaned_data['close_thread']:
            if self.thread.closed:
                self.thread.last_post.set_checkpoint(self.request, 'closed')
            else:
                self.thread.last_post.set_checkpoint(self.request, 'opened')

        # Notify user we quoted?
        if (self.quote and self.quote.user_id and not merged
                and self.quote.user_id != self.request.user.pk
                and not self.quote.user.is_ignoring(self.request.user)):
            alert = self.quote.user.alert(ugettext_lazy("%(username)s has replied to your post in thread %(thread)s").message)
            alert.profile('username', self.request.user)
            alert.post('thread', self.type_prefix, self.thread, self.post)
            alert.save_all()

        # E-mail users about new response
        self.thread.email_watchers(self.request, self.type_prefix, self.post)