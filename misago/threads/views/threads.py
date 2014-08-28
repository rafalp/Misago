from misago.threads.views import generic


class ThreadsMixin(object):
    templates_dir = 'misago/threads'


class ForumView(ThreadsMixin, generic.ForumView):
    link_name = 'misago:forum'

    def get_default_link_params(self, forum):
        return {'forum_slug': forum.slug, 'forum_id': forum.id}


class ThreadView(ThreadsMixin, generic.ThreadView):
    pass


class StartThreadView(ThreadsMixin, generic.EditorView):
    pass


class ReplyView(ThreadsMixin, generic.EditorView):
    pass


class EditView(ThreadsMixin, generic.EditorView):
    pass
