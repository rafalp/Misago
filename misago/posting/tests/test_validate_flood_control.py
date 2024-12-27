from django.core.exceptions import ValidationError

from ..formsets import get_start_thread_formset
from ..state import StartThreadState
from ..validators import validate_flood_control


def test_validate_flood_control_passes_user_without_posts(
    user_request, default_category
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert validate_flood_control(formset, state)


def test_validate_flood_control_fails_user_on_flood_control(
    user_request, default_category, user_reply
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert not validate_flood_control(formset, state)

    error = formset.errors[0]
    assert isinstance(error, ValidationError)
    assert error.message == (
        "You can't post a new message so soon after the previous one."
    )
    assert error.code == "flood_control"
