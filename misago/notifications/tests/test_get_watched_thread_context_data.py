from ..templates import (
    WATCH_THREAD_BUTTON_TEMPLATE,
    WATCH_THREAD_DROPDOWN_TEMPLATE,
)
from ..threads import watch_thread
from ..views import get_watched_thread_context_data


def test_get_watched_thread_context_data_for_unwatched_thread():
    context = get_watched_thread_context_data()

    assert context == {
        "button_template": WATCH_THREAD_BUTTON_TEMPLATE,
        "dropdown_template": WATCH_THREAD_DROPDOWN_TEMPLATE,
        "notifications_enabled": False,
        "notifications_site_and_email": False,
        "notifications_site_only": False,
        "notifications_disabled": True,
    }


def test_get_watched_thread_context_data_for_watched_thread_with_email_notifications(
    thread, user
):
    watched_thread = watch_thread(thread, user, send_emails=True)
    context = get_watched_thread_context_data(watched_thread)

    assert context == {
        "button_template": WATCH_THREAD_BUTTON_TEMPLATE,
        "dropdown_template": WATCH_THREAD_DROPDOWN_TEMPLATE,
        "notifications_enabled": True,
        "notifications_site_and_email": True,
        "notifications_site_only": False,
        "notifications_disabled": False,
    }


def test_get_watched_thread_context_data_for_watched_thread_without_email_notifications(
    thread, user
):
    watched_thread = watch_thread(thread, user, send_emails=False)
    context = get_watched_thread_context_data(watched_thread)

    assert context == {
        "button_template": WATCH_THREAD_BUTTON_TEMPLATE,
        "dropdown_template": WATCH_THREAD_DROPDOWN_TEMPLATE,
        "notifications_enabled": True,
        "notifications_site_and_email": False,
        "notifications_site_only": True,
        "notifications_disabled": False,
    }
