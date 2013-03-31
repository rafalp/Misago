from django.utils import translation

def ugettext_lazy(string):
    """
    Custom wrapper that preserves untranslated message on lazy translation string object
    """
    t = translation.ugettext_lazy(string)
    t.message = string
    return t


def get_msgid(gettext):
    """
    Function for extracting untranslated message from lazy translation string object
    made trough ugettext_lazy
    """
    try:
        return gettext.message
    except AttributeError:
        return None