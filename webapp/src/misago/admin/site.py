from django.urls import reverse


class Node:
    def __init__(self, *, name=None, description=None, icon=None, link=None):
        self.parent = None
        self.name = name
        self.description = description
        self.icon = icon
        self.link = link
        self._children = []
        self._children_dict = {}
        self._resolved_namespace = None

    @property
    def namespace(self):
        if self._resolved_namespace:
            return self._resolved_namespace

        bits = self.link.split(":")
        self._resolved_namespace = ":".join(bits[:-1])
        return self._resolved_namespace

    def children(self):
        return self._children

    def children_as_dicts(self):
        childrens = []
        for children in self._children:
            childrens.append(
                {
                    "name": children.name,
                    "description": children.description,
                    "icon": children.icon,
                    "link": reverse(children.link),
                    "namespace": children.namespace,
                }
            )
        return childrens

    def add_node(self, node, after=None, before=None):
        if after:
            return self.add_node_after(node, after)
        if before:
            return self.add_node_before(node, before)
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
                "Node %s is not a child of node %s" % (namespace, self.name)
            )

    def is_root(self):
        return False


class AdminSite:
    def __init__(self):
        self.nodes_record = []
        self.nodes_dict = {}

    def build_nodes_dict(self):
        nodes_dict = {"misago:admin": Node(link="misago:admin:index")}

        iterations = 0
        while self.nodes_record:
            iterations += 1
            if iterations > 512:
                message = (
                    "Misago Admin hierarchy is invalid or too complex to resolve. "
                    "Nodes left: %s"
                )
                raise ValueError(message % self.nodes_record)

            for index, node in enumerate(self.nodes_record):
                if node["parent"] in nodes_dict:
                    node_obj = Node(
                        name=node["name"],
                        description=node["description"],
                        icon=node["icon"],
                        link=node["link"],
                    )

                    parent = nodes_dict[node["parent"]]
                    if node["after"]:
                        node_added = parent.add_node(node_obj, after=node["after"])
                    elif node["before"]:
                        node_added = parent.add_node(node_obj, before=node["before"])
                    else:
                        node_added = parent.add_node(node_obj)

                    if node_added:
                        namespace = node.get("namespace") or node_obj.namespace

                        if namespace not in nodes_dict:
                            nodes_dict[namespace] = node_obj

                        del self.nodes_record[index]
                        break

        return nodes_dict

    def add_node(
        self,
        *,
        name=None,
        description=None,
        icon=None,
        parent=None,
        after=None,
        before=None,
        namespace=None,
        link="index",
    ):
        if self.nodes_dict:
            raise RuntimeError(
                "Misago admin site has already been initialized. "
                "You can't add new nodes to it."
            )

        if after and before:
            raise ValueError("after and before arguments are exclusive")

        self.nodes_record.append(
            {
                "name": name,
                "description": description,
                "icon": icon,
                "parent": join_namespace(parent),
                "after": join_namespace(parent, after) if after else None,
                "before": join_namespace(parent, before) if before else None,
                "namespace": join_namespace(parent, namespace),
                "link": join_namespace(parent, namespace, link),
            }
        )

    def visible_branches(self, request):
        if not self.nodes_dict:
            self.nodes_dict = self.build_nodes_dict()

        branches = []

        try:
            namespace = request.resolver_match.namespace
        except AttributeError:
            namespace = "misago:admin"

        if namespace in self.nodes_dict:
            node = self.nodes_dict[namespace]
            while node:
                children = node.children_as_dicts()
                if children:
                    branches.append(children)
                node = node.parent

        try:
            namespaces = request.resolver_match.namespaces
        except AttributeError:
            namespaces = ["misago", "admin"]

        branches.reverse()
        for depth, branch in enumerate(branches):
            depth_namespace = namespaces[2 : 3 + depth]
            for node in branch:
                node_namespace = node["namespace"].split(":")[2 : 3 + depth]
                if request.resolver_match:
                    node["is_active"] = depth_namespace == node_namespace
                else:
                    node["is_active"] = False

        return branches


def join_namespace(*args):
    parts = list(filter(None, args))
    parts.insert(0, "misago:admin")
    return ":".join(parts)


site = AdminSite()
