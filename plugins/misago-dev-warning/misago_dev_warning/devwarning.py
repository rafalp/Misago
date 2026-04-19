from time import time

from django.http import HttpRequest
import misago


def display_dev_warning(action, request: HttpRequest) -> dict:
    context_data = action(request)

    if not show_warning(request):
        return context_data

    context_data["before_head_close"].append(
        {
            "template_name": "misago_dev_warning/head.html",
        }
    )
    context_data["below_navbar"].append(
        {
            "template_name": "misago_dev_warning/message.html",
        }
    )

    return context_data


def show_warning(request: HttpRequest) -> bool:
    if misago.__released__:
        return False

    dismissed = request.session.get("dismiss_dev_warning")
    if not dismissed:
        return True

    if dismissed["version"] != misago.__version__:
        return True

    return time() - dismissed["time"] > 7 * 24 * 3600
