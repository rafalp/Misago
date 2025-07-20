from typing_extensions import TYPE_CHECKING

from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext

from ..categories.models import Category
from ..threads.models import Thread
from .enums import PublicPollsAvailability
from .fields import (
    EditPollChoicesField,
    PollChoicesField,
    PollChoicesValue,
)
from .models import Poll, PollVote
from .validators import validate_poll_choices, validate_poll_question

if TYPE_CHECKING:
    from ..users.models import User


class PollForm(forms.Form):
    request: HttpRequest
    required: bool

    question = forms.CharField(max_length=255, required=False)
    duration = forms.IntegerField(
        initial=0, min_value=0, max_value=1825, required=False
    )
    max_choices = forms.IntegerField(initial=1, min_value=1, required=False)
    can_change_vote = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.required = kwargs.pop("required", True)

        super().__init__(*args, **kwargs)

        self.setup_form_fields(self.request.settings)

    def setup_form_fields(self, settings):
        self.fields["question"].max_length = settings.poll_question_max_length
        self.fields["question"].required = self.required

    def clean_question(self):
        if data := self.cleaned_data["question"]:
            validate_poll_question(
                data,
                self.request.settings.poll_question_min_length,
                self.request.settings.poll_question_max_length,
                self.request,
            )
        return data

    def clean_choices(self) -> PollChoicesValue | None:
        data = self.cleaned_data["choices"]
        if not data and not self.required:
            return data

        validate_poll_choices(
            data.json(),
            self.request.settings.poll_max_choices,
            self.request.settings.poll_choice_min_length,
            self.request.settings.poll_choice_max_length,
            self.request,
        )
        return data


class StartPollForm(PollForm):
    def setup_form_fields(self, settings):
        super().setup_form_fields(settings)

        self.fields["choices"] = PollChoicesField(
            max_choices=settings.poll_max_choices,
            required=self.required,
        )

        if settings.enable_public_polls == PublicPollsAvailability.ENABLED:
            self.fields["is_public"] = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        if (
            self.required
            and not self.cleaned_data.get("choices")
            and not self.errors.get("choices")
        ):
            self.add_error(
                "choices", pgettext("form validation", "This field is required.")
            )

        return cleaned_data

    def create_poll_instance(
        self, category: Category, thread: Thread, user: "User"
    ) -> Poll:
        choices_json = self.cleaned_data["choices"].json()

        return Poll(
            category=category,
            thread=thread,
            starter=user,
            starter_name=user.username,
            starter_slug=user.slug,
            question=self.cleaned_data["question"],
            choices=choices_json,
            duration=self.cleaned_data.get("duration") or 0,
            max_choices=min(self.cleaned_data.get("max_choices", 1), len(choices_json)),
            can_change_vote=self.cleaned_data.get("can_change_vote") or False,
            is_public=self.cleaned_data.get("is_public") or False,
        )


class EditPollForm(PollForm):
    instance: Poll

    def __init__(self, *args, **kwargs):
        self.instance = instance = kwargs.pop("instance")

        kwargs["initial"] = {
            "question": instance.question,
            "duration": instance.duration,
            "max_choices": instance.max_choices,
            "can_change_vote": instance.can_change_vote,
        }

        super().__init__(*args, **kwargs)

    def setup_form_fields(self, settings):
        super().setup_form_fields(settings)

        self.fields["choices"] = EditPollChoicesField(
            initial=PollChoicesValue(choices=self.instance.choices),
            max_choices=settings.poll_max_choices,
            required=False,
        )

    def update_poll_instance(self) -> Poll:
        choices = self.cleaned_data["choices"]

        PollVote.objects.filter(
            poll=self.instance, choice_id__in=choices.delete
        ).delete()

        self.instance.question = self.cleaned_data["question"]
        self.instance.duration = self.cleaned_data["duration"] or 0
        self.instance.choices = choices.json()
        self.instance.max_choices = min(
            self.cleaned_data["max_choices"], len(self.instance.choices)
        )
        self.instance.can_change_vote = self.cleaned_data["can_change_vote"]
        self.instance.votes = PollVote.objects.filter(poll=self.instance).count()

        return self.instance
