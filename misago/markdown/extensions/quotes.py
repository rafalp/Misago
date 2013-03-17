import re
import markdown
from markdown.util import etree

# Global vars
QUOTE_AUTHOR_RE = re.compile(r'^(?P<arrows>(>|\s)+)?@(?P<username>(\w|\d)+)$')

class QuoteTitlesExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.add('mi_quote_title',
                             QuoteTitlesPreprocessor(md),
                             '>fenced_code_block')
        md.postprocessors.add('mi_quote_title',
                              QuoteTitlesPostprocessor(md),
                              '_end')


class QuoteTitlesPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)

    def run(self, lines):
        clean = []
        for l, line in enumerate(lines):
            try:
                if line.strip():
                    at_match = QUOTE_AUTHOR_RE.match(line.strip())
                    if at_match and lines[l + 1].strip()[0] == '>':
                        username = '<%(token)s:quotetitle>@%(name)s</%(token)s:quotetitle>' % {'token': self.markdown.mi_token, 'name': at_match.group('username')}
                        if at_match.group('arrows'):
                            clean.append('> %s%s' % (at_match.group('arrows'), username))
                        else:
                            clean.append('> %s' % username)
                    else:
                        clean.append(line)
                else:
                    clean.append(line)
            except IndexError:
                clean.append(line)
        return clean


class QuoteTitlesPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        text = text.replace('&lt;%s:quotetitle&gt;' % self.markdown.mi_token, '<h3><quotetitle>')
        text = text.replace('&lt;/%s:quotetitle&gt;' % self.markdown.mi_token, '</quotetitle></h3>')
        lines = text.splitlines()
        clean = []
        for l, line in enumerate(lines):
            clean.append(line)
            try:
                if line == '<blockquote>':
                    if lines[l + 1][0:7] != '<p><h3>':
                        clean.append('<h3><quotesingletitle></h3>')
            except IndexError:
                pass
        return '\r\n'.join(clean)
