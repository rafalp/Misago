from . import START, PostingMiddleware
from ..forms.posting import ThreadParticipantsForm
from ..participants import add_owner, add_participant


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
        add_owner(self.thread, self.user)
        for user in form.users_cache:
            add_participant(self.request, self.thread, user)
