from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.conf import settings
from misago.acl.exceptions import ACLError404
from misago.utils.translation import ugettext_lazy

class TypeMixin(object):
    type_prefix = 'private_thread'

    def type_available(self):
        return settings.enable_private_threads

    def check_permissions(self):
        try:
            if self.thread.pk:
                if not ((self.thread.replies_reported > 0 and self.request.acl.private_threads.is_mod())
                        or (self.request.user in self.thread.participants.all())):
                    raise ACLError404()
        except AttributeError:
            pass

    def invite_users(self, users):
        for user in users:
            if not user in self.thread.participants.all():
                self.thread.participants.add(user)
                user.email_user(self.request, 'private_thread_invite', _("You've been invited to private thread \"%(thread)s\" by %(user)s") % {'thread': self.thread.name, 'user': self.request.user.username}, {'author': self.request.user, 'thread': self.thread})
                alert = user.alert(ugettext_lazy("%(username)s has invited you to the %(thread)s private thread").message)
                alert.profile('username', self.request.user)
                alert.post('thread', self.type_prefix, self.thread, self.post)
                alert.save_all()
                self.post.mentions.add(user)
                if self.action == 'new_reply':
                    self.thread.set_checkpoint(self.request, 'invited', user)

    def force_stats_sync(self):
        self.thread.participants.exclude(id=self.request.user.id).update(sync_pds=True)

    def whitelist_mentions(self):
        try:
            if self.md.mentions:
                participants = self.thread.participants.all()
                for slug, user in self.md.mentions.items():
                    if user not in participants:
                        del self.md.mentions[slug]
        except AttributeError:
            pass

    def threads_list_redirect(self):
        return redirect(reverse('private_threads'))
