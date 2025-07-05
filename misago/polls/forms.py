from typing_extensions import TYPE_CHECKING

from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext

from ..categories.models import Category
from ..threads.models import Thread
from .choices import PollChoice, PollChoices
from .enums import PublicPollsAvailability
from .models import Poll
from .validators import validate_poll_choices, validate_poll_question

if TYPE_CHECKING:
    from ..users.models import User


class PollChoicesWidget(forms.Widget):
    def value_from_datadict(self, data, files, name):
        name_length = len(name)
        ids: set[str] = set()
        value = []

        for key in data:
            key_length = len(key)

            if name_length >= key_length:
                continue

            if key[:name_length] != name:
                continue

            if key[name_length] != "[":
                continue

            if key[key_length - 1] != "]":
                continue

            choice_id = key[name_length + 1 : key_length - 1].strip()
            if not choice_id:
                continue

            if choice_id in ids:
                continue

            ids.add(choice_id)
            value.append({"id": choice_id, "name": data.get(key, "").strip()})

        obj = PollChoices(value)
        for choice in data.getlist(f"{name}[]"):
            if choice := choice.strip():
                obj.add(choice)

        return obj

    def check_data_value_name(self, name: str, data_name: str) -> bool:
        if data_name == f"{name}[]":
            return True

        return False


class PollChoicesField(forms.Field):
    widget = PollChoicesWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.initial:
            self.initial = PollChoices()

    def clean(self, value: PollChoices) -> PollChoices:
        initial_ids: set[str] = set()
        initial_choices: PollChoice = []

        if self.initial:
            for choice in self.initial.values():
                if choice["id"]:
                    initial_ids.add(choice["id"])
                    initial_choices.append(choice)

        choices = PollChoices(initial_choices)
        for choice in value.values():
            if choice["id"] in initial_ids:
                choices[choice["id"]]["name"] = choice["name"]
                initial_ids.remove(choice["id"])
            else:
                choices.add(choice["name"])

        for removed_choice in initial_ids:
            del choices[removed_choice]

        return choices


class PollForm(forms.Form):
    request: HttpRequest
    required: bool

    question = forms.CharField(max_length=255, required=False)
    choices_text = forms.CharField(max_length=1000, required=False)
    choices_list = PollChoicesField(required=False)
    duration = forms.IntegerField(
        initial=0, min_value=0, max_value=1825, required=False
    )
    max_choices = forms.IntegerField(initial=1, min_value=1, required=False)
    can_change_vote = forms.BooleanField(required=False)
    is_public = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.required = kwargs.pop("required", True)

        super().__init__(*args, **kwargs)

        self.setup_form_fields(self.request.settings)

    def setup_form_fields(self, settings):
        self.fields["question"].max_length = settings.poll_question_max_length
        self.fields["question"].required = self.required

    def clean_question(self):
        if data:= self.cleaned_data["question"]:
            validate_poll_question(
                data,
                self.request.settings.poll_question_min_length,
                self.request.settings.poll_question_max_length,
                self.request,
            )
        return data

    def clean_choices_text(self):
        data = self.cleaned_data["choices_text"]
        choices_obj = PollChoices.from_str(data)
        return choices_obj.inputvalue()

    def clean_choices(self, cleaned_data: dict) -> PollChoices | None:
        if choices_list := cleaned_data.get("choices_list"):
            try:
                choices = choices_list
                validate_poll_choices(
                    choices,
                    self.request.settings.poll_max_choices,
                    self.request.settings.poll_choice_min_length,
                    self.request.settings.poll_choice_max_length,
                    self.request,
                )
                return choices
            except ValidationError as error:
                self.add_error("choices_list", error)

        if choices_text := cleaned_data.get("choices_text"):
            try:
                choices = PollChoices.from_str(choices_text)
                validate_poll_choices(
                    choices,
                    self.request.settings.poll_max_choices,
                    self.request.settings.poll_choice_min_length,
                    self.request.settings.poll_choice_max_length,
                    self.request,
                )
                return choices
            except ValidationError as error:
                self.add_error("choices_text", error)

        if self.required and not self.errors.get("choices_text") and not self.errors.get(
            "choices_list"
        ):
            self.add_error(
                "choices_text",
                pgettext("form validation", "This field is required."),
            )
            self.add_error(
                "choices_list",
                pgettext("form validation", "This field is required."),
            )

        return None


class StartPollForm(PollForm):
    def setup_form_fields(self, settings):
        super().setup_form_fields(settings)

        if settings.enable_public_polls != PublicPollsAvailability.ENABLED:
            del self.fields["is_public"]

    def clean(self):
        cleaned_data = super().clean()

        if choices := self.clean_choices(cleaned_data):
            cleaned_data["choices"] = choices

        return cleaned_data

    def create_poll(self, category: Category, thread: Thread, user: "User") -> Poll:
        return Poll(
            category=category,
            thread=thread,
            starter=user,
            starter_name=user.username,
            starter_slug=user.slug,
            question=self.cleaned_data["question"],
            choices=self.cleaned_data["choices"].json(),
            duration=self.cleaned_data.get("duration") or 0,
            max_choices=self.cleaned_data.get("max_choices", 1),
            can_change_vote=self.cleaned_data.get("can_change_vote") or False,
            is_public=self.cleaned_data.get("is_public") or False,
        )
    
    def save(self, category: Category, thread: Thread, user: "User") -> Poll:
        poll = self.create_poll(category, thread, user)
        poll.save()
        return poll
