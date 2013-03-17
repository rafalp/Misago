import re
import markdown
from markdown.util import etree
from django.core.urlresolvers import reverse
from misago.models import User
from misago.utils.strings import slugify

# Global vars
MENTION_RE = re.compile(r'([^\w]?)@(?P<username>(\w)+)', re.UNICODE)


class MentionsExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.mentions = {}
        md.registerExtension(self)
        md.preprocessors.add('mi_mentions',
                             MentionsPreprocessor(md),
                             '>mi_quote_title')
        md.postprocessors.add('mi_mentions',
                              MentionsPostprocessor(md),
                              '>mi_quote_title')


class MentionsPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)
        self.md = md

    def run(self, lines):
        def mention(match):
            slug = slugify(match.group(0)[1:])
            if slug in self.md.mentions:
                user = self.md.mentions[slug]
                return '%s[@%s](%s)' % (match.group(1), user.username, reverse('user', kwargs={
                                                                                              'user': user.pk,
                                                                                              'username': user.username_slug,
                                                                                              }))
            elif len(self.md.mentions) < 32:
                try:
                    user = User.objects.get(username_slug=slug)
                    self.md.mentions[slug] = user
                    return '%s[@%s](%s)' % (match.group(1), user.username, reverse('user', kwargs={
                                                                                                  'user': user.pk,
                                                                                                  'username': user.username_slug,
                                                                                                  }))
                except User.DoesNotExist:
                    pass
            return match.group(0)
        clean = []
        for l, line in enumerate(lines):
            if line.strip():
                line = MENTION_RE.sub(mention, line)
            clean.append(line)
        return clean


class MentionsPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        return text
