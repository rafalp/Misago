import markdown
from markdown.util import etree
from misago.utils.urls import is_url, is_inner, clean_inner

class CleanLinksExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.add('mi_cleanlinks',
                              CleanLinksTreeprocessor(md),
                              '_end')


class CleanLinksTreeprocessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        self.inurl = False
        return self.walk_tree(root)

    def walk_tree(self, node):
        if node.tag == 'a':
            self.inurl = True
            if is_inner(node.get('href')):
                node.set('href', clean_inner(node.get('href')))
            else:
                node.set('rel', 'nofollow')
        if node.tag == 'img':
            if is_inner(node.get('src')):
                node.set('src', '%s' % clean_inner(node.get('src')))

        try:
            if self.inurl and is_url(node.text) and is_inner(node.text):
                node.text = clean_inner(node.text)[1:]
        except TypeError:
            pass
            
        for i in node:
            self.walk_tree(i)
        self.inurl = False
