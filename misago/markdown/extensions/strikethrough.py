import re
import markdown
from markdown.inlinepatterns import SimpleTagPattern

# Global vars
STRIKETHROUGH_RE = r'(~{2})(.+?)\2'

class StrikethroughExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add('mi_strikethrough',
                              SimpleTagPattern(STRIKETHROUGH_RE, 'del'),
                              '_end')
