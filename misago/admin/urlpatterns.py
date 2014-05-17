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

    def get_child_patterns(self, parent):
        prefix = '%s:' % parent if parent else ''

        urlpatterns = self.namespace_patterns.get(parent, [])
        for namespace in self._namespaces:
            if namespace['parent'] == parent:
                prefixed_namespace = prefix + namespace['namespace']
                urlpatterns = self.get_child_patterns(prefixed_namespace)
                included_patterns = include(urlpatterns,
                                            namespace=namespace['namespace'])
                urlpatterns += patterns('',
                    url(namespace['path'], included_patterns)
                )

        return urlpatterns

    def sum_registered_patters(self):
        all_patterns = {}
        for urls in self._patterns:
            namespace = urls['namespace']
            urlpatterns = urls['urlpatterns']
            all_patterns.setdefault(namespace, []).extend(urlpatterns)

        self.namespace_patterns = all_patterns

    def build_root_urlpatterns(self):
        root_urlpatterns = []
        for namespace in self._namespaces:
            if not namespace['parent']:
                urlpatterns = self.get_child_patterns(namespace['namespace'])
                included_patterns = include(urlpatterns,
                                            namespace=namespace['namespace'])
                root_urlpatterns += patterns('',
                    url(namespace['path'], included_patterns)
                )

        return root_urlpatterns

    def build_urlpatterns(self):
        self.sum_registered_patters()
        return self.build_root_urlpatterns()

    def __call__(self):
        try:
            return self._urlpatterns
        except AttributeError:
            self._urlpatterns = self.build_urlpatterns()
            self._namespaces = []
            self._patterns = []
            return self._urlpatterns
