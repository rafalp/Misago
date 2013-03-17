from misago.markdown.factory import *

# Monkeypatch blockquote parser to handle codes
from markdown import util
import markdown.blockprocessors
from markdown.extensions.fenced_code import FENCED_BLOCK_RE, CODE_WRAP, LANG_TAG

class MisagoBlockQuoteProcessor(markdown.blockprocessors.BlockQuoteProcessor):
    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()] # Lines before blockquote
            # Pass lines before blockquote in recursively for parsing forst.
            self.parser.parseBlocks(parent, [before])
            # Remove ``> `` from begining of each line.
            block = '\n'.join([self.clean(line) for line in 
                            block[m.start():].split('\n')])

        sibling = self.lastChild(parent)
        if sibling and sibling.tag == "blockquote":
            # Previous block was a blockquote so set that as this blocks parent
            quote = sibling
        else:
            # This is a new blockquote. Create a new parent element.
            quote = util.etree.SubElement(parent, 'blockquote')
        # Recursively parse block with blockquote as parent.
        # change parser state so blockquotes embedded in lists use p tags
        self.parser.state.set('blockquote')
        # MONKEYPATCH START
        block = self.clear_codes(block)
        # MONKEYPATCH END
        self.parser.parseChunk(quote, block)
        self.parser.state.reset()

    # MONKEYPATCH START
    def clear_codes(self, text):
        while 1:
            m = FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = LANG_TAG % m.group('lang')
                code = CODE_WRAP % (lang, self._escape(m.group('code')))
                placeholder = self.parser.markdown.htmlStash.store(code, safe=True)
                text = '%s\n\n%s\n\n%s' % (text[:m.start()].strip(), placeholder.strip(), text[m.end():].strip())
            else:
                break
        return text.strip()

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt.strip()
    # MONKEYPATCH END

markdown.blockprocessors.BlockQuoteProcessor = MisagoBlockQuoteProcessor