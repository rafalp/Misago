from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from misago.acl.exceptions import ACLError403, ACLError404
from misago.models import Forum, Thread, Post, User

class MisagoSearchQuerySet(object):
    def __init__(self, user, acl):
        self.user = user
        self.acl = acl

    def search_in(self, target):
        self.target = target

        try:
            self.allow_forum_search(target)
        except AttributeError:
            self.allow_thread_search(target)

    def allow_forum_search(self, target):
        raise Exception(dir(target))

    def allow_thread_search(self, target):
        pass

    @property
    def query(self):
        try:
            return self._searchquery
        except AttributeError:
            pass

        sqs = SearchQuerySet()

        self._searchquery = sqs
        return self._searchquery
