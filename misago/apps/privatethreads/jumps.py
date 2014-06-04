from django.utils.translation import ugettext as _
from misago import messages
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


class FirstReportedView(FirstReportedBaseView, TypeMixin):
    pass


class ReportPostView(ReportPostBaseView, TypeMixin):
    pass


class ShowPostReportView(ShowPostReportBaseView, TypeMixin):
    pass


class InviteUserView(JumpView, TypeMixin):
    def make_jump(self):
        username = slugify(self.request.POST.get('username', '').strip()).replace('-', '')
        if not username:
            messages.error(self.request, _('You have to enter name of user you want to invite to thread.'), 'threads')
            return self.retreat_redirect()
        try:
            user = User.objects.get(username_slug=username)
            acl = user.acl()
            if user in self.thread.participants.all():
                if user.pk == self.request.user.pk:
                    messages.error(self.request, _('You cannot add yourself to this thread.'), 'threads')
                else:
                    messages.info(self.request, _('%(user)s is already participating in this thread.') % {'user': user.username}, 'threads')
            elif not acl.private_threads.can_participate():
                messages.info(self.request, _('%(user)s cannot participate in private threads.') % {'user': user.username}, 'threads')
            elif (not self.request.acl.private_threads.can_invite_ignoring() and
                    not user.allow_pd_invite(self.request.user)):
                messages.info(self.request, _('%(user)s restricts who can invite him to private threads.') % {'user': user.username}, 'threads')
            else:
                self.thread.participants.add(user)
                user.sync_pds = True
                user.save(force_update=True)
                user.email_user(self.request, 'private_thread_invite', _("You've been invited to private thread \"%(thread)s\" by %(user)s") % {'thread': self.thread.name, 'user': self.request.user.username}, {'author': self.request.user, 'thread': self.thread})
                self.thread.set_checkpoint(self.request, 'invited', user)
                messages.success(self.request, _('%(user)s has been added to this thread.') % {'user': user.username}, 'threads')
        except User.DoesNotExist:
            messages.error(self.request, _('User with requested username could not be found.'), 'threads')
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
                messages.info(self.request, _('Thread has been deleted because last participant left it.'), 'threads')
                return self.threads_list_redirect()
            # Nope, see if we removed ourselves
            if user.pk == self.request.user.pk:
                self.thread.set_checkpoint(self.request, 'left')
                messages.info(self.request, _('You have left the "%(thread)s" thread.') % {'thread': self.thread.name}, 'threads')
                return self.threads_list_redirect()
            # Nope, somebody else removed user
            user.sync_pds = True
            user.save(force_update=True)
            self.thread.set_checkpoint(self.request, 'removed', user)
            messages.info(self.request, _('Selected participant was removed from thread.'), 'threads')
            return self.retreat_redirect()
        except User.DoesNotExist:
            messages.error(self.request, _('Requested thread participant does not exist.'), 'threads')
            return self.retreat_redirect()
