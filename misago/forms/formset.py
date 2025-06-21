from django.forms import Form

from ..collections.dicts import set_after_key, set_before_key


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

    def add_form(self, form: Form):
        self._validate_new_form(form)
        self.forms[form.prefix] = form

    def add_form_after(self, form: Form, after: str):
        self._validate_new_form(form)

        if after not in self.forms:
            raise ValueError(
                f"Form with prefix '{after}' doesn't exist in this formset."
            )

        self.forms = set_after_key(self.forms, after, form.prefix, form)

    def add_form_before(self, form: Form, before: str):
        self._validate_new_form(form)

        if before not in self.forms:
            raise ValueError(
                f"Form with prefix '{before}' doesn't exist in this formset."
            )

        self.forms = set_before_key(self.forms, before, form.prefix, form)

    def _validate_new_form(self, form: Form):
        if not form.prefix:
            raise ValueError("Forms added to 'Formset' must have a prefix.")

        if form.prefix in self.forms:
            raise ValueError(
                f"Form with prefix '{form.prefix}' is already a part of this formset."
            )

    @property
    def is_bound(self) -> bool:
        return all([form.is_bound for form in self.forms.values()])

    def is_valid(self) -> bool:
        return all([form.is_valid() for form in self.forms.values()])

    def non_field_errors(self):
        errors = []
        for form in self.forms.values():
            errors += form.non_field_errors()
        return errors
