from misago.threads.views import generic


class ForumView(generic.ForumView):
    link_name = 'misago:forum'


class ThreadView(generic.ThreadView):
    pass


class ModeratedPostsListView(generic.ModeratedPostsListView):
    pass


class ReportedPostsListView(generic.ReportedPostsListView):
    pass


class GotoLastView(generic.GotoLastView):
    pass


class GotoNewView(generic.GotoNewView):
    pass


class GotoPostView(generic.GotoPostView):
    pass
