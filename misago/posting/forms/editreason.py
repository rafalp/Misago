from django import forms
from django.http import HttpRequest

from ..state import State
from .base import PostingForm


class EditReasonForm(PostingForm):
    form_prefix = "posting-edit-reason"
    template_name = "misago/posting/edit_reason_form.html"

    request: HttpRequest

    edit_reason = forms.CharField(required=False, max_length=255)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def update_state(self, state: State):
        state.set_edit_reason(self.cleaned_data["edit_reason"] or None)


def create_edit_reason_form(request: HttpRequest) -> EditReasonForm:
    if request.method == "POST":
        return EditReasonForm(
            request.POST,
            request=request,
            prefix=EditReasonForm.form_prefix,
        )

    return EditReasonForm(request=request, prefix=EditReasonForm.form_prefix)
