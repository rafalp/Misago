from misago.threads.forms.posting import ThreadParticipantsForm
from misago.threads.posting import PostingMiddleware, START
from misago.threads.models import ThreadParticipant


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
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        for user in form.users_cache:
            ThreadParticipant.objects.add_participant(self.thread, user)
