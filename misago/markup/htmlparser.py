import html
from dataclasses import dataclass

import html5lib

SINGLETON_TAGS = (
    "area",
    "base",
    "br",
    "col",
    "command",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


class Node:
    def __str__(self):
        raise NotImplementedError("Subclasses of 'Node' need to implement __str__")


@dataclass
class RootNode(Node):
    tag = None
    children: list

    def __str__(self):
        return "".join(str(child) for child in self.children)


@dataclass
class ElementNode(Node):
    tag: str
    attrs: dict
    children: list

    def __str__(self):
        attrs_padding = " " if self.attrs else ""
        attrs = " ".join(self.attrs_str())

        if self.tag in SINGLETON_TAGS:
            return f"<{self.tag}{attrs_padding}{attrs} />"

        children = "".join(str(child) for child in self.children)
        return f"<{self.tag}{attrs_padding}{attrs}>{children}</{self.tag}>"

    def attrs_str(self):
        for name, value in self.attrs.items():
            if value is True or not value:
                yield html.escape(str(name))
            else:
                yield (f'{html.escape(str(name))}="{html.escape(str(value))}"')


@dataclass
class TextNode(Node):
    text: str

    def __str__(self):
        return html.escape(self.text)


def parse_html_string(string: str) -> RootNode:
    element = html5lib.parse(
        string,
        namespaceHTMLElements=False,
    )

    body = element.find("body")
    root_node = RootNode(children=[])

    if body.text:
        root_node.children.append(TextNode(text=body.text))

    for child in body:
        add_child_node(root_node, child)

    return root_node


def add_child_node(parent, element):
    node = ElementNode(
        tag=element.tag,
        attrs=element.attrib,
        children=[],
    )

    if element.text:
        node.children.append(TextNode(text=element.text))

    parent.children.append(node)

    if element.tail:
        parent.children.append(TextNode(text=element.tail))

    for child in element:
        add_child_node(node, child)


def print_html_string(root_node: RootNode) -> str:
    return str(root_node)
