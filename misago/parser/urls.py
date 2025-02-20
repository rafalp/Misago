from .hooks import clean_displayed_url_hook


def clean_url(href: str) -> str:
    if href.startswith("/"):
        return href
    if href.startswith("://"):
        return "http" + href
    if "://" not in href:
        return "http://" + href
    return href


def clean_displayed_url(url: str) -> str:
    return clean_displayed_url_hook(_clean_displayed_url_action, url)


URL_LENGTH_LIMIT = 80
URL_HEAD_LENGTH = 35
URL_TAIL_LENGTH = 40


def _clean_displayed_url_action(url: str) -> str:
    if "://" in url:
        url = url[url.index("://") + 3 :]

    if "index" in url.lower():
        url = _clean_displayed_url_index(url)

    if not url.startswith("/") and url.endswith("/") and url.count("/") == 1:
        url = url.strip("/")

    if len(url) <= URL_LENGTH_LIMIT:
        return url

    return f"{url[:URL_HEAD_LENGTH]}...{url[URL_TAIL_LENGTH * -1:]}"


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
