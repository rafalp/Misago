#-*- coding: utf-8 -*-
import re
import markdown
from markdown.inlinepatterns import LinkPattern
from markdown.postprocessors import RawHtmlPostprocessor
from markdown.util import etree
from misago.utils.strings import html_escape
from misago.utils.urls import is_inner, clean_inner

# Global vars
MAGICLINKS_RE = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', re.UNICODE)

class MagicLinksExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.add('mi_magiclinks',
                              MagicLinksTreeprocessor(md),
                              '_end')


class MagicLinksTreeprocessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        return self.walk_tree(root)

    def walk_tree(self, node):
        def parse_link(matchobj):
            link = LinkPattern(MAGICLINKS_RE, self.markdown)
            href = link.sanitize_url(link.unescape(matchobj.group(0).strip()))
            if href:
                if is_inner(href):
                    clean = clean_inner(href)
                    return self.markdown.htmlStash.store('<a href="%s">%s</a>' % (clean, clean[1:]), safe=True)
                else:
                    return self.markdown.htmlStash.store('<a href="%(href)s" rel="nofollow">%(href)s</a>' % {'href': href}, safe=True)
            else:
                return matchobj.group(0)

        if node.tag not in ['code', 'pre', 'a', 'img']:
            if node.text and unicode(node.text).strip():
                node.text = MAGICLINKS_RE.sub(parse_link, unicode(node.text))
            if node.tail and unicode(node.tail).strip():
                node.tail = MAGICLINKS_RE.sub(parse_link, unicode(node.tail))
            for i in node:
                self.walk_tree(i)