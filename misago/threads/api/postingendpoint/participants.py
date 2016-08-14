from misago.categories.models import PRIVATE_THREADS_ROOT_NAME

from . import PostingEndpoint, PostingMiddleware
from ...participants import add_owner, add_participant


class ThreadParticipantsFormMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.tree_name == PRIVATE_THREADS_ROOT_NAME:
            return self.mode == PostingEndpoint.START
        else:
            return False

    def make_form(self):
        return ThreadParticipantsForm(self.request.POST, user=self.request.user)

    def save(self, serializer):
        add_owner(self.thread, self.user)
        for user in serializer.users_cache:
            add_participant(self.request, self.thread, user)
