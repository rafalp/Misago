from django.core.urlresolvers import reverse


class Node(object):
    def __init__(self, link=None, name=None, icon=None):
        self.parent = None
        self.link = link
        self.name = name
        self.icon = icon
        self._children = []
        self._children_dict = {}

    @property
    def namespace(self):
        try:
            return self._resolved_namespace
        except AttributeError:
            bits = self.link.split(':')
            self._resolved_namespace = ':'.join(bits[:-1])

        return self._resolved_namespace

    def children(self):
        return self._children

    def children_as_dicts(self):
        childrens = []
        for children in self._children:
            childrens.append({
                    'link': reverse(children.link),
                    'namespace': self.namespace,
                    'name': children.name,
                    'icon': children.icon,
                })
        return childrens

    def add_node(self, node, after=None, before=None):
        if after:
            return self.add_node_after(node, after)
        elif before:
            return self.add_node_before(node, before)
        else:
            node.parent = self
            self._children.append(node)
            self._children_dict[node.link] = node
            return True

    def add_node_after(self, node, after):
        success = False
        new_children_list = []

        for children in self._children:
            new_children_list.append(children)
            if children.link == after:
                new_children_list.append(node)
                success = True

        if success:
            node.parent = self
            self._children_dict[node.link] = node
            self._children = new_children_list
        return success

    def add_node_before(self, node, before):
        success = False
        new_children_list = []

        for children in self._children:
            if children.link == before:
                new_children_list.append(node)
                success = True
            new_children_list.append(children)

        if success:
            node.parent = self
            self._children_dict[node.link] = node
            self._children = new_children_list
        return success

    def child(self, namespace):
        try:
            return self._children_dict[namespace]
        except KeyError:
            raise ValueError(
                "Node %s is not a child of node %s" % (namespace, self.name))

    def is_root(self):
        return False


class AdminHierarchyBuilder(object):
    def __init__(self):
        self.nodes_record = []
        self.nodes_dict = {}

    def build_nodes_dict(self):
        nodes_dict = {'misago:admin': Node(link='misago:admin:index')}

        iterations = 0
        while self.nodes_record:
            iterations += 1
            if iterations > 512:
                message = ("Misago Admin hierarchy is invalid or too complex "
                          "to resolve. Nodes left: %s" % self.nodes_record)
                raise ValueError(message)

            for index, node in enumerate(self.nodes_record):
                if node['parent'] in nodes_dict:
                    node_obj = Node(link=node['link'],
                                    name=node['name'],
                                    icon=node['icon'])

                    parent = nodes_dict[node['parent']]
                    if node['after']:
                        node_added = parent.add_node(node_obj,
                                                     after=node['after'])
                    elif node['before']:
                        node_added = parent.add_node(node_obj,
                                                     before=node['before'])
                    else:
                        node_added = parent.add_node(node_obj)

                    if node_added:
                        if node['namespace']:
                            namespace = '%s:%s' % (node['parent'], node['namespace'])
                        else:
                            namespace = node['parent']

                        if namespace not in nodes_dict:
                            nodes_dict[namespace] = node_obj

                        del self.nodes_record[index]
                        break

        return nodes_dict

    def add_node(self, parent='misago:admin', after=None, before=None,
                 namespace=None, link=None, name=None, icon=None):
        if self.nodes_dict:
            raise ValueError("Misago admin site has already been "
                             "initialized. You can't add new nodes to it.")

        if after and before:
            raise ValueError("You cannot use both after and before kwargs.")

        self.nodes_record.append({
                'parent': parent,
                'namespace': namespace,
                'after': after,
                'before': before,
                'link': link,
                'name': name,
                'icon': icon,
            })

    def visible_branches(self, request):
        if not self.nodes_dict:
            self.nodes_dict = self.build_nodes_dict()

        branches = []

        if request.resolver_match.namespace in self.nodes_dict:
            node = self.nodes_dict[request.resolver_match.namespace]
            while node:
                children = node.children_as_dicts()
                if children:
                    branches.append(children)
                node = node.parent

        branches.reverse()

        # Lowest level branch, active link
        for node in branches[0]:
            node['is_active'] = node['link'] in request.path

        # Other levels branches
        for branch in branches[1:]:
            for node in branch:
                active = node['namespace'] in request.resolver_match.namespace
                node['is_active'] = active

        # Hack for index link
        full_url_name = '%s:%s' % (request.resolver_match.namespace,
                                   request.resolver_match.url_name)
        if full_url_name != 'misago:admin:index':
            branches[0][0]['is_active'] = False

        return branches


site = AdminHierarchyBuilder()
