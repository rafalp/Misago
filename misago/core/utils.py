import bleach
from markdown import Markdown
from unidecode import unidecode
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify as django_slugify


def _is_request_path_under_misago(request):
    # We are assuming that forum_index link is root of all Misago links
    forum_index = reverse('misago:index')
    path_info = request.path_info

    if len(forum_index) > len(path_info):
        return False
    return path_info[:len(forum_index)] == forum_index


def is_request_to_misago(request):
    try:
        return request._request_to_misago
    except AttributeError:
        request._request_to_misago = _is_request_path_under_misago(request)
        return request._request_to_misago


def slugify(string):
    string = unicode(string)
    string = unidecode(string)
    return django_slugify(string.replace('_', ' '))


MD_SUBSET_FORBID_SYNTAX = (
    # References are evil
    'reference', 'reference', 'image_reference', 'short_reference',

    # Blocks are evil too
    'hashheader', 'setextheader', 'code', 'quote', 'hr', 'olist', 'ulist',
)


def subset_markdown(text):
    if not text:
        return ''

    md = Markdown(safe_mode='escape', extensions=['nl2br'])

    for key in md.preprocessors.keys():
        if key in MD_SUBSET_FORBID_SYNTAX:
            del md.preprocessors[key]

    for key in md.inlinePatterns.keys():
        if key in MD_SUBSET_FORBID_SYNTAX:
            del md.inlinePatterns[key]

    for key in md.parser.blockprocessors.keys():
        if key in MD_SUBSET_FORBID_SYNTAX:
            del md.parser.blockprocessors[key]

    for key in md.treeprocessors.keys():
        if key in MD_SUBSET_FORBID_SYNTAX:
            del md.treeprocessors[key]

    for key in md.postprocessors.keys():
        if key in MD_SUBSET_FORBID_SYNTAX:
            del md.postprocessors[key]

    return bleach.linkify(md.convert(text))
