import re
import markdown
from markdown.util import etree

# Global vars
QUOTE_AUTHOR_RE = re.compile(r'^(?P<arrows>(>|\s)+)?@(?P<username>\w+)$', re.UNICODE)

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

    def find_quote_depth(self, line):
        depth = 0
        try:
            while line[0] == '>':
                depth += 1
                line = line[1:].strip()
        except IndexError:
            pass
        return depth

    def run(self, lines):
        clean = []
        quote_dept = 0
        for l, line in enumerate(lines):
            if quote_dept > self.find_quote_depth(line):
                clean.append("")
            quote_dept = self.find_quote_depth(line)
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
        print clean
        return clean


class QuoteTitlesPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        text = text.replace('&lt;%s:quotetitle&gt;' % self.markdown.mi_token, '<quotetitle>')
        text = text.replace('&lt;/%s:quotetitle&gt;' % self.markdown.mi_token, '</quotetitle>')
        lines = text.splitlines()
        clean = []
        for l, line in enumerate(lines):
            clean.append(line)
            try:
                if line == '<blockquote>':
                    if lines[l + 1][0:15] != '<p><quotetitle>':
                        clean.append('<header><quotesingletitle></header>')
                        clean.append('<article>')
                if line == '</blockquote>':
                    clean[-1] = '</article>'
                    clean.append('</blockquote>')
                if line.strip()[0:15] == '<p><quotetitle>':
                    line = line.strip()
                    header = line[3:-4]
                    clean[-1] = '<header>%s</header>' % header
                    clean.append('<article>')
                    if line[-4:] != '</p>':
                        clean.append('<p>')
            except IndexError:
                pass
        return '\r\n'.join(clean).replace('<p>\r\n', '<p>')
