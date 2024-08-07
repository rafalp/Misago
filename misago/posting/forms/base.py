from django import forms

from ..states.base import State


class PostingForm(forms.Form):
    def update_state(self, state: State):
        pass
