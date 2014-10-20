from misago.threads.forms.posting import ThreadPinForm
from misago.threads.posting import PostingMiddleware


class ThreadPinFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_pin_threads']:
            self.is_pinned = self.thread.is_pinned
            return True
        else:
            return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadPinForm(self.request.POST, prefix=self.prefix)
        else:
            initial = {'is_pinned': self.is_pinned}
            return ThreadPinForm(prefix=self.prefix, initial=initial)

    def pre_save(self, form):
        if form.is_valid():
            if self.is_pinned != form.cleaned_data.get('is_pinned'):
                self.thread.is_pinned = form.cleaned_data.get('is_pinned')
                self.thread.update_fields.append('is_pinned')
