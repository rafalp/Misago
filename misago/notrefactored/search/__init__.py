from django.utils.translation import ugettext_lazy as _

class SearchException(Exception):
    def __init__(self, message):
        self.message = message


class SearchQuery(object):
    def __init__(self, raw_query=None):
        """
        Build search query object
        """
        if raw_query:
            self.parse_query(raw_query)
        
    def parse_query(self, raw_query):
        """
        Parse raw search query into dict of lists of words that should be found and cant be found in string
        """
        self.criteria = {'+': [], '-': []}
        for word in unicode(raw_query).split():
            # Trim word and skip it if its empty
            word = unicode(word).strip().lower()
            if len(word) == 0:
                pass
            
            # Find word mode
            mode = '+'
            if word[0] == '-':
                mode = '-'
                word = unicode(word[1:]).strip()
                
            # Strip extra crap
            word = ''.join(e for e in word if e.isalnum())
            
            # Slice word?
            if len(word) <= 3:
                raise SearchException(_("One or more search phrases are shorter than four characters."))
            if mode == '+':
                if len(word) == 5:
                    word = word[0:-1]
                if len(word) == 6:
                    word = word[0:-2]
                if len(word) > 6:
                    word = word[0:-3]
            self.criteria[mode].append(word)
            
        # Complain that there are no positive matches
        if not self.criteria['+'] and not self.criteria['-']:
            raise SearchException(_("Search query is invalid."))
    
    def search(self, value):
        """
        See if value meets search criteria, return True for success and False otherwhise
        """
        try:
            value = unicode(value).strip().lower()
            # Search for only
            if self.criteria['+'] and not self.criteria['-']:
               return self.search_for(value)
            # Search against only
            if self.criteria['-'] and not self.criteria['+']:
               return self.search_against(value)
            # Search if contains for values but not against values
            return self.search_for(value) and not self.search_against(value)
        except AttributeError:
            raise SearchException(_("You have to define search query before you will be able to search."))
        
    def search_for(self, value):
        """
        See if value is required
        """
        for word in self.criteria['+']:
            if value.find(word) != -1:
                return True
        return False
        
    def search_against(self, value):
        """
        See if value is forbidden
        """
        for word in self.criteria['-']:
            if value.find(word) != -1:
                return True
        return False