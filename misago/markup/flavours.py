from misago.markup.parser import parse


def common(text, author=None, allow_mentions=True):
    """
    Common flavour

    Used in places where full Misago flavour is desired

    Breaks text into paragraphs, supports code, spoiler and quote blocks,
    headers, lists, images, spoilers, text styles

    Returns dict object
    """
    return parse(text, author=author, allow_mentions=allow_mentions)


def limited(text):
    """
    Limited flavour

    Breaks text in paragraphs, supports strong, em, i, u, b,
    automatically linkifies links.

    Returns parsed text
    """
    result = parse(text, allow_mentions=False, allow_links=True,
                   allow_images=False, allow_blocks=False)

    return result['parsed_text']


def signature(text, owner=None):
    result = parse(text, allow_mentions=False,
                   allow_blocks=owner.acl['allow_signature_blocks'],
                   allow_links=owner.acl['allow_signature_links'],
                   allow_images=owner.acl['allow_signature_images'])

    return result['parsed_text']
