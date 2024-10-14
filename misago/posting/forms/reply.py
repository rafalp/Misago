from django import forms
from django.http import HttpRequest

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


def get_reply_thread_formset(request: HttpRequest) -> ReplyThreadFormset:
    formset = ReplyThreadFormset()

    if request.method == "POST":
        reply_form = ReplyThreadForm(request.POST, request.FILES, prefix="reply")
    else:
        reply_form = ReplyThreadForm(prefix="reply")

    formset.add_form(reply_form)

    return formset
