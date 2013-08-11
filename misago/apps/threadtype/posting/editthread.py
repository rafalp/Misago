from django.utils import timezone
from misago.apps.threadtype.posting.base import PostingBaseView
from misago.apps.threadtype.posting.forms import EditThreadForm
from misago.markdown import post_markdown
from misago.utils.strings import slugify

class EditThreadBaseView(PostingBaseView):
    action = 'edit_thread'
    form_type = EditThreadForm
    block_flood_requests = False

    def set_context(self):
        self.set_thread_context()
        self.post = self.thread.start_post
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_thread_edit(self.request.user, self.proxy, self.thread, self.post)
        
    def form_initial_data(self):
        return {
                'thread_name': self.thread.name,
                'weight': self.thread.weight,
                'post': self.post.post,
                }

    def post_form(self, form):
        old_name = self.thread.name
        old_post = self.post.post

        changed_thread = old_name != form.cleaned_data['thread_name']
        changed_post = old_post != form.cleaned_data['post']

        if self.thread.last_post_id == self.post.pk:
            self.thread.last_post == self.post

        if 'close_thread' in form.cleaned_data and form.cleaned_data['close_thread']:
            self.thread.closed = not self.thread.closed
            changed_thread = True
            if self.thread.closed:
                self.thread.set_checkpoint(self.request, 'closed')
            else:
                self.thread.set_checkpoint(self.request, 'opened')

        if ('thread_weight' in form.cleaned_data and
                form.cleaned_data['thread_weight'] != self.thread.weight):
            self.thread.weight = form.cleaned_data['thread_weight']
            changed_thread = True

        if changed_thread:
            self.thread.name = form.cleaned_data['thread_name']
            self.thread.slug = slugify(form.cleaned_data['thread_name'])
            self.thread.save(force_update=True)
            if self.forum.last_thread_id == self.thread.pk:
                self.forum.last_thread_name = self.thread.name
                self.forum.last_thread_slug = self.thread.slug
                self.forum.save(force_update=True)

        if changed_post:
            self.post.post = form.cleaned_data['post']
            self.md, self.post.post_preparsed = post_markdown(form.cleaned_data['post'])
            self.post.save(force_update=True)

        if old_name != form.cleaned_data['thread_name']:
            self.thread.update_current_dates()

        if changed_thread or changed_post:
            self.record_edit(form, old_name, old_post)
