from ...forms.formset import Formset
from ..state.base import PostingState


class PostingFormset(Formset):
    def update_state(self, state: PostingState):
        for form in self.forms.values():
            if form.is_valid():
                form.update_state(state)
