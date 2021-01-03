from mistune import Markdown


BOLD_PATTERN = r"\[b\](.*)\[\/b\]"
ITALIC_PATTERN = r"\[i\](.*)\[\/i\]"
UNDERLINE_PATTERN = r"\[u\](.*)\[\/u\]"
STRIKETHROUGH_PATTERN = r"\[s\](.*)\[\/s\]"
SUBSCRIPT_PATTERN = r"\[sub\](.*)\[\/sub\]"
SUPERSCRIPT_PATTERN = r"\[sup\](.*)\[\/sup\]"


def formatting_plugin(markdown: Markdown, name: str, pattern: str):
    plugin_name = f"{name}_bbcode"

    def parse_format(parser, m, state):
        return name, parser(m.group(1), state)

    markdown.inline.register_rule(plugin_name, pattern, parse_format)
    markdown.inline.rules.append(plugin_name)

    if markdown.renderer.NAME == "ast":

        def render_ast_formatting_bbcode(children: str):
            return {"type": name, "children": children}

        markdown.renderer.register(plugin_name, render_ast_formatting_bbcode)


def plugin_bold_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "bold", BOLD_PATTERN)


def plugin_italic_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "italic", ITALIC_PATTERN)


def plugin_underline_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "underline", UNDERLINE_PATTERN)


def plugin_strikethrough_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "strikethrough", STRIKETHROUGH_PATTERN)


def plugin_subscript_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "subscript", SUBSCRIPT_PATTERN)


def plugin_superscript_bbcode(markdown: Markdown):
    formatting_plugin(markdown, "superscript", SUPERSCRIPT_PATTERN)
