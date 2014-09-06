from misago.threads.forms.posting import ThreadPrefixForm
from misago.threads.posting import PostingMiddleware


class ThreadPrefixFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.forum.acl['can_change_threads_prefix'] and self.forum.prefixes:
            self.thread_prefix_id = self.thread.prefix_id
            return True
        else:
            return False

    def make_form(self):
        if self.request.method == 'POST':
            return ThreadPrefixForm(self.request.POST, prefix=self.prefix,
                                    prefixes=self.forum.prefixes)
        else:
            initial = {'prefix_id': self.thread_prefix_id}
            return ThreadPrefixForm(prefix=self.prefix,
                                    prefixes=self.forum.prefixes,
                                    initial=initial)

    def pre_save(self, form):
        if self.thread_prefix_id != form.cleaned_data.get('prefix'):
            if form.cleaned_data.get('prefix'):
                self.thread.prefix_id = form.cleaned_data.get('prefix')
                self.thread.update_fields.append('prefix')
            else:
                self.thread.prefix = None
                self.thread.update_fields.append('prefix')
