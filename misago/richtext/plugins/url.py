from mistune.plugins import extra


def parse_url_link(self, m, state):
    if state.get("_in_link"):
        return "text", m.group(0)

    return extra.parse_url_link(self, m, state)


def plugin_url(md):
    md.inline.register_rule("url_link", extra.URL_LINK_PATTERN, parse_url_link)
    md.inline.rules.append("url_link")
