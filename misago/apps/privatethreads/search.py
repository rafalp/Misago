from misago.decorators import block_crawlers
from misago.models import Post
from misago.apps.errors import error404
from misago.apps.search.views import do_search, results

def allow_search(f):
    def decorator(*args, **kwargs):
        if not (request.acl.private_threads.can_participate()
                and request.settings['enable_private_threads']):
            return error404()
        return f(*args, **kwargs)
    return decorator


@block_crawlers
@allow_search
def search_private_threads(request):
    threads = [t.pk for t in request.user.private_thread_set.all()]
    queryset = Post.objects.filter(thread_id__in=threads)
    return do_search(request, queryset, 'private_threads')


@block_crawlers
@allow_search
def show_private_threads_results(request):
    return results(request, 'private_threads')
