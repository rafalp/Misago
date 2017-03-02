from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core.shortcuts import paginate, pagination_dict
from misago.search import SearchProvider

from .models import Post, Thread
from .permissions import exclude_invisible_threads
from .serializers import FeedSerializer
from .utils import add_categories_to_items
from .viewmodels import ThreadsRootCategory


class SearchThreads(SearchProvider):
    name = _("Threads")
    url = 'threads'

    def search(self, query, page=1):
        root_category = ThreadsRootCategory(self.request)
        threads_categories = [root_category.unwrap()] + root_category.subcategories

        if len(query) > 2:
            visible_threads = exclude_invisible_threads(
                self.request.user, threads_categories, Thread.objects
            )
            results = search_threads(self.request, query, visible_threads)
        else:
            results = []

        list_page = paginate(
            results,
            page,
            settings.MISAGO_POSTS_PER_PAGE,
            settings.MISAGO_POSTS_TAIL,
            allow_explicit_first_page=True,
        )
        paginator = pagination_dict(list_page)

        posts = list(list_page.object_list)
        threads = []

        for post in posts:
            threads.append(post.thread)

        add_categories_to_items(root_category.unwrap(), threads_categories, posts + threads)

        results = {
            'results': FeedSerializer(posts, many=True, context={
                'user': self.request.user,
            }).data,
        }
        results.update(paginator)

        return results


def search_threads(request, query, visible_threads):
    search_query = SearchQuery(query, config=settings.MISAGO_SEARCH_CONFIG)
    search_vector = SearchVector('search_document', config=settings.MISAGO_SEARCH_CONFIG)

    return Post.objects.select_related('thread', 'poster').filter(
        is_event=False,
        is_hidden=False,
        is_unapproved=False,
        thread_id__in=visible_threads.values('id'),
        search_vector=search_query,
    ).annotate(rank=SearchRank(search_vector, search_query)).order_by('-rank', '-id')
