from misago.threads.forms.posting import ThreadWeightForm
from misago.threads.posting import PostingMiddleware


class ThreadWeightFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_change_threads_weight']:
            self.thread_weight = self.thread.weight
            return True
        else:
            return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadWeightForm(self.request.POST, prefix=self.prefix)
        else:
            initial = {'weight': self.thread_weight}
            return ThreadWeightForm(prefix=self.prefix, initial=initial)

    def pre_save(self, form):
        if self.thread_weight != form.cleaned_data.get('weight'):
            self.thread.weight = form.cleaned_data.get('weight')
            self.thread.update_fields.append('weight')
