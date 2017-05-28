from django.conf.urls import include, url


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

    def patterns(self, namespace, *new_patterns):
        self._patterns.append({
            'namespace': namespace,
            'urlpatterns': new_patterns,
        })

    def get_child_patterns(self, parent):
        prefix = '%s:' % parent if parent else ''

        namespace_urlpatterns = self.namespace_patterns.get(parent, [])
        for namespace in self._namespaces:
            if namespace['parent'] == parent:
                prefixed_namespace = prefix + namespace['namespace']
                child_patterns = self.get_child_patterns(prefixed_namespace)
                included_patterns = include(
                    (child_patterns, namespace['namespace']),
                    namespace=namespace['namespace'],
                )
                namespace_urlpatterns.append(url(namespace['path'], included_patterns))

        return namespace_urlpatterns

    def sum_registered_patters(self):
        all_patterns = {}
        for urls in self._patterns:
            namespace = urls['namespace']
            added_patterns = urls['urlpatterns']
            all_patterns.setdefault(namespace, []).extend(added_patterns)

        self.namespace_patterns = all_patterns

    def build_root_urlpatterns(self):
        root_urlpatterns = []
        for namespace in self._namespaces:
            if not namespace['parent']:
                child_patterns = self.get_child_patterns(namespace['namespace'])
                included_patterns = include(
                    (child_patterns, namespace['namespace']),
                    namespace=namespace['namespace'],
                )
                root_urlpatterns.append(url(namespace['path'], included_patterns))

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


urlpatterns = URLPatterns()
