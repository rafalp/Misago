import django.template.defaultfilters
try:
    from unidecode import unidecode
    use_unidecode = True
except ImportError:
    use_unidecode = False

def slugify(string):
    if use_unidecode:
        string = unidecode(string)
    return django.template.defaultfilters.slugify(string)
