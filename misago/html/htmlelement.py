from html import escape


def html_element(
    tag: str,
    children: str | None = None,
    attrs: dict | None = None,
) -> str:
    html = tag

    if attrs:
        html += _html_attributes(attrs)

    if children is None:
        return f"<{html} />"

    return f"<{html}>{children}</{tag}>"


def _html_attributes(attrs: dict) -> str:
    html = ""
    for attr, value in attrs.items():
        if value is True:
            html += " " + attr
        elif value is not None:
            html += f' {attr}="{escape(value)}"'
    return html
