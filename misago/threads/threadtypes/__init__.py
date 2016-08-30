from .treesmap import trees_map


class ThreadType(object):
    """Abstract class for thread type strategy"""
    root_name = 'undefined'

    def get_forum_name(self, category):
        return category.name
