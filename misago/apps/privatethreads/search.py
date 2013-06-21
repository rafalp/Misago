from misago.models import Post
from misago.acl.exceptions import ACLError404
from misago.apps.search.views import SearchBaseView, ResultsBaseView

class SearchPrivateThreadsMixin(object):
    search_route = 'private_threads_search'
    results_route = 'private_threads_results'

    def check_acl(self):
        if not (self.request.acl.private_threads.can_participate()
                and self.request.settings['enable_private_threads']):
            raise ACLError404()

    def queryset(self):
        threads = [t.pk for t in self.request.user.private_thread_set.all()]
        return Post.objects.filter(thread_id__in=threads)


class SearchView(SearchPrivateThreadsMixin, SearchBaseView):
    pass


class ResultsView(SearchPrivateThreadsMixin, ResultsBaseView):
    pass
