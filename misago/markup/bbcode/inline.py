"""
Supported inline BBCodes: b, u, i
"""
import re

from markdown.inlinepatterns import SimpleTagPattern


class SimpleBBCodePattern(SimpleTagPattern):
    """
    Case insensitive simple BBCode
    """

    def __init__(self, bbcode, tag=None):
        self.pattern = r'(\[%s\](.*?)\[/%s\])' % (bbcode, bbcode)
        self.compiled_re = re.compile(
            "^(.*?)%s(.*?)$" % self.pattern, re.DOTALL | re.UNICODE | re.IGNORECASE
        )

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False

        # Store tag
        self.tag = tag or bbcode.lower()


"""
Register basic BBCodes
"""
bold = SimpleBBCodePattern('b')
italics = SimpleBBCodePattern('i')
underline = SimpleBBCodePattern('u')
