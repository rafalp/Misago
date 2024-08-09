from django import forms

from ..state.base import PostingState


class PostingForm(forms.Form):
    def update_state(self, state: PostingState):
        pass
