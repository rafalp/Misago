import re

import markdown
from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
from markdown.serializers import _escape_attrib_html


class CodeBlockExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.register(
            CodeBlockPreprocessor(md, self.getConfigs()), "misago_code_bbcode", 24
        )


class CodeBlockPreprocessor(FencedBlockPreprocessor):
    FENCED_BLOCK_RE = re.compile(
        r"""
\[code(=("?)(?P<lang>.*?)("?))?](([ ]*\n)+)?(?P<code>.*?)((\s|\n)+)?\[/code\]
""",
        re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    def run(self, lines):
        """Match and store Fenced Code Blocks in the HtmlStash."""

        # Check for dependent extensions
        if not self.checked_for_deps:
            for ext in self.md.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.getConfigs()
                if isinstance(ext, AttrListExtension):
                    self.use_attr_list = True

            self.checked_for_deps = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang, id, classes, config = None, "", [], {}
                if m.group("lang"):
                    lang = m.group("lang")

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlight the code
                if (
                    self.codehilite_conf
                    and self.codehilite_conf["use_pygments"]
                    and config.get("use_pygments", True)
                ):
                    local_config = self.codehilite_conf.copy()
                    local_config.update(config)
                    # Combine classes with cssclass. Ensure cssclass is at end
                    # as pygments appends a suffix under certain circumstances.
                    # Ignore ID as Pygments does not offer an option to set it.
                    if classes:
                        local_config["css_class"] = "{} {}".format(
                            " ".join(classes), local_config["css_class"]
                        )
                    highliter = CodeHilite(
                        m.group("code"),
                        lang=lang,
                        style=local_config.pop("pygments_style", "default"),
                        **local_config,
                    )

                    code = highliter.hilite(shebang=False)
                else:
                    id_attr = lang_attr = class_attr = kv_pairs = ""
                    if lang:
                        lang_attr = f' class="language-{_escape_attrib_html(lang)}"'
                    if classes:
                        class_attr = (
                            f' class="{_escape_attrib_html(" ".join(classes))}"'
                        )
                    if id:
                        id_attr = f' id="{_escape_attrib_html(id)}"'
                    if (
                        self.use_attr_list
                        and config
                        and not config.get("use_pygments", False)
                    ):
                        # Only assign key/value pairs to code element if attr_list ext is enabled, key/value pairs
                        # were defined on the code block, and the `use_pygments` key was not set to True. The
                        # `use_pygments` key could be either set to False or not defined. It is omitted from output.
                        kv_pairs = "".join(
                            f' {k}="{_escape_attrib_html(v)}"'
                            for k, v in config.items()
                            if k != "use_pygments"
                        )
                    code = self._escape(m.group("code"))
                    code = f"<pre{id_attr}{class_attr}><code{lang_attr}{kv_pairs}>{code}</code></pre>"

                placeholder = self.md.htmlStash.store(code)
                text = f"{text[:m.start()]}\n{placeholder}\n{text[m.end():]}"
            else:
                break
        return text.split("\n")
