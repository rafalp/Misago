from misago.markup.parser import parse_text


def common(text, author=None, allow_mentions=True):
    """
    Common flavour

    Used in places where full Misago flavour is desired

    Breaks text into paragraphs, supports code, spoiler and quote blocks,
    headers, lists, images, spoilers, text styles

    Returns dict object
    """
    return parse_text(text, author=author, allow_mentions=allow_mentions)


def limited(text):
    """
    Limited flavour

    Breaks text in paragraphs, supports strong, em, i, u, b,
    automatically linkifies links.

    Returns parsed text
    """
    result =  parse_text(text, allow_mentions=False, allow_links=True,
                         allow_images=False, allow_blocks=False)

    return result['parsed_text']
