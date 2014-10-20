from misago.threads.forms.posting import ThreadLabelForm
from misago.threads.posting import PostingMiddleware


class ThreadLabelFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_change_threads_labels'] and self.forum.labels:
            self.thread_label_id = self.thread.label_id
            return True
        else:
            return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadLabelForm(self.request.POST, prefix=self.prefix,
                                    labels=self.forum.labels)
        else:
            initial = {'label_id': self.thread_label_id}
            return ThreadLabelForm(prefix=self.prefix,
                                    labels=self.forum.labels,
                                    initial=initial)

    def pre_save(self, form):
        if form.is_valid():
            if self.thread_label_id != form.cleaned_data.get('label'):
                if form.cleaned_data.get('label'):
                    self.thread.label_id = form.cleaned_data.get('label')
                    self.thread.update_fields.append('label')
                else:
                    self.thread.label = None
                    self.thread.update_fields.append('label')
