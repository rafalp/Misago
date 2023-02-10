import re
from typing import Union

from django.http import Http404
from django.urls import resolve

from .htmlparser import ElementNode, RootNode, TextNode

MISAGO_ATTACHMENT_VIEWS = ("misago:attachment", "misago:attachment-thumbnail")
URL_RE = re.compile(
    r"(https?://)?"
    r"(www\.)?"
    r"(\w+((-|_)\w+)?\.)?"
    r"\w+((_|-|\w)+)?(\.[a-z][a-z]+)"
    r"(:[1-9][0-9]+)?"
    r"([^\s<>\[\]\(\);:]+)?"
)


def linkify_texts(node: Union[RootNode, ElementNode]):
    # Skip link replacement in some nodes
    if node.tag in ("pre", "code", "a"):
        return

    new_children = []
    for child in node.children:
        if isinstance(child, TextNode):
            if URL_RE.search(child.text):
                new_children += replace_links_in_text(child.text)
            else:
                new_children.append(child)
        else:
            new_children.append(child)
            linkify_texts(child)

    node.children = new_children


def replace_links_in_text(text: str) -> list:
    nodes = []

    while True:
        match = URL_RE.search(text)
        if not match:
            if text:
                nodes.append(TextNode(text=text))
            return nodes

        start, end = match.span()
        url = text[start:end]

        # Append text between 0 and start to nodes
        if start > 0:
            nodes.append(TextNode(text=text[:start]))

        nodes.append(
            ElementNode(
                tag="a",
                attrs={"href": url},
                children=[
                    TextNode(text=strip_link_protocol(url)),
                ],
            )
        )

        text = text[end:]


def clean_links(
    request,
    result,
    node: Union[RootNode, ElementNode, TextNode],
    force_shva=False,
):
    if isinstance(node, TextNode):
        return

    for child in node.children:
        if not isinstance(child, ElementNode):
            continue

        if child.tag == "a":
            clean_link_node(request, result, child, force_shva)
            clean_links(request, result, child, force_shva)
        elif child.tag == "img":
            clean_image_node(request, result, child, force_shva)
        else:
            clean_links(request, result, child, force_shva)


def clean_link_node(
    request,
    result: dict,
    node: ElementNode,
    force_shva: bool,
):
    host = request.get_host()
    href = node.attrs.get("href") or "/"

    if is_internal_link(href, host):
        href = clean_internal_link(href, host)
        result["internal_links"].append(href)
        href = clean_attachment_link(href, force_shva)
    else:
        result["outgoing_links"].append(strip_link_protocol(href))
        href = assert_link_prefix(href)
        node.attrs["rel"] = "external nofollow noopener"

    node.attrs["target"] = "_blank"
    node.attrs["href"] = href

    if len(node.children) == 0:
        node.children.append(strip_link_protocol(href))
    elif len(node.children) == 1 and isinstance(node.children[0], TextNode):
        text = node.children[0].text
        if URL_RE.match(text):
            node.children[0].text = strip_link_protocol(text)


def clean_image_node(
    request,
    result: dict,
    node: ElementNode,
    force_shva: bool,
):
    host = request.get_host()
    src = node.attrs.get("src") or "/"

    node.attrs["alt"] = strip_link_protocol(node.attrs["alt"])

    if is_internal_link(src, host):
        src = clean_internal_link(src, host)
        result["images"].append(src)
        src = clean_attachment_link(src, force_shva)
    else:
        result["images"].append(strip_link_protocol(src))
        src = assert_link_prefix(src)

    node.attrs["src"] = src


def is_internal_link(link, host):
    if link.startswith("/") and not link.startswith("//"):
        return True

    link = strip_link_protocol(link).lstrip("www.").lower()
    return link.lower().startswith(host.lstrip("www."))


def strip_link_protocol(link):
    if link.lower().startswith("https:"):
        link = link[6:]
    if link.lower().startswith("http:"):
        link = link[5:]
    if link.startswith("//"):
        link = link[2:]
    return link


def assert_link_prefix(link):
    if link.lower().startswith("https:"):
        return link
    if link.lower().startswith("http:"):
        return link
    if link.startswith("//"):
        return "http:%s" % link

    return "http://%s" % link


def clean_internal_link(link, host):
    link = strip_link_protocol(link)

    if link.lower().startswith("www."):
        link = link[4:]
    if host.lower().startswith("www."):
        host = host[4:]

    if link.lower().startswith(host):
        link = link[len(host) :]

    return link or "/"


def clean_attachment_link(link, force_shva=False):
    try:
        resolution = resolve(link)
        if not resolution.namespaces:
            return link
        url_name = ":".join(resolution.namespaces + [resolution.url_name])
    except (Http404, ValueError):
        return link

    if url_name in MISAGO_ATTACHMENT_VIEWS:
        if force_shva:
            link = "%s?shva=1" % link
        elif link.endswith("?shva=1"):
            link = link[:-7]
    return link
