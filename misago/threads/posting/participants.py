from misago.threads.forms.posting import ThreadParticipantsForm
from misago.threads.posting import PostingMiddleware, START


class ThreadParticipantsFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.is_private

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadParticipantsForm(
                self.request.POST, prefix=self.prefix)
        else:
            return ThreadParticipantsForm(prefix=self.prefix)
