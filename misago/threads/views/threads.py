from misago.threads.views import generic


class ThreadsMixin(object):
    templates_dir = 'misago/threads'


class ForumView(ThreadsMixin, generic.ForumView):
    pass


class ThreadView(ThreadsMixin, generic.ThreadView):
    pass


class StartThreadView(ThreadsMixin, generic.EditorView):
    pass


class ReplyView(ThreadsMixin, generic.EditorView):
    pass


class EditView(ThreadsMixin, generic.EditorView):
    pass
