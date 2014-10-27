from misago.threads.views import generic


class ThreadsMixin(object):
    pass


class ForumView(ThreadsMixin, generic.ForumView):
    link_name = 'misago:forum'


class ThreadView(ThreadsMixin, generic.ThreadView):
    pass


class ModeratedPostsListView(ThreadsMixin, generic.ModeratedPostsListView):
    pass


class ReportedPostsListView(ThreadsMixin, generic.ReportedPostsListView):
    pass


class GotoLastView(ThreadsMixin, generic.GotoLastView):
    pass


class GotoNewView(ThreadsMixin, generic.GotoNewView):
    pass


class GotoPostView(ThreadsMixin, generic.GotoPostView):
    pass
