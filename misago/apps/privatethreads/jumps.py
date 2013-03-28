from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.threadtype.jumps import *
from misago.models import User
from misago.utils.strings import slugify
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
        username = slugify(self.request.POST.get('username', '').strip())
        if not username:
            self.request.messages.set_flash(Message(_('You have to enter name of user you want to invite to thread.')), 'error', 'threads')
            return self.retreat_redirect()
        try:
            user = User.objects.get(username_slug=username)
            acl = user.acl(self.request)
            if user in self.thread.participants.all():
                if user.pk == self.request.user.pk:
                    self.request.messages.set_flash(Message(_('You cannot add yourself to this thread.')), 'error', 'threads')
                else:
                    self.request.messages.set_flash(Message(_('%(user)s is already participating in this thread.') % {'user': user.username}), 'info', 'threads')
            if not acl.private_threads.can_participate():
                    self.request.messages.set_flash(Message(_('%(user)s cannot participate in private threads.') % {'user': user.username}), 'info', 'threads')
            elif (not self.request.acl.private_threads.can_invite_ignoring() and
                    user.is_ignoring(self.request.user)):
                self.request.messages.set_flash(Message(_('%(user)s does not wish to participate in your private threads.') % {'user': user.username}), 'info', 'threads')
            else:
                self.thread.participants.add(user)
                user.sync_pds = True
                user.save(force_update=True)
                user.email_user(self.request, 'private_thread_invite', _("You've been invited to private thread \"%(thread)s\" by %(user)s") % {'thread': self.thread.name, 'user': self.request.user.username}, {'author': self.request.user, 'thread': self.thread})
                self.thread.last_post.set_checkpoint(self.request, 'invited', user)
                self.thread.last_post.save(force_update=True)
                self.request.messages.set_flash(Message(_('%(user)s has been added to this thread.') % {'user': user.username}), 'success', 'threads')
            return self.retreat_redirect()
        except User.DoesNotExist:
            self.request.messages.set_flash(Message(_('User with requested username could not be found.')), 'error', 'threads')
            return self.retreat_redirect()


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
            user.sync_pds = True
            user.save(force_update=True)
            # If there are no more participants in thread, remove it
            if self.thread.participants.count() == 0:
                self.thread.delete()
                self.request.messages.set_flash(Message(_('Thread has been deleted because last participant left it.')), 'info', 'threads')
                return self.threads_list_redirect()
            # Nope, see if we removed ourselves
            if user.pk == self.request.user.pk:
                self.thread.last_post.set_checkpoint(self.request, 'left')
                self.thread.last_post.save(force_update=True)
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
