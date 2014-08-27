from collections import OrderedDict

from misago.threads.posting import PostingMiddleware


class SaveChangesMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(SaveChangesMiddleware, self).__init__(**kwargs)
        self.reset_state()

    def reset_state(self):
        self.user.update_all = False
        self.forum.update_all = False
        self.thread.update_all = False
        self.post.update_all = False

        self.user.update_fields = []
        self.forum.update_fields = []
        self.thread.update_fields = []
        self.post.update_fields = []

    def save_models(self):
        self.save_model(self.user)
        self.save_model(self.forum)
        self.save_model(self.thread)
        self.save_model(self.post)
        self.reset_state()

    def save_model(self, model):
        if model.update_all:
            model.save()
        elif model.update_fields:
            update_fields = list(OrderedDict.fromkeys(model.update_fields))
            model.save(update_fields=update_fields)

    def save(self, form):
        self.save_models()

    def post_save(self, form):
        self.save_models(self.user)
