from HTMLParser import HTMLParser
from urlparse import urlparse
from django.conf import settings
from misago.utils.strings import random_string

class RemoveHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.clean_text = ''
        self.lookback = []
        
    def handle_entityref(self, name):
        if name == 'gt':
            self.clean_text += '>'
        if name == 'lt':
            self.clean_text += '<'

    def handle_starttag(self, tag, attrs):
        self.lookback.append(tag)

    def handle_endtag(self, tag):
        try:
            if self.lookback[-1] == tag:
                self.lookback.pop()
        except IndexError:
            pass
        
    def handle_data(self, data):
        # String does not repeat itself
        if self.clean_text[-len(data):] != data:
            # String is not "QUOTE"
            try:
                if self.lookback[-1] in ('strong', 'em'):
                    self.clean_text += data
                elif not (data == 'Quote' and self.lookback[-1] == 'h3' and self.lookback[-2] == 'blockquote'):
                    self.clean_text += data
            except IndexError:
                self.clean_text += data