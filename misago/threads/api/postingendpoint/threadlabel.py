from . import EDIT, START, PostingMiddleware
from ..forms.posting import ThreadLabelForm
from ..models import Label
from ..moderation import label_thread, unlabel_thread
from ..permissions import can_edit_thread


class ThreadLabelFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.labels and self.forum.acl['can_change_threads_labels']:
            self.label_id = self.thread.label_id

            if self.mode == START:
                return True

            if self.mode == EDIT and can_edit_thread(self.user, self.thread):
                return True

        return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadLabelForm(self.request.POST, prefix=self.prefix,
                                    labels=self.forum.labels)
        else:
            initial = {'label_id': self.label_id}
            return ThreadLabelForm(prefix=self.prefix,
                                    labels=self.forum.labels,
                                    initial=initial)

    def pre_save(self, form):
        if form.is_valid() and self.mode == START:
            if self.label_id != form.cleaned_data.get('label'):
                if form.cleaned_data.get('label'):
                    self.thread.label_id = form.cleaned_data.get('label')
                    self.thread.update_fields.append('label')
                else:
                    self.thread.label = None
                    self.thread.update_fields.append('label')

    def post_save(self, form):
        if form.is_valid() and self.mode != START:
            if self.label_id != form.cleaned_data.get('label'):
                if form.cleaned_data.get('label'):
                    labels_dict = Label.objects.get_cached_labels_dict()
                    new_label = labels_dict.get(form.cleaned_data.get('label'))
                    if new_label:
                        label_thread(self.user, self.thread, new_label)
                else:
                    unlabel_thread(self.user, self.thread)
