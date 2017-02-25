from django.urls import resolve
from django.utils import six
from django.utils.six.moves.urllib.parse import urlparse

from .models import PostLike


def add_categories_to_items(root_category, categories, items):
    categories_dict = {}
    for category in categories:
        categories_dict[category.pk] = category

    top_categories_map = {}

    for item in items:
        item.top_category = None
        item.category = categories_dict[item.category_id]

        if item.category == root_category:
            continue
        elif item.category.parent_id == root_category.pk:
            item.top_category = item.category
        elif item.category_id in top_categories_map:
            item.top_category = top_categories_map[item.category_id]
        elif root_category.has_child(item.category):
            # item in subcategory resolution
            for category in categories:
                if (category.parent_id == root_category.pk and category.has_child(item.category)):
                    top_categories_map[item.category_id] = category
                    item.top_category = category
        else:
            # item from other category's scope
            for category in categories:
                category_is_parent = category.has_child(item.category)
                if category.level == 1 and (category == item.category or category_is_parent):
                    top_categories_map[item.category_id] = category
                    item.top_category = category


def add_likes_to_posts(user, posts):
    if user.is_anonymous:
        return

    posts_map = {}
    for post in posts:
        posts_map[post.id] = post
        post.is_liked = False

    queryset = PostLike.objects.filter(liker=user, post_id__in=posts_map.keys())

    for like in queryset.values('post_id'):
        posts_map[like['post_id']].is_liked = True


SUPPORTED_THREAD_ROUTES = {
    'misago:thread': 'pk',
    'misago:thread-post': 'pk',
    'misago:thread-last': 'pk',
    'misago:thread-new': 'pk',
    'misago:thread-unapproved': 'pk',
}


def get_thread_id_from_url(request, url):
    try:
        clean_url = six.text_type(url).strip()
        bits = urlparse(clean_url)
    except:
        return None

    if bits.netloc and bits.netloc != request.get_host():
        return None

    if bits.path.startswith(request.get_host()):
        clean_path = bits.path.lstrip(request.get_host())
    else:
        clean_path = bits.path

    try:
        wsgi_alias = request.path[:len(request.path_info) * -1]
        resolution = resolve(clean_path[len(wsgi_alias):])
    except:
        return None

    if not resolution.namespaces:
        return None

    url_name = '{}:{}'.format(':'.join(resolution.namespaces), resolution.url_name)
    kwargname = SUPPORTED_THREAD_ROUTES.get(url_name)

    if not kwargname:
        return None

    try:
        return int(resolution.kwargs.get(kwargname))
    except (TypeError, ValueError):
        return None
