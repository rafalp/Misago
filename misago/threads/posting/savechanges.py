from misago.threads.posting import PostingMiddleware


class SaveChangesMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(SaveChangesMiddleware, self).__init__(**kwargs)

        self.user.save_model = False
        self.forum.save_model = False
        self.thread.save_model = False
        self.post.save_model = False

        self.user.update_fields = []
        self.forum.update_fields = []
        self.thread.update_fields = []
        self.post.update_fields = []

    def save(self, form):
        self.save_model(self.user)
        self.save_model(self.forum)
        self.save_model(self.thread)
        self.save_model(self.post)

    def save_model(self, model):
        if model.save_model:
            model.save()
        elif model.update_fields:
           model.save(update_fields=model.update_fields)
