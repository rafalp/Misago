from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError404

class TypeMixin(object):
    type_prefix = 'private_thread'

    def type_available(self):
        return self.request.settings['enable_private_threads']

    def check_permissions(self):
        try:
            if self.thread.pk:
                if not self.request.user in self.thread.participants.all():
                    raise ACLError404()
        except AttributeError:
            pass

    def invite_users(self, users):
        sync_last_post = False
        for user in users:
            if not user in self.thread.participants.all():
                self.thread.participants.add(user)
                user.email_user(self.request, 'private_thread_invite', _("You've been invited to private thread \"%(thread)s\" by %(user)s") % {'thread': self.thread.name, 'user': self.request.user.username}, {'author': self.request.user, 'thread': self.thread})
                if self.action == 'new_reply':
                    self.thread.last_post.set_checkpoint(self.request, 'invited', user)
        if sync_last_post:
            self.thread.last_post.save(force_update=True)

    def force_stats_sync(self):
        self.thread.participants.exclude(id=self.request.user.id).update(sync_pds=True)
                
    def whitelist_mentions(self):
        participants = self.thread.participants.all()
        mentioned = self.post.mentions.all()
        for user in self.md.mentions:
            if user not in participants and user not in mentioned:
                self.post.mentioned.add(user)

    def threads_list_redirect(self):
        return redirect(reverse('private_threads'))
