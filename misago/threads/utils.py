from django.core.urlresolvers import resolve
from django.utils import six
from django.utils.six.moves.urllib.parse import urlparse


def add_categories_to_threads(root_category, categories, threads):
    categories_dict = {}
    for category in categories:
        categories_dict[category.pk] = category

    top_categories_map = {}

    for thread in threads:
        thread.top_category = None
        thread.category = categories_dict[thread.category_id]

        if thread.category == root_category:
            continue
        elif thread.category.parent_id == root_category.pk:
            thread.top_category = thread.category
        elif thread.category_id in top_categories_map:
            thread.top_category = top_categories_map[thread.category_id]
        elif root_category.has_child(thread.category):
            # thread in subcategory resolution
            for category in categories:
                if (category.parent_id == root_category.pk and
                        category.has_child(thread.category)):
                    top_categories_map[thread.category_id] = category
                    thread.top_category = category
        else:
            # global thread in other category resolution
            for category in categories:
                if category.level == 1 and (
                        category == thread.category or
                        category.has_child(thread.category)):
                    top_categories_map[thread.category_id] = category
                    thread.top_category = category


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
