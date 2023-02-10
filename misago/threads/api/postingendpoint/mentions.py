from . import PostingEndpoint, PostingMiddleware


class MentionsMiddleware(PostingMiddleware):
    def post_save(self, serializer):
        existing_mentions = []
        if self.mode == PostingEndpoint.EDIT:
            existing_mentions = self.get_existing_mentions()

        new_mentions = []
        for user_pk in self.post.parsing_result["mentions"]:
            if user_pk not in existing_mentions:
                new_mentions.append(user_pk)

        if new_mentions:
            self.post.mentions.add(*new_mentions)

    def get_existing_mentions(self):
        return [u["id"] for u in self.post.mentions.values("id").iterator()]
