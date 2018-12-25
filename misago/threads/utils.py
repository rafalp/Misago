from urllib.parse import urlparse

from django.urls import Resolver404, resolve

from .models import PostLike


def add_categories_to_items(root_category, categories, items):
    categories_dict = {}
    for category in categories:
        categories_dict[category.pk] = category

    for item in items:
        item.category = categories_dict[item.category_id]


def add_likes_to_posts(user, posts):
    if user.is_anonymous:
        return

    posts_map = {}
    for post in posts:
        posts_map[post.id] = post
        post.is_liked = False

    queryset = PostLike.objects.filter(liker=user, post_id__in=posts_map.keys())

    for like in queryset.values("post_id"):
        posts_map[like["post_id"]].is_liked = True


SUPPORTED_THREAD_ROUTES = {
    "misago:thread": "pk",
    "misago:thread-post": "pk",
    "misago:thread-last": "pk",
    "misago:thread-new": "pk",
    "misago:thread-unapproved": "pk",
}


def get_thread_id_from_url(request, url):  # pylint: disable=too-many-return-statements
    clean_url = str(url).strip()
    url_bits = urlparse(clean_url)

    if url_bits.netloc and url_bits.netloc != request.get_host():
        return None

    if url_bits.path.startswith(request.get_host()):
        clean_path = url_bits.path.lstrip(request.get_host())
    else:
        clean_path = url_bits.path

    wsgi_alias = request.path[: len(request.path_info) * -1]
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
