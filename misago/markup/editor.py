class Editor(object):
    """
    Misago editor class
    """
    def __init__(self, field, body_template='misago/editor/body.html',
                 js_template='misago/editor/js.html', allow_mentions=True,
                 allow_links=True, allow_images=True, allow_blocks=True,
                 has_preview=False, uploads_url=None):
        self.field = field
        self.auto_id = 'misago-editor-%s' % field.auto_id

        self.body_template = body_template
        self.js_template = js_template

        self.uploads_url = uploads_url

        self.allow_mentions = allow_mentions
        self.allow_links = allow_links
        self.allow_images = allow_images
        self.allow_blocks = allow_blocks

        self.has_preview = has_preview
