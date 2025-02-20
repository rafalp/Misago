from .hooks import clean_displayed_url_hook


def clean_url(href: str) -> str:
    if href.startswith("://"):
        return "http" + href
    if "://" not in href:
        return "http://" + href
    return href


def clean_displayed_url(url: str) -> str:
    return clean_displayed_url_hook(_clean_displayed_url_action, url)


def _clean_displayed_url_action(url: str) -> str:
    if "://" in url:
        url = url[url.index("://") + 3 :]

    if "?" in url:
        url = _clean_displayed_url_querystring(url)

    if "index" in url.lower():
        url = _clean_displayed_url_index(url)

    if "/" not in url.strip("/"):
        url = url.strip("/")
    else:
        url = _clean_displayed_url_path(url)

    return url


QUERYSTRING_LENGTH_LIMIT = 15


def _clean_displayed_url_querystring(url: str) -> str:
    querystring = url[url.index("?") :]
    if len(querystring) > QUERYSTRING_LENGTH_LIMIT:
        url = url[: url.index("?")]
        url += f"{querystring[:QUERYSTRING_LENGTH_LIMIT]}..."
    return url


INDEX_FILE_NAMES = ("index.php", "index.html", "index.htm")


def _clean_displayed_url_index(url: str) -> str:
    for filename in INDEX_FILE_NAMES:
        if filename in url:
            start = url.lower().index(filename)
            stop = start + len(filename)
            tail = url[stop:]
            if not tail or tail[0] == "?":
                return url[:start] + url[stop:]

    return url


PATH_MAX_LENGTH = 50


def _clean_displayed_url_path(url: str) -> str:
    start = url.index("/")

    if "?" in url:
        end = url.index("?")
    else:
        end = len(url)

    path = url[start:end]
    if len(path) > PATH_MAX_LENGTH:
        return f"{url[:start]}{path[:20]}...{path[-20:]}{url[end:]}"

    return url
