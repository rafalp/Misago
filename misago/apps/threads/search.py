from misago.models import Forum, Post
from misago.apps.search.views import SearchBaseView, ResultsBaseView

class SearchThreadsMixin(object):
    def queryset(self):
        return Post.objects.filter(forum__in=Forum.objects.readable_forums(self.request.acl))


class SearchView(SearchThreadsMixin, SearchBaseView):
    pass


class ResultsView(SearchThreadsMixin, ResultsBaseView):
    pass
