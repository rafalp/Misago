from misago.models import Forum, Post
from misago.acl.exceptions import ACLError404
from misago.apps.search.views import SearchBaseView, ResultsBaseView

class SearchReportsMixin(object):
    search_route = 'reports_search'
    results_route = 'reports_results'
    
    def check_acl(self):
        if not self.request.acl.reports.can_handle():
            raise ACLError404()

    def queryset(self):
        return Post.objects.filter(forum=Forum.objects.special_pk('reports'))


class SearchView(SearchReportsMixin, SearchBaseView):
    pass


class ResultsView(SearchReportsMixin, ResultsBaseView):
    pass
