from misago.threads.views import generic


class ThreadsMixin(object):
    pass


class ForumView(ThreadsMixin, generic.ForumView):
    link_name = 'misago:forum'


class ThreadView(ThreadsMixin, generic.ThreadView):
    pass


class StartThreadView(ThreadsMixin, generic.EditorView):
    pass


class ReplyView(ThreadsMixin, generic.EditorView):
    pass


class EditView(ThreadsMixin, generic.EditorView):
    pass
