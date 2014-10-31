from misago.threads import moderation
from misago.threads.forms.posting import ThreadCloseForm
from misago.threads.posting import PostingMiddleware, START


class ThreadCloseFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_close_threads']:
            self.is_closed = self.thread.is_closed
            return True
        else:
            return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadCloseForm(self.request.POST, prefix=self.prefix)
        else:
            initial = {'is_closed': self.is_closed}
            return ThreadCloseForm(prefix=self.prefix, initial=initial)

    def pre_save(self, form):
        if form.is_valid() and self.mode == START:
            if form.cleaned_data.get('is_closed'):
                self.thread.is_closed = form.cleaned_data.get('is_closed')
                self.thread.update_fields.append('is_closed')

    def post_save(self, form):
        if form.is_valid() and self.mode != START:
            if self.is_closed != form.cleaned_data.get('is_closed'):
                if self.thread.is_closed:
                    moderation.open_thread(self.user, self.thread)
                else:
                    moderation.close_thread(self.user, self.thread)
