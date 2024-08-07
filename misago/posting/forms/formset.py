from ...forms.formset import Formset
from ..states.base import State


class PostingFormset(Formset):
    def update_state(self, state: State):
        for form in self.forms.values():
            if form.is_valid():
                form.update_state(state)
