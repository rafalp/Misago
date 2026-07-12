from dataclasses import dataclass, field
from typing import Optional

from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..categories.models import Category
from ..threadevents.models import ThreadEvent
from ..threads.models import Post, Thread


class ModerationAction:
    multistage = False
    swap_root = False

    id: str
    full_name: str | None = None
    button_label: str

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def validate(self):
        pass

    def execute(self) -> Optional["ModerationResult"]:
        raise NotImplementedError("'FormMixin' subclasses must implement 'execute'")


@dataclass(frozen=True)
class ModerationResult:
    created_items: list[Model] = field(default_factory=list)
    updated_items: list[Model] = field(default_factory=list)
    deleted_items: list[Model] = field(default_factory=list)
    thread_updates: list[ThreadEvent] = field(default_factory=list)

    refresh: bool = False
    redirect_to: str | None = None


@dataclass(frozen=True)
class ModerationActionTemplateResult(ModerationResult):
    context: dict = field(default_factory=dict)

    def update_context(self, context: dict):
        self.context.update(context)

    def render(
        self, request: HttpRequest, template_name: str, context: dict | None = None
    ) -> HttpResponse:
        if context:
            final_context = context
            final_context.update(self.context)
        else:
            final_context = self.context

        return render(request, template_name, final_context)


class ConfirmMixin:
    multistage = True

    id: str
    full_name: str | None = None
    button_label: str

    confirmation_message: str
    template_name: str = "misago/moderation/confirm.html"

    def execute(self) -> ModerationResult:
        if self.request.POST.get("confirm"):
            return self.confirmed()

        return ModerationActionTemplateResult(
            context=self.get_context_data(),
        )

    def get_context_data(self) -> dict:
        return {
            "template_name": self.template_name,
            "confirmation_message": self.confirmation_message,
            "full_name": self.full_name or self.button_label,
            "button_label": self.button_label,
        }

    def confirmed(self) -> ModerationResult:
        raise NotImplementedError(
            "'ConfirmMixin' subclasses must implement 'confirmed' method."
        )


class FormMixin:
    multistage = True

    id: str
    full_name: str | None = None
    button_label: str

    form_class: Form
    form_prefix: str = "moderation"
    template_name: str

    def execute(self) -> ModerationResult:
        form_submitted = bool(self.request.POST.get("confirm"))
        form = self.get_form(form_submitted)

        if form_submitted and form.is_valid():
            return self.form_valid(form)

        return ModerationActionTemplateResult(
            context=self.get_context_data(form),
        )

    def get_form(self, form_submitted: bool) -> Form:
        if form_submitted:
            return self.form_class(
                self.request.POST,
                request=self.request,
                prefix=self.form_prefix,
            )

        return self.form_class(request=self.request, prefix=self.form_prefix)

    def get_context_data(self, form: Form) -> dict:
        return {
            "template_name": self.template_name,
            "form": form,
            "full_name": self.full_name or self.button_label,
            "button_label": self.button_label,
        }

    def form_valid(self, form: Form) -> ModerationResult:
        raise NotImplementedError(
            "'FormMixin' subclasses must implement 'form_valid' method."
        )


class ThreadsModerationAction(ModerationAction):
    swap_root = True

    category: Category | None
    threads: list[Thread]

    def __init__(
        self,
        request: HttpRequest,
        threads: list[Thread],
        category: Category | None = None,
    ):
        super().__init__(request)

        self.category = Category
        self.threads = threads


class PostsModerationAction(ModerationAction):
    category: Category
    thread: Thread
    posts: list[Post]

    def __init__(self, request: HttpRequest, thread: Thread, posts: list[Post]):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread
        self.posts = posts


class ThreadModerationAction(ModerationAction):
    category: Category
    thread: Thread

    def __init__(self, request: HttpRequest, thread: Thread):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread


class PostModerationAction(ModerationAction):
    category: Category
    thread: Thread
    post: Post

    def __init__(self, request: HttpRequest, thread: Thread, post: Post):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread
        self.post = post
