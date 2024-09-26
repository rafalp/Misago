from django import forms

from ..state.reply import ReplyThreadState
from .base import PostingForm
from .formset import PostingFormset


class ReplyThreadFormset(PostingFormset):
    pass


class ReplyThreadForm(PostingForm):
    template_name = "misago/posting/reply_thread_form.html"

    post = forms.CharField(max_length=2000, widget=forms.Textarea)

    def update_state(self, state: ReplyThreadState):
        state.set_post_message(self.cleaned_data["post"])
