from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.models import User
from misago.apps.threadtype.jumps import *
from misago.apps.privatethreads.mixins import TypeMixin

class LastReplyView(LastReplyBaseView, TypeMixin):
    pass


class FindReplyView(FindReplyBaseView, TypeMixin):
    pass


class NewReplyView(NewReplyBaseView, TypeMixin):
    pass


class ShowHiddenRepliesView(ShowHiddenRepliesBaseView, TypeMixin):
    pass


class WatchThreadView(WatchThreadBaseView, TypeMixin):
    pass


class WatchEmailThreadView(WatchEmailThreadBaseView, TypeMixin):
    pass


class UnwatchThreadView(UnwatchThreadBaseView, TypeMixin):
    pass


class UnwatchEmailThreadView(UnwatchEmailThreadBaseView, TypeMixin):
    pass


class UpvotePostView(UpvotePostBaseView, TypeMixin):
    pass


class DownvotePostView(DownvotePostBaseView, TypeMixin):
    pass


class InviteUserView(JumpView, TypeMixin):
    def make_jump(self):
        print 'ZOMG INVITING USER'


class RemoveUserView(JumpView, TypeMixin):
    def make_jump(self):
        target_user = int(self.request.POST.get('user', 0))
        if (not (self.request.user.pk == self.thread.start_poster_id or
                self.request.acl.private_threads.is_mod()) and
                target_user != self.request.user.pk):
            raise ACLError403(_("You don't have permission to remove discussion participants."))
        try:
            user = self.thread.participants.get(id=target_user)
            self.thread.participants.remove(user)
            self.thread.threadread_set.filter(id=user.pk).delete()
            self.thread.watchedthread_set.filter(id=user.pk).delete()
            # If there are no more participants in thread, remove it
            if self.thread.participants.count() == 0:
                self.thread.delete()
                self.request.messages.set_flash(Message(_('Thread has been deleted because last participant left it.')), 'info', 'threads')
                return self.threads_list_redirect()
            # Nope, see if we removed ourselves
            if user.pk == self.request.user.pk:
                self.thread.last_post.set_checkpoint(self.request, 'left')
                self.request.messages.set_flash(Message(_('You have left the "%(thread)s" thread.') % {'thread': self.thread.name}), 'info', 'threads')
                return self.threads_list_redirect()
            # Nope, somebody else removed user
            self.thread.last_post.set_checkpoint(self.request, 'removed', user)
            self.thread.last_post.save(force_update=True)
            self.request.messages.set_flash(Message(_('Selected participant was removed from thread.')), 'info', 'threads')
            return self.retreat_redirect()
        except User.DoesNotExist:
            self.request.messages.set_flash(Message(_('Requested thread participant does not exist.')), 'error', 'threads')
            return self.retreat_redirect()
