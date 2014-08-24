from misago.threads.forms.reply import (FullThreadStateForm, ThreadWeightForm,
                                        CloseThreadForm)
from misago.threads.posting import PostingMiddleware, START, REPLY, EDIT


class ThreadStateFormMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(ThreadStateFormMiddleware, self).__init__(**kwargs)

        self.thread_weight = self.thread.weight
        self.thread_is_closed = self.thread.is_closed

    def make_form(self):
        StateFormType = None
        initial = {
            'weight': self.thread_weight,
            'is_closed': self.thread_is_closed,
        }

        can_change_threads_weight = self.forum.acl['can_change_threads_weight']
        can_close_threads = self.forum.acl['can_close_threads']

        if can_change_threads_weight and can_close_threads:
            StateFormType = FullThreadStateForm
        elif can_change_threads_weight:
            StateFormType = ThreadWeightForm
        elif can_close_threads:
            StateFormType = CloseThreadForm

        if StateFormType:
            if self.request.method == 'POST':
                return StateFormType(self.request.POST, prefix=self.prefix)
            else:
                return StateFormType(prefix=self.prefix, initial=initial)
        else:
            return False

    def pre_save(self, form):
        if self.forum.acl['can_change_threads_weight']:
            if self.thread_weight != form.cleaned_data.get('weight'):
                self.thread.weight = form.cleaned_data.get('weight')
                self.thread.update_fields.append('weight')
        if self.forum.acl['can_close_threads']:
            if self.thread_is_closed != form.cleaned_data.get('is_closed'):
                self.thread.is_closed = form.cleaned_data.get('is_closed')
                self.thread.update_fields.append('is_closed')

    def save(self, form):
        pass
