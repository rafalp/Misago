from functools import cached_property

from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest

from ...forms.formset import Formset
from ..forms import InviteUsersForm, PostForm, TitleForm
from ..state.base import PostingState


class PostingFormset(Formset):
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
    def invite_users(self) -> InviteUsersForm | None:
        return self.forms.get(InviteUsersForm.form_prefix)

    def update_state(self, state: PostingState):
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


class TabbedPostingFormset(PostingFormset):
    tabs: dict[str, "PostingFormsetTab"]

    def __init__(self):
        super().__init__()
        self.tabs = {}

    def get_tabs(self) -> list[Form]:
        return list(self.tabs.values())

    def add_tab(self, tab_id: str, name: str) -> "PostingFormsetTab":
        tab = PostingFormsetTab(tab_id, name)
        self.tabs[tab_id] = tab
        return tab

    def add_form(
        self,
        form: Form,
        tab: str | None = None,
    ):
        if tab and tab not in self.tabs:
            raise ValueError(f"Tab '{tab}' doesn't exist")
        if not tab:
            tab = next(self.tabs)

        super().add_form(form)
        self.tabs[tab].add_form(form)

    @cached_property
    def has_multiple_tabs(self) -> bool:
        tabs_with_forms = 0
        for tab in self.tabs.values():
            if tab.forms:
                tabs_with_forms += 1
        return tabs_with_forms > 1


class PostingFormsetTab(Formset):
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
        return f"formset_tab_{self.id}"
