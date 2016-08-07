from . import START, PostingMiddleware
from .. import moderation
from ..forms.posting import ThreadPinForm


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
        if form.is_valid() and self.mode == START:
            if form.cleaned_data.get('is_pinned'):
                self.thread.is_pinned = form.cleaned_data.get('is_pinned')
                self.thread.update_fields.append('is_pinned')

    def post_save(self, form):
        if form.is_valid() and self.mode != START:
            if self.is_pinned != form.cleaned_data.get('is_pinned'):
                if self.thread.is_pinned:
                    moderation.unpin_thread(self.user, self.thread)
                else:
                    moderation.pin_thread(self.user, self.thread)
