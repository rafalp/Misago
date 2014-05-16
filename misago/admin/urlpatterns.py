from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse


class URLPatterns(object):
    def __init__(self):
        self._namespaces = []
        self._patterns = []

    def namespace(self, path, namespace, parent=None):
        self._namespaces.append({
            'path': path,
            'parent': parent,
            'namespace': namespace,
            })

    def patterns(self, namespace, *urlpatterns):
        self._patterns.append({
            'namespace': namespace,
            'urlpatterns': patterns('', *urlpatterns),
            })

    def subpatterns(self, namespace):
        prefix = '%s:' % namespace if namespace else ''

        urlpatterns = self.namespace_patterns.get(namespace, [])
        for subspace in self._namespaces:
            if subspace['parent'] == namespace:
                subspace_name = prefix + subspace['namespace']
                namespace_patterns = self.subpatterns(subspace_name)
                included = include(namespace_patterns,
                                   namespace=subspace['namespace'])
                urlpatterns += patterns('',
                    url(subspace['path'], included)
                )

        return urlpatterns

    def sum_registered_patters(self):
        all_patterns = {}
        for urls in self._patterns:
            namespace = urls['namespace']
            urlpatterns = urls['urlpatterns']
            all_patterns.setdefault(namespace, []).extend(urlpatterns)

        self.namespace_patterns = all_patterns

    def build_urlpatterns(self):
        self.sum_registered_patters()

        urlpatterns = []
        for namespace in self._namespaces:
            if not namespace['parent']:
                namespace_patterns = self.subpatterns(namespace['namespace'])
                included = include(namespace_patterns,
                                   namespace=namespace['namespace'])
                urlpatterns += patterns('',
                    url(namespace['path'], included)
                )

        return urlpatterns

    def __call__(self):
        try:
            return self._urlpatterns
        except AttributeError:
            self._urlpatterns = self.build_urlpatterns()
            self._namespaces = []
            self._patterns = []
            return self._urlpatterns

