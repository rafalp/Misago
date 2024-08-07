from functools import cached_property

from django.forms import Form


class Formset:
    """Formset that combines forms of any type.

    Used by views and templates that display multiple forms that should be validated
    together.
    """

    def __init__(self):
        self.forms: dict[str, Form] = {}

    def __getitem__(self, form_id: str):
        return self.forms[form_id]

    def get_forms(self) -> list[Form]:
        return list(self.forms.values())

    def add_form(self, form: Form, *, append: bool = True):
        if not form.prefix:
            raise ValueError("Forms added to 'Formset' must define a prefix.")
        if form.prefix in self.forms:
            raise ValueError(
                f"Form with prefix '{form.prefix}' is already a part of this formset."
            )

        if append:
            self.forms[form.prefix] = form

        else:
            forms: dict[str, Form] = {}
            forms[form.prefix] = form
            forms.update(self.forms)
            self.forms = forms

    @cached_property
    def is_bound(self) -> bool:
        return all([form.is_bound for form in self.forms.values()])

    def is_valid(self) -> bool:
        return all([form.is_valid() for form in self.forms.values()])

    def non_field_errors(self):
        errors = []
        for form in self.forms.values():
            errors += form.non_field_errors()
        return errors
