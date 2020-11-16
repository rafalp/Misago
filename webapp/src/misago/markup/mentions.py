import re

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

SUPPORTED_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "div", "p")
USERNAME_RE = re.compile(r"@[0-9a-z]+", re.IGNORECASE)
MENTIONS_LIMIT = 24


def add_mentions(request, result):
    if "@" not in result["parsed_text"]:
        return

    mentions_dict = {}

    soup = BeautifulSoup(result["parsed_text"], "html5lib")

    elements = []
    for tagname in SUPPORTED_TAGS:
        if tagname in result["parsed_text"]:
            elements += soup.find_all(tagname)
    for element in elements:
        add_mentions_to_element(request, element, mentions_dict)

    result["parsed_text"] = str(soup.body)[6:-7].strip()
    result["mentions"] = list(filter(bool, mentions_dict.values()))


def add_mentions_to_element(request, element, mentions_dict):
    for item in element.contents:
        if item.name:
            if item.name != "a":
                add_mentions_to_element(request, item, mentions_dict)
        elif "@" in item.string:
            parse_string(request, item, mentions_dict)


def parse_string(request, element, mentions_dict):
    User = get_user_model()

    def replace_mentions(matchobj):
        if len(mentions_dict) >= MENTIONS_LIMIT:
            return matchobj.group(0)

        username = matchobj.group(0)[1:].strip().lower()

        if username not in mentions_dict:
            if username == request.user.slug:
                mentions_dict[username] = request.user
            else:
                try:
                    mentions_dict[username] = User.objects.get(slug=username)
                except User.DoesNotExist:
                    mentions_dict[username] = None

        if mentions_dict[username]:
            user = mentions_dict[username]
            return '<a href="%s">@%s</a>' % (user.get_absolute_url(), user.username)

        # we've failed to resolve user for username
        return matchobj.group(0)

    replaced_string = USERNAME_RE.sub(replace_mentions, element.string)
    element.replace_with(BeautifulSoup(replaced_string, "html.parser"))
