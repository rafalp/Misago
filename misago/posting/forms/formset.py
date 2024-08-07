from ...forms.formset import Formset
from ..states.base import State


class PostingFormset(Formset):
    def update_state(self, state: State):
        for form in self.forms.values():
            form.update_state(state)
