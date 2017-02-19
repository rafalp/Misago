import re

from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.utils import six


SUPPORTED_TAGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p')
USERNAME_RE = re.compile(r'@[0-9a-z]+', re.IGNORECASE)
MENTIONS_LIMIT = 24


def add_mentions(request, result):
    if '@' not in result['parsed_text']:
        return

    mentions_dict = {}

    soup = BeautifulSoup(result['parsed_text'], 'html5lib')

    elements = []
    for tagname in SUPPORTED_TAGS:
        if tagname in result['parsed_text']:
            elements += soup.find_all(tagname)
    for element in elements:
        add_mentions_to_element(request, element, mentions_dict)

    result['parsed_text'] = six.text_type(soup.body)[6:-7].strip()
    result['mentions'] = list(filter(bool, mentions_dict.values()))


def add_mentions_to_element(request, element, mentions_dict):
    for item in element.contents:
        if item.name:
            if item.name != 'a':
                add_mentions_to_element(request, item, mentions_dict)
        elif '@' in item.string:
            parse_string(request, item, mentions_dict)


def parse_string(request, element, mentions_dict):
    UserModel = get_user_model()

    def replace_mentions(matchobj):
        if len(mentions_dict) >= MENTIONS_LIMIT:
            return matchobj.group(0)

        username = matchobj.group(0)[1:].strip().lower()

        if username not in mentions_dict:
            if username == request.user.slug:
                mentions_dict[username] = request.user
            else:
                try:
                    mentions_dict[username] = UserModel.objects.get(slug=username)
                except UserModel.DoesNotExist:
                    mentions_dict[username] = None

        if mentions_dict[username]:
            user = mentions_dict[username]
            return u'<a href="{}">@{}</a>'.format(user.get_absolute_url(), user.username)
        else:
            # we've failed to resolve user for username
            return matchobj.group(0)

    replaced_string = USERNAME_RE.sub(replace_mentions, element.string)
    element.replace_with(BeautifulSoup(replaced_string, 'html.parser'))
