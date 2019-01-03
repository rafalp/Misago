import requests
from celery import shared_task
from requests.exceptions import RequestException

from ..models import Css


@shared_task
def update_remote_css_size(pk):
    try:
        css = Css.objects.get(pk=pk)
        css.size = get_remove_css_size(css.url)
    except Css.DoesNotExist:
        pass
    else:
        css.save(update_fields=["size"])


def get_remove_css_size(url):
    try:
        response = requests.head(url)
        response.raise_for_status()
    except RequestException:
        return 0
    else:
        try:
            return int(response.headers.get("content-length", 0))
        except (TypeError, ValueError):
            return 0
