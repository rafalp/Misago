import re
from functools import wraps


REGEX_CACHE = {}
ELEMENT_RE_TPL = r"\<E(?P<args>.*?)\>(?P<children>.*?)\</E\>"


def replace_html_element(html: str, element: str, sub) -> str:
    if element not in REGEX_CACHE:
        REGEX_CACHE[element] = re.compile(
            ELEMENT_RE_TPL.replace("E", element), re.DOTALL
        )

    return REGEX_CACHE[element].sub(sub, html)


def replace_html_element_func(f):
    @wraps(f)
    def _html_element_replacer_wrapper(match):
        if args := match.group("args").strip():
            args = parse_args(args)
        else:
            args = None

        return f(match.group(0), match.group("children"), args)

    return _html_element_replacer_wrapper


ARG_RE = re.compile(r"(?P<name>[a-z-]+)(\=\"(?P<value>.*?)\")?", re.DOTALL)


def parse_args(args: str) -> dict[str, str | bool] | None:
    clean_args: dict[str, str | bool] = {}
    for name, value_match, value in ARG_RE.findall(args):
        clean_args[name] = value.strip() if value_match else True
    return clean_args or None
