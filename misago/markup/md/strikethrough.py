import markdown
from markdown.inlinepatterns import SimpleTagPattern

STRIKETHROUGH_RE = r"(~{2})(.+?)\2"


class StrikethroughExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(
            SimpleTagPattern(STRIKETHROUGH_RE, "del"), "misago_strikethrough", 100
        )
