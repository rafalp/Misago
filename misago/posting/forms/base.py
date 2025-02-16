from django import forms
from django.http import HttpRequest

from ..state.base import PostingState


class PostingForm(forms.Form):
    def update_state(self, state: PostingState):
        pass

    @classmethod
    def is_request_upload(cls, request: HttpRequest) -> bool:
        return False

    def clear_errors_in_preview(self):
        self.clear_all_errors()

    def clear_errors_in_upload(self):
        self.clear_all_errors()

    def clear_all_errors(self):
        self.errors.clear()
