class Node(object):
    def __init__(self, link=None, name=None, icon=None):
        self.link = link
        self.name = name
        self.icon = icon
        self._children = []
        self._children_dict = {}

    def children(self):
        return self._children

    def add_node(self, node, after=None, before=None):
        self._children.append(node)
        self._children_dict[node['link']] = node

    def child(self, node):
        try:
            return self._children_dict[node]
        except KeyError:
            raise ValueError(
                "Node %s is not a child of node %s" % (node, self.name))

    def is_root(self):
        return False



class AdminHierarchyBuilder(object):
    def __init__(self):
        self.nodes_record = []
        self.nodes_dict = {}

    def build_nodes_dict(self):
        nodes_dict = {'misago:admin': Node()}

        iterations = 0
        while self.nodes_record:
            iterations += 1
            if iterations > 512:
                message = ("Misago Admin hierarchy is invalid or too complex "
                          "to resolve. Nodes left: %s" % self.nodes_record)
                raise ValueError(message)

            node = self.nodes_record[0]
            if node['parent'] in nodes_dict:
                parent = nodes_dict[node['parent']]
                node_obj = Node(link=node['link'],
                                name=node['name'],
                                icon=node['icon'])
                if node['after']:
                    parent.add_node(node, after=node['after'])
                elif node['before']:
                    parent.add_node(node, before=node['before'])
                else:
                    parent.add_node(node)

                namespace = ':'.join(node['link'].split(':')[:-1])
                if namespace not in nodes_dict:
                    nodes_dict[namespace] = node
                self.nodes_record = self.nodes_record[1:]

        return nodes_dict

    def add_node(self, parent='misago:admin', after=None, before=None,
                 link=None, name=None, icon=None):
        if self.nodes_dict:
            raise ValueError("Misago admin site has already been "
                             "initialized. You can't add new nodes to it.")

        if after and before:
            raise ValueError("You cannot use both after and before kwargs.")

        self.nodes_record.append({
                'parent': parent,
                'after': after,
                'before': before,
                'link': link,
                'name': name,
                'icon': icon,
            })

    def is_root(self):
        return True

    def children(self, node='misago:admin'):
        if not self.nodes_dict:
            self.nodes_dict = self.build_nodes_dict()
        return self.nodes_dict[node].children()

    def parent(self):
        raise ValueError("Root node has no parent!")


site = AdminHierarchyBuilder()
