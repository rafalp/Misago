from urllib.parse import urlparse

from django.db import transaction
from django.urls import Resolver404, resolve

from .models import Thread

SUPPORTED_THREAD_ROUTES = {
    "misago:thread": "thread_id",
    "misago:thread-post": "thread_id",
    "misago:thread-post-last": "thread_id",
    "misago:thread-post-unapproved": "thread_id",
    "misago:thread-post-unread": "thread_id",
    "misago:thread-post-solution": "thread_id",
}


def get_thread_id_from_url(request, url):
    clean_url = str(url).strip()
    url_bits = urlparse(clean_url)

    if url_bits.netloc and url_bits.netloc != request.get_host():
        return None

    if url_bits.path.startswith(request.get_host()):
        clean_path = url_bits.path.lstrip(request.get_host())
    else:
        clean_path = url_bits.path

    wsgi_alias = request.path_info[: len(request.path_info) * -1]
    if wsgi_alias and not clean_path.startswith(wsgi_alias):
        return None

    try:
        resolution = resolve(clean_path[len(wsgi_alias) :])
    except Resolver404:
        return None

    if not resolution.namespaces:
        return None

    url_name = "%s:%s" % (":".join(resolution.namespaces), resolution.url_name)
    kwargname = SUPPORTED_THREAD_ROUTES.get(url_name)

    if not kwargname:
        return None

    try:
        return int(resolution.kwargs.get(kwargname))
    except (TypeError, ValueError):
        return None


def remove_private_threads_without_members(user):
    queryset = Thread.objects.filter(
        id__in=user.privatethreadmember_set.values("thread_id"),
    ).order_by("-id")
    for thread in queryset.iterator(chunk_size=50):
        if thread.privatethreadmember_set.count() <= 1:
            with transaction.atomic():
                thread.delete()
