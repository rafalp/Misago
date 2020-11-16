from .followers import Followers


class Follows(Followers):
    def get_queryset(self, profile):
        return profile.follows

    def get_template_context(self):
        return {"follows": self.users, "count": self.paginator["count"]}
