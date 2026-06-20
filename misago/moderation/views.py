from typing import Iterable

from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import pgettext

from .actions import ModerationAction, ModerationActionResult


def get_moderation_action(
    actions: Iterable[ModerationAction], action_id: str
) -> ModerationAction:
    for action in actions:
        if action.id == action_id:
            return action

    raise ValidationError(
        pgettext("moderation action error", "Invalid moderation action."),
    )


def get_moderation_action_choices(actions: list[ModerationAction]) -> list[dict]:
    return [
        {
            "id": action.id,
            "full_name": action.full_name or action.button_label,
            "button_label": action.button_label,
            "multistage": action.multistage,
        }
        for action in actions
    ]


def get_moderation_result_response(
    request: HttpRequest, result: ModerationActionResult
) -> HttpResponse | None:
    if result.refresh:
        if not request.is_htmx:
            return redirect(request.get_full_path())

        response = HttpResponse(status=201)
        response.headers["hx-refresh"] = "true"
        set_moderation_response_headers(request, response)
        return response

    if result.redirect_to:
        if not request.is_htmx:
            return redirect(result.redirect_to)

        response = HttpResponse(status=201)
        response.headers["hx-redirect"] = result.redirect_to
        set_moderation_response_headers(request, response)
        return response

    return None


def set_moderation_response_headers(request: HttpRequest, response: HttpResponse):
    response.headers["hx-trigger"] = "misago:afterModeration"

    if request.POST.get("success-hx-target"):
        response.headers["hx-retarget"] = request.POST["success-hx-target"]

    if request.POST.get("success-hx-swap"):
        response.headers["hx-reswap"] = request.POST["success-hx-swap"]
