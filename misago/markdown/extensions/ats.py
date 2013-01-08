import re
import markdown
from markdown.util import etree

# Global vars
QUOTE_AUTHOR_RE = re.compile(r'^(?P<arrows>(>|\s)+)?@(?P<username>(\w|\d)+)$')

class AtsExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.add('mi_usernames',
                             AtsPreprocessor(md),
                             '>mi_quote_title')
        md.postprocessors.add('mi_usernames',
                              AtsPostprocessor(md),
                              '>mi_quote_title')


class AtsPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)

    def run(self, lines):
        clean = []
        for l, line in enumerate(lines):
            clean.append(line)
        return clean


class AtsPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        text = text.replace('&lt;%s:username&gt;' % self.markdown.mi_token, '<username>')
        text = text.replace('&lt;/%s:username&gt;' % self.markdown.mi_token, '</username>')
        return text
