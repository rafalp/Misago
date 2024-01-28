def clean_href(href: str) -> str:
    if href.startswith("://"):
        return "http" + href
    if "://" not in href:
        return "http://" + href
    return href
