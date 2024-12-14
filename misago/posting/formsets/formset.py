from django.core.exceptions import ValidationError

from ...forms.formset import Formset
from ..state.base import PostingState


class PostingFormset(Formset):
    errors: list[ValidationError]

    def __init__(self):
        super().__init__()
        self.errors = []

    def update_state(self, state: PostingState):
        for form in self.forms.values():
            if form.is_valid():
                form.update_state(state)

    def add_error(self, error: ValidationError):
        self.errors.append(error)
