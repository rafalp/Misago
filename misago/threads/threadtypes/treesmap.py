from importlib import import_module

from misago.conf import settings


class TreesMap(object):
    """Object that maps trees to strategies"""

    def __init__(self, types_modules):
        self.is_loaded = False
        self.types_modules = types_modules

    def load(self):
        self.types = self.load_types(self.types_modules)
        self.trees = self.load_trees(self.types)
        self.roots = self.get_roots(self.trees)
        self.is_loaded = True

    def load_types(self, types_modules):
        loaded_types = {}
        for path in types_modules:
            module = import_module('.'.join(path.split('.')[:-1]))
            type_cls = getattr(module, path.split('.')[-1])
            loaded_types[type_cls.root_name] = type_cls()
        return loaded_types

    def load_trees(self, types):
        from misago.categories.models import Category
        trees = {}
        for category in Category.objects.filter(level=0, special_role__in=types.keys()):
            trees[category.tree_id] = types[category.special_role]
        return trees

    def get_roots(self, trees):
        roots = {}
        for tree_id in trees:
            roots[trees[tree_id].root_name] = tree_id
        return roots

    def get_type_for_tree_id(self, tree_id):
        if not self.is_loaded:
            self.load()

        try:
            return self.trees[tree_id]
        except KeyError:
            raise KeyError("'%s' tree id has no type defined" % tree_id)

    def get_tree_id_for_root(self, root_name):
        if not self.is_loaded:
            self.load()

        try:
            return self.roots[root_name]
        except KeyError:
            raise KeyError('"%s" root has no tree defined' % root_name)


trees_map = TreesMap(settings.MISAGO_THREAD_TYPES)
