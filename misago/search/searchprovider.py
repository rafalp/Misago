class SearchProvider(object):
    def __init__(self, request):
        self.request = request

    def allow_search(self):
        pass

    def search(self, query, page=1):
        raise NotImplementedError(
            '%s has to define search(query, page=1) method' % self.__class__.__name__
        )
