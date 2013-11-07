from django.utils.translation import ugettext as _
from misago.apps.threadtype.thread import ThreadBaseView, ThreadModeration, PostsModeration
from misago.models import Forum, Thread, ThreadPrefix
from misago.apps.threads.forms import PollVoteForm
from misago.apps.threads.mixins import TypeMixin

class ThreadView(ThreadBaseView, ThreadModeration, PostsModeration, TypeMixin):
    def template_vars(self, context):
        prefixes = ThreadPrefix.objects.forum_prefixes(self.forum)
        if self.thread.prefix_id in prefixes:
            context['prefix'] = prefixes[self.thread.prefix_id]

        self.add_poll(context)
        return super(ThreadView, self).template_vars(context)

    def add_poll(self, context):
        context['poll'] = None
        context['poll_form'] = None
        if self.thread.has_poll:
            context['poll'] = self.thread.poll
            self.thread.poll.message = self.request.messages.get_message('poll_%s' % self.thread.poll.pk)
            if self.request.user.is_authenticated():
                self.thread.poll.user_votes = [x.option_id for x in self.request.user.pollvote_set.filter(poll=self.thread.poll)]
                if self.request.acl.threads.can_vote_in_polls(self.forum, self.thread, self.thread.poll):
                    context['poll_form'] = PollVoteForm(request=self.request, poll=self.thread.poll)

    def posts_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_approve'] and self.thread.replies_moderated > 0:
                actions.append(('accept', _('Accept posts')))
            if acl['can_move_threads_posts']:
                actions.append(('merge', _('Merge posts into one')))
                actions.append(('split', _('Split posts to new thread')))
                actions.append(('move', _('Move posts to other thread')))
            if acl['can_protect_posts']:
                actions.append(('protect', _('Protect posts')))
                actions.append(('unprotect', _('Remove posts protection')))
            if acl['can_delete_posts']:
                if self.thread.replies_deleted > 0:
                    actions.append(('undelete', _('Restore posts')))
                actions.append(('soft', _('Hide posts')))
            if acl['can_delete_posts'] == 2:
                actions.append(('hard', _('Delete posts')))
        except KeyError:
            pass
        return actions

    def thread_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_approve'] and self.thread.moderated:
                actions.append(('accept', _('Accept this thread')))
            if acl['can_pin_threads'] == 2 and self.thread.weight < 2:
                actions.append(('annouce', _('Change this thread to announcement')))
            if acl['can_pin_threads'] > 0 and self.thread.weight != 1:
                actions.append(('sticky', _('Change this thread to sticky')))
            if acl['can_pin_threads'] > 0:
                if self.thread.weight == 2:
                    actions.append(('normal', _('Change this thread to normal')))
                if self.thread.weight == 1:
                    actions.append(('normal', _('Unpin this thread')))
            if acl['can_move_threads_posts']:
                actions.append(('move', _('Move this thread')))
            if acl['can_close_threads']:
                if self.thread.closed:
                    actions.append(('open', _('Open this thread')))
                else:
                    actions.append(('close', _('Close this thread')))
            if acl['can_delete_threads']:
                if self.thread.deleted:
                    actions.append(('undelete', _('Restore this thread')))
                else:
                    actions.append(('soft', _('Hide this thread')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Delete this thread')))
        except KeyError:
            pass
        return actions