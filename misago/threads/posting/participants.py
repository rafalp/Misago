from misago.threads.forms.posting import ThreadParticipantsForm
from misago.threads.posting import PostingMiddleware, START
from misago.threads.participants import add_participant


class ThreadParticipantsFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.is_private and self.mode == START

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadParticipantsForm(
                self.request.POST, user=self.request.user, prefix=self.prefix)
        else:
            return ThreadParticipantsForm(prefix=self.prefix)

    def save(self, form):
        add_participant(self.request, self.thread, self.user, True)
        for user in form.users_cache:
            add_participant(self.request, self.thread, user)
