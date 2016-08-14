class Editor(object):
    """
    Misago editor class
    """
    def __init__(self, field, allow_mentions=True, allow_links=True, allow_images=True, allow_blocks=True):
        self.field = field
        self.auto_id = 'misago-editor-%s' % field.auto_id

        self.allow_mentions = allow_mentions
        self.allow_links = allow_links
        self.allow_images = allow_images
        self.allow_blocks = allow_blocks
