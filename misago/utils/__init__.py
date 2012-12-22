"""
Smart slugify
"""
import django.template.defaultfilters

use_unidecode = True
try:
    from unidecode import unidecode
except ImportError:
    use_unidecode = False
    
def slugify(string):
    if use_unidecode:
        string = unidecode(string)
    return django.template.defaultfilters.slugify(string)


"""
Lazy translate that allows us to access original message
"""
from django.utils import translation

def ugettext_lazy(str):
    t = translation.ugettext_lazy(str)
    t.message = str
    return t
def get_msgid(gettext):
    try:
        return gettext.message
    except AttributeError:
        return None


"""
Random string
"""
from django.utils import crypto
    
def get_random_string(length):
    return crypto.get_random_string(length, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")


"""
Date formats
"""               
from django.utils.formats import get_format

formats = {
    'DATE_FORMAT': '',
    'DATETIME_FORMAT': '',
    'TIME_FORMAT': '',
    'YEAR_MONTH_FORMAT': '',
    'MONTH_DAY_FORMAT': '',
    'SHORT_DATE_FORMAT': '',
    'SHORT_DATETIME_FORMAT': '',
}

for key in formats:
    formats[key] = get_format(key).replace('P', 'g:i a')
    
    
"""
Build pagination list
"""
import math

def make_pagination(page, total, max):
    pagination = {'start': 0, 'stop': 0, 'prev': -1, 'next': -1}
    page = int(page)
    if page > 0:
        pagination['start'] = (page - 1) * max
        
    # Set page and total stat
    pagination['page'] = int(pagination['start'] / max) + 1
    pagination['total'] = int(math.ceil(total / float(max)))
        
    # Fix too large offset
    if pagination['start'] > total:
        pagination['start'] = 0
        
    # Allow prev/next?
    if total > max:
        if pagination['page'] > 1:
            pagination['prev'] = pagination['page'] - 1
        if pagination['page'] < pagination['total']:
            pagination['next'] = pagination['page'] + 1
            
    # Set stop offset
    pagination['stop'] = pagination['start'] + max
    return pagination