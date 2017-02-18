from .followers import Followers


class Follows(Followers):
    def get_queryset(self, profile):
        return profile.follows
