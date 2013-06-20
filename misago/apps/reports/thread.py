from django.utils.translation import ugettext as _
from misago.apps.threadtype.thread import ThreadBaseView, ThreadModeration, PostsModeration
from misago.messages import Message
from misago.models import Forum, Thread
from misago.apps.reports.mixins import TypeMixin

class ThreadView(ThreadBaseView, ThreadModeration, PostsModeration, TypeMixin):
    def posts_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
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
            if self.thread.weight != 1:
                actions.append(('sticky', _('Change to resolved')))
            if self.thread.weight != 0:
                actions.append(('normal', _('Change to bogus')))
            if acl['can_delete_threads']:
                if self.thread.deleted:
                    actions.append(('undelete', _('Restore this report')))
                else:
                    actions.append(('soft', _('Hide this report')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Delete this report')))
        except KeyError:
            pass
        return actions

    def after_thread_action_sticky(self):
        self.thread.set_checkpoint(self.request, 'resolved')
        self.request.messages.set_flash(Message(_('Report has been set as resolved.')), 'success', 'threads')

    def after_thread_action_normal(self):
        self.thread.set_checkpoint(self.request, 'bogus')
        self.request.messages.set_flash(Message(_('Report has been set as bogus.')), 'success', 'threads')

    def after_thread_action_undelete(self):
        self.request.messages.set_flash(Message(_('Report has been restored.')), 'success', 'threads')

    def after_thread_action_soft(self):
        self.request.messages.set_flash(Message(_('Report has been hidden.')), 'success', 'threads')

    def after_thread_action_hard(self):
        self.request.messages.set_flash(Message(_('Report "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
