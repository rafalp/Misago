import requests
from celery import shared_task
from requests.exceptions import RequestException

from ..cache import clear_theme_cache
from ..models import Theme, Css
from .css import get_theme_media_map, rebuild_css


@shared_task
def update_remote_css_size(pk):
    try:
        css = Css.objects.get(pk=pk, url__isnull=False)
    except Css.DoesNotExist:
        pass
    else:
        css.size = get_remote_css_size(css.url)
        css.save(update_fields=["size"])


def get_remote_css_size(url):
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


@shared_task
def build_single_theme_css(pk):
    try:
        css = Css.objects.get(pk=pk, source_needs_building=True)
    except Css.DoesNotExist:
        pass
    else:
        media_map = get_theme_media_map(css.theme)
        rebuild_css(media_map, css)
        clear_theme_cache()


@shared_task
def build_theme_css(pk):
    try:
        theme = Theme.objects.get(pk=pk)
    except Theme.DoesNotExist:
        pass
    else:
        media_map = get_theme_media_map(theme)
        for css in theme.css.filter(source_needs_building=True):
            rebuild_css(media_map, css)
        clear_theme_cache()
