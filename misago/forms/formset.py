from functools import cached_property

from django.forms import Form

from ..collections.dicts import set_key_after, set_key_before


class Formset:
    """Formset that combines forms of any type.

    Used by views and templates that display multiple forms that should be validated
    together.
    """

    forms: dict[str, Form]

    def __init__(self):
        self.forms: dict[str, Form] = {}

    def __getitem__(self, form_id: str):
        return self.forms[form_id]

    def __contains__(self, form: Form | str):
        if isinstance(form, str):
            return form in self.forms

        if not form.prefix:
            raise ValueError(f"{type(form)} instance must have a prefix.")

        return form.prefix in self.forms

    def get_forms(self) -> list[Form]:
        return list(self.forms.values())

    def add_form(self, form: Form) -> Form:
        self.validate_new_form(form)
        self.forms[form.prefix] = form
        return form

    def add_form_after(self, after: str, form: Form) -> Form:
        self.validate_new_form(form)

        if after not in self.forms:
            raise ValueError(f"Formset does not contain a form with prefix '{after}'.")

        self.forms = set_key_after(self.forms, after, form.prefix, form)
        return form

    def add_form_before(self, before: str, form: Form) -> Form:
        self.validate_new_form(form)

        if before not in self.forms:
            raise ValueError(f"Formset does not contain a form with prefix '{before}'.")

        self.forms = set_key_before(self.forms, before, form.prefix, form)
        return form

    def validate_new_form(self, form: Form):
        if not form.prefix:
            raise ValueError("Forms added to 'Formset' must have a prefix.")

        if form.prefix in self.forms:
            raise ValueError(
                f"Form with prefix '{form.prefix}' is already part of this formset."
            )

    def is_bound(self) -> bool:
        return all([form.is_bound for form in self.forms.values()])

    def is_valid(self) -> bool:
        return all([form.is_valid() for form in self.forms.values()])

    def non_field_errors(self):
        errors = []
        for form in self.forms.values():
            errors += form.non_field_errors()
        return errors
