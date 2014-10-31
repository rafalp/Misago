from misago.threads.forms.posting import ThreadLabelForm
from misago.threads.models import Label
from misago.threads.moderation import label_thread, unlabel_thread
from misago.threads.permissions import can_edit_thread
from misago.threads.posting import PostingMiddleware, START, EDIT


class ThreadLabelFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_change_threads_labels'] and self.forum.labels:
            self.thread_label_id = self.thread.label_id
            if self.mode == EDIT and can_edit_thread(self.user, self.thread):
                return True
            else:
                return self.mode == START
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
        if form.is_valid() and self.mode == START:
            if self.thread_label_id != form.cleaned_data.get('label'):
                if form.cleaned_data.get('label'):
                    self.thread.label_id = form.cleaned_data.get('label')
                    self.thread.update_fields.append('label')
                else:
                    self.thread.label = None
                    self.thread.update_fields.append('label')

    def post_save(self, form):
        if form.is_valid() and self.mode != START:
            if self.thread_label_id != form.cleaned_data.get('label'):
                if form.cleaned_data.get('label'):
                    labels_dict = Label.objects.get_cached_labels_dict()
                    new_label = labels_dict.get(form.cleaned_data.get('label'))
                    if new_label:
                        label_thread(self.user, self.thread, new_label)
                else:
                    unlabel_thread(self.user, self.thread)
