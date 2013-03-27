from misago.acl.exceptions import ACLError404

class TypeMixin(object):
    type_prefix = 'private_thread'

    def check_permissions(self):
        try:
            if self.thread.pk:
                if not self.request.user in self.thread.participants.all():
                    raise ACLError404()
        except AttributeError:
            pass

    def whitelist_mentions(self):
        participants = self.thread.participants.all()
        mentioned = self.post.mentions.all()
        for user in self.md.mentions:
            if user not in participants and user not in mentioned:
                self.post.mentioned.add(user)

    def threads_list_redirect(self):
        return redirect(reverse('private_threads'))
