from misago.decorators import block_crawlers
from misago.models import Forum, Post
from misago.apps.errors import error404
from misago.apps.search.views import do_search, results

def allow_search(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.acl.reports.can_handle():
            return error404()
        return f(*args, **kwargs)
    return decorator


@block_crawlers
@allow_search
def search_reports(request):
    queryset = Post.objects.filter(forum=Forum.objects.special_pk('reports'))
    return do_search(request, queryset, 'reports')


@block_crawlers
@allow_search
def show_reports_results(request, page=0):
    return results(request, page, 'reports')
