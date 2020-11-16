from collections import OrderedDict

from . import PostingMiddleware
from ....categories.models import Category


class SaveChangesMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset_state()

    def reset_state(self):
        self.user.update_all = False
        self.thread.update_all = False
        self.post.update_all = False

        self.user.update_fields = []
        self.thread.update_fields = []
        self.post.update_fields = []

        try:
            self.thread.category.update_all = False
            self.thread.category.update_fields = []
        except Category.DoesNotExist:
            # Exception for cases when thread has no category associated
            # If this is the case, its Category's middleware job to set those flags
            pass

    def save_models(self):
        self.save_model(self.user)
        self.save_model(self.thread.category)
        self.save_model(self.thread)
        self.save_model(self.post)
        self.reset_state()

    def save_model(self, model):
        if model.update_all:
            model.save()
        elif model.update_fields:
            update_fields = list(OrderedDict.fromkeys(model.update_fields))
            model.save(update_fields=update_fields)

    def save(self, serializer):
        self.save_models()

    def post_save(self, serializer):
        self.save_models()
