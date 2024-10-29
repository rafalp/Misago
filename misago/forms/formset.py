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

    def __contains__(self, form: Form | str):
        if isinstance(form, str):
            return form in self.forms

        if not form.prefix:
            raise ValueError(f"{type(form)} instance must have a prefix.")

        return form.prefix in self.forms

    def get_forms(self) -> list[Form]:
        return list(self.forms.values())

    def add_form(
        self, form: Form, *, after: str | None = None, before: str | None = None
    ):
        if not form.prefix:
            raise ValueError("Forms added to 'Formset' must have a prefix.")
        if form.prefix in self.forms:
            raise ValueError(
                f"Form with prefix '{form.prefix}' is already a part of this formset."
            )

        if after and before:
            raise ValueError("'after' and 'before' arguments can't be combined.")

        if after or before:
            self._add_form_at_position(form, after=after, before=before)
        else:
            self.forms[form.prefix] = form

    def _add_form_at_position(
        self, form: Form, *, after: str | None = None, before: str | None = None
    ):
        if (after or before) not in self.forms:
            raise ValueError(
                f"Form with prefix '{after or before}' doesn't exist in this formset."
            )

        new_forms: dict[str, Form] = {}
        for form_id, form_obj in self.forms.items():
            if form_id == before:
                new_forms[form.prefix] = form

            new_forms[form_id] = form_obj

            if form_id == after:
                new_forms[form.prefix] = form

        self.forms = new_forms

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
