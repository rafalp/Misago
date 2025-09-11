from functools import cached_property

from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest

from ...collections.dicts import set_key_after, set_key_before
from ...forms import formset
from ..forms import MembersForm, PostForm, TitleForm
from ..state.state import State


class Formset(formset.Formset):
    preview_action: str = "preview"

    errors: list[ValidationError]

    def __init__(self):
        super().__init__()
        self.errors = []

    @property
    def title(self) -> TitleForm | None:
        return self.forms.get(TitleForm.form_prefix)

    @property
    def post(self) -> PostForm | None:
        return self.forms.get(PostForm.form_prefix)

    @property
    def members(self) -> MembersForm | None:
        return self.forms.get(MembersForm.form_prefix)

    def update_state(self, state: State):
        for form in self.forms.values():
            if form.is_valid():
                form.update_state(state)

    def add_error(self, error: ValidationError):
        self.errors.append(error)

    def is_request_preview(self, request: HttpRequest) -> bool:
        return bool(request.method == "POST" and request.POST.get(self.preview_action))

    def is_request_upload(self, request: HttpRequest) -> bool:
        if request.method == "POST":
            for form in self.forms.values():
                if form.is_request_upload(request):
                    return True

        return False

    def clear_errors_in_preview(self):
        for form in self.forms.values():
            form.clear_errors_in_preview()

    def clear_errors_in_upload(self):
        for form in self.forms.values():
            form.clear_errors_in_upload()


class TabbedFormset(Formset):
    tabs: dict[str, "FormsetTab"]

    def __init__(self):
        super().__init__()
        self.tabs = {}

    def get_tabs(self) -> list["FormsetTab"]:
        return list(self.tabs.values())

    def add_tab(self, tab_id: str, name: str) -> "FormsetTab":
        tab = FormsetTab(tab_id, name)
        self.tabs[tab_id] = tab
        return tab

    def add_tab_after(self, after: str, tab_id: str, name: str) -> "FormsetTab":
        if after not in self.tabs:
            raise ValueError(f"Formset does not contain a tab with ID '{after}'.")

        tab = FormsetTab(tab_id, name)
        self.tabs = set_key_after(self.tabs, after, tab_id, tab)
        return tab

    def add_tab_before(self, before: str, tab_id: str, name: str) -> "FormsetTab":
        if before not in self.tabs:
            raise ValueError(f"Formset does not contain a tab with ID '{before}'.")

        tab = FormsetTab(tab_id, name)
        self.tabs[tab_id] = tab
        self.tabs = set_key_before(self.tabs, before, tab_id, tab)
        return tab

    def add_form(
        self,
        tab: str,
        form: Form,
    ) -> Form:
        self.validate_tab(tab)
        super().add_form(form)
        self.tabs[tab].add_form(form)
        return form

    def add_form_after(self, tab: str, after: str, form: Form) -> Form:
        self.validate_tab(tab)
        self.validate_new_form(form)

        if after not in self.forms:
            raise ValueError(f"Formset does not contain a form with prefix '{after}'.")

        if after not in self.tabs[tab].forms:
            raise ValueError(
                f"Tab '{tab}' does not contain a form with prefix '{after}'."
            )

        self.forms = set_key_after(self.forms, after, form.prefix, form)
        self.tabs[tab].add_form_after(after, form)
        return form

    def add_form_before(self, tab: str, before: str, form: Form) -> Form:
        self.validate_tab(tab)
        self.validate_new_form(form)

        if before not in self.forms:
            raise ValueError(f"Formset does not contain a form with prefix '{before}'.")

        if before not in self.tabs[tab].forms:
            raise ValueError(
                f"Tab '{tab}' does not contain a form with prefix '{before}'."
            )

        self.forms = set_key_before(self.forms, before, form.prefix, form)
        self.tabs[tab].add_form_before(before, form)
        return form

    def validate_tab(self, tab: str):
        if tab not in self.tabs:
            raise ValueError(f"Formset does not contain a tab with ID '{tab}'.")

    @cached_property
    def has_multiple_tabs(self) -> bool:
        tabs_with_forms = 0
        for tab in self.tabs.values():
            if tab.forms:
                tabs_with_forms += 1
        return tabs_with_forms > 1


class FormsetTab(Formset):
    id: str
    name: str

    def __init__(self, id: str, name: str):
        super().__init__()

        self.id = id
        self.name = name

    def __str__(self) -> str:
        return self.name

    @property
    def html_id(self):
        return f"tab-{self.id}"
