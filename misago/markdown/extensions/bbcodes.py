import re
import markdown
from markdown.inlinepatterns import SimpleTagPattern

EMPHASIS_RE = r'\[i\]([^*]+)\[/i\]'
STRONG_RE = r'\[b\]([^*]+)\[/b\]'
STRONG_ALT_RE = r'\[u\]([^*]+)\[/u\]'

class BBCodesExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add('mi_bb_bold_alt',
                              SimpleTagPattern(STRONG_ALT_RE, 'strong'),
                              '>strong')
        md.inlinePatterns.add('mi_bb_bold',
                              SimpleTagPattern(STRONG_RE, 'strong'),
                              '>strong')
        md.inlinePatterns.add('mi_bb_italics',
                              SimpleTagPattern(EMPHASIS_RE, 'em'),
                              '>emphasis')
