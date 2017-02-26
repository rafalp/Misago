from __future__ import unicode_literals

import sys

from lib2to3.pytree import Node, Leaf
from lib2to3.fixer_util import token, syms

from yapf.yapflib import pytree_utils

from django.utils import six


def fix_formatting(filesource):
    if not ('{'  in filesource and ('[' in filesource or '(' in filesource)):
        return filesource

    tree = pytree_utils.ParseCodeToTree(filesource)
    for node in tree.children:
        walk_tree(node, node.children)
    return six.text_type(tree)


def walk_tree(node, children):
    for item in children:
        if item.type == syms.dictsetmaker:
            walk_dict_tree(item, item.children)
        else:
            walk_tree(item, item.children)


def walk_dict_tree(node, children):
    for item in children:
        prev = item.prev_sibling
        if isinstance(prev, Leaf) and prev.value == ':':
            if isinstance(item, Leaf):
                if six.text_type(item).startswith("\n"):
                    # first case: intended string
                    item.replace(Leaf(
                        item.type,
                        item.value,
                        prefix=' ',
                    ))
            elif six.text_type(item).strip()[0] in ('[', '{'):
                walk_tree(item, item.children)
            else:
                walk_dedent_tree(item, item.children)


def walk_dedent_tree(node, children):
    for item in children:
        prev = item.prev_sibling
        if not prev:
            if isinstance(item, Leaf) and six.text_type(item).startswith("\n"):
                # first case: intended string
                item.replace(Leaf(
                    item.type,
                    item.value,
                    prefix=' ',
                ))
        elif isinstance(item, Node):
            for subitem in item.children[1:]:
                walk_dedent_tree_node(subitem, subitem.children)


def walk_dedent_tree_node(node, children):
    if six.text_type(node).startswith("\n"):
        if isinstance(node, Leaf):
            prev = node.prev_sibling
            is_followup = prev and prev.type == token.STRING and node.type == token.STRING
            if is_followup:
                new_prefix = "\n%s" % (' ' * (len(prev.prefix.lstrip("\n")) / 4 * 4))
                node.replace(Leaf(
                    node.type,
                    "%s\n%s" % (node.value, (' ' * ((len(prev.prefix.lstrip("\n")) / 4 - 1) * 4))),
                    prefix=new_prefix,
                ))
            else:
                node.replace(Leaf(
                    node.type,
                    node.value,
                    prefix=node.prefix[:-4],
                ))
        else:
            for item in children:
                walk_dedent_tree_node(item, item.children)
    elif isinstance(node, Leaf):
        if node.type == token.STRING:
            prev = node.prev_sibling
            next = node.next_sibling

            is_opening = prev is None and six.text_type(node.parent.parent).strip()[0] == '('
            has_followup = next and next.type == token.STRING

            if is_opening and has_followup:
                new_prefix = "\n%s" % (' ' * (len(next.prefix.lstrip("\n")) / 4 * 4))

                node.replace(Leaf(
                    node.type,
                    node.value,
                    prefix=new_prefix,
                ))
    else:
        for item in children:
            walk_dedent_tree_node(item, item.children)

